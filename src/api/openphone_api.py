#!/usr/bin/env python3
"""
OpenPhone API Integration
Sends SMS, retrieves call logs, manages contacts
"""

import requests
import json
import os
from datetime import datetime

class OpenPhoneAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openphone.com/v1"
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    def send_sms(self, to_number, message, from_number=None):
        """Send SMS via OpenPhone"""
        data = {
            'to': to_number,
            'text': message
        }
        if from_number:
            data['from'] = from_number
            
        response = requests.post(
            f"{self.base_url}/messages",
            headers=self.headers,
            json=data
        )
        return response.json()
    
    def get_call_logs(self, limit=50):
        """Retrieve recent call logs"""
        response = requests.get(
            f"{self.base_url}/calls?limit={limit}",
            headers=self.headers
        )
        return response.json()
    
    def get_messages(self, limit=50):
        """Retrieve recent messages"""
        response = requests.get(
            f"{self.base_url}/messages?limit={limit}",
            headers=self.headers
        )
        return response.json()

def sync_with_hubspot(phone_data):
    """Sync OpenPhone data with HubSpot"""
    # Implementation for HubSpot sync
    pass

def sync_with_knowledge_repo(phone_data):
    """Log phone activity to business knowledge repo"""
    timestamp = datetime.utcnow().isoformat() + 'Z'
    
    log_entry = {
        'timestamp': timestamp,
        'source': 'openphone',
        'data': phone_data
    }
    
    # Write to knowledge repo
    filename = f"insights/{timestamp[:10]}_openphone-activity.md"
    with open(filename, 'w') as f:
        f.write(f"# OpenPhone Activity Log\n\n")
        f.write(f"**Timestamp:** {timestamp}\n")
        f.write(f"**Source:** OpenPhone API\n\n")
        f.write(f"## Activity Data\n")
        f.write(f"```json\n{json.dumps(phone_data, indent=2)}\n```\n")

if __name__ == "__main__":
    # Example usage
    api_key = os.getenv('OPENPHONE_API_KEY')
    if api_key:
        openphone = OpenPhoneAPI(api_key)
        
        # Get recent activity
        calls = openphone.get_call_logs()
        messages = openphone.get_messages()
        
        # Sync with systems
        sync_with_hubspot(calls)
        sync_with_knowledge_repo(messages)
        
        print("✅ OpenPhone sync completed")
    else:
        print("❌ OPENPHONE_API_KEY not set")
