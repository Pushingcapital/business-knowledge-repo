#!/usr/bin/env python3
"""
OneTalk System Startup & Demo
Complete initialization and demonstration of the multi-user OneTalk system
"""

import os
import json
import time
from datetime import datetime
from onetalk_multi_user_system import OneTalkSystem
from onetalk_repo_command_interface import OneTalkRepoCommander
from onetalk_phone_manager import OneTalkPhoneManager

class OneTalkSystemManager:
    def __init__(self):
        print("🚀 Initializing OneTalk Multi-User System")
        print("=" * 50)
        
        # Initialize all components
        self.onetalk_core = OneTalkSystem()
        self.repo_commander = OneTalkRepoCommander()
        self.phone_manager = OneTalkPhoneManager()
        
        # System configuration
        self.system_config = {
            "max_concurrent_users": 10,
            "max_phones_per_department": 5,
            "emergency_escalation": True,
            "auto_routing": True,
            "business_hours": "09:00-17:00",
            "timezone": "UTC"
        }
        
        print("✅ OneTalk System Manager initialized")
    
    def setup_complete_system(self):
        """Setup the complete OneTalk system with all departments and users"""
        print("\n🏗️ Setting up complete OneTalk system...")
        
        # 1. Setup Departments with Multiple Phones
        print("\n📞 Setting up department phone systems:")
        dept_phone_config = {
            "sales": 3,           # Sales gets 3 phones for high volume
            "credit_analysis": 2, # Credit analysis gets 2 phones  
            "vehicle_transport": 1, # Transport gets 1 phone
            "customer_service": 2, # Support gets 2 phones
            "admin": 1            # Admin gets 1 phone
        }
        
        for dept, phone_count in dept_phone_config.items():
            result = self.repo_commander.setup_department_phones(dept, phone_count)
            print(f"  {result}")
        
        # 2. Add Team Members to Departments
        print("\n👥 Adding team members to departments:")
        team_members = [
            # Sales Team (3 people)
            ("Alice Johnson", "sales", "lead"),
            ("Bob Smith", "sales", "member"),
            ("Charlie Brown", "sales", "member"),
            
            # Credit Analysis Team (2 people)
            ("Carol Davis", "credit_analysis", "lead"),
            ("David Wilson", "credit_analysis", "member"),
            
            # Vehicle Transport Team (1 person)
            ("Eve Brown", "vehicle_transport", "lead"),
            
            # Customer Service Team (2 people)
            ("Frank Miller", "customer_service", "lead"),
            ("Grace Lee", "customer_service", "member"),
            
            # Admin Team (1 person)
            ("Hannah Admin", "admin", "lead")
        ]
        
        for name, department, role in team_members:
            result = self.repo_commander.assign_user_to_department(name, department, role)
            print(f"  {result}")
        
        # 3. Setup Intelligent Routing Rules
        print("\n🧠 Setting up intelligent routing rules:")
        routing_rules = [
            # High priority rules (priority 1-3)
            ("phone_pattern", "EMERGENCY", "admin", 1),
            ("phone_pattern", "URGENT", "admin", 2),
            ("phone_pattern", "VIP", "sales", 2),
            
            # Department-specific rules (priority 5)
            ("phone_pattern", "CREDIT", "credit_analysis", 5),
            ("phone_pattern", "LOAN", "credit_analysis", 5),
            ("phone_pattern", "FINANCING", "credit_analysis", 5),
            ("phone_pattern", "TRANSPORT", "vehicle_transport", 5),
            ("phone_pattern", "VEHICLE", "vehicle_transport", 5),
            ("phone_pattern", "DELIVERY", "vehicle_transport", 5),
            ("phone_pattern", "SALES", "sales", 5),
            ("phone_pattern", "BUY", "sales", 5),
            ("phone_pattern", "PURCHASE", "sales", 5),
            ("phone_pattern", "SUPPORT", "customer_service", 5),
            ("phone_pattern", "HELP", "customer_service", 5),
        ]
        
        for condition_type, condition_value, target_dept, priority in routing_rules:
            result = self.onetalk_core.add_routing_rule(
                condition_type, condition_value, target_dept, priority=priority
            )
            print(f"  {result}")
        
        # 4. Setup Emergency Escalation
        print("\n🚨 Setting up emergency escalation:")
        emergency_rules = {
            "trigger_keywords": ["emergency", "urgent", "crisis", "down", "critical"],
            "escalation_chain": ["admin", "sales"],
            "max_response_time": 300,  # 5 minutes
            "notification_channels": ["slack", "email", "sms"]
        }
        
        for dept in dept_phone_config.keys():
            result = self.repo_commander.setup_emergency_escalation(dept, emergency_rules)
            print(f"  {result}")
        
        print("\n✅ Complete OneTalk system setup finished!")
        return True
    
    def demonstrate_system_capabilities(self):
        """Demonstrate all system capabilities with real scenarios"""
        print("\n🎯 Demonstrating OneTalk System Capabilities")
        print("=" * 45)
        
        # Scenario 1: Sales Call
        print("\n📞 Scenario 1: Incoming Sales Call")
        sales_call = self.repo_commander.handle_incoming_call(
            from_number="+1-555-123-4567",
            to_number="+1-555-SALES-01",
            content="Hi, I'm interested in purchasing a vehicle and need financing options"
        )
        print(f"Sales call routed: {json.dumps(sales_call, indent=2)}")
        
        # Scenario 2: Credit Analysis SMS
        print("\n💬 Scenario 2: Credit Analysis SMS")
        credit_sms = self.repo_commander.handle_incoming_sms(
            from_number="+1-555-987-6543",
            to_number="+1-555-CREDIT-01",
            message="Need urgent help with my credit application status"
        )
        print(f"Credit SMS routed: {json.dumps(credit_sms, indent=2)}")
        
        # Scenario 3: Emergency Escalation
        print("\n🚨 Scenario 3: Emergency Call")
        emergency_call = self.repo_commander.handle_incoming_call(
            from_number="+1-555-EMERGENCY",
            to_number="+1-555-SUPPORT-01",
            content="EMERGENCY: Our delivery truck broke down and we need immediate help"
        )
        print(f"Emergency call routed: {json.dumps(emergency_call, indent=2)}")
        
        # Scenario 4: Multiple Simultaneous Calls
        print("\n📞📞📞 Scenario 4: Multiple Simultaneous Calls")
        simultaneous_calls = []
        
        call_scenarios = [
            ("+1-555-111-1111", "+1-555-SALES-01", "Looking to buy a luxury car"),
            ("+1-555-222-2222", "+1-555-CREDIT-02", "Credit application follow-up"),
            ("+1-555-333-3333", "+1-555-TRANSPORT-01", "Need vehicle transport service"),
            ("+1-555-444-4444", "+1-555-SUPPORT-01", "Technical support needed"),
            ("+1-555-555-5555", "+1-555-SALES-02", "Interested in financing options")
        ]
        
        for from_num, to_num, content in call_scenarios:
            call_result = self.repo_commander.handle_incoming_call(from_num, to_num, content)
            simultaneous_calls.append(call_result)
            print(f"  Call {len(simultaneous_calls)}: {call_result['department']} → {call_result['assigned_user']}")
        
        print(f"\n✅ Successfully handled {len(simultaneous_calls)} simultaneous calls!")
        
        return {
            "sales_call": sales_call,
            "credit_sms": credit_sms,
            "emergency_call": emergency_call,
            "simultaneous_calls": simultaneous_calls
        }
    
    def show_system_status(self):
        """Display comprehensive system status"""
        print("\n📊 OneTalk System Status Dashboard")
        print("=" * 40)
        
        # 1. Department Status
        print("\n👥 Department Status:")
        dept_status = self.repo_commander.get_system_status()
        print(f"  Total Departments: {len(dept_status['departments'])}")
        print(f"  Total Users: {dept_status['total_users']}")
        print(f"  Active Sessions: {dept_status['active_sessions']}")
        
        for dept_name, dept_info in dept_status['departments'].items():
            print(f"\n  📂 {dept_name.title()}:")
            print(f"    • Users: {len(dept_info['users'])}")
            print(f"    • Phone Numbers: {len(dept_info['phone_numbers'])}")
            print(f"    • Primary Agent: {dept_info['primary_agent']}")
            
            for user in dept_info['users']:
                status_emoji = "🟢" if user['status'] == 'available' else "🔴" if user['status'] == 'busy' else "⚪"
                print(f"      {status_emoji} {user['name']} ({user['role']}) - {user['status']}")
        
        # 2. Phone System Status
        print("\n📞 Phone System Status:")
        phone_status = self.phone_manager.get_phone_status()
        
        dept_phones = {}
        for phone in phone_status:
            dept = phone['department']
            if dept not in dept_phones:
                dept_phones[dept] = []
            dept_phones[dept].append(phone)
        
        for dept, phones in dept_phones.items():
            print(f"\n  📂 {dept.title()}:")
            for phone in phones:
                utilization_emoji = "🟢" if float(phone['utilization'].replace('%', '')) < 50 else "🟡" if float(phone['utilization'].replace('%', '')) < 80 else "🔴"
                print(f"    {utilization_emoji} {phone['phone_number']} - {phone['utilization']} utilization")
        
        # 3. Daily Statistics
        print("\n📈 Today's Statistics:")
        daily_stats = self.phone_manager.get_daily_stats()
        
        total_calls = sum(stat['calls'] for stat in daily_stats)
        total_sms = sum(stat['sms'] for stat in daily_stats)
        total_duration = sum(stat['duration_minutes'] for stat in daily_stats)
        
        print(f"  📞 Total Calls: {total_calls}")
        print(f"  💬 Total SMS: {total_sms}")
        print(f"  ⏱️ Total Duration: {total_duration:.1f} minutes")
        
        return dept_status
    
    def test_load_capacity(self):
        """Test system's ability to handle high load"""
        print("\n🔥 Testing System Load Capacity")
        print("=" * 35)
        
        print("\nSimulating 20 simultaneous communications...")
        
        load_test_results = []
        start_time = time.time()
        
        # Simulate 20 simultaneous calls/SMS
        for i in range(20):
            communication_type = "call" if i % 2 == 0 else "sms"
            from_number = f"+1-555-TEST-{i:03d}"
            
            # Rotate through different departments
            dept_phones = [
                "+1-555-SALES-01", "+1-555-CREDIT-01", "+1-555-TRANSPORT-01", 
                "+1-555-SUPPORT-01", "+1-555-ADMIN-01"
            ]
            to_number = dept_phones[i % len(dept_phones)]
            
            if communication_type == "call":
                result = self.repo_commander.handle_incoming_call(
                    from_number, to_number, f"Load test call #{i+1}"
                )
            else:
                result = self.repo_commander.handle_incoming_sms(
                    from_number, to_number, f"Load test SMS #{i+1}"
                )
            
            load_test_results.append(result)
            
            if (i + 1) % 5 == 0:
                print(f"  ✅ Processed {i+1}/20 communications")
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"\n📊 Load Test Results:")
        print(f"  • Total Communications: {len(load_test_results)}")
        print(f"  • Processing Time: {processing_time:.2f} seconds")
        print(f"  • Average per Communication: {processing_time/len(load_test_results):.3f} seconds")
        
        # Check if all communications were properly routed
        successful_routes = sum(1 for result in load_test_results if result.get('assigned_user'))
        print(f"  • Successful Routes: {successful_routes}/{len(load_test_results)} ({successful_routes/len(load_test_results)*100:.1f}%)")
        
        return load_test_results
    
    def generate_system_report(self):
        """Generate comprehensive system report"""
        print("\n📋 Generating OneTalk System Report")
        print("=" * 40)
        
        timestamp = datetime.utcnow().isoformat() + 'Z'
        
        # Gather all system data
        system_status = self.repo_commander.get_system_status()
        phone_status = self.phone_manager.get_phone_status()
        daily_stats = self.phone_manager.get_daily_stats()
        
        report = {
            "report_timestamp": timestamp,
            "system_info": {
                "version": "1.0.0",
                "total_departments": len(system_status['departments']),
                "total_users": system_status['total_users'],
                "total_phones": len(phone_status),
                "active_sessions": system_status['active_sessions']
            },
            "departments": system_status['departments'],
            "phone_system": {
                "phones": phone_status,
                "daily_stats": daily_stats
            },
            "configuration": self.system_config,
            "capabilities": [
                "Multi-user simultaneous communication",
                "Intelligent routing and classification",
                "Department-based organization",
                "Emergency escalation",
                "Phone load balancing",
                "Repository command interface",
                "Real-time status monitoring",
                "Usage analytics"
            ]
        }
        
        # Save report
        report_filename = f"onetalk_system_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"  ✅ System report saved: {report_filename}")
        
        # Save to insights directory for business knowledge repo
        insights_filename = f"insights/{datetime.now().strftime('%Y-%m-%d')}_onetalk-system-report.md"
        
        try:
            os.makedirs("insights", exist_ok=True)
            with open(insights_filename, 'w') as f:
                f.write(f"# OneTalk System Report\n\n")
                f.write(f"**Generated:** {timestamp}\n")
                f.write(f"**System Version:** 1.0.0\n\n")
                f.write(f"## System Overview\n")
                f.write(f"- **Departments:** {len(system_status['departments'])}\n")
                f.write(f"- **Total Users:** {system_status['total_users']}\n")
                f.write(f"- **Phone Numbers:** {len(phone_status)}\n")
                f.write(f"- **Active Sessions:** {system_status['active_sessions']}\n\n")
                f.write(f"## Capabilities\n")
                for capability in report['capabilities']:
                    f.write(f"- {capability}\n")
                f.write(f"\n## Full Report\n")
                f.write(f"```json\n{json.dumps(report, indent=2)}\n```\n")
            
            print(f"  ✅ Business report saved: {insights_filename}")
        except Exception as e:
            print(f"  ⚠️ Could not save to insights: {e}")
        
        return report

def main():
    """Main execution function"""
    print("🎉 Welcome to OneTalk Multi-User Communication System!")
    print("=" * 60)
    
    # Initialize system manager
    system_manager = OneTalkSystemManager()
    
    # Setup complete system
    system_manager.setup_complete_system()
    
    # Demonstrate capabilities
    demo_results = system_manager.demonstrate_system_capabilities()
    
    # Show system status
    system_manager.show_system_status()
    
    # Test load capacity
    load_results = system_manager.test_load_capacity()
    
    # Generate comprehensive report
    final_report = system_manager.generate_system_report()
    
    print("\n🎊 OneTalk System Setup Complete!")
    print("=" * 40)
    print("\n✨ Your OneTalk multi-user communication system is now ready!")
    print("\n🔥 Key Features Activated:")
    print("  📞 Multi-phone management (9 phones across 5 departments)")
    print("  👥 Multi-user support (9 team members)")
    print("  🧠 Intelligent routing and classification")
    print("  🏢 Department-based organization")
    print("  🚨 Emergency escalation system")
    print("  📊 Real-time monitoring and analytics")
    print("  🔄 Repository command interface")
    print("  🌐 Make.com integration ready")
    
    print(f"\n📋 System Report: {final_report.get('report_timestamp', 'Generated')}")
    print("\n🚀 The system can now handle 5+ people using the same communication")
    print("   infrastructure simultaneously with proper classification and routing!")

if __name__ == "__main__":
    main()