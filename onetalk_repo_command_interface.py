#!/usr/bin/env python3
"""
OneTalk Repository Command Interface
Commands repos responsible for different departments and manages multi-user communications
"""

import json
import os
import subprocess
import requests
from typing import Dict, List, Optional
from datetime import datetime
from onetalk_multi_user_system import OneTalkSystem

class OneTalkRepoCommander:
    def __init__(self):
        self.onetalk = OneTalkSystem()
        self.repo_configs = self.load_repo_configurations()
        self.active_sessions = {}  # Track active communication sessions
        
    def load_repo_configurations(self):
        """Load repository configurations for each department"""
        return {
            "sales": {
                "repo_path": "business_repo_knowledge/ai_agents/",
                "primary_agent": "grok_ceo_agent.py",
                "backup_agents": ["integrations_manager_agent.py"],
                "api_endpoints": ["hubspot", "make_com"],
                "phone_numbers": ["+1-555-SALES-01", "+1-555-SALES-02", "+1-555-SALES-03"]
            },
            "credit_analysis": {
                "repo_path": "business_repo_knowledge/services/credit_strategy/",
                "primary_agent": "make_credit_strategy.json",
                "backup_agents": [],
                "api_endpoints": ["airtable", "hubspot"],
                "phone_numbers": ["+1-555-CREDIT-01", "+1-555-CREDIT-02"]
            },
            "vehicle_transport": {
                "repo_path": "business_repo_knowledge/services/vehicle_transport/",
                "primary_agent": "make_vehicle_transport.json",
                "backup_agents": [],
                "api_endpoints": ["make_com", "openphone"],
                "phone_numbers": ["+1-555-TRANSPORT-01"]
            },
            "customer_service": {
                "repo_path": "business_repo_knowledge/communications/",
                "primary_agent": "communications_manager_agent.py",
                "backup_agents": ["email_intelligence_agent.py"],
                "api_endpoints": ["slack", "openphone", "email"],
                "phone_numbers": ["+1-555-SUPPORT-01", "+1-555-SUPPORT-02"]
            },
            "admin": {
                "repo_path": "business_repo_knowledge/ai_agents/",
                "primary_agent": "cursor_ai_agent.py",
                "backup_agents": ["integrations_manager_agent.py"],
                "api_endpoints": ["all"],
                "phone_numbers": ["+1-555-ADMIN-01"]
            }
        }
    
    def setup_department_phones(self, department: str, phone_count: int = 2):
        """Setup multiple phone numbers for a department"""
        if department not in self.repo_configs:
            return f"❌ Unknown department: {department}"
        
        dept_config = self.repo_configs[department]
        current_phones = dept_config.get("phone_numbers", [])
        
        # Generate additional phone numbers if needed
        while len(current_phones) < phone_count:
            phone_num = f"+1-555-{department.upper()}-{len(current_phones)+1:02d}"
            current_phones.append(phone_num)
        
        # Update configuration
        dept_config["phone_numbers"] = current_phones
        
        # Create department in OneTalk system
        self.onetalk.create_department(
            dept_id=department,
            name=department.replace("_", " ").title(),
            phone_numbers=current_phones
        )
        
        return f"✅ {department} department setup with {len(current_phones)} phone numbers"
    
    def assign_user_to_department(self, user_name: str, department: str, role: str = "member", phone_preference: str = None):
        """Assign a user to a department with optional phone preference"""
        if department not in self.repo_configs:
            return f"❌ Unknown department: {department}"
        
        # Generate user ID
        user_id = f"{department}_{user_name.lower().replace(' ', '_')}"
        
        # Assign phone number
        dept_phones = self.repo_configs[department]["phone_numbers"]
        assigned_phone = phone_preference if phone_preference in dept_phones else dept_phones[0]
        
        # Add user to OneTalk system
        result = self.onetalk.add_user(
            user_id=user_id,
            name=user_name,
            department=department,
            phone_number=assigned_phone,
            role=role
        )
        
        # Command the responsible repo to acknowledge new user
        self.command_department_repo(department, "user_added", {
            "user_id": user_id,
            "name": user_name,
            "role": role,
            "phone": assigned_phone
        })
        
        return f"✅ {user_name} assigned to {department} with phone {assigned_phone}"
    
    def command_department_repo(self, department: str, action: str, data: Dict = None):
        """Send commands to department-specific repositories"""
        if department not in self.repo_configs:
            return f"❌ Unknown department: {department}"
        
        dept_config = self.repo_configs[department]
        timestamp = datetime.utcnow().isoformat() + 'Z'
        
        command_data = {
            "timestamp": timestamp,
            "department": department,
            "action": action,
            "data": data or {},
            "source": "onetalk_repo_commander"
        }
        
        # Execute command based on action type
        if action == "route_communication":
            return self._route_communication_to_repo(department, command_data)
        elif action == "user_added":
            return self._notify_repo_user_added(department, command_data)
        elif action == "status_check":
            return self._check_repo_status(department)
        elif action == "emergency_escalation":
            return self._emergency_escalation(department, command_data)
        else:
            return self._generic_repo_command(department, command_data)
    
    def _route_communication_to_repo(self, department: str, command_data: Dict):
        """Route communication to department's responsible repository"""
        dept_config = self.repo_configs[department]
        
        # Log to department-specific knowledge repo
        dept_log_path = f"{dept_config['repo_path']}/communications/"
        os.makedirs(dept_log_path, exist_ok=True)
        
        log_file = f"{dept_log_path}/active_communications_{datetime.now().strftime('%Y-%m-%d')}.json"
        
        try:
            # Load existing communications
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    communications = json.load(f)
            else:
                communications = []
            
            # Add new communication
            communications.append(command_data)
            
            # Save updated communications
            with open(log_file, 'w') as f:
                json.dump(communications, f, indent=2)
            
            # Trigger department agent if available
            self._trigger_department_agent(department, command_data)
            
            return f"✅ Communication routed to {department} repository"
            
        except Exception as e:
            return f"❌ Error routing to {department} repo: {e}"
    
    def _trigger_department_agent(self, department: str, command_data: Dict):
        """Trigger the department's AI agent to handle the communication"""
        dept_config = self.repo_configs[department]
        primary_agent = dept_config["primary_agent"]
        
        # If it's a Python agent, try to execute it
        if primary_agent.endswith('.py'):
            agent_path = f"{dept_config['repo_path']}/{primary_agent}"
            if os.path.exists(agent_path):
                try:
                    # Execute agent with communication data
                    env = os.environ.copy()
                    env['ONETALK_COMMAND_DATA'] = json.dumps(command_data)
                    
                    subprocess.run(['python3', agent_path], env=env, capture_output=True)
                    return True
                except Exception as e:
                    print(f"⚠️ Error executing {primary_agent}: {e}")
        
        # If it's a Make.com scenario, trigger via webhook
        elif primary_agent.endswith('.json'):
            return self._trigger_make_scenario(department, command_data)
        
        return False
    
    def _trigger_make_scenario(self, department: str, command_data: Dict):
        """Trigger Make.com scenario for department"""
        make_webhook_url = os.getenv('MAKE_WEBHOOK_URL')
        if make_webhook_url:
            try:
                response = requests.post(make_webhook_url, json={
                    "source": "onetalk_repo_commander",
                    "department": department,
                    "trigger": "communication_received",
                    "data": command_data
                })
                return response.status_code == 200
            except Exception as e:
                print(f"⚠️ Error triggering Make.com for {department}: {e}")
        return False
    
    def handle_incoming_call(self, from_number: str, to_number: str, content: str = ""):
        """Handle incoming call and route to appropriate department"""
        
        # Classify the communication
        routing_result = self.onetalk.classify_incoming_communication(
            from_number=from_number,
            to_number=to_number,
            message_type="call",
            content=content
        )
        
        department = routing_result.get("department")
        assigned_user = routing_result.get("assigned_user")
        comm_id = routing_result.get("communication_id")
        
        # Command the responsible repo
        repo_result = self.command_department_repo(department, "route_communication", {
            "communication_id": comm_id,
            "from_number": from_number,
            "to_number": to_number,
            "assigned_user": assigned_user,
            "type": "call",
            "content": content
        })
        
        # Track active session
        self.active_sessions[comm_id] = {
            "department": department,
            "user": assigned_user,
            "start_time": datetime.utcnow().isoformat() + 'Z',
            "status": "active"
        }
        
        return {
            "communication_id": comm_id,
            "department": department,
            "assigned_user": assigned_user,
            "repo_command_result": repo_result,
            "phone_numbers": self.repo_configs[department]["phone_numbers"]
        }
    
    def handle_incoming_sms(self, from_number: str, to_number: str, message: str):
        """Handle incoming SMS and route to appropriate department"""
        
        # Classify the communication
        routing_result = self.onetalk.classify_incoming_communication(
            from_number=from_number,
            to_number=to_number,
            message_type="sms",
            content=message
        )
        
        department = routing_result.get("department")
        assigned_user = routing_result.get("assigned_user")
        comm_id = routing_result.get("communication_id")
        
        # Command the responsible repo
        repo_result = self.command_department_repo(department, "route_communication", {
            "communication_id": comm_id,
            "from_number": from_number,
            "to_number": to_number,
            "assigned_user": assigned_user,
            "type": "sms",
            "message": message
        })
        
        return {
            "communication_id": comm_id,
            "department": department,
            "assigned_user": assigned_user,
            "repo_command_result": repo_result
        }
    
    def get_system_status(self):
        """Get comprehensive status of the OneTalk system"""
        
        # Get department status from OneTalk
        dept_status = self.onetalk.get_department_status()
        
        # Add repo status for each department
        system_status = {
            "timestamp": datetime.utcnow().isoformat() + 'Z',
            "departments": {},
            "active_sessions": len(self.active_sessions),
            "total_users": sum(len(users) for users in dept_status.values())
        }
        
        for dept_name, users in dept_status.items():
            repo_status = self.command_department_repo(dept_name, "status_check")
            
            system_status["departments"][dept_name] = {
                "users": users,
                "phone_numbers": self.repo_configs.get(dept_name, {}).get("phone_numbers", []),
                "repo_status": repo_status,
                "primary_agent": self.repo_configs.get(dept_name, {}).get("primary_agent", "N/A")
            }
        
        return system_status
    
    def setup_emergency_escalation(self, department: str, escalation_rules: Dict):
        """Setup emergency escalation rules for a department"""
        
        # Add escalation routing rule
        self.onetalk.add_routing_rule(
            condition_type="emergency",
            condition_value=escalation_rules.get("trigger_keyword", "emergency"),
            target_department="admin",
            priority=1
        )
        
        # Save escalation config
        escalation_config = {
            "department": department,
            "rules": escalation_rules,
            "created_at": datetime.utcnow().isoformat() + 'Z'
        }
        
        config_path = f"business_repo_knowledge/escalations/{department}_escalation.json"
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        with open(config_path, 'w') as f:
            json.dump(escalation_config, f, indent=2)
        
        return f"✅ Emergency escalation setup for {department}"
    
    def _notify_repo_user_added(self, department: str, command_data: Dict):
        """Notify repository that a new user was added"""
        dept_config = self.repo_configs[department]
        
        # Log user addition to department repo
        user_log_path = f"{dept_config['repo_path']}/users/"
        os.makedirs(user_log_path, exist_ok=True)
        
        log_file = f"{user_log_path}/users_{datetime.now().strftime('%Y-%m-%d')}.json"
        
        try:
            # Load existing users
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    users = json.load(f)
            else:
                users = []
            
            # Add new user
            users.append(command_data)
            
            # Save updated users
            with open(log_file, 'w') as f:
                json.dump(users, f, indent=2)
            
            return f"✅ User addition logged to {department} repository"
            
        except Exception as e:
            return f"❌ Error logging user to {department} repo: {e}"
    
    def _emergency_escalation(self, department: str, command_data: Dict):
        """Handle emergency escalation"""
        # Send to admin department immediately
        admin_result = self.command_department_repo("admin", "emergency_received", command_data)
        
        # Log emergency
        emergency_log_path = "business_repo_knowledge/emergencies/"
        os.makedirs(emergency_log_path, exist_ok=True)
        
        emergency_file = f"{emergency_log_path}/emergency_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
        
        try:
            with open(emergency_file, 'w') as f:
                json.dump(command_data, f, indent=2)
            
            return f"🚨 Emergency escalated from {department} to admin"
            
        except Exception as e:
            return f"❌ Error handling emergency: {e}"
    
    def _check_repo_status(self, department: str):
        """Check the status of a department's repository"""
        dept_config = self.repo_configs[department]
        
        status = {
            "department": department,
            "repo_path": dept_config["repo_path"],
            "primary_agent": dept_config["primary_agent"],
            "phone_numbers": dept_config["phone_numbers"],
            "repo_accessible": os.path.exists(dept_config["repo_path"]),
            "agent_accessible": os.path.exists(f"{dept_config['repo_path']}/{dept_config['primary_agent']}")
        }
        
        return status
    
    def _generic_repo_command(self, department: str, command_data: Dict):
        """Execute generic repository command"""
        # Log command to department repo
        dept_config = self.repo_configs[department]
        command_log_path = f"{dept_config['repo_path']}/commands/"
        os.makedirs(command_log_path, exist_ok=True)
        
        log_file = f"{command_log_path}/commands_{datetime.now().strftime('%Y-%m-%d')}.json"
        
        try:
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    commands = json.load(f)
            else:
                commands = []
            
            commands.append(command_data)
            
            with open(log_file, 'w') as f:
                json.dump(commands, f, indent=2)
            
            return f"✅ Command logged to {department} repository"
            
        except Exception as e:
            return f"❌ Error executing command: {e}"

if __name__ == "__main__":
    # Initialize OneTalk Repository Commander
    commander = OneTalkRepoCommander()
    
    print("🎛️ OneTalk Repository Command Interface")
    print("======================================")
    
    # Setup departments with multiple phones
    print("\n📞 Setting up department phone systems:")
    print(commander.setup_department_phones("sales", 3))
    print(commander.setup_department_phones("credit_analysis", 2))
    print(commander.setup_department_phones("vehicle_transport", 1))
    print(commander.setup_department_phones("customer_service", 2))
    print(commander.setup_department_phones("admin", 1))
    
    # Assign users to departments
    print("\n👥 Assigning users to departments:")
    print(commander.assign_user_to_department("Alice Johnson", "sales", "lead"))
    print(commander.assign_user_to_department("Bob Smith", "sales", "member"))
    print(commander.assign_user_to_department("Carol Davis", "credit_analysis", "lead"))
    print(commander.assign_user_to_department("David Wilson", "vehicle_transport", "lead"))
    print(commander.assign_user_to_department("Eve Brown", "customer_service", "lead"))
    
    # Test incoming communication
    print("\n📞 Testing incoming communication:")
    call_result = commander.handle_incoming_call(
        from_number="+1234567890",
        to_number="+1-555-CREDIT-01",
        content="I need help with my credit application urgently"
    )
    print(f"Call routed: {call_result}")
    
    # Get system status
    print("\n📊 System Status:")
    status = commander.get_system_status()
    print(f"Active departments: {len(status['departments'])}")
    print(f"Total users: {status['total_users']}")
    print(f"Active sessions: {status['active_sessions']}")
    
    for dept_name, dept_info in status['departments'].items():
        print(f"\n{dept_name.title()}:")
        print(f"  • Users: {len(dept_info['users'])}")
        print(f"  • Phones: {len(dept_info['phone_numbers'])}")
        print(f"  • Agent: {dept_info['primary_agent']}")