#!/bin/bash

# Airtable Live Data Connector
# Connects to Airtable API to pull real-time data from business intelligence base

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/../.env"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Airtable Configuration
AIRTABLE_BASE_ID="appLPGFO41RF6QKHo"
AIRTABLE_BASE_URL="https://api.airtable.com/v0"

usage() {
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  setup-api           Configure Airtable API connection"
    echo "  test-connection     Test Airtable API connectivity"
    echo "  list-tables         List all tables in the base"
    echo "  pull-records        Pull records from a specific table"
    echo "  create-record       Create a new record in a table"
    echo "  sync-all           Pull all data and update local files"
    echo ""
    echo "Prerequisites:"
    echo "  - Airtable API key from https://airtable.com/account"
    echo "  - Access to base: https://airtable.com/$AIRTABLE_BASE_ID"
    exit 1
}

setup_api() {
    echo -e "${BLUE}🔧 Setting up Airtable API connection...${NC}"
    echo ""
    
    if [ ! -f "$CONFIG_FILE" ]; then
        echo "# Airtable API Configuration" > "$CONFIG_FILE"
        echo "# Created: $TIMESTAMP" >> "$CONFIG_FILE"
        echo "" >> "$CONFIG_FILE"
    fi
    
    echo "To connect to Airtable API, you need:"
    echo "1. Go to https://airtable.com/account"
    echo "2. Generate API key"
    echo "3. Copy the API key"
    echo ""
    echo "Base URL: https://airtable.com/$AIRTABLE_BASE_ID"
    echo ""
    
    read -p "Enter your Airtable API key: " -s token
    echo ""
    
    # Add or update token in .env file
    if grep -q "AIRTABLE_API_KEY" "$CONFIG_FILE"; then
        sed -i.bak "s/AIRTABLE_API_KEY=.*/AIRTABLE_API_KEY=$token/" "$CONFIG_FILE"
    else
        echo "" >> "$CONFIG_FILE"
        echo "# Airtable API Configuration" >> "$CONFIG_FILE"
        echo "AIRTABLE_API_KEY=$token" >> "$CONFIG_FILE"
        echo "AIRTABLE_BASE_ID=$AIRTABLE_BASE_ID" >> "$CONFIG_FILE"
    fi
    
    echo -e "${GREEN}✅ API key saved to .env file${NC}"
    echo -e "${YELLOW}⚠️  Make sure .env is in .gitignore for security${NC}"
}

test_connection() {
    echo -e "${BLUE}🔍 Testing Airtable API connection...${NC}"
    
    if [ ! -f "$CONFIG_FILE" ]; then
        echo -e "${RED}❌ No .env file found. Run 'setup-api' first.${NC}"
        return 1
    fi
    
    source "$CONFIG_FILE"
    
    if [ -z "$AIRTABLE_API_KEY" ]; then
        echo -e "${RED}❌ No API key found. Run 'setup-api' first.${NC}"
        return 1
    fi
    
    # Test API call to list tables
    response=$(curl -s -w "%{http_code}" -H "Authorization: Bearer $AIRTABLE_API_KEY" \
        "$AIRTABLE_BASE_URL/meta/bases/$AIRTABLE_BASE_ID/tables")
    
    http_code="${response: -3}"
    response_body="${response%???}"
    
    if [ "$http_code" = "200" ]; then
        echo -e "${GREEN}✅ Airtable API connection successful${NC}"
        echo -e "${BLUE}📊 Base ID: $AIRTABLE_BASE_ID${NC}"
        
        # Parse and display table names
        table_count=$(echo "$response_body" | grep -o '"name"' | wc -l)
        echo -e "${GREEN}📋 Found $table_count tables in base${NC}"
        
        return 0
    else
        echo -e "${RED}❌ API connection failed. HTTP code: $http_code${NC}"
        echo "Response: $response_body"
        echo "Check your API key and base access."
        return 1
    fi
}

list_tables() {
    echo -e "${BLUE}📋 Listing Airtable tables...${NC}"
    
    if [ ! -f "$CONFIG_FILE" ]; then
        echo -e "${RED}❌ No .env file found. Run 'setup-api' first.${NC}"
        return 1
    fi
    
    source "$CONFIG_FILE"
    
    if [ -z "$AIRTABLE_API_KEY" ]; then
        echo -e "${RED}❌ No API key found. Run 'setup-api' first.${NC}"
        return 1
    fi
    
    response=$(curl -s -H "Authorization: Bearer $AIRTABLE_API_KEY" \
        "$AIRTABLE_BASE_URL/meta/bases/$AIRTABLE_BASE_ID/tables")
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Tables in base:${NC}"
        echo "$response" | grep -o '"name":"[^"]*"' | sed 's/"name":"//g' | sed 's/"//g' | nl
    else
        echo -e "${RED}❌ Failed to list tables${NC}"
        return 1
    fi
}

pull_records() {
    if [ -z "$1" ]; then
        echo "Usage: $0 pull-records <table_name>"
        echo ""
        echo "Available tables:"
        list_tables
        return 1
    fi
    
    table_name="$1"
    echo -e "${BLUE}📊 Pulling records from table: $table_name${NC}"
    
    if [ ! -f "$CONFIG_FILE" ]; then
        echo -e "${RED}❌ No .env file found. Run 'setup-api' first.${NC}"
        return 1
    fi
    
    source "$CONFIG_FILE"
    
    if [ -z "$AIRTABLE_API_KEY" ]; then
        echo -e "${RED}❌ No API key found. Run 'setup-api' first.${NC}"
        return 1
    fi
    
    # URL encode table name
    encoded_table=$(echo "$table_name" | sed 's/ /%20/g')
    
    response=$(curl -s -H "Authorization: Bearer $AIRTABLE_API_KEY" \
        "$AIRTABLE_BASE_URL/$AIRTABLE_BASE_ID/$encoded_table")
    
    if [ $? -eq 0 ]; then
        record_count=$(echo "$response" | grep -o '"id"' | wc -l)
        echo -e "${GREEN}✅ Found $record_count records in $table_name${NC}"
        
        # Save to file
        output_file="airtable_${table_name}_$(date +%Y%m%d_%H%M%S).json"
        echo "$response" > "$output_file"
        echo -e "${BLUE}💾 Saved to: $output_file${NC}"
    else
        echo -e "${RED}❌ Failed to pull records${NC}"
        return 1
    fi
}

create_record() {
    if [ -z "$1" ] || [ -z "$2" ]; then
        echo "Usage: $0 create-record <table_name> <json_fields>"
        echo "Example: $0 create-record 'Business Decisions' '{\"Title\":\"Test Decision\",\"Status\":\"Active\"}'"
        return 1
    fi
    
    table_name="$1"
    fields_json="$2"
    
    echo -e "${BLUE}➕ Creating record in table: $table_name${NC}"
    
    if [ ! -f "$CONFIG_FILE" ]; then
        echo -e "${RED}❌ No .env file found. Run 'setup-api' first.${NC}"
        return 1
    fi
    
    source "$CONFIG_FILE"
    
    if [ -z "$AIRTABLE_API_KEY" ]; then
        echo -e "${RED}❌ No API key found. Run 'setup-api' first.${NC}"
        return 1
    fi
    
    # URL encode table name
    encoded_table=$(echo "$table_name" | sed 's/ /%20/g')
    
    # Create record data
    record_data="{\"fields\":$fields_json}"
    
    response=$(curl -s -X POST \
        -H "Authorization: Bearer $AIRTABLE_API_KEY" \
        -H "Content-Type: application/json" \
        -d "$record_data" \
        "$AIRTABLE_BASE_URL/$AIRTABLE_BASE_ID/$encoded_table")
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Record created successfully${NC}"
        echo "Response: $response"
    else
        echo -e "${RED}❌ Failed to create record${NC}"
        echo "Response: $response"
        return 1
    fi
}

sync_all() {
    echo -e "${BLUE}🔄 Syncing all Airtable data...${NC}"
    
    # First test connection
    if ! test_connection; then
        return 1
    fi
    
    # List tables and pull data from each
    tables=$(curl -s -H "Authorization: Bearer $AIRTABLE_API_KEY" \
        "$AIRTABLE_BASE_URL/meta/bases/$AIRTABLE_BASE_ID/tables" | \
        grep -o '"name":"[^"]*"' | sed 's/"name":"//g' | sed 's/"//g')
    
    for table in $tables; do
        echo -e "${BLUE}📊 Syncing table: $table${NC}"
        pull_records "$table" > /dev/null 2>&1
    done
    
    echo -e "${GREEN}✅ All tables synced${NC}"
}

# Main command handling
case "${1:-}" in
    "setup-api")
        setup_api
        ;;
    "test-connection")
        test_connection
        ;;
    "list-tables")
        list_tables
        ;;
    "pull-records")
        pull_records "$2"
        ;;
    "create-record")
        create_record "$2" "$3"
        ;;
    "sync-all")
        sync_all
        ;;
    *)
        usage
        ;;
esac 