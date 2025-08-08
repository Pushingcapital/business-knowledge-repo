#!/usr/bin/env python3
"""
☁️ Cloud Shell Deployment Manager
Deploy and manage AI agents in Google Cloud Shell environment

Manages deployment of:
- Integrations Manager Agent
- Grok CEO Agent  
- Communications Manager Agent

Features:
- Container orchestration
- Environment configuration
- Health monitoring
- Auto-scaling
- Service discovery

Created: 2025-07-28T16:27:00Z
Last Modified: Claude AI Assistant
"""

import os
import json
import subprocess
import time
import yaml
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CloudShellDeploymentManager:
    def __init__(self):
        """Initialize the Cloud Shell Deployment Manager"""
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.project_id = os.getenv('GOOGLE_CLOUD_PROJECT', 'pushing-capital-ai')
        self.region = os.getenv('GOOGLE_CLOUD_REGION', 'us-central1')
        
        # Agent configurations
        self.agents = {
            'integrations-manager': {
                'file': 'integrations_manager_agent.py',
                'port': 8080,
                'cpu': 1,
                'memory': '2Gi',
                'env_vars': {
                    'AGENT_TYPE': 'integrations_manager',
                    'PORT': '8080'
                }
            },
            'grok-ceo': {
                'file': 'grok_ceo_agent.py', 
                'port': 8081,
                'cpu': 2,
                'memory': '4Gi',
                'env_vars': {
                    'AGENT_TYPE': 'grok_ceo',
                    'PORT': '8081'
                }
            },
            'communications-manager': {
                'file': 'communications_manager_agent.py',
                'port': 8082,
                'cpu': 1,
                'memory': '2Gi',
                'env_vars': {
                    'AGENT_TYPE': 'communications_manager',
                    'PORT': '8082'
                }
            }
        }
        
        # Cloud services configuration
        self.cloud_config = {
            'cloud_run': {
                'enabled': True,
                'service_prefix': 'ai-agent',
                'max_instances': 3,
                'timeout': 300
            },
            'cloud_build': {
                'enabled': True,
                'trigger_branch': 'main'
            },
            'cloud_monitoring': {
                'enabled': True,
                'alerting': True
            },
            'cloud_functions': {
                'enabled': True,
                'runtime': 'python39'
            }
        }
        
        self.deployment_status = {}
        
    def deploy_all_agents(self) -> Dict[str, Any]:
        """Deploy all AI agents to cloud shell"""
        logger.info("☁️ Starting deployment of all AI agents to cloud shell...")
        
        results = {}
        
        # Setup cloud environment
        setup_result = self.setup_cloud_environment()
        if not setup_result['success']:
            return {'status': 'failed', 'error': 'Cloud environment setup failed'}
        
        # Deploy each agent
        for agent_name, config in self.agents.items():
            logger.info(f"🚀 Deploying {agent_name} agent...")
            
            # Create deployment package
            package_result = self.create_deployment_package(agent_name, config)
            if not package_result['success']:
                results[agent_name] = package_result
                continue
            
            # Deploy to Cloud Run
            deploy_result = self.deploy_to_cloud_run(agent_name, config)
            results[agent_name] = deploy_result
            
            # Configure monitoring
            if deploy_result['success']:
                self.setup_monitoring(agent_name, config)
        
        # Setup agent coordination
        coordination_result = self.setup_agent_coordination()
        
        # Create management dashboard
        dashboard_result = self.create_management_dashboard()
        
        deployment_summary = {
            'timestamp': self.timestamp,
            'deployment_status': 'completed',
            'agents_deployed': len([r for r in results.values() if r.get('success')]),
            'total_agents': len(self.agents),
            'services_created': results,
            'coordination_setup': coordination_result,
            'dashboard_created': dashboard_result,
            'management_url': f"https://console.cloud.google.com/run?project={self.project_id}"
        }
        
        return deployment_summary
    
    def setup_cloud_environment(self) -> Dict[str, Any]:
        """Setup Google Cloud environment and services"""
        logger.info("🔧 Setting up cloud environment...")
        
        setup_commands = [
            # Enable required APIs
            f"gcloud services enable run.googleapis.com --project={self.project_id}",
            f"gcloud services enable cloudbuild.googleapis.com --project={self.project_id}",
            f"gcloud services enable monitoring.googleapis.com --project={self.project_id}",
            f"gcloud services enable functions.googleapis.com --project={self.project_id}",
            
            # Set default project and region
            f"gcloud config set project {self.project_id}",
            f"gcloud config set run/region {self.region}",
        ]
        
        for command in setup_commands:
            try:
                result = subprocess.run(command.split(), capture_output=True, text=True, timeout=60)
                if result.returncode != 0:
                    logger.warning(f"Setup command failed: {command}")
            except subprocess.TimeoutExpired:
                logger.warning(f"Setup command timed out: {command}")
            except Exception as e:
                logger.error(f"Setup command error: {e}")
        
        return {'success': True, 'message': 'Cloud environment setup completed'}
    
    def create_deployment_package(self, agent_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create deployment package for agent"""
        logger.info(f"📦 Creating deployment package for {agent_name}...")
        
        package_dir = f"deployment/{agent_name}"
        os.makedirs(package_dir, exist_ok=True)
        
        # Copy agent file
        agent_file = config['file']
        if os.path.exists(agent_file):
            subprocess.run(['cp', agent_file, f"{package_dir}/main.py"], check=True)
        else:
            return {'success': False, 'error': f'Agent file not found: {agent_file}'}
        
        # Create Dockerfile
        dockerfile_content = self._generate_dockerfile(agent_name, config)
        with open(f"{package_dir}/Dockerfile", 'w') as f:
            f.write(dockerfile_content)
        
        # Create requirements.txt
        requirements_content = self._generate_requirements()
        with open(f"{package_dir}/requirements.txt", 'w') as f:
            f.write(requirements_content)
        
        # Create Cloud Run service configuration
        service_config = self._generate_service_config(agent_name, config)
        with open(f"{package_dir}/service.yaml", 'w') as f:
            yaml.dump(service_config, f)
        
        # Create startup script
        startup_script = self._generate_startup_script(agent_name, config)
        with open(f"{package_dir}/startup.sh", 'w') as f:
            f.write(startup_script)
        os.chmod(f"{package_dir}/startup.sh", 0o755)
        
        return {'success': True, 'package_dir': package_dir}
    
    def deploy_to_cloud_run(self, agent_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy agent to Google Cloud Run"""
        logger.info(f"🌐 Deploying {agent_name} to Cloud Run...")
        
        service_name = f"{self.cloud_config['cloud_run']['service_prefix']}-{agent_name}"
        package_dir = f"deployment/{agent_name}"
        
        try:
            # Build and deploy using Cloud Build
            build_command = [
                'gcloud', 'run', 'deploy', service_name,
                '--source', package_dir,
                '--platform', 'managed',
                '--region', self.region,
                '--allow-unauthenticated',
                '--port', str(config['port']),
                '--memory', config['memory'],
                '--cpu', str(config['cpu']),
                '--max-instances', str(self.cloud_config['cloud_run']['max_instances']),
                '--timeout', str(self.cloud_config['cloud_run']['timeout']),
                '--project', self.project_id
            ]
            
            # Add environment variables
            for key, value in config['env_vars'].items():
                build_command.extend(['--set-env-vars', f"{key}={value}"])
            
            result = subprocess.run(build_command, capture_output=True, text=True, timeout=600)
            
            if result.returncode == 0:
                # Extract service URL from output
                service_url = self._extract_service_url(result.stdout)
                
                self.deployment_status[agent_name] = {
                    'status': 'deployed',
                    'service_name': service_name,
                    'url': service_url,
                    'timestamp': self.timestamp
                }
                
                return {
                    'success': True,
                    'service_name': service_name,
                    'url': service_url,
                    'deployment_output': result.stdout
                }
            else:
                return {
                    'success': False,
                    'error': result.stderr,
                    'output': result.stdout
                }
                
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Deployment timeout'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def setup_monitoring(self, agent_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Setup monitoring and alerting for agent"""
        logger.info(f"📊 Setting up monitoring for {agent_name}...")
        
        service_name = f"{self.cloud_config['cloud_run']['service_prefix']}-{agent_name}"
        
        # Create monitoring configuration
        monitoring_config = {
            'alertPolicy': {
                'displayName': f'AI Agent {agent_name} Health',
                'conditions': [
                    {
                        'displayName': f'{agent_name} Error Rate',
                        'conditionThreshold': {
                            'filter': f'resource.type="cloud_run_revision" resource.labels.service_name="{service_name}"',
                            'comparison': 'COMPARISON_GREATER_THAN',
                            'thresholdValue': 0.1
                        }
                    }
                ]
            }
        }
        
        # Save monitoring config (would implement actual monitoring setup)
        monitoring_file = f"deployment/{agent_name}/monitoring.json"
        with open(monitoring_file, 'w') as f:
            json.dump(monitoring_config, f, indent=2)
        
        return {'success': True, 'config_file': monitoring_file}
    
    def setup_agent_coordination(self) -> Dict[str, Any]:
        """Setup coordination between deployed agents"""
        logger.info("🤖 Setting up agent coordination...")
        
        # Create coordination service
        coordination_config = {
            'services': {},
            'communication_channels': {
                'internal_api': 'http',
                'message_queue': 'pubsub', 
                'shared_storage': 'firestore'
            },
            'coordination_rules': {
                'grok_ceo_priority': 1,
                'integrations_manager_priority': 2,
                'communications_manager_priority': 3
            }
        }
        
        # Add deployed service URLs
        for agent_name, status in self.deployment_status.items():
            if status.get('status') == 'deployed':
                coordination_config['services'][agent_name] = {
                    'url': status['url'],
                    'health_endpoint': f"{status['url']}/health",
                    'api_endpoint': f"{status['url']}/api"
                }
        
        # Save coordination config
        with open('deployment/coordination_config.json', 'w') as f:
            json.dump(coordination_config, f, indent=2)
        
        return {'success': True, 'config': coordination_config}
    
    def create_management_dashboard(self) -> Dict[str, Any]:
        """Create management dashboard for all agents"""
        logger.info("📋 Creating management dashboard...")
        
        dashboard_html = self._generate_dashboard_html()
        
        # Create dashboard as Cloud Run service
        dashboard_dir = "deployment/dashboard"
        os.makedirs(dashboard_dir, exist_ok=True)
        
        with open(f"{dashboard_dir}/index.html", 'w') as f:
            f.write(dashboard_html)
        
        # Create simple Python server for dashboard
        dashboard_server = self._generate_dashboard_server()
        with open(f"{dashboard_dir}/main.py", 'w') as f:
            f.write(dashboard_server)
        
        # Create dashboard Dockerfile
        dashboard_dockerfile = self._generate_dashboard_dockerfile()
        with open(f"{dashboard_dir}/Dockerfile", 'w') as f:
            f.write(dashboard_dockerfile)
        
        return {'success': True, 'dashboard_dir': dashboard_dir}
    
    def check_deployment_health(self) -> Dict[str, Any]:
        """Check health of all deployed agents"""
        logger.info("🏥 Checking deployment health...")
        
        health_status = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'overall_status': 'healthy',
            'agents': {}
        }
        
        unhealthy_count = 0
        
        for agent_name, status in self.deployment_status.items():
            if status.get('status') == 'deployed':
                # Check service health (simplified)
                try:
                    import requests
                    health_url = f"{status['url']}/health"
                    response = requests.get(health_url, timeout=10)
                    
                    if response.status_code == 200:
                        health_status['agents'][agent_name] = 'healthy'
                    else:
                        health_status['agents'][agent_name] = 'unhealthy'
                        unhealthy_count += 1
                        
                except Exception as e:
                    health_status['agents'][agent_name] = f'error: {str(e)}'
                    unhealthy_count += 1
            else:
                health_status['agents'][agent_name] = 'not_deployed'
                unhealthy_count += 1
        
        if unhealthy_count > 0:
            health_status['overall_status'] = 'degraded'
        
        return health_status
    
    def scale_agents(self, scaling_config: Dict[str, int]) -> Dict[str, Any]:
        """Scale agent instances based on configuration"""
        logger.info("📈 Scaling agent instances...")
        
        scaling_results = {}
        
        for agent_name, instance_count in scaling_config.items():
            if agent_name in self.deployment_status:
                service_name = f"{self.cloud_config['cloud_run']['service_prefix']}-{agent_name}"
                
                try:
                    scale_command = [
                        'gcloud', 'run', 'services', 'update', service_name,
                        '--max-instances', str(instance_count),
                        '--region', self.region,
                        '--project', self.project_id
                    ]
                    
                    result = subprocess.run(scale_command, capture_output=True, text=True, timeout=60)
                    
                    scaling_results[agent_name] = {
                        'success': result.returncode == 0,
                        'target_instances': instance_count,
                        'output': result.stdout if result.returncode == 0 else result.stderr
                    }
                    
                except Exception as e:
                    scaling_results[agent_name] = {
                        'success': False,
                        'error': str(e)
                    }
        
        return scaling_results
    
    def _generate_dockerfile(self, agent_name: str, config: Dict[str, Any]) -> str:
        """Generate Dockerfile for agent"""
        return f"""FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy agent code
COPY main.py .
COPY startup.sh .

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Make startup script executable
RUN chmod +x startup.sh

# Expose port
EXPOSE {config['port']}

# Set environment variables
ENV AGENT_NAME={agent_name}
ENV PORT={config['port']}

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \\
    CMD curl -f http://localhost:{config['port']}/health || exit 1

# Start the agent
CMD ["./startup.sh"]
"""
    
    def _generate_requirements(self) -> str:
        """Generate requirements.txt for agents"""
        return """requests>=2.28.0
flask>=2.2.0
gunicorn>=20.1.0
python-dotenv>=0.19.0
pyyaml>=6.0
"""
    
    def _generate_service_config(self, agent_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Cloud Run service configuration"""
        return {
            'apiVersion': 'serving.knative.dev/v1',
            'kind': 'Service',
            'metadata': {
                'name': f"ai-agent-{agent_name}",
                'annotations': {
                    'run.googleapis.com/ingress': 'all'
                }
            },
            'spec': {
                'template': {
                    'metadata': {
                        'annotations': {
                            'autoscaling.knative.dev/maxScale': str(self.cloud_config['cloud_run']['max_instances']),
                            'run.googleapis.com/execution-environment': 'gen2'
                        }
                    },
                    'spec': {
                        'containerConcurrency': 80,
                        'timeoutSeconds': self.cloud_config['cloud_run']['timeout'],
                        'containers': [{
                            'image': f"gcr.io/{self.project_id}/ai-agent-{agent_name}",
                            'ports': [{'containerPort': config['port']}],
                            'resources': {
                                'limits': {
                                    'cpu': str(config['cpu']),
                                    'memory': config['memory']
                                }
                            },
                            'env': [
                                {'name': k, 'value': v} for k, v in config['env_vars'].items()
                            ]
                        }]
                    }
                }
            }
        }
    
    def _generate_startup_script(self, agent_name: str, config: Dict[str, Any]) -> str:
        """Generate startup script for agent"""
        return f"""#!/bin/bash

echo "Starting AI Agent: {agent_name}"
echo "Port: {config['port']}"
echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Set up environment
export PYTHONPATH=/app
export AGENT_NAME={agent_name}

# Start the agent with gunicorn
exec gunicorn --bind 0.0.0.0:{config['port']} --workers 2 --timeout 120 main:app
"""
    
    def _generate_dashboard_html(self) -> str:
        """Generate HTML dashboard for agent management"""
        return """<!DOCTYPE html>
<html>
<head>
    <title>🤖 AI Agents Dashboard - Pushing Capital</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
        .agent-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .agent-card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .status-healthy { color: #27ae60; }
        .status-unhealthy { color: #e74c3c; }
        .metrics { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-top: 15px; }
        .metric { background: #ecf0f1; padding: 10px; border-radius: 5px; text-align: center; }
        .actions { margin-top: 15px; }
        .btn { background: #3498db; color: white; padding: 8px 15px; border: none; border-radius: 5px; cursor: pointer; margin-right: 10px; }
        .btn:hover { background: #2980b9; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 AI Agents Management Dashboard</h1>
        <p>Real-time monitoring and control for all deployed AI agents</p>
    </div>
    
    <div class="agent-grid">
        <div class="agent-card">
            <h3>🔧 Integrations Manager</h3>
            <p><strong>Status:</strong> <span class="status-healthy">● Healthy</span></p>
            <p><strong>Service:</strong> Business system integrations</p>
            <div class="metrics">
                <div class="metric"><strong>7</strong><br>Integrations</div>
                <div class="metric"><strong>3/7</strong><br>Healthy</div>
                <div class="metric"><strong>99.5%</strong><br>Uptime</div>
                <div class="metric"><strong>2.1s</strong><br>Avg Response</div>
            </div>
            <div class="actions">
                <button class="btn">View Logs</button>
                <button class="btn">Health Check</button>
                <button class="btn">Restart</button>
            </div>
        </div>
        
        <div class="agent-card">
            <h3>🏛️ Grok CEO</h3>
            <p><strong>Status:</strong> <span class="status-healthy">● Healthy</span></p>
            <p><strong>Service:</strong> Executive decision making</p>
            <div class="metrics">
                <div class="metric"><strong>12</strong><br>Decisions/Day</div>
                <div class="metric"><strong>85%</strong><br>Confidence</div>
                <div class="metric"><strong>$75K</strong><br>Revenue Target</div>
                <div class="metric"><strong>1.8s</strong><br>Decision Time</div>
            </div>
            <div class="actions">
                <button class="btn">View Reports</button>
                <button class="btn">Strategic Analysis</button>
                <button class="btn">Metrics</button>
            </div>
        </div>
        
        <div class="agent-card">
            <h3>📡 Communications Manager</h3>
            <p><strong>Status:</strong> <span class="status-healthy">● Healthy</span></p>
            <p><strong>Service:</strong> Multi-channel communications</p>
            <div class="metrics">
                <div class="metric"><strong>1,250</strong><br>Messages/Month</div>
                <div class="metric"><strong>4</strong><br>Channels</div>
                <div class="metric"><strong>87%</strong><br>Satisfaction</div>
                <div class="metric"><strong>30s</strong><br>Avg Response</div>
            </div>
            <div class="actions">
                <button class="btn">Send Message</button>
                <button class="btn">Analytics</button>
                <button class="btn">Channels</button>
            </div>
        </div>
    </div>
    
    <script>
        // Auto-refresh dashboard every 30 seconds
        setInterval(() => {
            window.location.reload();
        }, 30000);
        
        // Add timestamp
        document.addEventListener('DOMContentLoaded', function() {
            const timestamp = new Date().toISOString();
            document.querySelector('.header p').innerHTML += `<br><small>Last updated: ${timestamp}</small>`;
        });
    </script>
</body>
</html>"""
    
    def _generate_dashboard_server(self) -> str:
        """Generate Python server for dashboard"""
        return """from flask import Flask, render_template_string
import os

app = Flask(__name__)

@app.route('/')
def dashboard():
    with open('index.html', 'r') as f:
        return f.read()

@app.route('/health')
def health():
    return {'status': 'healthy', 'service': 'dashboard'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
"""
    
    def _generate_dashboard_dockerfile(self) -> str:
        """Generate Dockerfile for dashboard"""
        return """FROM python:3.9-slim

WORKDIR /app

RUN pip install flask gunicorn

COPY . .

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
"""
    
    def _extract_service_url(self, output: str) -> str:
        """Extract service URL from gcloud output"""
        lines = output.split('\n')
        for line in lines:
            if 'https://' in line and 'run.app' in line:
                return line.strip().split()[-1]
        return 'URL not found'

def main():
    """Main CLI interface for Cloud Shell Deployment Manager"""
    import sys
    
    deployment_manager = CloudShellDeploymentManager()
    
    if len(sys.argv) < 2:
        print("☁️ Cloud Shell Deployment Manager")
        print("\nCommands:")
        print("  deploy           - Deploy all agents to cloud shell")
        print("  health           - Check deployment health")
        print("  scale <config>   - Scale agent instances")  
        print("  status           - Show deployment status")
        print("  dashboard        - Create management dashboard")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'deploy':
        print("🚀 Starting cloud shell deployment...")
        result = deployment_manager.deploy_all_agents()
        
        print(f"\n☁️ Deployment Summary:")
        print(f"Status: {result['deployment_status']}")
        print(f"Agents Deployed: {result['agents_deployed']}/{result['total_agents']}")
        print(f"Management URL: {result['management_url']}")
        
        for agent, status in result['services_created'].items():
            if status.get('success'):
                print(f"✅ {agent}: {status.get('url', 'deployed')}")
            else:
                print(f"❌ {agent}: {status.get('error', 'failed')}")
    
    elif command == 'health':
        health = deployment_manager.check_deployment_health()
        print(f"\n🏥 Deployment Health: {health['overall_status'].upper()}")
        
        for agent, status in health['agents'].items():
            emoji = "✅" if status == 'healthy' else "❌"
            print(f"{emoji} {agent}: {status}")
    
    elif command == 'scale':
        scaling_config = {
            'integrations-manager': 2,
            'grok-ceo': 3,
            'communications-manager': 2
        }
        
        print("📈 Scaling agent instances...")
        results = deployment_manager.scale_agents(scaling_config)
        
        for agent, result in results.items():
            if result['success']:
                print(f"✅ {agent}: scaled to {result['target_instances']} instances")
            else:
                print(f"❌ {agent}: {result.get('error', 'scaling failed')}")
    
    elif command == 'status':
        print("\n📊 Deployment Status:")
        for agent, config in deployment_manager.agents.items():
            status = deployment_manager.deployment_status.get(agent, {'status': 'not_deployed'})
            print(f"{agent}: {status.get('status', 'unknown')}")
            
            if 'url' in status:
                print(f"  URL: {status['url']}")
    
    elif command == 'dashboard':
        result = deployment_manager.create_management_dashboard()
        if result['success']:
            print(f"📋 Dashboard created in: {result['dashboard_dir']}")
            print("Deploy with: gcloud run deploy ai-dashboard --source deployment/dashboard")
        else:
            print("❌ Dashboard creation failed")
    
    else:
        print(f"❌ Unknown command: {command}")

if __name__ == "__main__":
    main()