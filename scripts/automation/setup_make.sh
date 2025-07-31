#!/bin/bash

# Make.com Integration Hub
# Connects all business systems through Make.com automation

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "🔄 Setting up Make.com Integration Hub..."
echo "======================================"
echo ""

# Analyze existing Make.com blueprints
analyze_existing_blueprints() {
    echo "📋 Analyzing existing Make.com blueprints..."
    
    DOWNLOADS_PATH="/Users/emmanuelhaddad/Downloads"
    
    echo "Found Make.com blueprints:"
    find "$DOWNLOADS_PATH" -name "*.blueprint.json" | while read blueprint; do
        echo "  📄 $(basename "$blueprint")"
    done
    
    echo ""
    echo "Found Make.com integration files:"
    find "$DOWNLOADS_PATH" -name "*make*" -o -name "*blueprint*" | head -10
}

# Create comprehensive Make.com business hub
create_make_business_hub() {
    echo "🏗️ Creating Make.com Business Intelligence Hub..."
    
    cat > make_business_hub.json << 'EOF'
{
  "name": "Pushing Capital Business Intelligence Hub",
  "description": "Master automation connecting HubSpot, OpenPhone, Slack, and Knowledge Repo",
  "flow": [
    {
      "id": 1,
      "module": "webhook:customWebhook",
      "version": 1,
      "parameters": {
        "name": "business_events_webhook",
        "description": "Central webhook for all business events"
      },
      "metadata": {
        "designer": {
          "x": 0,
          "y": 0
        }
      }
    },
    {
      "id": 2,
      "module": "tools:basicRouter",
      "version": 1,
      "parameters": {},
      "routes": [
        {
          "name": "HubSpot Events",
          "condition": "{{1.source}} = hubspot"
        },
        {
          "name": "OpenPhone Events", 
          "condition": "{{1.source}} = openphone"
        },
        {
          "name": "Slack Events",
          "condition": "{{1.source}} = slack"
        },
        {
          "name": "Form Submissions",
          "condition": "{{1.source}} = form"
        }
      ],
      "metadata": {
        "designer": {
          "x": 300,
          "y": 0
        }
      }
    },
    {
      "id": 3,
      "module": "hubspot:createDeal",
      "version": 1,
      "parameters": {},
      "mapper": {
        "dealname": "{{1.deal_name}}",
        "amount": "{{1.amount}}",
        "dealstage": "{{1.stage}}",
        "pipeline": "{{1.pipeline}}"
      },
      "routes": [2],
      "metadata": {
        "designer": {
          "x": 600,
          "y": -100
        }
      }
    },
    {
      "id": 4,
      "module": "slack:createMessage",
      "version": 1,
      "parameters": {},
      "mapper": {
        "channel": "#business-alerts",
        "text": "🎯 New business event: {{1.description}}\n💰 Value: ${{1.amount}}\n📊 Pipeline: {{1.pipeline}}\n🕐 Time: {{formatDate(now; 'YYYY-MM-DD HH:mm')}}"
      },
      "routes": [2],
      "metadata": {
        "designer": {
          "x": 600,
          "y": 0
        }
      }
    },
    {
      "id": 5,
      "module": "googleDrive:uploadFile",
      "version": 1,
      "parameters": {
        "folder": "Business Intelligence Logs"
      },
      "mapper": {
        "fileName": "business-event-{{formatDate(now; 'YYYY-MM-DD-HH-mm')}}.md",
        "content": "# Business Event Log\n\n**Timestamp:** {{formatDate(now; 'YYYY-MM-DD HH:mm:ss')}}\n**Source:** {{1.source}}\n**Type:** {{1.type}}\n**Description:** {{1.description}}\n\n## Event Data\n```json\n{{formatJSON(1)}}\n```\n\n## Business Impact\n- **Pipeline Value:** ${{1.amount}}\n- **Stage:** {{1.stage}}\n- **Priority:** {{1.priority}}\n\n## Action Items\n- [ ] Review and validate data\n- [ ] Update relevant stakeholders\n- [ ] Schedule follow-up if needed"
      },
      "routes": [2],
      "metadata": {
        "designer": {
          "x": 600,
          "y": 100
        }
      }
    },
    {
      "id": 6,
      "module": "airtable:createRecord",
      "version": 1,
      "parameters": {
        "base": "appLPGFO41RF6QKHo",
        "table": "Business Insights"
      },
      "mapper": {
        "fields": {
          "Insight Title": "Make.com Event: {{1.description}}",
          "Source": "Make.com Automation",
          "Category": "{{1.category}}",
          "Priority": "{{1.priority}}",
          "Description": "{{1.description}}",
          "Discovery Date": "{{formatDate(now; 'YYYY-MM-DD')}}"
        }
      },
      "routes": [2],
      "metadata": {
        "designer": {
          "x": 600,
          "y": 200
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
      "sequential": false
    }
  }
}
EOF

    echo "✅ Make.com Business Hub blueprint created"
}

# Create specific automation scenarios
create_vehicle_transport_automation() {
    echo "🚛 Creating vehicle transport automation..."
    
    cat > make_vehicle_transport.json << 'EOF'
{
  "name": "Vehicle Transport Quote to Deal Pipeline",
  "description": "Automates vehicle transport from form submission to HubSpot deal",
  "flow": [
    {
      "id": 1,
      "module": "webhook:customWebhook",
      "version": 1,
      "parameters": {
        "name": "vehicle_transport_form"
      }
    },
    {
      "id": 2,
      "module": "hubspot:searchContacts",
      "version": 1,
      "parameters": {},
      "mapper": {
        "email": "{{1.email}}"
      }
    },
    {
      "id": 3,
      "module": "hubspot:createContact",
      "version": 1,
      "parameters": {},
      "mapper": {
        "email": "{{1.email}}",
        "firstname": "{{1.first_name}}",
        "lastname": "{{1.last_name}}",
        "phone": "{{1.phone}}"
      },
      "filter": {
        "name": "Contact Not Found",
        "conditions": [
          {
            "a": "{{length(2.results)}}",
            "o": "number:equal",
            "b": "0"
          }
        ]
      }
    },
    {
      "id": 4,
      "module": "math:evaluateExpression",
      "version": 1,
      "parameters": {},
      "mapper": {
        "expression": "{{calculateTransportQuote(1.pickup_zip, 1.delivery_zip, 1.vehicle_type)}}"
      }
    },
    {
      "id": 5,
      "module": "hubspot:createDeal",
      "version": 1,
      "parameters": {},
      "mapper": {
        "dealname": "{{1.pickup_zip}} >{{1.delivery_zip}}",
        "amount": "{{4.result}}",
        "dealstage": "Collect Quote",
        "pipeline": "Nationwide Vehicle Transport Solutions",
        "vehicle_type": "{{1.vehicle_type}}",
        "pickup_location": "{{1.pickup_address}}",
        "delivery_location": "{{1.delivery_address}}",
        "service_type": "{{1.service_type}}"
      }
    },
    {
      "id": 6,
      "module": "slack:createMessage",
      "version": 1,
      "parameters": {},
      "mapper": {
        "channel": "#transport-quotes",
        "text": "🚛 New Transport Quote Generated!\n\n**Route:** {{1.pickup_zip}} → {{1.delivery_zip}}\n**Vehicle:** {{1.vehicle_type}}\n**Quote:** ${{4.result}}\n**Customer:** {{1.first_name}} {{1.last_name}}\n\n**HubSpot Deal:** {{5.id}}"
      }
    }
  ]
}
EOF

    echo "✅ Vehicle transport automation created"
}

create_credit_strategy_automation() {
    echo "💳 Creating credit strategy automation..."
    
    cat > make_credit_strategy.json << 'EOF'
{
  "name": "Credit Strategy Service Pipeline",
  "description": "Automates credit strategy from intake to completion",
  "flow": [
    {
      "id": 1,
      "module": "webhook:customWebhook",
      "version": 1,
      "parameters": {
        "name": "credit_intake_form"
      }
    },
    {
      "id": 2,
      "module": "hubspot:createDeal",
      "version": 1,
      "parameters": {},
      "mapper": {
        "dealname": "{{1.first_name}} - Credit Strategy",
        "amount": "1500",
        "dealstage": "Onboarding",
        "pipeline": "Customer Pipeline",
        "credit_score": "{{1.credit_score}}",
        "services_needed": "{{1.services}}"
      }
    },
    {
      "id": 3,
      "module": "googleDrive:createFile",
      "version": 1,
      "parameters": {},
      "mapper": {
        "fileName": "Credit Analysis - {{1.first_name}} {{1.last_name}} - {{formatDate(now; 'YYYY-MM-DD')}}",
        "content": "# Credit Strategy Analysis\n\n**Client:** {{1.first_name}} {{1.last_name}}\n**Email:** {{1.email}}\n**Current Credit Score:** {{1.credit_score}}\n**Services Requested:** {{1.services}}\n**Intake Date:** {{formatDate(now; 'YYYY-MM-DD')}}\n\n## Assessment\n- Current score: {{1.credit_score}}\n- Target improvement: [TBD]\n- Timeline: [TBD]\n\n## Action Plan\n- [ ] Initial credit report review\n- [ ] Dispute letter preparation\n- [ ] Follow-up strategy\n\n**Deal ID:** {{2.id}}"
      }
    },
    {
      "id": 4,
      "module": "slack:createMessage",
      "version": 1,
      "parameters": {},
      "mapper": {
        "channel": "#credit-services",
        "text": "💳 New Credit Strategy Client!\n\n**Client:** {{1.first_name}} {{1.last_name}}\n**Current Score:** {{1.credit_score}}\n**Services:** {{1.services}}\n**Deal Value:** $1,500\n\n**HubSpot Deal:** {{2.id}}\n**Analysis Doc:** {{3.id}}"
      }
    }
  ]
}
EOF

    echo "✅ Credit strategy automation created"
}

# Create Make.com management CLI
create_make_cli() {
    echo "⌨️ Creating Make.com management CLI..."
    
    cat > make_management_cli.sh << 'EOF'
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
EOF

    chmod +x make_management_cli.sh
    echo "✅ Make.com management CLI created"
}

# Execute setup functions
analyze_existing_blueprints
create_make_business_hub
create_vehicle_transport_automation
create_credit_strategy_automation
create_make_cli

echo ""
echo "🎉 Make.com Integration Hub Setup Complete!"
echo ""
echo "Blueprints created:"
echo "  📄 make_business_hub.json - Master business intelligence hub"
echo "  🚛 make_vehicle_transport.json - Vehicle transport automation"
echo "  💳 make_credit_strategy.json - Credit strategy automation"
echo ""
echo "Next steps:"
echo "1. Upload blueprints to Make.com"
echo "2. Configure webhook URLs in applications"
echo "3. Set MAKE_API_TOKEN in .env file"
echo "4. Test scenarios with sample data"
