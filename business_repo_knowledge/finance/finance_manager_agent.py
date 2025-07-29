#!/usr/bin/env python3
"""
Finance Manager Agent for OneTalk System
Handles all finance-related communications and tasks
"""

import os
import json
from datetime import datetime

def handle_finance_communication(communication_data):
    """Handle incoming finance communication"""
    print(f"💰 Finance Agent: Processing {communication_data.get('type', 'communication')}")
    
    # Log to finance communications
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + 'Z',
        "communication_id": communication_data.get("communication_id"),
        "type": communication_data.get("type"),
        "content": communication_data.get("content", ""),
        "assigned_user": communication_data.get("assigned_user"),
        "priority": "high" if any(word in communication_data.get("content", "").upper() 
                                 for word in ["URGENT", "EMERGENCY", "CASH", "PAYMENT"]) else "normal"
    }
    
    # Save to finance communications log
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = f"business_repo_knowledge/finance/communications/finance_comms_{today}.json"
    
    try:
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        
        logs.append(log_entry)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
        
        print(f"✅ Finance communication logged: {communication_data.get('communication_id', 'N/A')[:8]}")
        
    except Exception as e:
        print(f"❌ Error logging finance communication: {e}")

if __name__ == "__main__":
    # Check for OneTalk command data
    command_data = os.getenv('ONETALK_COMMAND_DATA')
    if command_data:
        try:
            data = json.loads(command_data)
            handle_finance_communication(data.get("data", {}))
        except Exception as e:
            print(f"❌ Error processing OneTalk command: {e}")
    else:
        print("💰 Finance Manager Agent ready and waiting for communications...")
