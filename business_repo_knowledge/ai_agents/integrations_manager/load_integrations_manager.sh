#!/bin/bash

# 🤖 Integrations Manager Agent Launcher
# Quick start script for the AI-powered integrations manager

echo "🚀 Loading Integrations Manager Agent..."
echo "Created: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo "Last Modified: Claude AI Assistant"
echo ""

# Make sure the agent is executable
chmod +x integrations_manager_agent.py

# Check if the agent exists
if [ ! -f "integrations_manager_agent.py" ]; then
    echo "❌ Integrations Manager Agent not found!"
    exit 1
fi

# If no command provided, show status
if [ $# -eq 0 ]; then
    echo "🔍 Running integration status check..."
    python3 integrations_manager_agent.py status
else
    # Pass all arguments to the agent
    python3 integrations_manager_agent.py "$@"
fi

echo ""
echo "🎯 Available commands:"
echo "  ./load_integrations_manager.sh status"
echo "  ./load_integrations_manager.sh report" 
echo "  ./load_integrations_manager.sh fix"
echo "  ./load_integrations_manager.sh check <service>"
echo "  ./load_integrations_manager.sh monitor"