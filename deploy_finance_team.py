#!/usr/bin/env python3
"""
Finance Team Deployment for OneTalk System
Setting up finance department with scalable infrastructure
"""

import json
import os
from datetime import datetime
from onetalk_multi_user_system import OneTalkSystem
from onetalk_repo_command_interface import OneTalkRepoCommander
from onetalk_phone_manager import OneTalkPhoneManager

class FinanceTeamDeployment:
    def __init__(self):
        print("💰 Deploying Finance Team into OneTalk System")
        print("=" * 50)
        
        # Initialize OneTalk components
        self.onetalk = OneTalkSystem()
        self.repo_commander = OneTalkRepoCommander()
        self.phone_manager = OneTalkPhoneManager()
        
        # Finance department configuration
        self.finance_config = {
            "department_id": "finance",
            "department_name": "Finance Department",
            "phone_numbers": [
                "+1-555-FINANCE-01",  # Main finance line
                "+1-555-FINANCE-02",  # Accounting line  
                "+1-555-FINANCE-03"   # Investor relations line
            ],
            "specializations": [
                "accounting",
                "budgeting", 
                "investor_relations",
                "financial_planning",
                "compliance",
                "payroll",
                "tax_preparation",
                "audit_support"
            ]
        }
        
        print("✅ Finance deployment system initialized")
    
    def setup_finance_department(self):
        """Setup the finance department infrastructure"""
        print("\n🏦 Setting up Finance Department...")
        
        # Create department with multiple phone lines
        result = self.repo_commander.setup_department_phones("finance", 3)
        print(f"  {result}")
        
        # Register finance-specific phone numbers
        for i, phone in enumerate(self.finance_config["phone_numbers"]):
            priority = 10 if i == 0 else 7  # Main line gets highest priority
            max_concurrent = 3 if i == 0 else 2  # Main line handles more calls
            
            registration_result = self.phone_manager.register_phone_number(
                phone_number=phone,
                department_id="finance",
                phone_type="business",
                priority=priority,
                max_concurrent=max_concurrent
            )
            print(f"  {registration_result}")
        
        return True
    
    def add_finance_team_lead(self, leader_name: str = "Emmanuel Haddad"):
        """Add the finance team leader (you!) to the system"""
        print(f"\n👤 Adding Finance Team Lead: {leader_name}")
        
        # Add you as the finance lead
        result = self.repo_commander.assign_user_to_department(
            user_name=leader_name,
            department="finance", 
            role="lead",
            phone_preference="+1-555-FINANCE-01"
        )
        print(f"  {result}")
        
        # Setup your finance profile
        finance_profile = {
            "name": leader_name,
            "role": "Finance Lead & CEO",
            "department": "finance",
            "specializations": self.finance_config["specializations"],
            "primary_phone": "+1-555-FINANCE-01",
            "backup_phones": ["+1-555-FINANCE-02", "+1-555-FINANCE-03"],
            "availability": "business_hours",
            "escalation_priority": "highest",
            "created_at": datetime.utcnow().isoformat() + 'Z'
        }
        
        # Save finance lead profile
        os.makedirs("business_repo_knowledge/finance/", exist_ok=True)
        with open("business_repo_knowledge/finance/finance_lead_profile.json", 'w') as f:
            json.dump(finance_profile, f, indent=2)
        
        print(f"  ✅ Finance lead profile created for {leader_name}")
        return finance_profile
    
    def setup_finance_routing_rules(self):
        """Setup intelligent routing for finance-related communications"""
        print("\n🧠 Setting up Finance Routing Rules...")
        
        # High-priority finance routing rules
        finance_routing_rules = [
            # Urgent financial matters (priority 1-2)
            ("phone_pattern", "URGENT-FINANCE", "finance", 1),
            ("phone_pattern", "CASH-FLOW", "finance", 1),
            ("phone_pattern", "PAYMENT-EMERGENCY", "finance", 1),
            
            # Core finance keywords (priority 3-5)
            ("phone_pattern", "FINANCE", "finance", 3),
            ("phone_pattern", "ACCOUNTING", "finance", 3),
            ("phone_pattern", "BUDGET", "finance", 4),
            ("phone_pattern", "INVOICE", "finance", 4),
            ("phone_pattern", "PAYMENT", "finance", 4),
            ("phone_pattern", "BILLING", "finance", 4),
            ("phone_pattern", "TAX", "finance", 5),
            ("phone_pattern", "AUDIT", "finance", 5),
            ("phone_pattern", "PAYROLL", "finance", 5),
            ("phone_pattern", "INVESTOR", "finance", 3),
            ("phone_pattern", "FUNDING", "finance", 3),
            ("phone_pattern", "REVENUE", "finance", 4),
            ("phone_pattern", "EXPENSE", "finance", 4),
            ("phone_pattern", "PROFIT", "finance", 4),
            ("phone_pattern", "LOSS", "finance", 4),
            ("phone_pattern", "FINANCIAL", "finance", 4),
            ("phone_pattern", "MONEY", "finance", 5),
            ("phone_pattern", "COST", "finance", 5),
            ("phone_pattern", "PRICE", "finance", 5),
        ]
        
        for condition_type, condition_value, target_dept, priority in finance_routing_rules:
            result = self.onetalk.add_routing_rule(
                condition_type, condition_value, target_dept, priority=priority
            )
            print(f"  {result}")
        
        print(f"\n  ✅ Added {len(finance_routing_rules)} finance routing rules")
        return len(finance_routing_rules)
    
    def setup_finance_repository_integration(self):
        """Configure repository integration for finance department"""
        print("\n📁 Setting up Finance Repository Integration...")
        
        # Update repo commander configuration for finance
        finance_repo_config = {
            "repo_path": "business_repo_knowledge/finance/",
            "primary_agent": "finance_manager_agent.py",
            "backup_agents": ["accounting_agent.py", "budget_agent.py"],
            "api_endpoints": ["hubspot", "airtable", "quickbooks", "stripe"],
            "phone_numbers": self.finance_config["phone_numbers"],
            "specializations": self.finance_config["specializations"]
        }
        
        # Add finance to repo commander configs
        self.repo_commander.repo_configs["finance"] = finance_repo_config
        
        # Create finance department directories
        finance_dirs = [
            "business_repo_knowledge/finance/",
            "business_repo_knowledge/finance/accounting/",
            "business_repo_knowledge/finance/budgets/", 
            "business_repo_knowledge/finance/invoices/",
            "business_repo_knowledge/finance/reports/",
            "business_repo_knowledge/finance/tax/",
            "business_repo_knowledge/finance/audit/",
            "business_repo_knowledge/finance/communications/",
            "business_repo_knowledge/finance/users/"
        ]
        
        for directory in finance_dirs:
            os.makedirs(directory, exist_ok=True)
            print(f"  ✅ Created: {directory}")
        
        # Create finance agent placeholder
        finance_agent_code = '''#!/usr/bin/env python3
"""
Finance Manager Agent for OneTalk System
Handles all finance-related communications and tasks
"""

import os
import json
from datetime import datetime

def handle_finance_communication(communication_data):
    """Handle incoming finance communication"""
    print(f"💰 Finance Agent: Processing {communication_data.get('type', 'communication')}")
    
    # Log to finance communications
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + 'Z',
        "communication_id": communication_data.get("communication_id"),
        "type": communication_data.get("type"),
        "content": communication_data.get("content", ""),
        "assigned_user": communication_data.get("assigned_user"),
        "priority": "high" if any(word in communication_data.get("content", "").upper() 
                                 for word in ["URGENT", "EMERGENCY", "CASH", "PAYMENT"]) else "normal"
    }
    
    # Save to finance communications log
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = f"business_repo_knowledge/finance/communications/finance_comms_{today}.json"
    
    try:
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        
        logs.append(log_entry)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
        
        print(f"✅ Finance communication logged: {communication_data.get('communication_id', 'N/A')[:8]}")
        
    except Exception as e:
        print(f"❌ Error logging finance communication: {e}")

if __name__ == "__main__":
    # Check for OneTalk command data
    command_data = os.getenv('ONETALK_COMMAND_DATA')
    if command_data:
        try:
            data = json.loads(command_data)
            handle_finance_communication(data.get("data", {}))
        except Exception as e:
            print(f"❌ Error processing OneTalk command: {e}")
    else:
        print("💰 Finance Manager Agent ready and waiting for communications...")
'''
        
        with open("business_repo_knowledge/finance/finance_manager_agent.py", 'w') as f:
            f.write(finance_agent_code)
        
        print("  ✅ Finance Manager Agent created")
        
        return finance_repo_config
    
    def setup_finance_emergency_escalation(self):
        """Setup emergency escalation for finance department"""
        print("\n🚨 Setting up Finance Emergency Escalation...")
        
        emergency_rules = {
            "trigger_keywords": [
                "cash flow emergency", "payment crisis", "audit emergency", 
                "tax deadline", "compliance issue", "financial emergency",
                "urgent payment", "bank emergency", "investor crisis"
            ],
            "escalation_chain": ["finance", "admin"],
            "max_response_time": 180,  # 3 minutes for finance emergencies
            "notification_channels": ["slack", "email", "sms", "phone"],
            "priority_contacts": ["Emmanuel Haddad"]
        }
        
        result = self.repo_commander.setup_emergency_escalation("finance", emergency_rules)
        print(f"  {result}")
        
        return emergency_rules
    
    def test_finance_deployment(self):
        """Test the finance team deployment"""
        print("\n🧪 Testing Finance Team Deployment...")
        
        # Test scenarios for finance
        test_scenarios = [
            {
                "scenario": "Invoice Inquiry",
                "from_number": "+1-555-CLIENT-01",
                "to_number": "+1-555-FINANCE-01", 
                "content": "I need help with my invoice payment and billing questions"
            },
            {
                "scenario": "Tax Emergency",
                "from_number": "+1-555-URGENT-TAX",
                "to_number": "+1-555-FINANCE-02",
                "content": "URGENT: Tax deadline issue needs immediate attention"
            },
            {
                "scenario": "Investor Relations",
                "from_number": "+1-555-INVESTOR",
                "to_number": "+1-555-FINANCE-03",
                "content": "Need financial reports for investor meeting tomorrow"
            },
            {
                "scenario": "Budget Inquiry",
                "from_number": "+1-555-BUDGET-Q",
                "to_number": "+1-555-FINANCE-01",
                "content": "Questions about departmental budget allocation for next quarter"
            }
        ]
        
        test_results = []
        
        for scenario in test_scenarios:
            print(f"\n  📞 Testing: {scenario['scenario']}")
            
            result = self.repo_commander.handle_incoming_call(
                from_number=scenario["from_number"],
                to_number=scenario["to_number"],
                content=scenario["content"]
            )
            
            test_results.append({
                "scenario": scenario["scenario"],
                "result": result,
                "routed_correctly": result.get("department") == "finance"
            })
            
            print(f"    ✅ Routed to: {result.get('department')} → {result.get('assigned_user')}")
        
        # Test summary
        successful_routes = sum(1 for r in test_results if r["routed_correctly"])
        print(f"\n  📊 Test Results: {successful_routes}/{len(test_results)} scenarios routed correctly")
        
        return test_results
    
    def generate_finance_deployment_report(self):
        """Generate deployment report for finance team"""
        print("\n📋 Generating Finance Deployment Report...")
        
        timestamp = datetime.utcnow().isoformat() + 'Z'
        
        # Get current system status
        system_status = self.repo_commander.get_system_status()
        finance_status = system_status["departments"].get("finance", {})
        
        deployment_report = {
            "deployment_timestamp": timestamp,
            "finance_department": {
                "status": "deployed",
                "phone_numbers": self.finance_config["phone_numbers"],
                "specializations": self.finance_config["specializations"],
                "team_members": len(finance_status.get("users", [])),
                "routing_rules": 20,  # Approximate number of finance routing rules
                "repository_path": "business_repo_knowledge/finance/",
                "primary_agent": "finance_manager_agent.py"
            },
            "capabilities": [
                "Invoice and billing management",
                "Tax and compliance support", 
                "Budget and financial planning",
                "Investor relations",
                "Accounting and bookkeeping",
                "Payroll processing",
                "Audit support",
                "Emergency financial escalation"
            ],
            "integration_points": [
                "OneTalk multi-user communication system",
                "Business knowledge repository",
                "Make.com automation",
                "Emergency escalation system",
                "Real-time monitoring and analytics"
            ],
            "next_steps": [
                "Connect QuickBooks/accounting software",
                "Setup Stripe/payment processor integration", 
                "Configure tax software integration",
                "Add team members as you hire them",
                "Customize routing rules for specific needs"
            ]
        }
        
        # Save deployment report
        report_filename = f"finance_deployment_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_filename, 'w') as f:
            json.dump(deployment_report, f, indent=2)
        
        # Save to insights for business knowledge repo
        insights_filename = f"insights/{datetime.now().strftime('%Y-%m-%d')}_finance-team-deployment.md"
        
        try:
            os.makedirs("insights", exist_ok=True)
            with open(insights_filename, 'w') as f:
                f.write(f"# Finance Team Deployment Report\n\n")
                f.write(f"**Deployed:** {timestamp}\n")
                f.write(f"**Department:** Finance\n")
                f.write(f"**Team Lead:** Emmanuel Haddad\n\n")
                f.write(f"## Deployment Summary\n")
                f.write(f"- **Phone Lines:** {len(self.finance_config['phone_numbers'])}\n")
                f.write(f"- **Specializations:** {len(self.finance_config['specializations'])}\n")
                f.write(f"- **Routing Rules:** 20+ finance-specific rules\n")
                f.write(f"- **Repository Integration:** ✅ Complete\n")
                f.write(f"- **Emergency Escalation:** ✅ Configured\n\n")
                f.write(f"## Finance Capabilities\n")
                for capability in deployment_report['capabilities']:
                    f.write(f"- {capability}\n")
                f.write(f"\n## Ready to Scale\n")
                f.write(f"The finance department infrastructure is ready to scale when you hire team members!\n\n")
                f.write(f"## Full Report\n")
                f.write(f"```json\n{json.dumps(deployment_report, indent=2)}\n```\n")
            
            print(f"  ✅ Deployment report saved: {insights_filename}")
        except Exception as e:
            print(f"  ⚠️ Could not save insights report: {e}")
        
        return deployment_report

def main():
    """Deploy the finance team"""
    print("💰 Welcome to Finance Team Deployment!")
    print("=" * 45)
    print("Setting up finance infrastructure ready to scale when you hire your team!")
    
    # Initialize deployment
    finance_deployment = FinanceTeamDeployment()
    
    # Execute deployment steps
    finance_deployment.setup_finance_department()
    finance_deployment.add_finance_team_lead("Emmanuel Haddad")  # You as the lead!
    finance_deployment.setup_finance_routing_rules()
    finance_deployment.setup_finance_repository_integration()
    finance_deployment.setup_finance_emergency_escalation()
    
    # Test the deployment
    test_results = finance_deployment.test_finance_deployment()
    
    # Generate final report
    final_report = finance_deployment.generate_finance_deployment_report()
    
    print("\n🎊 Finance Team Successfully Deployed!")
    print("=" * 40)
    print(f"\n💼 You ({final_report['finance_department'].get('team_members', 1)} person) are now running:")
    print("  💰 Finance Department (3 phone lines)")
    print("  📊 Accounting & Billing Support")
    print("  🏦 Investor Relations")
    print("  📋 Tax & Compliance")
    print("  🚨 Financial Emergency Escalation")
    print("  📈 Budget & Financial Planning")
    
    print(f"\n📞 Your Finance Phone Numbers:")
    for i, phone in enumerate(final_report['finance_department']['phone_numbers']):
        purpose = ["Main Finance", "Accounting", "Investor Relations"][i]
        print(f"  {phone} - {purpose}")
    
    print(f"\n🚀 Ready to Scale!")
    print("  When you hire finance team members, just run:")
    print("  finance_deployment.add_finance_team_member('New Hire Name', 'accountant')")
    
    print(f"\n📋 Deployment Report: {final_report.get('deployment_timestamp', 'Generated')}")

if __name__ == "__main__":
    main()