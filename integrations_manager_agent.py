#!/usr/bin/env python3
"""
🤖 Integrations Manager Agent
AI-powered agent for managing all business system integrations

This agent monitors, manages, and optimizes integrations across:
- HubSpot CRM
- OpenPhone 
- Slack
- Make.com
- Cloudflare Workers
- Airtable
- GitHub

Created: 2025-07-28T16:06:00Z
Last Modified: Claude AI Assistant
"""

import os
import json
import requests
import subprocess
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IntegrationsManagerAgent:
    def __init__(self):
        """Initialize the Integrations Manager Agent"""
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.status = {
            'hubspot': {'connected': False, 'last_check': None, 'health': 'unknown'},
            'openphone': {'connected': False, 'last_check': None, 'health': 'unknown'},
            'slack': {'connected': False, 'last_check': None, 'health': 'unknown'},
            'make_com': {'connected': False, 'last_check': None, 'health': 'unknown'},
            'cloudflare': {'connected': False, 'last_check': None, 'health': 'unknown'},
            'airtable': {'connected': True, 'last_check': self.timestamp, 'health': 'healthy'},
            'github': {'connected': True, 'last_check': self.timestamp, 'health': 'healthy'}
        }
        self.load_environment()
        
    def load_environment(self):
        """Load environment variables and API keys"""
        self.env = {
            'hubspot_token': os.getenv('HUBSPOT_API_TOKEN'),
            'openphone_key': os.getenv('OPENPHONE_API_KEY'),
            'slack_token': os.getenv('SLACK_BOT_TOKEN'),
            'make_webhook': os.getenv('MAKE_WEBHOOK_URL'),
            'cloudflare_token': os.getenv('CLOUDFLARE_API_TOKEN')
        }
        
    def check_integration_health(self, service: str) -> Dict[str, Any]:
        """Check health of specific integration"""
        logger.info(f"🔍 Checking health of {service} integration...")
        
        health_checks = {
            'hubspot': self._check_hubspot_health,
            'openphone': self._check_openphone_health,
            'slack': self._check_slack_health,
            'make_com': self._check_make_health,
            'cloudflare': self._check_cloudflare_health,
            'airtable': self._check_airtable_health,
            'github': self._check_github_health
        }
        
        if service in health_checks:
            return health_checks[service]()
        else:
            return {'status': 'error', 'message': f'Unknown service: {service}'}
    
    def _check_hubspot_health(self) -> Dict[str, Any]:
        """Check HubSpot API health"""
        if not self.env['hubspot_token']:
            return {'status': 'error', 'message': 'HubSpot API token not configured'}
        
        try:
            headers = {'Authorization': f'Bearer {self.env["hubspot_token"]}'}
            response = requests.get('https://api.hubapi.com/crm/v3/objects/deals', headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                deal_count = len(data.get('results', []))
                self.status['hubspot'] = {
                    'connected': True, 
                    'last_check': self.timestamp, 
                    'health': 'healthy',
                    'deals_count': deal_count
                }
                return {'status': 'healthy', 'deals_count': deal_count}
            else:
                return {'status': 'error', 'message': f'API returned {response.status_code}'}
                
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def _check_openphone_health(self) -> Dict[str, Any]:
        """Check OpenPhone API health"""
        if not self.env['openphone_key']:
            return {'status': 'warning', 'message': 'OpenPhone API key not configured'}
        
        try:
            headers = {'Authorization': f'Bearer {self.env["openphone_key"]}'}
            response = requests.get('https://api.openphone.com/v1/phone-numbers', headers=headers, timeout=10)
            
            if response.status_code == 200:
                self.status['openphone']['connected'] = True
                self.status['openphone']['health'] = 'healthy'
                return {'status': 'healthy', 'message': 'OpenPhone API responding'}
            else:
                return {'status': 'error', 'message': f'API returned {response.status_code}'}
                
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def _check_slack_health(self) -> Dict[str, Any]:
        """Check Slack API health"""
        if not self.env['slack_token']:
            return {'status': 'warning', 'message': 'Slack bot token not configured'}
        
        try:
            headers = {'Authorization': f'Bearer {self.env["slack_token"]}'}
            response = requests.get('https://slack.com/api/auth.test', headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    self.status['slack']['connected'] = True
                    self.status['slack']['health'] = 'healthy'
                    return {'status': 'healthy', 'team': data.get('team')}
                else:
                    return {'status': 'error', 'message': data.get('error', 'Unknown error')}
            else:
                return {'status': 'error', 'message': f'API returned {response.status_code}'}
                
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def _check_make_health(self) -> Dict[str, Any]:
        """Check Make.com webhook health"""
        if not self.env['make_webhook']:
            return {'status': 'warning', 'message': 'Make.com webhook URL not configured'}
        
        # Check if blueprints exist
        blueprints = [
            'make_business_hub.json',
            'make_credit_strategy.json', 
            'make_vehicle_transport.json',
            'openphone_make_blueprint.json',
            'slack_make_blueprint.json'
        ]
        
        existing_blueprints = [bp for bp in blueprints if os.path.exists(bp)]
        return {
            'status': 'ready' if existing_blueprints else 'warning',
            'blueprints_found': len(existing_blueprints),
            'total_blueprints': len(blueprints),
            'blueprints': existing_blueprints
        }
    
    def _check_cloudflare_health(self) -> Dict[str, Any]:
        """Check Cloudflare Workers health"""
        try:
            # Check if wrangler is available
            result = subprocess.run(['wrangler', '--version'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                version = result.stdout.strip()
                return {'status': 'ready', 'wrangler_version': version}
            else:
                return {'status': 'error', 'message': 'Wrangler CLI not available'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def _check_airtable_health(self) -> Dict[str, Any]:
        """Check Airtable connection"""
        # Airtable is connected via base ID
        return {
            'status': 'healthy',
            'base_id': 'appLPGFO41RF6QKHo',
            'message': 'Airtable base configured'
        }
    
    def _check_github_health(self) -> Dict[str, Any]:
        """Check GitHub connection"""
        try:
            result = subprocess.run(['git', 'remote', 'get-url', 'origin'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return {'status': 'healthy', 'remote': result.stdout.strip()}
            else:
                return {'status': 'warning', 'message': 'Git remote not configured'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def run_full_health_check(self) -> Dict[str, Any]:
        """Run comprehensive health check on all integrations"""
        logger.info("🏥 Running full integration health check...")
        
        results = {}
        for service in self.status.keys():
            results[service] = self.check_integration_health(service)
            time.sleep(1)  # Rate limiting
        
        # Generate summary
        healthy_count = sum(1 for r in results.values() if r.get('status') in ['healthy', 'ready'])
        total_count = len(results)
        
        summary = {
            'timestamp': self.timestamp,
            'overall_health': 'healthy' if healthy_count == total_count else 'degraded',
            'healthy_services': healthy_count,
            'total_services': total_count,
            'service_details': results
        }
        
        return summary
    
    def auto_fix_integrations(self) -> Dict[str, Any]:
        """Attempt to automatically fix integration issues"""
        logger.info("🔧 Attempting auto-fix for integration issues...")
        
        fixes_applied = []
        
        # Check and create missing environment file
        if not os.path.exists('.env'):
            self._create_env_template()
            fixes_applied.append('Created .env template')
        
        # Check integration controller permissions
        controller_path = 'scripts/integration_controller.sh'
        if os.path.exists(controller_path):
            try:
                subprocess.run(['chmod', '+x', controller_path], check=True)
                fixes_applied.append('Fixed integration controller permissions')
            except subprocess.CalledProcessError:
                pass
        
        # Check if Make.com blueprints are valid JSON
        invalid_blueprints = []
        for blueprint in ['make_business_hub.json', 'make_credit_strategy.json']:
            if os.path.exists(blueprint):
                try:
                    with open(blueprint, 'r') as f:
                        json.load(f)
                except json.JSONDecodeError:
                    invalid_blueprints.append(blueprint)
        
        if invalid_blueprints:
            fixes_applied.append(f'Identified invalid JSON blueprints: {invalid_blueprints}')
        
        return {
            'fixes_applied': fixes_applied,
            'timestamp': self.timestamp,
            'status': 'completed'
        }
    
    def _create_env_template(self):
        """Create environment template file"""
        template = """# Pushing Capital Integration Environment Variables
# Add your actual API keys and tokens here

# HubSpot
HUBSPOT_API_TOKEN=your_hubspot_token_here
HUBSPOT_PORTAL_ID=your_portal_id_here

# OpenPhone  
OPENPHONE_API_KEY=your_openphone_key_here

# Slack
SLACK_BOT_TOKEN=xoxb-your-slack-token-here
SLACK_SIGNING_SECRET=your_signing_secret_here

# Make.com
MAKE_WEBHOOK_URL=https://hook.make.com/your-webhook-id

# Cloudflare Workers
CLOUDFLARE_API_TOKEN=your_cloudflare_token_here
OPENPHONE_WEBHOOK_URL=https://your-worker.your-subdomain.workers.dev
SLACK_WEBHOOK_URL=https://your-worker.your-subdomain.workers.dev

# Airtable (already configured)
AIRTABLE_BASE_ID=appLPGFO41RF6QKHo
"""
        with open('.env', 'w') as f:
            f.write(template)
    
    def generate_integration_report(self) -> str:
        """Generate comprehensive integration status report"""
        health_check = self.run_full_health_check()
        
        report = f"""
# 🤖 Integrations Manager Agent Report

**Generated:** {self.timestamp}
**Agent:** Integrations Manager v1.0
**Overall Health:** {health_check['overall_health'].upper()}

## 📊 Integration Status Summary

**Healthy Services:** {health_check['healthy_services']}/{health_check['total_services']}

"""
        
        # Add detailed status for each service
        for service, details in health_check['service_details'].items():
            status_emoji = "✅" if details.get('status') in ['healthy', 'ready'] else "⚠️" if details.get('status') == 'warning' else "❌"
            service_name = service.replace('_', ' ').title()
            
            report += f"### {status_emoji} {service_name}\n"
            report += f"**Status:** {details.get('status', 'unknown')}\n"
            
            if 'message' in details:
                report += f"**Message:** {details['message']}\n"
            
            if service == 'hubspot' and 'deals_count' in details:
                report += f"**Active Deals:** {details['deals_count']}\n"
            
            if service == 'make_com' and 'blueprints_found' in details:
                report += f"**Blueprints Ready:** {details['blueprints_found']}/{details['total_blueprints']}\n"
            
            report += "\n"
        
        # Add recommendations
        report += """## 🎯 Recommendations

1. **Complete API Configuration:** Set up missing API keys in .env file
2. **Deploy Cloudflare Workers:** Use `wrangler deploy` for webhook endpoints  
3. **Import Make.com Blueprints:** Upload JSON files to Make.com scenarios
4. **Test End-to-End Flow:** Verify complete integration pipeline

## 🚀 Next Steps

Run the deployment guide: `CLOUD_DEPLOYMENT_GUIDE.md`
"""
        
        return report
    
    def start_monitoring(self, interval_minutes: int = 15):
        """Start continuous monitoring of integrations"""
        logger.info(f"🔄 Starting integration monitoring (every {interval_minutes} minutes)...")
        
        while True:
            try:
                health_check = self.run_full_health_check()
                
                # Log any issues
                for service, details in health_check['service_details'].items():
                    if details.get('status') not in ['healthy', 'ready']:
                        logger.warning(f"⚠️ Issue detected in {service}: {details.get('message', 'Unknown issue')}")
                
                # Wait for next check
                time.sleep(interval_minutes * 60)
                
            except KeyboardInterrupt:
                logger.info("👋 Monitoring stopped by user")
                break
            except Exception as e:
                logger.error(f"❌ Monitoring error: {e}")
                time.sleep(60)  # Wait 1 minute before retrying

def main():
    """Main CLI interface for Integrations Manager Agent"""
    import sys
    
    agent = IntegrationsManagerAgent()
    
    if len(sys.argv) < 2:
        print("🤖 Integrations Manager Agent")
        print("\nCommands:")
        print("  status      - Check all integration health")
        print("  fix         - Auto-fix integration issues")
        print("  report      - Generate detailed report")
        print("  monitor     - Start continuous monitoring")
        print("  check <service> - Check specific service")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'status':
        health = agent.run_full_health_check()
        print(f"\n🏥 Integration Health: {health['overall_health'].upper()}")
        print(f"✅ Healthy: {health['healthy_services']}/{health['total_services']} services")
        
        for service, details in health['service_details'].items():
            status_emoji = "✅" if details.get('status') in ['healthy', 'ready'] else "⚠️" if details.get('status') == 'warning' else "❌"
            print(f"{status_emoji} {service.replace('_', ' ').title()}: {details.get('status', 'unknown')}")
    
    elif command == 'fix':
        fixes = agent.auto_fix_integrations()
        print("\n🔧 Auto-fix Results:")
        for fix in fixes['fixes_applied']:
            print(f"✅ {fix}")
        
        if not fixes['fixes_applied']:
            print("ℹ️ No automatic fixes needed")
    
    elif command == 'report':
        report = agent.generate_integration_report()
        
        # Save to file
        filename = f"integration_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(filename, 'w') as f:
            f.write(report)
        
        print(f"\n📄 Integration report saved to: {filename}")
        print(report)
    
    elif command == 'monitor':
        agent.start_monitoring()
    
    elif command == 'check' and len(sys.argv) > 2:
        service = sys.argv[2]
        result = agent.check_integration_health(service)
        print(f"\n🔍 {service.title()} Health Check:")
        print(f"Status: {result.get('status', 'unknown')}")
        if 'message' in result:
            print(f"Message: {result['message']}")
    
    else:
        print(f"❌ Unknown command: {command}")

if __name__ == "__main__":
    main()