#!/usr/bin/env python3
"""
Quick Start Script for Security Login Automation
Sets up the system with interactive configuration
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_banner():
    """Print welcome banner"""
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║           🔐 Security Login Automation System                ║
    ║                                                               ║
    ║        Cutting-edge Selenium automation for daily            ║
    ║           security login requirements                         ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_commands = ['docker', 'docker-compose', 'python3']
    missing = []
    
    for cmd in required_commands:
        if subprocess.run(['which', cmd], capture_output=True).returncode != 0:
            missing.append(cmd)
    
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        print("\nPlease install the missing dependencies:")
        print("- Docker: https://docs.docker.com/get-docker/")
        print("- Docker Compose: https://docs.docker.com/compose/install/")
        print("- Python 3: https://www.python.org/downloads/")
        return False
    
    print("✅ All dependencies found")
    return True

def deploy_system():
    """Deploy the automation system"""
    print("\n🚀 Deploying Security Login Automation System...")
    
    try:
        # Make deploy script executable
        os.chmod('deploy.sh', 0o755)
        
        # Run deployment
        result = subprocess.run(['./deploy.sh', 'deploy'], check=True)
        
        if result.returncode == 0:
            print("✅ System deployed successfully!")
            return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Deployment failed: {e}")
        return False
    
    return False

def setup_first_site():
    """Guide user through setting up their first site"""
    print("\n🏠 Let's set up your first site for automation!")
    print("This interactive setup will help you configure your first login site.")
    
    try:
        subprocess.run(['python3', 'config_manager.py', 'add'], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Site setup failed: {e}")
        return False

def show_next_steps():
    """Show what to do next"""
    print("\n🎉 Setup Complete! Here's what you can do now:")
    print("""
    📊 Monitoring Dashboards:
       • Grafana:    http://localhost:3000 (admin/admin123)
       • Prometheus: http://localhost:9090
       • Metrics:    http://localhost:8080/metrics

    🔧 Management Commands:
       • List sites:     python3 config_manager.py list
       • Test login:     python3 config_manager.py test
       • Add more sites: python3 config_manager.py add

    🐳 Docker Commands:
       • View logs:      docker-compose logs -f
       • Stop system:    docker-compose down
       • Restart:        docker-compose restart

    📁 Important Files:
       • Logs:           ./logs/
       • Screenshots:    ./screenshots/
       • Configuration:  ./configs/
    """)

def main():
    """Main setup flow"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Deploy system
    if not deploy_system():
        print("\n❌ Deployment failed. Please check the logs and try again.")
        sys.exit(1)
    
    # Wait for services to be ready
    print("\n⏳ Waiting for services to be ready...")
    time.sleep(15)
    
    # Setup first site
    setup_choice = input("\n🤔 Would you like to set up your first site now? (y/n): ")
    if setup_choice.lower().startswith('y'):
        if setup_first_site():
            # Test the site
            test_choice = input("\n🧪 Would you like to test the login now? (y/n): ")
            if test_choice.lower().startswith('y'):
                try:
                    subprocess.run(['python3', 'config_manager.py', 'test'])
                except subprocess.CalledProcessError:
                    print("Test completed (check logs for details)")
    
    # Show next steps
    show_next_steps()
    
    print("\n🚀 Your Security Login Automation System is ready!")
    print("💡 Tip: The system will automatically run daily at 9:00 AM")

if __name__ == "__main__":
    main() 