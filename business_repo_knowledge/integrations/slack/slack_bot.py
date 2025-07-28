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
