#!/bin/bash

# 🔗 HubSpot API Quick Setup for Owner
# Get immediate access to Darcy appraisals deal

echo "🔗 HUBSPOT API QUICK SETUP"
echo "=========================="
echo "Owner: Emmanuel Haddad"
echo "Target: Darcy Appraisals Deal Access"
echo ""

echo "📋 Required Steps:"
echo ""
echo "1. 🌐 Get HubSpot API Token:"
echo "   - Go to: https://app.hubspot.com/settings/integrations/api"
echo "   - Click 'Create token'"
echo "   - Copy the token"
echo ""

echo "2. ⚙️ Set Environment Variable:"
echo "   Run this command with your actual token:"
echo "   export HUBSPOT_API_TOKEN='your-token-here'"
echo ""

echo "3. 🔍 Re-run Darcy Search:"
echo "   python3 hubspot_deal_finder.py"
echo ""

echo "4. 📧 Alternative - Manual HubSpot Search:"
echo "   - Log into HubSpot: https://app.hubspot.com"
echo "   - Search for: 'Darcy' in deals"
echo "   - Filter by: 'appraisal' keyword"
echo ""

# Check if token is already set
if [ -n "$HUBSPOT_API_TOKEN" ]; then
    echo "✅ HubSpot API token is already configured!"
    echo "🎯 Running Darcy search now..."
    python3 hubspot_deal_finder.py
else
    echo "❌ HubSpot API token not configured"
    echo ""
    echo "📱 IMMEDIATE ACTION FOR OWNER:"
    echo "1. Copy this command: export HUBSPOT_API_TOKEN='YOUR_TOKEN'"
    echo "2. Replace YOUR_TOKEN with actual HubSpot token"
    echo "3. Run the command in terminal"
    echo "4. Run this script again"
    echo ""
    echo "🚨 PRIORITY: Get live access to Darcy appraisals deal"
fi

echo ""
echo "📧 Email monitoring: ACTIVE for emmanuel@pushingcap.com"
echo "🤖 All AI agents: STANDING BY for owner commands"