#!/usr/bin/env python3
"""
Google Cloud Super Admin Setup
Configures Google Cloud authentication and admin privileges for agent deployment
Created by: Claude AI Agent
Last updated: $(date '+%Y-%m-%d %H:%M:%S')
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

class GoogleCloudSetup:
    """Handle Google Cloud authentication and initial setup"""
    
    def __init__(self):
        self.timestamp = datetime.utcnow().isoformat() + 'Z'
        self.config_dir = Path.home() / ".config" / "business-intelligence"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
    def check_gcloud_cli(self):
        """Check if Google Cloud CLI is installed"""
        print("🔍 Checking Google Cloud CLI installation...")
        
        try:
            result = subprocess.run(["gcloud", "version"], 
                                  capture_output=True, text=True, check=True)
            print("✅ Google Cloud CLI is installed")
            print(f"📋 Version: {result.stdout.split()[2]}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Google Cloud CLI not found")
            return False
    
    def install_gcloud_cli(self):
        """Install Google Cloud CLI"""
        print("🔧 Installing Google Cloud CLI...")
        
        system = os.uname().sysname.lower()
        
        if system == "linux":
            commands = [
                "curl https://sdk.cloud.google.com | bash",
                "exec -l $SHELL",
                "gcloud init"
            ]
        elif system == "darwin":  # macOS
            commands = [
                "curl https://sdk.cloud.google.com | bash",
                "exec -l $SHELL",
                "gcloud init"
            ]
        else:
            print("❌ Unsupported operating system")
            return False
        
        print("📋 Installation commands:")
        for cmd in commands:
            print(f"   {cmd}")
        
        print("\n⚠️  Please run these commands manually to install Google Cloud CLI")
        return False
    
    def authenticate_super_admin(self):
        """Authenticate with super admin privileges"""
        print("🔐 Setting up super admin authentication...")
        
        # Check current authentication
        try:
            result = subprocess.run(["gcloud", "auth", "list"], 
                                  capture_output=True, text=True, check=True)
            if "ACTIVE" in result.stdout:
                print("✅ Already authenticated with Google Cloud")
                return True
        except subprocess.CalledProcessError:
            pass
        
        print("🚀 Starting authentication process...")
        print("📋 This will open a browser window for Google Cloud authentication")
        
        try:
            # Authenticate with full cloud platform scope
            subprocess.run([
                "gcloud", "auth", "login", 
                "--scopes=https://www.googleapis.com/auth/cloud-platform"
            ], check=True)
            
            print("✅ Authentication successful!")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Authentication failed: {e}")
            return False
    
    def setup_project(self, project_id: str = None):
        """Setup or select Google Cloud project"""
        print("🌐 Setting up Google Cloud project...")
        
        if not project_id:
            # List available projects
            try:
                result = subprocess.run(["gcloud", "projects", "list"], 
                                      capture_output=True, text=True, check=True)
                print("📋 Available projects:")
                print(result.stdout)
                
                project_id = input("Enter your Google Cloud Project ID: ").strip()
                
            except subprocess.CalledProcessError:
                print("❌ Failed to list projects")
                project_id = input("Enter your Google Cloud Project ID: ").strip()
        
        # Set the active project
        try:
            subprocess.run(["gcloud", "config", "set", "project", project_id], check=True)
            print(f"✅ Project set to: {project_id}")
            
            # Enable required APIs
            self.enable_required_apis(project_id)
            
            return project_id
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to set project: {e}")
            return None
    
    def enable_required_apis(self, project_id: str):
        """Enable required Google Cloud APIs"""
        print("🔧 Enabling required Google Cloud APIs...")
        
        apis = [
            "storage.googleapis.com",
            "compute.googleapis.com",
            "iam.googleapis.com",
            "secretmanager.googleapis.com",
            "cloudresourcemanager.googleapis.com",
            "logging.googleapis.com",
            "monitoring.googleapis.com",
            "pubsub.googleapis.com",
            "bigquery.googleapis.com",
            "aiplatform.googleapis.com"
        ]
        
        for api in apis:
            try:
                print(f"🔧 Enabling {api}...")
                subprocess.run([
                    "gcloud", "services", "enable", api, 
                    "--project", project_id
                ], check=True, capture_output=True)
                print(f"✅ {api} enabled")
                
            except subprocess.CalledProcessError as e:
                print(f"⚠️  Failed to enable {api}: {e}")
    
    def create_service_account(self, project_id: str):
        """Create service account for agent deployment"""
        print("👤 Creating service account for agent deployment...")
        
        sa_name = "business-intelligence-admin"
        sa_email = f"{sa_name}@{project_id}.iam.gserviceaccount.com"
        
        try:
            # Create service account
            subprocess.run([
                "gcloud", "iam", "service-accounts", "create", sa_name,
                "--display-name", "Business Intelligence Admin",
                "--description", "Super admin service account for AI agent deployment",
                "--project", project_id
            ], check=True)
            
            print(f"✅ Service account created: {sa_email}")
            
            # Grant necessary roles
            roles = [
                "roles/owner",  # Super admin access
                "roles/storage.admin",
                "roles/compute.admin",
                "roles/iam.serviceAccountAdmin",
                "roles/secretmanager.admin",
                "roles/logging.admin",
                "roles/monitoring.admin"
            ]
            
            for role in roles:
                subprocess.run([
                    "gcloud", "projects", "add-iam-policy-binding", project_id,
                    "--member", f"serviceAccount:{sa_email}",
                    "--role", role
                ], check=True)
                print(f"✅ Granted role: {role}")
            
            # Create and download key
            key_file = self.config_dir / f"{sa_name}-key.json"
            subprocess.run([
                "gcloud", "iam", "service-accounts", "keys", "create", str(key_file),
                "--iam-account", sa_email,
                "--project", project_id
            ], check=True)
            
            print(f"✅ Service account key saved: {key_file}")
            
            # Set environment variable
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(key_file)
            
            return str(key_file)
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create service account: {e}")
            return None
    
    def configure_environment(self, project_id: str, credentials_path: str):
        """Configure environment variables and settings"""
        print("⚙️  Configuring environment...")
        
        # Update .env file
        env_vars = {
            "GOOGLE_CLOUD_PROJECT": project_id,
            "GOOGLE_APPLICATION_CREDENTIALS": credentials_path,
            "DEPLOYMENT_TIMESTAMP": self.timestamp,
            "SUPER_ADMIN_MODE": "true"
        }
        
        env_file = Path(".env")
        
        # Read existing .env
        existing_vars = {}
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    if "=" in line and not line.startswith("#"):
                        key, value = line.strip().split("=", 1)
                        existing_vars[key] = value
        
        # Update with new variables
        existing_vars.update(env_vars)
        
        # Write back to .env
        with open(env_file, "w") as f:
            f.write(f"# Business Intelligence Environment Configuration\n")
            f.write(f"# Updated by Claude AI Agent at {self.timestamp}\n\n")
            
            for key, value in existing_vars.items():
                f.write(f"{key}={value}\n")
        
        print("✅ Environment configured")
        
        # Create configuration summary
        config_summary = {
            "setup_timestamp": self.timestamp,
            "project_id": project_id,
            "credentials_path": credentials_path,
            "super_admin_enabled": True,
            "apis_enabled": True,
            "service_account_created": True
        }
        
        with open(self.config_dir / "setup_summary.json", "w") as f:
            json.dump(config_summary, f, indent=2)
        
        return config_summary
    
    def verify_setup(self, project_id: str):
        """Verify the Google Cloud setup"""
        print("🧪 Verifying Google Cloud setup...")
        
        tests = [
            ("Authentication", self.test_authentication),
            ("Project Access", lambda: self.test_project_access(project_id)),
            ("Storage Access", lambda: self.test_storage_access(project_id)),
            ("IAM Permissions", lambda: self.test_iam_permissions(project_id))
        ]
        
        results = {}
        for test_name, test_func in tests:
            try:
                result = test_func()
                results[test_name] = "✅ PASS" if result else "❌ FAIL"
                print(f"{results[test_name]} {test_name}")
            except Exception as e:
                results[test_name] = f"❌ ERROR: {e}"
                print(f"{results[test_name]} {test_name}")
        
        return all("✅" in result for result in results.values())
    
    def test_authentication(self):
        """Test authentication"""
        try:
            result = subprocess.run(["gcloud", "auth", "list"], 
                                  capture_output=True, text=True, check=True)
            return "ACTIVE" in result.stdout
        except:
            return False
    
    def test_project_access(self, project_id: str):
        """Test project access"""
        try:
            result = subprocess.run(["gcloud", "projects", "describe", project_id], 
                                  capture_output=True, text=True, check=True)
            return project_id in result.stdout
        except:
            return False
    
    def test_storage_access(self, project_id: str):
        """Test storage access"""
        try:
            subprocess.run(["gcloud", "storage", "buckets", "list", "--project", project_id], 
                         capture_output=True, check=True)
            return True
        except:
            return False
    
    def test_iam_permissions(self, project_id: str):
        """Test IAM permissions"""
        try:
            subprocess.run(["gcloud", "iam", "service-accounts", "list", "--project", project_id], 
                         capture_output=True, check=True)
            return True
        except:
            return False

def main():
    """Main setup function"""
    print("🎯 GOOGLE CLOUD SUPER ADMIN SETUP")
    print("=" * 50)
    
    setup = GoogleCloudSetup()
    
    # Check prerequisites
    if not setup.check_gcloud_cli():
        setup.install_gcloud_cli()
        print("Please install Google Cloud CLI and run this script again.")
        return
    
    # Authenticate
    if not setup.authenticate_super_admin():
        print("❌ Authentication failed. Please check your Google account permissions.")
        return
    
    # Setup project
    project_id = setup.setup_project()
    if not project_id:
        print("❌ Project setup failed.")
        return
    
    # Create service account
    credentials_path = setup.create_service_account(project_id)
    if not credentials_path:
        print("❌ Service account creation failed.")
        return
    
    # Configure environment
    config = setup.configure_environment(project_id, credentials_path)
    
    # Verify setup
    if setup.verify_setup(project_id):
        print("\n🎉 GOOGLE CLOUD SETUP COMPLETED!")
        print("=" * 50)
        print(f"📋 Project ID: {project_id}")
        print(f"🔐 Credentials: {credentials_path}")
        print(f"👑 Super Admin: Enabled")
        print(f"🚀 Ready for agent deployment!")
        print("\nNext step: Run python3 super_admin_deployment.py")
    else:
        print("\n❌ Setup verification failed. Please check the errors above.")

if __name__ == "__main__":
    main()