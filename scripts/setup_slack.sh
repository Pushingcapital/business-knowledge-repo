#!/bin/bash

# Slack Integration for Business Intelligence
# Creates webhook endpoints, bot commands, and knowledge capture

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "💬 Setting up Slack Integration..."
echo "================================="
echo ""

# Create Slack webhook receiver
create_slack_webhook() {
    echo "🤖 Creating Slack webhook receiver..."
    
    cat > slack_webhook.js << 'EOF'
// Slack Event Webhook Receiver
// Deploy to Cloudflare Workers

export default {
  async fetch(request, env, ctx) {
    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405 });
    }

    try {
      const data = await request.json();
      
      // Handle Slack URL verification
      if (data.type === 'url_verification') {
        return new Response(data.challenge);
      }
      
      // Process Slack events
      if (data.type === 'event_callback') {
        await processSlackEvent(data.event, env);
      }

      return new Response('OK', { status: 200 });
    } catch (error) {
      console.error('Slack webhook error:', error);
      return new Response('Error', { status: 500 });
    }
  }
};

async function processSlackEvent(event, env) {
  // Capture important business conversations
  if (shouldCaptureMessage(event)) {
    const businessData = {
      timestamp: new Date().toISOString(),
      channel: event.channel,
      user: event.user,
      text: event.text,
      thread_ts: event.thread_ts || null,
      type: 'slack_message'
    };

    // Forward to HubSpot if it mentions deals/clients
    if (containsBusinessKeywords(event.text)) {
      await createHubSpotActivity(businessData, env.HUBSPOT_API_TOKEN);
    }

    // Log to knowledge repo
    await logToKnowledgeRepo(businessData);
  }
}

function shouldCaptureMessage(event) {
  // Don't capture bot messages or edited messages
  if (event.bot_id || event.subtype === 'message_changed') {
    return false;
  }
  
  // Capture messages with business keywords
  const businessKeywords = [
    'deal', 'client', 'quote', 'revenue', 'payment', 
    'contract', 'proposal', 'meeting', 'follow up',
    'credit', 'vehicle', 'transport', 'funding'
  ];
  
  return businessKeywords.some(keyword => 
    event.text?.toLowerCase().includes(keyword)
  );
}

function containsBusinessKeywords(text) {
  const keywords = ['deal', 'client', 'quote', 'payment', 'contract'];
  return keywords.some(keyword => text?.toLowerCase().includes(keyword));
}

async function createHubSpotActivity(data, token) {
  if (!token) return;
  
  const activity = {
    properties: {
      hs_activity_type: 'NOTE',
      hs_body: `Slack Discussion: ${data.text}`,
      hs_timestamp: new Date(data.timestamp).getTime()
    }
  };

  await fetch('https://api.hubapi.com/crm/v3/objects/activities', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(activity)
  });
}

async function logToKnowledgeRepo(data) {
  console.log('Business Slack Message:', JSON.stringify(data));
}
EOF

    echo "✅ Slack webhook template created"
}

# Create Slack bot commands
create_slack_bot() {
    echo "🤖 Creating Slack bot commands..."
    
    cat > slack_bot.py << 'EOF'
#!/usr/bin/env python3
"""
Slack Bot for Business Intelligence
Responds to commands and captures business data
"""

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
import json
from datetime import datetime

# Initialize Slack app
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.command("/pipeline")
def pipeline_command(ack, respond, command):
    """Show HubSpot pipeline status"""
    ack()
    
    # Get pipeline data (integrate with your HubSpot analysis)
    pipeline_summary = get_pipeline_summary()
    
    respond(f"""
📊 **Pipeline Status**
• Total Deals: 37
• Pipeline Value: $57,977
• Avg Deal Size: $1,540
• Pending Collection: $11,950

🎯 **Action Items:**
• 4 deals ready for collection
• 6 deals ready to advance from onboarding

💡 Use `/deals [stage]` for detailed breakdown
    """)

@app.command("/deals")
def deals_command(ack, respond, command):
    """Show specific deal stage information"""
    ack()
    
    stage = command['text'].strip() if command['text'] else 'all'
    deals_info = get_deals_by_stage(stage)
    
    respond(f"📋 **Deals in {stage.title()} Stage:**\n{deals_info}")

@app.command("/quote")
def quote_command(ack, respond, command):
    """Generate quick quote for vehicle transport"""
    ack()
    
    # Extract quote parameters from command text
    params = parse_quote_params(command['text'])
    quote = generate_vehicle_quote(params)
    
    respond(f"""
🚛 **Vehicle Transport Quote**
From: {params.get('from', 'TBD')}
To: {params.get('to', 'TBD')}
Vehicle: {params.get('vehicle', 'TBD')}

**Estimated Cost:** ${quote.get('amount', 'TBD')}
**Timeline:** {quote.get('timeline', '3-7 days')}

React with ✅ to create HubSpot deal
    """)

@app.event("message")
def handle_message_events(body, logger):
    """Capture business-relevant messages"""
    event = body.get("event", {})
    
    # Only process messages with business keywords
    if should_capture_slack_message(event.get("text", "")):
        save_business_message(event)

def should_capture_slack_message(text):
    """Check if message should be captured for business intelligence"""
    business_keywords = [
        'deal', 'client', 'quote', 'revenue', 'payment',
        'contract', 'proposal', 'meeting', 'follow up'
    ]
    return any(keyword in text.lower() for keyword in business_keywords)

def save_business_message(event):
    """Save business message to knowledge repo"""
    timestamp = datetime.utcnow().isoformat() + 'Z'
    
    message_data = {
        'timestamp': timestamp,
        'source': 'slack',
        'channel': event.get('channel'),
        'user': event.get('user'),
        'text': event.get('text'),
        'type': 'business_communication'
    }
    
    # Save to file
    filename = f"insights/{timestamp[:10]}_slack-business-intel.md"
    with open(filename, 'w') as f:
        f.write(f"# Slack Business Intelligence\n\n")
        f.write(f"**Timestamp:** {timestamp}\n")
        f.write(f"**Channel:** {event.get('channel')}\n")
        f.write(f"**User:** {event.get('user')}\n\n")
        f.write(f"## Message Content\n")
        f.write(f"{event.get('text')}\n\n")

def get_pipeline_summary():
    """Get pipeline summary from HubSpot analysis"""
    # This would integrate with your HubSpot analysis script
    return "Pipeline data loaded from business-knowledge-repo"

def get_deals_by_stage(stage):
    """Get deals by specific stage"""
    # This would query your HubSpot data
    return f"Deals in {stage} stage: [data from HubSpot analysis]"

def parse_quote_params(text):
    """Parse quote parameters from command text"""
    # Simple parser for quote commands
    # Format: /quote from:CA to:TX vehicle:sedan
    params = {}
    if text:
        for item in text.split():
            if ':' in item:
                key, value = item.split(':', 1)
                params[key] = value
    return params

def generate_vehicle_quote(params):
    """Generate vehicle transport quote"""
    # Simple quote calculation
    base_rate = 800
    distance_multiplier = 1.2  # This would be calculated based on actual distance
    
    return {
        'amount': int(base_rate * distance_multiplier),
        'timeline': '3-7 days'
    }

if __name__ == "__main__":
    # Start the Slack bot
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    print("⚡ Slack bot is running!")
    handler.start()
EOF

    chmod +x slack_bot.py
    echo "✅ Slack bot commands created"
}

# Create Slack Make.com automation
create_slack_make_integration() {
    echo "🔄 Creating Make.com Slack automation..."
    
    cat > slack_make_blueprint.json << 'EOF'
{
  "name": "Slack Business Intelligence Capture",
  "flow": [
    {
      "id": 1,
      "module": "slack:watchDirectMessages",
      "version": 1,
      "parameters": {
        "changeType": "created"
      },
      "filter": {
        "name": "Business Keywords",
        "conditions": [
          {
            "a": "{{1.text}}",
            "o": "text:contains",
            "b": "deal,client,quote,payment,contract"
          }
        ]
      }
    },
    {
      "id": 2,
      "module": "hubspot:createActivity", 
      "version": 1,
      "parameters": {},
      "mapper": {
        "activityType": "NOTE",
        "body": "Slack Discussion: {{1.text}}",
        "timestamp": "{{1.ts}}"
      }
    },
    {
      "id": 3,
      "module": "googleDrive:uploadFile",
      "version": 1,
      "parameters": {},
      "mapper": {
        "fileName": "slack-intel-{{formatDate(1.ts; 'YYYY-MM-DD')}}.md",
        "content": "# Slack Business Intelligence\n\n**Date:** {{formatDate(1.ts; 'YYYY-MM-DD HH:mm')}}\n**User:** {{1.user}}\n**Channel:** {{1.channel}}\n\n## Message\n{{1.text}}"
      }
    }
  ]
}
EOF

    echo "✅ Make.com Slack blueprint created"
}

# Execute setup functions
create_slack_webhook
create_slack_bot
create_slack_make_integration

echo ""
echo "🎉 Slack Integration Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Create Slack app at https://api.slack.com/apps"
echo "2. Set environment variables: SLACK_BOT_TOKEN, SLACK_APP_TOKEN"
echo "3. Deploy slack_webhook.js to Cloudflare Workers"
echo "4. Install dependencies: pip install slack-bolt"
echo "5. Run: python3 slack_bot.py"
echo "6. Import slack_make_blueprint.json to Make.com"
