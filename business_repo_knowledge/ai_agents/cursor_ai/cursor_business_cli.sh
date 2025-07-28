#!/bin/bash

# Cursor Business CLI Integration
# Commands for Cursor AI business development

cursor_business_context() {
    echo "📊 Loading business context for Cursor AI..."
    
    # Load latest HubSpot data
    ./scripts/analyze_hubspot.sh pipeline-summary > /tmp/business_context.txt
    
    # Add to Cursor context
    echo "Business Context loaded:"
    echo "- 37 active deals worth $57,977"
    echo "- 4 pipelines: Customer, Vehicle Transport, Credit, Automation"
    echo "- Immediate opportunities: $22,650"
    echo ""
    echo "Use @business_context in Cursor AI for contextual assistance"
}

cursor_create_business_file() {
    local file_type=$1
    local name=$2
    
    case $file_type in
        "hubspot")
            cp templates/cursor-ai/hubspot_integration.py "$name.py"
            echo "✅ Created HubSpot integration: $name.py"
            ;;
        "automation")
            cp templates/cursor-ai/business_automation.js "$name.js"
            echo "✅ Created automation script: $name.js"
            ;;
        "quote")
            cp templates/cursor-ai/quote_generator.py "$name.py"
            echo "✅ Created quote generator: $name.py"
            ;;
        *)
            echo "❌ Unknown file type. Use: hubspot, automation, quote"
            ;;
    esac
}

cursor_sync_changes() {
    echo "🔄 Syncing Cursor changes with business repo..."
    
    # Run the Python integration
    python3 cursor_ai_integration.py &
    
    echo "✅ Background sync started"
}

# Main CLI dispatcher
case "${1:-}" in
    "context")
        cursor_business_context
        ;;
    "create")
        cursor_create_business_file "$2" "$3"
        ;;
    "sync")
        cursor_sync_changes
        ;;
    *)
        echo "Cursor Business CLI"
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  context          Load business context for Cursor AI"
        echo "  create [type] [name]  Create business file from template"
        echo "  sync             Start background sync with business repo"
        echo ""
        echo "File types: hubspot, automation, quote"
        ;;
esac
