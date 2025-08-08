#!/bin/bash

# Make.com Management CLI
# Manage Make.com scenarios and webhooks

MAKE_API_TOKEN=""  # Set in .env file
MAKE_TEAM_ID=""    # Set in .env file

source .env 2>/dev/null

make_list_scenarios() {
    echo "📋 Listing Make.com scenarios..."
    
    if [ -z "$MAKE_API_TOKEN" ]; then
        echo "❌ MAKE_API_TOKEN not set in .env file"
        return 1
    fi
    
    curl -s -H "Authorization: Token $MAKE_API_TOKEN" \
        "https://us1.make.com/api/v2/scenarios" | \
        jq -r '.scenarios[] | "\(.id) - \(.name) - \(.isActive)"'
}

make_upload_blueprint() {
    local blueprint_file=$1
    
    if [ ! -f "$blueprint_file" ]; then
        echo "❌ Blueprint file not found: $blueprint_file"
        return 1
    fi
    
    echo "📤 Uploading blueprint: $blueprint_file"
    
    # This would upload to Make.com
    echo "Manual upload required:"
    echo "1. Go to https://make.com/scenarios"
    echo "2. Click 'Create a new scenario'"
    echo "3. Import blueprint: $blueprint_file"
}

make_create_webhook() {
    local webhook_name=$1
    
    echo "🔗 Creating webhook: $webhook_name"
    echo "Webhook URL will be: https://hook.make.com/[scenario-id]"
    echo "Add this to your applications for integration"
}

make_test_scenario() {
    local scenario_id=$1
    
    echo "🧪 Testing scenario: $scenario_id"
    
    curl -s -X POST \
        -H "Authorization: Token $MAKE_API_TOKEN" \
        "https://us1.make.com/api/v2/scenarios/$scenario_id/run"
}

# CLI dispatcher
case "${1:-}" in
    "list")
        make_list_scenarios
        ;;
    "upload")
        make_upload_blueprint "$2"
        ;;
    "webhook")
        make_create_webhook "$2"
        ;;
    "test")
        make_test_scenario "$2"
        ;;
    *)
        echo "Make.com Management CLI"
        echo "Usage: $0 [command] [options]"
        echo ""
        echo "Commands:"
        echo "  list                List all scenarios"
        echo "  upload [file]       Upload blueprint file"
        echo "  webhook [name]      Create webhook endpoint"
        echo "  test [scenario_id]  Test scenario execution"
        echo ""
        echo "Setup:"
        echo "  1. Add MAKE_API_TOKEN to .env file"
        echo "  2. Add MAKE_TEAM_ID to .env file"
        ;;
esac
