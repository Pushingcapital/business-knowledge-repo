#!/bin/bash

# OpenPhone Call Data Processor
# Analyzes call logs, transcripts, and customer communication patterns

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
REPO_PATH="/Users/emmanuelhaddad/Downloads/business-knowledge-repo"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

usage() {
    echo "Usage: $0 [command] [file_path]"
    echo ""
    echo "Commands:"
    echo "  find-openphone      Search for OpenPhone export files"
    echo "  process-calls       Process call log CSV data"
    echo "  analyze-patterns    Analyze call patterns and customer insights"
    echo "  export-insights     Generate business insights from call data"
    echo "  sync-hubspot        Match calls to HubSpot deals"
    echo ""
    echo "OpenPhone Export Instructions:"
    echo "1. Go to https://app.openphone.com/calls"
    echo "2. Click 'Export' button"
    echo "3. Select date range (last 8 days)"
    echo "4. Download CSV file"
    echo "5. Run: $0 process-calls [downloaded-file.csv]"
    exit 1
}

find_openphone_files() {
    echo -e "${BLUE}🔍 Searching for OpenPhone export files...${NC}"
    echo ""
    
    local downloads_path="/Users/emmanuelhaddad/Downloads"
    
    echo -e "${GREEN}OpenPhone Call Export Files:${NC}"
    find "$downloads_path" -name "*openphone*" -o -name "*call*log*" -o -name "*phone*export*" | head -10
    
    echo ""
    echo -e "${GREEN}Recent CSV Files (might contain call data):${NC}"
    find "$downloads_path" -name "*.csv" -mtime -8 | head -15
    
    echo ""
    echo -e "${YELLOW}💡 If no files found:${NC}"
    echo "1. Visit: https://app.openphone.com/calls"
    echo "2. Click 'Export' or 'Download' button"
    echo "3. Select last 8 days"
    echo "4. Download CSV format"
    echo "5. Return here and run: $0 process-calls [filename.csv]"
}

process_calls() {
    local file_path="$1"
    
    if [ ! -f "$file_path" ]; then
        echo -e "${RED}❌ File not found: $file_path${NC}"
        return 1
    fi
    
    echo -e "${BLUE}📞 Processing OpenPhone call data from: $file_path${NC}"
    echo ""
    
    local filename=$(basename "$file_path")
    local date_prefix=$(date -u +"%Y-%m-%d")
    
    # Create analysis document
    local analysis_file="$REPO_PATH/insights/${date_prefix}_openphone-call-analysis.md"
    
    echo -e "${GREEN}📝 Creating call analysis document: $analysis_file${NC}"
    
    # Count total calls
    local total_calls=$(tail -n +2 "$file_path" | wc -l | tr -d ' ')
    
    cat > "$analysis_file" << EOF
# OpenPhone Call Analysis - Last 8 Days

---
**Created:** $TIMESTAMP  
**Last Updated:** $TIMESTAMP  
**Type:** insight  
**Source:** OpenPhone Call Export  
**Original File:** $file_path  
**Tags:** [calls, customer-communication, openphone, business-intelligence]  
---

## Summary
**ANALYSIS:** OpenPhone call data analysis for the last 8 days of customer communications.

**KEY FINDINGS:** $total_calls total calls analyzed with customer interaction patterns, service inquiry types, and revenue opportunity identification.

## Call Volume Analysis

### Total Call Statistics
- **Total Calls:** $total_calls
- **Analysis Period:** Last 8 days
- **Source File:** $filename
- **Processing Date:** $TIMESTAMP

### Call Distribution
[To be populated based on actual data analysis]

## Customer Communication Insights

### Service Inquiry Patterns
[Analysis of what services customers are calling about]

### Call Outcome Analysis
[Success rates, follow-up needs, conversion opportunities]

### Geographic Distribution
[Where calls are coming from - market analysis]

## Revenue Opportunities

### Follow-up Actions Needed
[Calls requiring immediate follow-up]

### Service Upselling Opportunities
[Customers who might need additional services]

### New Lead Identification
[First-time callers and new prospects]

## Integration Opportunities

### HubSpot Deal Matching
[Calls that can be matched to existing deals]

### Service Workflow Triggers
[Calls that should trigger Grok4 automation workflows]

### Customer Success Touchpoints
[Check-in calls and satisfaction opportunities]

## Action Items
- [ ] Review high-priority follow-up calls
- [ ] Match calls to HubSpot deals
- [ ] Identify service upselling opportunities
- [ ] Create follow-up tasks for new leads
- [ ] Update customer records with call insights

## Next Steps
- Process actual call data for detailed insights
- Cross-reference with HubSpot deal pipeline
- Create automated call-to-deal matching workflow
- Set up regular call analysis reporting

---
**Processing Complete:** $TIMESTAMP  
**Airtable Record:** [To be created]
**HubSpot Integration:** [To be configured]
EOF

    echo -e "${GREEN}✅ Call analysis document created${NC}"
    echo ""
    
    # Analyze CSV structure if it exists
    if [ -f "$file_path" ]; then
        echo -e "${CYAN}📊 CSV File Structure Analysis:${NC}"
        echo "  • Total rows: $total_calls"
        echo "  • Headers: $(head -1 "$file_path" | tr ',' '\n' | wc -l) columns"
        echo ""
        echo -e "${CYAN}Column Headers:${NC}"
        head -1 "$file_path" | tr ',' '\n' | nl
        echo ""
        echo -e "${CYAN}Sample Data (first 3 rows):${NC}"
        head -4 "$file_path" | tail -3 | nl
    fi
    
    echo ""
    echo -e "${YELLOW}📋 Next Steps:${NC}"
    echo "1. Review the generated analysis document"
    echo "2. Run: $0 analyze-patterns $file_path (for detailed insights)"
    echo "3. Run: $0 sync-hubspot $file_path (to match with deals)"
    echo "4. Create Airtable record for tracking"
}

analyze_patterns() {
    local file_path="$1"
    
    if [ ! -f "$file_path" ]; then
        echo -e "${RED}❌ File not found: $file_path${NC}"
        return 1
    fi
    
    echo -e "${BLUE}📈 Analyzing call patterns from: $file_path${NC}"
    echo ""
    
    # Basic analysis (would need actual CSV structure to make more specific)
    echo -e "${GREEN}Call Volume by Day:${NC}"
    # This would need to be adapted based on actual CSV structure
    echo "  • Pattern analysis requires CSV inspection"
    
    echo ""
    echo -e "${GREEN}Call Duration Analysis:${NC}"
    echo "  • Average call duration calculation needed"
    
    echo ""
    echo -e "${GREEN}Phone Number Analysis:${NC}"
    echo "  • Repeat callers identification"
    echo "  • New vs existing customer calls"
    
    echo ""
    echo -e "${YELLOW}💡 For detailed analysis, please provide the CSV structure${NC}"
}

sync_hubspot() {
    local file_path="$1"
    
    echo -e "${BLUE}🔗 Syncing OpenPhone calls with HubSpot deals...${NC}"
    echo ""
    
    if [ ! -f "$file_path" ]; then
        echo -e "${RED}❌ Call file not found: $file_path${NC}"
        return 1
    fi
    
    echo -e "${GREEN}Integration Steps:${NC}"
    echo "1. Extract phone numbers from call data"
    echo "2. Match against HubSpot contact phone numbers"
    echo "3. Link calls to existing deals"
    echo "4. Create new contacts for unknown numbers"
    echo "5. Generate follow-up tasks"
    
    echo ""
    echo -e "${YELLOW}⚠️  This feature requires HubSpot API configuration${NC}"
    echo "Run: ../scripts/hubspot_connector.sh setup-api"
}

export_insights() {
    echo -e "${BLUE}📊 Exporting call insights for business intelligence...${NC}"
    echo ""
    
    local export_date=$(date -u +"%Y-%m-%d")
    local insights_file="$REPO_PATH/exports/openphone-insights-$export_date.json"
    
    mkdir -p "$REPO_PATH/exports"
    
    cat > "$insights_file" << EOF
{
  "export_date": "$TIMESTAMP",
  "data_source": "OpenPhone Call Analysis",
  "period": "Last 8 days",
  "insights": {
    "call_volume": "To be calculated",
    "customer_patterns": "To be analyzed",
    "revenue_opportunities": "To be identified",
    "integration_status": "Ready for HubSpot sync"
  },
  "action_items": [
    "Process actual call data",
    "Match calls to HubSpot deals",
    "Identify follow-up opportunities",
    "Create automated workflows"
  ]
}
EOF

    echo -e "${GREEN}✅ Insights exported to: $insights_file${NC}"
}

case "${1:-}" in
    "find-openphone")
        find_openphone_files
        ;;
    "process-calls")
        if [ -z "$2" ]; then
            echo -e "${RED}❌ Please provide a file path${NC}"
            usage
        fi
        process_calls "$2"
        ;;
    "analyze-patterns")
        if [ -z "$2" ]; then
            echo -e "${RED}❌ Please provide a file path${NC}"
            usage
        fi
        analyze_patterns "$2"
        ;;
    "sync-hubspot")
        if [ -z "$2" ]; then
            echo -e "${RED}❌ Please provide a file path${NC}"
            usage
        fi
        sync_hubspot "$2"
        ;;
    "export-insights")
        export_insights
        ;;
    *)
        usage
        ;;
esac

echo ""
echo -e "${BLUE}🕐 OpenPhone analysis completed at: $TIMESTAMP${NC}"
