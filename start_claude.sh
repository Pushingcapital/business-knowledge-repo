#!/bin/bash

# Claude Terminal Startup Script
# Quick launcher for business intelligence command center

clear

echo "🎯 Starting Claude Terminal..."
echo "🤖 Business Intelligence Command Center"
echo "⚡ No APIs required - Ready to run!"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Start Claude Terminal
python3 claude_terminal.py

echo ""
echo "👋 Claude Terminal session ended."
echo "📝 Check logs/ directory for session data"