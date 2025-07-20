#!/bin/bash

# HubSpot Live Data Connector
# Connects to HubSpot API to pull real-time deal and quote data

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/../.env"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

usage() {
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  setup-api           Configure HubSpot API connection"
    echo "  test-connection     Test HubSpot API connectivity"
    echo "  pull-deals          Pull live deals data"
    echo "  pull-contacts       Pull contacts data"
    echo "  pull-companies      Pull companies data"
    echo "  sync-all           Pull all data and update local files"
    echo ""
    echo "Prerequisites:"
    echo "  - HubSpot Private App with scope: crm.objects.deals.read, crm.objects.contacts.read"
    echo "  - API token stored in .env file"
    exit 1
}

setup_api() {
    echo -e "${BLUE}🔧 Setting up HubSpot API connection...${NC}"
    echo ""
    
    if [ ! -f "$CONFIG_FILE" ]; then
        echo "# HubSpot API Configuration" > "$CONFIG_FILE"
        echo "# Created: $TIMESTAMP" >> "$CONFIG_FILE"
        echo "" >> "$CONFIG_FILE"
    fi
    
    echo "To connect to HubSpot API, you need:"
    echo "1. Go to HubSpot → Settings → Integrations → Private Apps"
    echo "2. Create new private app with these scopes:"
    echo "   - crm.objects.deals.read"
    echo "   - crm.objects.contacts.read"
    echo "   - crm.objects.companies.read"
    echo "3. Copy the access token"
    echo ""
    
    read -p "Enter your HubSpot API token: " -s token
    echo ""
    
    # Add or update token in .env file
    if grep -q "HUBSPOT_API_TOKEN" "$CONFIG_FILE"; then
        sed -i.bak "s/HUBSPOT_API_TOKEN=.*/HUBSPOT_API_TOKEN=$token/" "$CONFIG_FILE"
    else
        echo "HUBSPOT_API_TOKEN=$token" >> "$CONFIG_FILE"
    fi
    
    echo -e "${GREEN}✅ API token saved to .env file${NC}"
    echo -e "${YELLOW}⚠️  Make sure .env is in .gitignore for security${NC}"
}

test_connection() {
    echo -e "${BLUE}🔍 Testing HubSpot API connection...${NC}"
    
    if [ ! -f "$CONFIG_FILE" ]; then
        echo -e "${RED}❌ No .env file found. Run 'setup-api' first.${NC}"
        return 1
    fi
    
    source "$CONFIG_FILE"
    
    if [ -z "$HUBSPOT_API_TOKEN" ]; then
        echo -e "${RED}❌ No API token found. Run 'setup-api' first.${NC}"
        return 1
    fi
    
    # Test API call
    response=$(curl -s -w "%{http_code}" -H "Authorization: Bearer $HUBSPOT_API_TOKEN" \
        "https://api.hubapi.com/crm/v3/objects/deals?limit=1")
    
    http_code="${response: -3}"
    
    if [ "$http_code" = "200" ]; then
        echo -e "${GREEN}✅ HubSpot API connection successful${NC}"
        return 0
    else
        echo -e "${RED}❌ API connection failed. HTTP code: $http_code${NC}"
        echo "Check your API token and scopes."
        return 1
    fi
}

pull_deals() {
    echo -e "${BLUE}📊 Pulling live deals data from HubSpot...${NC}"
    
    if ! test_connection; then
        return 1
    fi
    
    source "$CONFIG_FILE"
    
    # Create output directory
    local output_dir="../exports/$(date +%Y-%m-%d)"
    mkdir -p "$output_dir"
    
    # Pull deals with properties
    local deals_file="$output_dir/hubspot-deals-live-$TIMESTAMP.json"
    
    echo "Fetching deals with all properties..."
    curl -s -H "Authorization: Bearer $HUBSPOT_API_TOKEN" \
        "https://api.hubapi.com/crm/v3/objects/deals?limit=100&properties=dealname,amount,dealstage,pipeline,closedate,hubspot_owner_id,deal_currency_code,hs_deal_stage_probability" \
        > "$deals_file"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Deals data saved to: $deals_file${NC}"
        
        # Convert to CSV for analysis
        local csv_file="$output_dir/hubspot-deals-live-$(date +%Y-%m-%d).csv"
        echo "Deal ID,Deal Name,Amount,Stage,Pipeline,Close Date,Owner ID" > "$csv_file"
        
        # Process JSON to CSV (basic extraction)
        # Note: This requires jq for proper JSON parsing
        if command -v jq >/dev/null 2>&1; then
            jq -r '.results[] | [.id, .properties.dealname, .properties.amount, .properties.dealstage, .properties.pipeline, .properties.closedate, .properties.hubspot_owner_id] | @csv' "$deals_file" >> "$csv_file"
            echo -e "${GREEN}✅ CSV export saved to: $csv_file${NC}"
        else
            echo -e "${YELLOW}⚠️  Install 'jq' for CSV conversion: brew install jq${NC}"
        fi
        
    else
        echo -e "${RED}❌ Failed to fetch deals data${NC}"
    fi
}

sync_all() {
    echo -e "${BLUE}🔄 Syncing all HubSpot data...${NC}"
    echo ""
    
    pull_deals
    echo ""
    
    # Add other sync operations here
    echo -e "${GREEN}✅ All data sync completed${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Review exported data in exports/ directory"
    echo "2. Run ../scripts/analyze_hubspot.sh on new data"
    echo "3. Update business-knowledge-repo with insights"
}

case "${1:-}" in
    "setup-api")
        setup_api
        ;;
    "test-connection")
        test_connection
        ;;
    "pull-deals")
        pull_deals
        ;;
    "sync-all")
        sync_all
        ;;
    *)
        usage
        ;;
esac
