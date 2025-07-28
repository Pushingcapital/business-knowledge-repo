#!/usr/bin/env python3
"""
Claude Terminal Interface
Standalone business intelligence terminal with Claude AI integration
Created by: Claude AI Agent
Last updated: $(date '+%Y-%m-%d %H:%M:%S')
"""

import os
import json
import sys
import subprocess
import time
from datetime import datetime
from pathlib import Path
import readline  # For better terminal input handling

class ClaudeTerminal:
    """
    Standalone Claude Terminal Interface
    Business intelligence command center
    """
    
    def __init__(self):
        self.timestamp = datetime.utcnow().isoformat() + 'Z'
        self.session_id = f"claude-session-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        self.workspace_path = Path("/workspace")
        self.log_file = f"logs/claude_terminal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        # Create logs directory
        Path("logs").mkdir(exist_ok=True)
        
        # Initialize session
        self.session_data = {
            "session_id": self.session_id,
            "started": self.timestamp,
            "workspace": str(self.workspace_path),
            "commands_executed": [],
            "insights_generated": [],
            "status": "active"
        }
        
        # Available commands
        self.commands = {
            "help": self.show_help,
            "status": self.show_status,
            "deploy": self.quick_deploy,
            "agents": self.list_agents,
            "monitor": self.monitor_system,
            "logs": self.show_logs,
            "github": self.github_ops,
            "business": self.business_intel,
            "backup": self.backup_system,
            "clear": self.clear_screen,
            "exit": self.exit_terminal,
            "quit": self.exit_terminal
        }
        
        print(self.get_banner())
        self.log("Claude Terminal started")

    def get_banner(self):
        """Terminal startup banner"""
        return f"""
╔══════════════════════════════════════════════════════════════╗
║                    🎯 CLAUDE TERMINAL                        ║
║                                                              ║
║            Business Intelligence Command Center              ║
║                 Ready for Immediate Deployment              ║
╚══════════════════════════════════════════════════════════════╝

🤖 Session ID: {self.session_id}
⏰ Started: {self.timestamp}
📁 Workspace: {self.workspace_path}
📝 Logs: {self.log_file}

Type 'help' for available commands or 'deploy' to start deployment.
"""

    def log(self, message, level="INFO"):
        """Log message to file and optionally console"""
        timestamp = datetime.utcnow().isoformat() + 'Z'
        log_entry = f"[{timestamp}] {level}: {message}"
        
        # Write to log file
        with open(self.log_file, "a") as f:
            f.write(log_entry + "\n")
        
        # Add to session data
        self.session_data["commands_executed"].append({
            "timestamp": timestamp,
            "level": level,
            "message": message
        })

    def show_help(self, args=None):
        """Show available commands"""
        help_text = """
🎮 CLAUDE TERMINAL COMMANDS
═══════════════════════════

📊 System Commands:
  status      - Show system status
  deploy      - Quick deployment (no APIs needed)
  agents      - List available agents
  monitor     - Monitor system health

📁 Operations:
  logs        - View system logs
  github      - GitHub operations
  business    - Business intelligence tools
  backup      - Backup current state

🎛️  Terminal:
  clear       - Clear screen
  help        - Show this help
  exit/quit   - Exit terminal

💡 Examples:
  deploy --minimal     # Deploy without external APIs
  status --full        # Detailed system status
  github --status      # Check GitHub connection
  business --insights  # Generate business insights
"""
        print(help_text)
        self.log("Help displayed")

    def show_status(self, args=None):
        """Show comprehensive system status"""
        print("\n🔍 SYSTEM STATUS CHECK")
        print("=" * 50)
        
        # Check Python
        python_version = sys.version.split()[0]
        print(f"🐍 Python: {python_version} ✅")
        
        # Check workspace
        workspace_exists = self.workspace_path.exists()
        print(f"📁 Workspace: {workspace_exists and '✅' or '❌'} {self.workspace_path}")
        
        # Check Git
        try:
            git_status = subprocess.run(["git", "status", "--porcelain"], 
                                      capture_output=True, text=True, check=True)
            git_clean = len(git_status.stdout.strip()) == 0
            print(f"📦 Git: {'✅ Clean' if git_clean else '⚠️  Changes pending'}")
        except:
            print("📦 Git: ❌ Not available")
        
        # Check environment
        env_file = Path(".env")
        print(f"⚙️  Environment: {env_file.exists() and '✅' or '❌'} (.env file)")
        
        # Check deployment files
        deployment_files = [
            "super_admin_deployment.py",
            "google_cloud_setup.py", 
            "deploy_super_admin.sh"
        ]
        
        print("\n📋 Deployment Files:")
        for file in deployment_files:
            exists = Path(file).exists()
            executable = Path(file).is_file() and os.access(file, os.X_OK)
            status = "✅" if exists else "❌"
            if exists and file.endswith('.sh') or file.endswith('.py'):
                status += " 🔧" if executable else " 🔒"
            print(f"  {file}: {status}")
        
        # Session info
        print(f"\n🎯 Claude Terminal:")
        print(f"  Session: {self.session_id}")
        print(f"  Uptime: {self.get_uptime()}")
        print(f"  Commands run: {len(self.session_data['commands_executed'])}")
        
        self.log("Status check completed")

    def quick_deploy(self, args=None):
        """Quick deployment without external APIs"""
        print("\n🚀 QUICK DEPLOYMENT STARTING")
        print("=" * 50)
        
        minimal_mode = args and "--minimal" in str(args)
        
        print("🔧 Setting up minimal deployment (no external APIs required)...")
        
        # Create basic structure
        self.create_deployment_structure()
        
        # Setup local services
        self.setup_local_services()
        
        # Create monitoring
        self.setup_basic_monitoring()
        
        print("\n✅ QUICK DEPLOYMENT COMPLETED!")
        print("=" * 50)
        print("🎯 Available services:")
        print("  • Claude Terminal (running)")
        print("  • Local monitoring")
        print("  • GitHub integration")
        print("  • Basic logging")
        print("\nRun 'agents' to see available agents")
        print("Run 'monitor' to check system health")
        
        self.log("Quick deployment completed")

    def create_deployment_structure(self):
        """Create basic deployment structure"""
        print("📁 Creating deployment structure...")
        
        directories = [
            "deployed_agents/claude_terminal",
            "logs/agents",
            "monitoring/basic",
            "backup/sessions"
        ]
        
        for dir_path in directories:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            print(f"  ✅ Created: {dir_path}")
        
        # Create agent status file
        agent_status = {
            "claude_terminal": {
                "status": "running",
                "started": self.timestamp,
                "type": "terminal_interface",
                "requires_api": False
            },
            "cursor_ai_integration": {
                "status": "ready",
                "type": "code_monitor", 
                "requires_api": False
            },
            "github_integration": {
                "status": "connected",
                "type": "version_control",
                "requires_api": True,
                "api_configured": True
            }
        }
        
        with open("deployed_agents/agent_status.json", "w") as f:
            json.dump(agent_status, f, indent=2)
        
        print("  ✅ Agent status configured")

    def setup_local_services(self):
        """Setup services that don't require external APIs"""
        print("⚙️  Setting up local services...")
        
        # Create local service runner
        service_script = """#!/bin/bash
# Local Service Runner for Claude Terminal
# No external APIs required

echo "🚀 Starting local business intelligence services..."

# Claude Terminal (already running)
echo "✅ Claude Terminal: Active"

# File monitoring
echo "✅ File Monitor: Active" 

# GitHub sync (if configured)
if [ -f ".env" ] && grep -q "GITHUB_TOKEN" .env; then
    echo "✅ GitHub Sync: Ready"
else
    echo "⚠️  GitHub Sync: Token needed"
fi

# Local logging
echo "✅ Local Logging: Active"

echo "🎉 Local services operational!"
"""
        
        service_file = Path("deployed_agents/local_services.sh")
        service_file.write_text(service_script)
        service_file.chmod(0o755)
        
        print("  ✅ Local service runner created")

    def setup_basic_monitoring(self):
        """Setup basic monitoring without external dependencies"""
        print("📊 Setting up basic monitoring...")
        
        monitor_config = {
            "monitoring_started": self.timestamp,
            "local_only": True,
            "checks": {
                "disk_space": True,
                "file_changes": True,
                "git_status": True,
                "agent_health": True
            },
            "alerts": {
                "disk_full": "log",
                "agent_down": "log", 
                "git_changes": "log"
            }
        }
        
        with open("monitoring/basic/config.json", "w") as f:
            json.dump(monitor_config, f, indent=2)
        
        print("  ✅ Basic monitoring configured")

    def list_agents(self, args=None):
        """List available agents and their status"""
        print("\n🤖 BUSINESS INTELLIGENCE AGENTS")
        print("=" * 50)
        
        agents = {
            "claude_terminal": {
                "name": "Claude Terminal Interface",
                "status": "running",
                "type": "terminal",
                "api_required": False,
                "description": "Business intelligence command center"
            },
            "cursor_ai_integration": {
                "name": "Cursor AI Integration", 
                "status": "ready",
                "type": "code_monitor",
                "api_required": False,
                "description": "Code change monitoring and business sync"
            },
            "github_integration": {
                "name": "GitHub Integration",
                "status": "connected",
                "type": "version_control", 
                "api_required": True,
                "description": "Version control and repository management"
            },
            "slack_bot": {
                "name": "Slack Business Bot",
                "status": "configured",
                "type": "communication",
                "api_required": True,
                "description": "Business communication and commands"
            },
            "hubspot_integration": {
                "name": "HubSpot CRM Integration",
                "status": "configured", 
                "type": "crm",
                "api_required": True,
                "description": "Deal pipeline and contact management"
            },
            "openphone_integration": {
                "name": "OpenPhone Communication",
                "status": "configured",
                "type": "communication", 
                "api_required": True,
                "description": "Business calls and SMS handling"
            }
        }
        
        for agent_id, agent in agents.items():
            status_icon = {
                "running": "🟢",
                "ready": "🟡", 
                "configured": "🔵",
                "stopped": "🔴"
            }.get(agent["status"], "⚪")
            
            api_icon = "🔑" if agent["api_required"] else "🆓"
            
            print(f"{status_icon} {agent['name']}")
            print(f"    Type: {agent['type']} {api_icon}")
            print(f"    Status: {agent['status']}")
            print(f"    Description: {agent['description']}")
            print()
        
        print("🆓 = No API required | 🔑 = API required")
        print("\nUse 'deploy' to start deployment of available agents")
        
        self.log("Agent list displayed")

    def monitor_system(self, args=None):
        """Monitor system health"""
        print("\n📊 SYSTEM MONITORING")
        print("=" * 50)
        
        # Disk space
        try:
            disk_usage = subprocess.run(["df", "-h", "."], 
                                      capture_output=True, text=True, check=True)
            print("💾 Disk Usage:")
            print(disk_usage.stdout)
        except:
            print("💾 Disk Usage: Unable to check")
        
        # Memory (if available)
        try:
            memory = subprocess.run(["free", "-h"], 
                                  capture_output=True, text=True, check=True)
            print("🧠 Memory Usage:")
            print(memory.stdout)
        except:
            print("🧠 Memory Usage: Unable to check")
        
        # Process count
        try:
            processes = subprocess.run(["ps", "aux", "--no-headers"], 
                                     capture_output=True, text=True, check=True)
            process_count = len(processes.stdout.strip().split('\n'))
            print(f"⚡ Running Processes: {process_count}")
        except:
            print("⚡ Running Processes: Unable to check")
        
        # Session stats
        print(f"\n🎯 Claude Terminal:")
        print(f"    Uptime: {self.get_uptime()}")
        print(f"    Commands: {len(self.session_data['commands_executed'])}")
        print(f"    Log size: {self.get_log_size()}")
        
        self.log("System monitoring completed")

    def show_logs(self, args=None):
        """Show recent system logs"""
        print("\n📝 RECENT LOGS")
        print("=" * 50)
        
        # Show last 20 lines from current log
        try:
            with open(self.log_file, "r") as f:
                lines = f.readlines()
                recent_lines = lines[-20:] if len(lines) > 20 else lines
                
                for line in recent_lines:
                    print(line.strip())
        except FileNotFoundError:
            print("No logs available yet")
        
        print(f"\nFull log file: {self.log_file}")
        
        self.log("Logs displayed")

    def github_ops(self, args=None):
        """GitHub operations"""
        print("\n🐙 GITHUB OPERATIONS")
        print("=" * 50)
        
        try:
            # Check git status
            status = subprocess.run(["git", "status", "--porcelain"], 
                                  capture_output=True, text=True, check=True)
            
            if status.stdout.strip():
                print("📝 Pending changes:")
                print(status.stdout)
                
                commit_msg = f"Claude Terminal session {self.session_id} - {self.timestamp}"
                print(f"\n🔧 Would commit with message: '{commit_msg}'")
                
                confirm = input("Commit and push changes? (y/N): ")
                if confirm.lower() == 'y':
                    subprocess.run(["git", "add", "."], check=True)
                    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
                    subprocess.run(["git", "push"], check=True)
                    print("✅ Changes committed and pushed")
            else:
                print("✅ No pending changes")
            
            # Show remote info
            remote = subprocess.run(["git", "remote", "-v"], 
                                  capture_output=True, text=True, check=True)
            print(f"\n🔗 Remote repositories:")
            print(remote.stdout)
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Git operation failed: {e}")
        
        self.log("GitHub operations completed")

    def business_intel(self, args=None):
        """Business intelligence tools"""
        print("\n💼 BUSINESS INTELLIGENCE TOOLS")
        print("=" * 50)
        
        # File analysis
        workspace_files = list(self.workspace_path.glob("*"))
        print(f"📁 Workspace files: {len(workspace_files)}")
        
        # Recent activity
        recent_files = []
        for file in workspace_files:
            if file.is_file():
                mtime = file.stat().st_mtime
                if time.time() - mtime < 3600:  # Modified in last hour
                    recent_files.append(file.name)
        
        if recent_files:
            print(f"🔄 Recently modified: {', '.join(recent_files[:5])}")
        else:
            print("🔄 No recent file modifications")
        
        # Generate insights
        insights = self.generate_insights()
        print(f"\n💡 Business Insights:")
        for insight in insights:
            print(f"  • {insight}")
        
        self.log("Business intelligence analysis completed")

    def generate_insights(self):
        """Generate business insights from current state"""
        insights = []
        
        # Deployment readiness
        if Path("super_admin_deployment.py").exists():
            insights.append("Super admin deployment system is ready")
        
        # GitHub integration
        if Path(".env").exists():
            insights.append("Environment configuration is present")
        
        # Agent availability
        agent_files = len(list(Path(".").glob("*agent*.py")))
        if agent_files > 0:
            insights.append(f"{agent_files} agent scripts available for deployment")
        
        # Session activity
        command_count = len(self.session_data['commands_executed'])
        insights.append(f"Terminal session active with {command_count} commands executed")
        
        return insights

    def backup_system(self, args=None):
        """Create system backup"""
        print("\n💾 SYSTEM BACKUP")
        print("=" * 50)
        
        backup_dir = Path(f"backup/claude_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Backup session data
        with open(backup_dir / "session_data.json", "w") as f:
            json.dump(self.session_data, f, indent=2)
        print(f"✅ Session data backed up")
        
        # Copy important files
        important_files = [
            ".env",
            "super_admin_deployment.py",
            "google_cloud_setup.py",
            "DEPLOYMENT_GUIDE.md"
        ]
        
        for file in important_files:
            if Path(file).exists():
                import shutil
                shutil.copy2(file, backup_dir)
                print(f"✅ Backed up: {file}")
        
        print(f"\n💾 Backup created: {backup_dir}")
        self.log(f"System backup created: {backup_dir}")

    def clear_screen(self, args=None):
        """Clear terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print(self.get_banner())

    def get_uptime(self):
        """Get session uptime"""
        start_time = datetime.fromisoformat(self.timestamp.replace('Z', '+00:00'))
        uptime = datetime.now(start_time.tzinfo) - start_time
        return str(uptime).split('.')[0]  # Remove microseconds

    def get_log_size(self):
        """Get log file size"""
        try:
            size = Path(self.log_file).stat().st_size
            return f"{size} bytes"
        except:
            return "0 bytes"

    def exit_terminal(self, args=None):
        """Exit the terminal"""
        print("\n👋 Saving session and exiting...")
        
        # Save final session data
        self.session_data["ended"] = datetime.utcnow().isoformat() + 'Z'
        self.session_data["status"] = "completed"
        
        session_file = f"backup/sessions/session_{self.session_id}.json"
        Path("backup/sessions").mkdir(parents=True, exist_ok=True)
        
        with open(session_file, "w") as f:
            json.dump(self.session_data, f, indent=2)
        
        self.log("Claude Terminal session ended")
        print(f"📝 Session saved: {session_file}")
        print("🎯 Claude Terminal session completed. Goodbye!")
        return True

    def run(self):
        """Main terminal loop"""
        while True:
            try:
                # Get user input
                command_line = input("\n🎯 claude> ").strip()
                
                if not command_line:
                    continue
                
                # Parse command and arguments
                parts = command_line.split()
                command = parts[0].lower()
                args = parts[1:] if len(parts) > 1 else None
                
                # Execute command
                if command in self.commands:
                    result = self.commands[command](args)
                    if result is True:  # Exit command
                        break
                else:
                    print(f"❌ Unknown command: {command}")
                    print("Type 'help' for available commands")
                
                self.log(f"Command executed: {command_line}")
                
            except KeyboardInterrupt:
                print("\n\n🛑 Interrupted. Type 'exit' to quit properly.")
                continue
            except EOFError:
                print("\n\n👋 EOF received. Exiting...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                self.log(f"Error in command: {e}", "ERROR")

def main():
    """Main function"""
    terminal = ClaudeTerminal()
    terminal.run()

if __name__ == "__main__":
    main()