#!/usr/bin/env python3
"""
OneTalk Phone Management System
Manages multiple phone numbers and distributes them across departments
"""

import json
import sqlite3
import os
from datetime import datetime
from typing import Dict, List, Optional
from openphone_api import OpenPhoneAPI

class OneTalkPhoneManager:
    def __init__(self, db_path="onetalk_system.db"):
        self.db_path = db_path
        self.openphone = None
        self.init_phone_database()
        
        # Initialize OpenPhone if API key available
        api_key = os.getenv('OPENPHONE_API_KEY')
        if api_key:
            self.openphone = OpenPhoneAPI(api_key)
    
    def init_phone_database(self):
        """Initialize phone management database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Phone numbers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS phone_numbers (
                id TEXT PRIMARY KEY,
                phone_number TEXT UNIQUE NOT NULL,
                department_id TEXT,
                user_id TEXT,
                status TEXT DEFAULT 'available',  -- available, busy, maintenance
                type TEXT DEFAULT 'business',     -- business, emergency, personal
                priority INTEGER DEFAULT 5,      -- 1-10 priority for routing
                max_concurrent_calls INTEGER DEFAULT 1,
                current_calls INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (department_id) REFERENCES departments (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Call routing table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS call_routing (
                id TEXT PRIMARY KEY,
                from_number TEXT NOT NULL,
                to_number TEXT NOT NULL,
                routed_to_number TEXT,
                routed_to_user TEXT,
                department TEXT,
                routing_reason TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                call_duration INTEGER,
                status TEXT DEFAULT 'active'  -- active, completed, failed
            )
        ''')
        
        # Phone usage statistics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS phone_stats (
                id TEXT PRIMARY KEY,
                phone_number TEXT NOT NULL,
                date TEXT NOT NULL,  -- YYYY-MM-DD
                total_calls INTEGER DEFAULT 0,
                total_sms INTEGER DEFAULT 0,
                total_duration INTEGER DEFAULT 0,  -- seconds
                department_breakdown TEXT,  -- JSON
                UNIQUE(phone_number, date)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def register_phone_number(self, phone_number: str, department_id: str = None, user_id: str = None, 
                            phone_type: str = "business", priority: int = 5, max_concurrent: int = 1):
        """Register a new phone number in the system"""
        import uuid
        
        phone_id = str(uuid.uuid4())
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO phone_numbers 
                (id, phone_number, department_id, user_id, type, priority, max_concurrent_calls)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (phone_id, phone_number, department_id, user_id, phone_type, priority, max_concurrent))
            
            conn.commit()
            
            # Update daily stats
            self.update_phone_stats(phone_number, new_registration=True)
            
            return f"✅ Phone {phone_number} registered for {department_id or 'general use'}"
            
        except sqlite3.IntegrityError:
            return f"❌ Phone {phone_number} already registered"
        except Exception as e:
            return f"❌ Error registering phone: {e}"
        finally:
            conn.close()
    
    def assign_phone_to_department(self, phone_number: str, department_id: str):
        """Assign phone number to a specific department"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE phone_numbers 
            SET department_id = ? 
            WHERE phone_number = ?
        ''', (department_id, phone_number))
        
        if cursor.rowcount > 0:
            conn.commit()
            conn.close()
            return f"✅ Phone {phone_number} assigned to {department_id}"
        else:
            conn.close()
            return f"❌ Phone {phone_number} not found"
    
    def get_available_phone(self, department_id: str = None, priority_min: int = 1):
        """Get available phone number for department or general use"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Try department-specific phones first
        if department_id:
            cursor.execute('''
                SELECT phone_number, max_concurrent_calls, current_calls
                FROM phone_numbers 
                WHERE department_id = ? 
                  AND status = 'available'
                  AND current_calls < max_concurrent_calls
                  AND priority >= ?
                ORDER BY priority DESC, current_calls ASC
                LIMIT 1
            ''', (department_id, priority_min))
            
            result = cursor.fetchone()
            if result:
                conn.close()
                return result[0]
        
        # Fall back to general available phones
        cursor.execute('''
            SELECT phone_number, max_concurrent_calls, current_calls
            FROM phone_numbers 
            WHERE (department_id IS NULL OR department_id = 'general')
              AND status = 'available'
              AND current_calls < max_concurrent_calls
              AND priority >= ?
            ORDER BY priority DESC, current_calls ASC
            LIMIT 1
        ''', (priority_min,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
    
    def route_incoming_call(self, from_number: str, to_number: str, department_hint: str = None):
        """Route incoming call to best available phone/user"""
        import uuid
        
        route_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat() + 'Z'
        
        # Determine target department
        target_department = self.determine_target_department(to_number, department_hint)
        
        # Get best available phone for routing
        routed_phone = self.get_available_phone(target_department)
        
        if not routed_phone:
            # All phones busy, use overflow logic
            routed_phone, routing_reason = self.handle_overflow_routing(target_department)
        else:
            routing_reason = "normal_routing"
        
        # Log the routing decision
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO call_routing 
            (id, from_number, to_number, routed_to_number, department, routing_reason, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (route_id, from_number, to_number, routed_phone, target_department, routing_reason, timestamp))
        
        # Update phone usage
        self.increment_phone_usage(routed_phone, "call")
        
        conn.commit()
        conn.close()
        
        return {
            "route_id": route_id,
            "from_number": from_number,
            "to_number": to_number,
            "routed_to": routed_phone,
            "department": target_department,
            "routing_reason": routing_reason,
            "timestamp": timestamp
        }
    
    def determine_target_department(self, to_number: str, department_hint: str = None):
        """Determine which department should handle the call"""
        
        if department_hint:
            return department_hint
        
        # Check if incoming number is department-specific
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT department_id FROM phone_numbers 
            WHERE phone_number = ? AND department_id IS NOT NULL
        ''', (to_number,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0]
        
        # Default routing based on phone number patterns
        if "SALES" in to_number.upper():
            return "sales"
        elif "CREDIT" in to_number.upper():
            return "credit_analysis"
        elif "TRANSPORT" in to_number.upper():
            return "vehicle_transport"
        elif "SUPPORT" in to_number.upper():
            return "customer_service"
        else:
            return "general"
    
    def handle_overflow_routing(self, department: str):
        """Handle routing when all department phones are busy"""
        
        # Try to find phone with lowest current load
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT phone_number, current_calls, max_concurrent_calls
            FROM phone_numbers 
            WHERE department_id = ? AND status = 'available'
            ORDER BY (current_calls * 1.0 / max_concurrent_calls) ASC
            LIMIT 1
        ''', (department,))
        
        result = cursor.fetchone()
        
        if result:
            conn.close()
            return result[0], "overflow_same_department"
        
        # Try any available phone in system
        cursor.execute('''
            SELECT phone_number, current_calls, max_concurrent_calls
            FROM phone_numbers 
            WHERE status = 'available'
            ORDER BY priority DESC, (current_calls * 1.0 / max_concurrent_calls) ASC
            LIMIT 1
        ''')
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0], "overflow_cross_department"
        
        # All phones busy - use voicemail or callback system
        return self.get_voicemail_number(), "overflow_voicemail"
    
    def get_voicemail_number(self):
        """Get dedicated voicemail number"""
        return "+1-555-VOICE-MAIL"  # Could be configured
    
    def increment_phone_usage(self, phone_number: str, usage_type: str):
        """Increment usage counters for phone number"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Update current calls if it's a call
        if usage_type == "call":
            cursor.execute('''
                UPDATE phone_numbers 
                SET current_calls = current_calls + 1 
                WHERE phone_number = ?
            ''', (phone_number,))
        
        # Update daily stats
        today = datetime.now().strftime('%Y-%m-%d')
        
        if usage_type == "call":
            cursor.execute('''
                INSERT OR IGNORE INTO phone_stats (id, phone_number, date)
                VALUES (?, ?, ?)
            ''', (f"{phone_number}_{today}", phone_number, today))
            
            cursor.execute('''
                UPDATE phone_stats 
                SET total_calls = total_calls + 1 
                WHERE phone_number = ? AND date = ?
            ''', (phone_number, today))
        
        elif usage_type == "sms":
            cursor.execute('''
                INSERT OR IGNORE INTO phone_stats (id, phone_number, date)
                VALUES (?, ?, ?)
            ''', (f"{phone_number}_{today}", phone_number, today))
            
            cursor.execute('''
                UPDATE phone_stats 
                SET total_sms = total_sms + 1 
                WHERE phone_number = ? AND date = ?
            ''', (phone_number, today))
        
        conn.commit()
        conn.close()
    
    def end_call(self, route_id: str, duration_seconds: int):
        """Mark call as ended and update statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get routing info
        cursor.execute('''
            SELECT routed_to_number FROM call_routing WHERE id = ?
        ''', (route_id,))
        
        result = cursor.fetchone()
        if result:
            routed_phone = result[0]
            
            # Update call routing record
            cursor.execute('''
                UPDATE call_routing 
                SET call_duration = ?, status = 'completed'
                WHERE id = ?
            ''', (duration_seconds, route_id))
            
            # Decrement current calls
            cursor.execute('''
                UPDATE phone_numbers 
                SET current_calls = MAX(0, current_calls - 1) 
                WHERE phone_number = ?
            ''', (routed_phone,))
            
            # Update daily duration stats
            today = datetime.now().strftime('%Y-%m-%d')
            cursor.execute('''
                UPDATE phone_stats 
                SET total_duration = total_duration + ?
                WHERE phone_number = ? AND date = ?
            ''', (duration_seconds, routed_phone, today))
        
        conn.commit()
        conn.close()
    
    def get_phone_status(self, department: str = None):
        """Get current status of all phones"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if department:
            cursor.execute('''
                SELECT phone_number, status, current_calls, max_concurrent_calls, type, priority
                FROM phone_numbers 
                WHERE department_id = ?
                ORDER BY priority DESC, phone_number
            ''', (department,))
        else:
            cursor.execute('''
                SELECT phone_number, department_id, status, current_calls, max_concurrent_calls, type, priority
                FROM phone_numbers 
                ORDER BY department_id, priority DESC, phone_number
            ''')
        
        results = cursor.fetchall()
        conn.close()
        
        phone_status = []
        for row in results:
            if department:
                phone_status.append({
                    "phone_number": row[0],
                    "status": row[1],
                    "current_calls": row[2],
                    "max_concurrent": row[3],
                    "type": row[4],
                    "priority": row[5],
                    "utilization": f"{(row[2]/row[3]*100):.1f}%" if row[3] > 0 else "0%"
                })
            else:
                phone_status.append({
                    "phone_number": row[0],
                    "department": row[1] or "general",
                    "status": row[2],
                    "current_calls": row[3],
                    "max_concurrent": row[4],
                    "type": row[5],
                    "priority": row[6],
                    "utilization": f"{(row[3]/row[4]*100):.1f}%" if row[4] > 0 else "0%"
                })
        
        return phone_status
    
    def get_daily_stats(self, date: str = None):
        """Get daily usage statistics"""
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.phone_number, p.department_id, 
                   s.total_calls, s.total_sms, s.total_duration
            FROM phone_numbers p
            LEFT JOIN phone_stats s ON p.phone_number = s.phone_number AND s.date = ?
            ORDER BY p.department_id, p.phone_number
        ''', (date,))
        
        results = cursor.fetchall()
        conn.close()
        
        stats = []
        for row in results:
            stats.append({
                "phone_number": row[0],
                "department": row[1] or "general",
                "calls": row[2] or 0,
                "sms": row[3] or 0,
                "duration_minutes": round((row[4] or 0) / 60, 1)
            })
        
        return stats
    
    def update_phone_stats(self, phone_number: str, new_registration: bool = False):
        """Update phone statistics"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        if new_registration:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR IGNORE INTO phone_stats (id, phone_number, date)
                VALUES (?, ?, ?)
            ''', (f"{phone_number}_{today}", phone_number, today))
            
            conn.commit()
            conn.close()

if __name__ == "__main__":
    # Initialize phone manager
    phone_manager = OneTalkPhoneManager()
    
    print("📞 OneTalk Phone Management System")
    print("=================================")
    
    # Register sample phone numbers
    print("\n📱 Registering phone numbers:")
    departments = {
        "sales": ["+1-555-SALES-01", "+1-555-SALES-02", "+1-555-SALES-03"],
        "credit_analysis": ["+1-555-CREDIT-01", "+1-555-CREDIT-02"],
        "vehicle_transport": ["+1-555-TRANSPORT-01"],
        "customer_service": ["+1-555-SUPPORT-01", "+1-555-SUPPORT-02"],
        "admin": ["+1-555-ADMIN-01"]
    }
    
    for dept, phones in departments.items():
        for i, phone in enumerate(phones):
            priority = 10 if i == 0 else 5  # First phone gets higher priority
            result = phone_manager.register_phone_number(phone, dept, priority=priority)
            print(f"  {result}")
    
    # Test call routing
    print("\n📞 Testing call routing:")
    routing_result = phone_manager.route_incoming_call(
        from_number="+1234567890",
        to_number="+1-555-SALES-01"
    )
    print(f"Call routed: {routing_result}")
    
    # Show phone status
    print("\n📊 Phone Status:")
    status = phone_manager.get_phone_status()
    for phone in status:
        print(f"  {phone['phone_number']} ({phone['department']}) - {phone['status']} - {phone['utilization']} utilization")
    
    # Show daily stats
    print("\n📈 Daily Statistics:")
    stats = phone_manager.get_daily_stats()
    for stat in stats:
        print(f"  {stat['phone_number']}: {stat['calls']} calls, {stat['sms']} SMS, {stat['duration_minutes']}min")