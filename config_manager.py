#!/usr/bin/env python3
"""
Configuration Manager for Security Login Automation
Easy setup and management of login credentials and site configurations
"""

import argparse
import getpass
import json
import sys
from pathlib import Path
from typing import Dict, List

import pyotp
import qrcode
from cryptography.fernet import Fernet
from loguru import logger

from security_login_automation import SecurityLoginAutomation, LoginCredentials


class ConfigurationManager:
    """Manage automation configurations and credentials"""
    
    def __init__(self):
        self.automation = SecurityLoginAutomation()
    
    def add_site_interactive(self):
        """Interactive site addition with user prompts"""
        print("\n=== Add New Site for Security Login Automation ===\n")
        
        site_name = input("Site name (e.g., 'gmail', 'github'): ").strip()
        if not site_name:
            print("Site name is required!")
            return
        
        site_url = input("Login URL: ").strip()
        if not site_url:
            print("Login URL is required!")
            return
        
        username = input("Username/Email: ").strip()
        if not username:
            print("Username is required!")
            return
        
        password = getpass.getpass("Password: ")
        if not password:
            print("Password is required!")
            return
        
        # 2FA setup
        use_2fa = input("Does this site use 2FA/TOTP? (y/n): ").lower().startswith('y')
        totp_secret = None
        
        if use_2fa:
            print("\nChoose 2FA setup method:")
            print("1. I have the secret key")
            print("2. I have a QR code to scan")
            print("3. Skip 2FA for now")
            
            choice = input("Enter choice (1-3): ").strip()
            
            if choice == "1":
                totp_secret = input("Enter TOTP secret key: ").strip()
                if totp_secret:
                    # Test the secret
                    try:
                        totp = pyotp.TOTP(totp_secret)
                        test_code = totp.now()
                        print(f"Test TOTP code: {test_code}")
                        if input("Does this code match your authenticator app? (y/n): ").lower().startswith('y'):
                            print("✓ TOTP secret verified!")
                        else:
                            print("⚠ TOTP secret may be incorrect")
                    except Exception as e:
                        print(f"⚠ Error testing TOTP: {e}")
            
            elif choice == "2":
                print("Please scan the QR code with your authenticator app and enter the secret key manually.")
                totp_secret = input("Enter TOTP secret key from QR code: ").strip()
        
        # Create credentials
        credentials = LoginCredentials(
            username=username,
            password=password,
            totp_secret=totp_secret,
            site_url=site_url,
            site_name=site_name
        )
        
        # Save credentials
        try:
            self.automation.add_site_credentials(credentials)
            print(f"\n✓ Site '{site_name}' added successfully!")
            print(f"  URL: {site_url}")
            print(f"  Username: {username}")
            print(f"  2FA: {'Enabled' if totp_secret else 'Disabled'}")
            
            # Test login option
            if input("\nWould you like to test the login now? (y/n): ").lower().startswith('y'):
                self.test_login(site_name)
        
        except Exception as e:
            print(f"✗ Error adding site: {e}")
    
    def list_sites(self):
        """List all configured sites"""
        print("\n=== Configured Sites ===\n")
        
        sites = self.automation.config.get('sites', [])
        if not sites:
            print("No sites configured yet.")
            print("Use 'python config_manager.py add' to add a site.")
            return
        
        for i, site in enumerate(sites, 1):
            print(f"{i}. {site['name']}")
            print(f"   URL: {site['url']}")
            print(f"   Enabled: {site.get('enabled', True)}")
            print(f"   Schedule: {site.get('schedule', 'Not set')}")
            
            # Check if credentials exist
            creds = self.automation.get_site_credentials(site['name'])
            if creds:
                print(f"   Username: {creds.username}")
                print(f"   2FA: {'Enabled' if creds.totp_secret else 'Disabled'}")
            else:
                print("   ⚠ No credentials found!")
            print()
    
    def test_login(self, site_name: str = None):
        """Test login for a specific site"""
        if not site_name:
            site_name = input("Enter site name to test: ").strip()
        
        credentials = self.automation.get_site_credentials(site_name)
        if not credentials:
            print(f"No credentials found for '{site_name}'")
            return
        
        print(f"\n=== Testing Login for {site_name} ===\n")
        
        from security_login_automation import BrowserConfig
        import asyncio
        
        config = BrowserConfig(
            browser_type="chrome",
            headless=False,  # Show browser for testing
            stealth_mode=True
        )
        
        async def run_test():
            success = await self.automation.perform_login(credentials, config)
            if success:
                print("✓ Login test successful!")
            else:
                print("✗ Login test failed!")
        
        try:
            asyncio.run(run_test())
        except Exception as e:
            print(f"✗ Test error: {e}")
    
    def enable_disable_site(self):
        """Enable or disable a site"""
        self.list_sites()
        
        site_name = input("\nEnter site name to enable/disable: ").strip()
        sites = self.automation.config.get('sites', [])
        
        site = next((s for s in sites if s['name'] == site_name), None)
        if not site:
            print(f"Site '{site_name}' not found!")
            return
        
        current_status = site.get('enabled', True)
        new_status = not current_status
        site['enabled'] = new_status
        
        # Save config
        import yaml
        with open(self.automation.config_path, 'w') as f:
            yaml.dump(self.automation.config, f, default_flow_style=False)
        
        print(f"Site '{site_name}' {'enabled' if new_status else 'disabled'}")
    
    def update_schedule(self):
        """Update schedule for a site"""
        self.list_sites()
        
        site_name = input("\nEnter site name to update schedule: ").strip()
        sites = self.automation.config.get('sites', [])
        
        site = next((s for s in sites if s['name'] == site_name), None)
        if not site:
            print(f"Site '{site_name}' not found!")
            return
        
        print("\nCurrent schedule:", site.get('schedule', 'Not set'))
        print("\nSchedule format: cron expression (minute hour day month dayofweek)")
        print("Examples:")
        print("  '0 9 * * *'   - Daily at 9:00 AM")
        print("  '0 */6 * * *' - Every 6 hours")
        print("  '0 9 * * 1'   - Weekly on Monday at 9:00 AM")
        
        new_schedule = input("Enter new schedule: ").strip()
        if new_schedule:
            site['schedule'] = new_schedule
            
            # Save config
            import yaml
            with open(self.automation.config_path, 'w') as f:
                yaml.dump(self.automation.config, f, default_flow_style=False)
            
            print(f"Schedule updated for '{site_name}': {new_schedule}")
    
    def export_config(self):
        """Export configuration to backup file"""
        import datetime
        backup_file = f"automation_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        config_data = {
            'config': self.automation.config,
            'sites': []
        }
        
        # Export site credentials (encrypted)
        for site_config in self.automation.config.get('sites', []):
            site_name = site_config['name']
            try:
                # Get encrypted credentials from keyring
                import keyring
                encrypted_creds = keyring.get_password("security_automation", site_name)
                if encrypted_creds:
                    config_data['sites'].append({
                        'name': site_name,
                        'encrypted_credentials': encrypted_creds
                    })
            except Exception as e:
                print(f"Warning: Could not export credentials for {site_name}: {e}")
        
        with open(backup_file, 'w') as f:
            json.dump(config_data, f, indent=2)
        
        print(f"Configuration exported to: {backup_file}")
    
    def generate_2fa_qr(self):
        """Generate QR code for 2FA setup"""
        site_name = input("Enter site name: ").strip()
        account_name = input("Enter account name/email: ").strip()
        
        # Generate a new secret
        secret = pyotp.random_base32()
        
        # Create TOTP URI
        totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=account_name,
            issuer_name=site_name
        )
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(totp_uri)
        qr.make(fit=True)
        
        # Save QR code image
        qr_file = f"2fa_qr_{site_name}_{account_name}.png"
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(qr_file)
        
        print(f"\n2FA Setup Information:")
        print(f"Secret Key: {secret}")
        print(f"QR Code saved: {qr_file}")
        print(f"TOTP URI: {totp_uri}")
        print(f"\nCurrent TOTP code: {pyotp.TOTP(secret).now()}")


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="Security Login Automation Configuration Manager")
    parser.add_argument('action', choices=['add', 'list', 'test', 'enable-disable', 'schedule', 'export', 'qr'], 
                       help='Action to perform')
    parser.add_argument('--site', help='Site name (for test action)')
    
    args = parser.parse_args()
    
    config_manager = ConfigurationManager()
    
    try:
        if args.action == 'add':
            config_manager.add_site_interactive()
        elif args.action == 'list':
            config_manager.list_sites()
        elif args.action == 'test':
            config_manager.test_login(args.site)
        elif args.action == 'enable-disable':
            config_manager.enable_disable_site()
        elif args.action == 'schedule':
            config_manager.update_schedule()
        elif args.action == 'export':
            config_manager.export_config()
        elif args.action == 'qr':
            config_manager.generate_2fa_qr()
    
    except KeyboardInterrupt:
        print("\n\nOperation cancelled.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main() 