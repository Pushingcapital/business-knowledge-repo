#!/bin/bash

# OpenPhone Integration via Webhooks and API
# Creates webhook endpoints and SMS/call automation

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "🔧 Setting up OpenPhone Integration..."
echo "=================================="
echo ""

# Create OpenPhone webhook receiver
create_openphone_webhook() {
    echo "📞 Creating OpenPhone webhook receiver..."
    
    # Using Cloudflare Workers for webhook endpoint
    cat > openphone_webhook.js << 'EOF'
// OpenPhone Webhook Receiver
// Deploy to Cloudflare Workers for reliable webhook handling

export default {
  async fetch(request, env, ctx) {
    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405 });
    }

    try {
      const data = await request.json();
      
      // Process OpenPhone webhook data
      const event = {
        type: data.type, // 'call', 'sms', 'voicemail'
        phone: data.phone_number,
        contact: data.contact_name,
        message: data.message || data.transcription,
        timestamp: new Date().toISOString(),
        duration: data.duration || null
      };

      // Forward to HubSpot (create contact/activity)
      if (env.HUBSPOT_API_TOKEN) {
        await forwardToHubSpot(event, env.HUBSPOT_API_TOKEN);
      }

      // Log to business knowledge repo
      await logToKnowledgeRepo(event);

      return new Response('Webhook processed', { status: 200 });
    } catch (error) {
      console.error('Webhook error:', error);
      return new Response('Webhook error', { status: 500 });
    }
  }
};

async function forwardToHubSpot(event, token) {
  // Create HubSpot activity
  const hubspotData = {
    properties: {
      hs_activity_type: event.type === 'call' ? 'CALL' : 'NOTE',
      hs_body: `${event.type.toUpperCase()}: ${event.message}`,
      hs_timestamp: new Date(event.timestamp).getTime()
    }
  };

  await fetch('https://api.hubapi.com/crm/v3/objects/activities', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(hubspotData)
  });
}

async function logToKnowledgeRepo(event) {
  // This would integrate with your knowledge repo
  // For now, we'll create a simple log format
  const logEntry = {
    timestamp: event.timestamp,
    type: 'openphone_event',
    data: event
  };
  
  console.log('OpenPhone Event:', JSON.stringify(logEntry));
}
EOF

    echo "✅ OpenPhone webhook template created"
}

# Create OpenPhone API connector
create_openphone_api() {
    echo "📞 Creating OpenPhone API connector..."
    
    cat > openphone_api.py << 'EOF'
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
EOF

    chmod +x openphone_api.py
    echo "✅ OpenPhone API connector created"
}

# Create OpenPhone automation via Make.com
create_openphone_make_integration() {
    echo "🔄 Creating Make.com OpenPhone automation..."
    
    cat > openphone_make_blueprint.json << 'EOF'
{
  "name": "OpenPhone to Business Intelligence Pipeline",
  "flow": [
    {
      "id": 1,
      "module": "openphone:watchIncomingCalls",
      "version": 1,
      "parameters": {},
      "mapper": {},
      "metadata": {
        "designer": {
          "x": 0,
          "y": 0
        }
      }
    },
    {
      "id": 2,
      "module": "hubspot:createActivity",
      "version": 1,
      "parameters": {},
      "mapper": {
        "activityType": "CALL",
        "body": "{{1.transcription}}",
        "timestamp": "{{1.created_at}}"
      },
      "metadata": {
        "designer": {
          "x": 300,
          "y": 0
        }
      }
    },
    {
      "id": 3,
      "module": "googleDrive:uploadFile",
      "version": 1,
      "parameters": {},
      "mapper": {
        "fileName": "call-log-{{formatDate(1.created_at; 'YYYY-MM-DD')}}.md",
        "content": "# Call Log\n\n**Date:** {{1.created_at}}\n**Phone:** {{1.phone_number}}\n**Duration:** {{1.duration}}\n**Transcription:** {{1.transcription}}"
      },
      "metadata": {
        "designer": {
          "x": 600,
          "y": 0
        }
      }
    }
  ],
  "metadata": {
    "instant": true,
    "version": 1,
    "scenario": {
      "roundtrips": 1,
      "maxErrors": 3,
      "autoCommit": true,
      "sequential": false,
      "confidential": false,
      "dataloss": false,
      "dlq": false
    },
    "designer": {
      "orphans": []
    },
    "zone": "us1.make.com"
  }
}
EOF

    echo "✅ Make.com OpenPhone blueprint created"
}

# Execute all setup functions
create_openphone_webhook
create_openphone_api
create_openphone_make_integration

echo ""
echo "🎉 OpenPhone Integration Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Deploy openphone_webhook.js to Cloudflare Workers"
echo "2. Set OpenPhone webhook URL to your Cloudflare Worker"
echo "3. Set OPENPHONE_API_KEY environment variable"
echo "4. Import openphone_make_blueprint.json to Make.com"
echo "5. Run: python3 openphone_api.py for manual sync"
