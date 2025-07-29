#!/usr/bin/env python3
"""
OneTalk Multi-User Communication System
Manages simultaneous communication for multiple users with department classification
"""

import json
import sqlite3
import datetime
import requests
import os
from dataclasses import dataclass
from typing import List, Dict, Optional
from openphone_api import OpenPhoneAPI

@dataclass
class User:
    id: str
    name: str
    department: str
    phone_number: str
    role: str
    status: str = "available"  # available, busy, offline

@dataclass
class Department:
    id: str
    name: str
    lead_user_id: str
    members: List[str]
    phone_numbers: List[str]
    
@dataclass
class Communication:
    id: str
    timestamp: str
    from_number: str
    to_number: str
    user_id: str
    department_id: str
    type: str  # call, sms, voicemail
    content: str
    status: str  # active, completed, missed

class OneTalkSystem:
    def __init__(self, db_path="onetalk_system.db"):
        self.db_path = db_path
        self.openphone = None
        self.init_database()
        
        # Initialize OpenPhone if API key available
        api_key = os.getenv('OPENPHONE_API_KEY')
        if api_key:
            self.openphone = OpenPhoneAPI(api_key)
    
    def init_database(self):
        """Initialize SQLite database for OneTalk system"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                phone_number TEXT,
                role TEXT NOT NULL,
                status TEXT DEFAULT 'available',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Departments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS departments (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                lead_user_id TEXT,
                phone_numbers TEXT,  -- JSON array
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Communications table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS communications (
                id TEXT PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                from_number TEXT NOT NULL,
                to_number TEXT NOT NULL,
                user_id TEXT,
                department_id TEXT,
                type TEXT NOT NULL,
                content TEXT,
                status TEXT DEFAULT 'active',
                duration INTEGER,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (department_id) REFERENCES departments (id)
            )
        ''')
        
        # Communication routing rules
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS routing_rules (
                id TEXT PRIMARY KEY,
                priority INTEGER NOT NULL,
                condition_type TEXT NOT NULL,  -- phone_pattern, time_based, department
                condition_value TEXT NOT NULL,
                target_department TEXT NOT NULL,
                target_user TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_user(self, user_id: str, name: str, department: str, phone_number: str = None, role: str = "member"):
        """Add a new user to the OneTalk system"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO users (id, name, department, phone_number, role)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, name, department, phone_number, role))
        
        conn.commit()
        conn.close()
        
        # Update department membership
        self.update_department_membership(department, user_id)
        
        return f"✅ User {name} added to {department} department"
    
    def create_department(self, dept_id: str, name: str, lead_user_id: str = None, phone_numbers: List[str] = None):
        """Create a new department"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        phone_nums_json = json.dumps(phone_numbers or [])
        
        cursor.execute('''
            INSERT OR REPLACE INTO departments (id, name, lead_user_id, phone_numbers)
            VALUES (?, ?, ?, ?)
        ''', (dept_id, name, lead_user_id, phone_nums_json))
        
        conn.commit()
        conn.close()
        
        return f"✅ Department {name} created"
    
    def classify_incoming_communication(self, from_number: str, to_number: str, message_type: str, content: str = ""):
        """Classify and route incoming communication to appropriate user/department"""
        
        # Check routing rules first
        target_dept, target_user = self.apply_routing_rules(from_number, to_number, message_type)
        
        if not target_dept:
            # Default classification logic
            target_dept, target_user = self.default_classification(from_number, to_number, content)
        
        # Find available user in target department
        assigned_user = self.find_available_user(target_dept, target_user)
        
        # Create communication record
        comm_id = self.create_communication_record(
            from_number, to_number, assigned_user, target_dept, message_type, content
        )
        
        # Route to appropriate handler
        self.route_communication(comm_id, assigned_user, target_dept, message_type, content)
        
        return {
            "communication_id": comm_id,
            "assigned_user": assigned_user,
            "department": target_dept,
            "routing_method": "rules" if target_dept else "default"
        }
    
    def apply_routing_rules(self, from_number: str, to_number: str, message_type: str):
        """Apply routing rules to determine target department/user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT target_department, target_user, condition_type, condition_value
            FROM routing_rules 
            WHERE is_active = TRUE 
            ORDER BY priority ASC
        ''')
        
        rules = cursor.fetchall()
        conn.close()
        
        for target_dept, target_user, condition_type, condition_value in rules:
            if condition_type == "phone_pattern":
                if condition_value in from_number or condition_value in to_number:
                    return target_dept, target_user
            elif condition_type == "time_based":
                # Implement time-based routing if needed
                pass
            elif condition_type == "department":
                if self.check_department_condition(condition_value, from_number):
                    return target_dept, target_user
        
        return None, None
    
    def default_classification(self, from_number: str, to_number: str, content: str):
        """Default classification logic when no routing rules match"""
        
        # Check if caller is existing customer (in database)
        existing_customer = self.find_existing_customer(from_number)
        if existing_customer:
            return existing_customer["department"], existing_customer["assigned_user"]
        
        # Content-based classification
        content_lower = content.lower()
        
        if any(word in content_lower for word in ["credit", "loan", "financing", "approval"]):
            return "credit_analysis", None
        elif any(word in content_lower for word in ["transport", "vehicle", "shipping", "delivery"]):
            return "vehicle_transport", None
        elif any(word in content_lower for word in ["sales", "buy", "purchase", "deal"]):
            return "sales", None
        else:
            return "customer_service", None
    
    def find_available_user(self, department: str, preferred_user: str = None):
        """Find an available user in the specified department"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Try preferred user first
        if preferred_user:
            cursor.execute('''
                SELECT id FROM users 
                WHERE id = ? AND department = ? AND status = 'available'
            ''', (preferred_user, department))
            
            if cursor.fetchone():
                conn.close()
                return preferred_user
        
        # Find any available user in department
        cursor.execute('''
            SELECT id FROM users 
            WHERE department = ? AND status = 'available'
            ORDER BY role DESC, name ASC
            LIMIT 1
        ''', (department,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
    
    def create_communication_record(self, from_number: str, to_number: str, user_id: str, dept_id: str, msg_type: str, content: str):
        """Create a communication record in the database"""
        import uuid
        
        comm_id = str(uuid.uuid4())
        timestamp = datetime.datetime.utcnow().isoformat() + 'Z'
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO communications 
            (id, timestamp, from_number, to_number, user_id, department_id, type, content)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (comm_id, timestamp, from_number, to_number, user_id, dept_id, msg_type, content))
        
        conn.commit()
        conn.close()
        
        return comm_id
    
    def route_communication(self, comm_id: str, user_id: str, department: str, msg_type: str, content: str):
        """Route communication to appropriate handler/system"""
        
        # Update user status to busy if it's a call
        if msg_type == "call":
            self.update_user_status(user_id, "busy")
        
        # Send to business intelligence hub
        self.send_to_business_hub({
            "communication_id": comm_id,
            "assigned_user": user_id,
            "department": department,
            "type": msg_type,
            "content": content,
            "timestamp": datetime.datetime.utcnow().isoformat() + 'Z'
        })
        
        # Log to knowledge repo
        self.log_to_knowledge_repo(comm_id, user_id, department, msg_type, content)
    
    def send_to_business_hub(self, comm_data: dict):
        """Send communication data to Make.com business hub"""
        webhook_url = os.getenv('MAKE_WEBHOOK_URL')
        if webhook_url:
            try:
                response = requests.post(webhook_url, json={
                    "source": "onetalk",
                    "type": "communication_routed",
                    "data": comm_data
                })
                return response.status_code == 200
            except Exception as e:
                print(f"❌ Error sending to business hub: {e}")
        return False
    
    def log_to_knowledge_repo(self, comm_id: str, user_id: str, department: str, msg_type: str, content: str):
        """Log communication to business knowledge repository"""
        timestamp = datetime.datetime.utcnow().isoformat() + 'Z'
        
        log_entry = {
            'timestamp': timestamp,
            'source': 'onetalk_system',
            'communication_id': comm_id,
            'assigned_user': user_id,
            'department': department,
            'type': msg_type,
            'content': content[:200] + "..." if len(content) > 200 else content  # Truncate for privacy
        }
        
        # Write to insights directory
        date_str = timestamp[:10]
        filename = f"insights/{date_str}_onetalk-communications.md"
        
        try:
            # Append to daily log file
            with open(filename, 'a') as f:
                f.write(f"\n## Communication {comm_id[:8]}\n")
                f.write(f"**Time:** {timestamp}\n")
                f.write(f"**Department:** {department}\n")
                f.write(f"**Assigned User:** {user_id}\n")
                f.write(f"**Type:** {msg_type}\n")
                f.write(f"**Preview:** {content[:100]}...\n\n")
        except Exception as e:
            print(f"❌ Error logging to knowledge repo: {e}")
    
    def update_user_status(self, user_id: str, status: str):
        """Update user availability status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users SET status = ? WHERE id = ?
        ''', (status, user_id))
        
        conn.commit()
        conn.close()
    
    def get_department_status(self, department: str = None):
        """Get current status of department(s) and their users"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if department:
            cursor.execute('''
                SELECT u.id, u.name, u.status, u.role, d.name as dept_name
                FROM users u
                JOIN departments d ON u.department = d.id
                WHERE u.department = ?
                ORDER BY u.role DESC, u.name ASC
            ''', (department,))
        else:
            cursor.execute('''
                SELECT u.id, u.name, u.status, u.role, d.name as dept_name
                FROM users u
                JOIN departments d ON u.department = d.id
                ORDER BY d.name, u.role DESC, u.name ASC
            ''')
        
        results = cursor.fetchall()
        conn.close()
        
        # Group by department
        status_report = {}
        for user_id, name, status, role, dept_name in results:
            if dept_name not in status_report:
                status_report[dept_name] = []
            
            status_report[dept_name].append({
                "user_id": user_id,
                "name": name,
                "status": status,
                "role": role
            })
        
        return status_report
    
    def add_routing_rule(self, condition_type: str, condition_value: str, target_department: str, target_user: str = None, priority: int = 10):
        """Add a new routing rule"""
        import uuid
        
        rule_id = str(uuid.uuid4())
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO routing_rules 
            (id, priority, condition_type, condition_value, target_department, target_user)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (rule_id, priority, condition_type, condition_value, target_department, target_user))
        
        conn.commit()
        conn.close()
        
        return f"✅ Routing rule added: {condition_type}={condition_value} → {target_department}"

    def update_department_membership(self, department: str, user_id: str):
        """Update department membership when user is added"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get current department members
        cursor.execute('SELECT phone_numbers FROM departments WHERE id = ?', (department,))
        result = cursor.fetchone()
        
        if result:
            # Department exists, membership is tracked via users table
            pass
        else:
            # Create department if it doesn't exist
            self.create_department(department, department.replace("_", " ").title())
        
        conn.close()
    
    def find_existing_customer(self, phone_number: str):
        """Find if phone number belongs to existing customer"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if phone number has previous communications
        cursor.execute('''
            SELECT c.department_id, c.user_id, COUNT(*) as interaction_count
            FROM communications c
            WHERE c.from_number = ? OR c.to_number = ?
            GROUP BY c.department_id, c.user_id
            ORDER BY interaction_count DESC, c.timestamp DESC
            LIMIT 1
        ''', (phone_number, phone_number))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                "department": result[0],
                "assigned_user": result[1],
                "interaction_count": result[2]
            }
        
        return None
    
    def check_department_condition(self, condition_value: str, from_number: str):
        """Check department-specific conditions for routing"""
        # This can be extended with business logic
        # For now, simple keyword matching
        return condition_value.lower() in from_number.lower()

if __name__ == "__main__":
    # Initialize OneTalk system
    onetalk = OneTalkSystem()
    
    # Example setup
    print("🚀 OneTalk Multi-User System Initialized")
    print("==========================================")
    
    # Create departments
    onetalk.create_department("sales", "Sales Department")
    onetalk.create_department("credit_analysis", "Credit Analysis")
    onetalk.create_department("vehicle_transport", "Vehicle Transport")
    onetalk.create_department("customer_service", "Customer Service")
    
    # Add sample users
    onetalk.add_user("user_001", "Alice Johnson", "sales", role="lead")
    onetalk.add_user("user_002", "Bob Smith", "sales", role="member")
    onetalk.add_user("user_003", "Carol Davis", "credit_analysis", role="lead")
    onetalk.add_user("user_004", "David Wilson", "vehicle_transport", role="lead")
    onetalk.add_user("user_005", "Eve Brown", "customer_service", role="lead")
    
    # Add routing rules
    onetalk.add_routing_rule("phone_pattern", "555-CREDIT", "credit_analysis", priority=1)
    onetalk.add_routing_rule("phone_pattern", "555-TRANSPORT", "vehicle_transport", priority=1)
    
    # Test classification
    print("\n📞 Testing Communication Classification:")
    result = onetalk.classify_incoming_communication(
        from_number="+1234567890",
        to_number="555-CREDIT-01",
        message_type="call",
        content="Hi, I need help with my credit application"
    )
    
    print(f"✅ Communication routed to: {result}")
    
    # Show department status
    print("\n👥 Current Department Status:")
    status = onetalk.get_department_status()
    for dept, users in status.items():
        print(f"\n{dept}:")
        for user in users:
            print(f"  • {user['name']} ({user['role']}) - {user['status']}")