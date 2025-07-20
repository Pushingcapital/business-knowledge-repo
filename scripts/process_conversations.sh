#!/bin/bash

# Conversation Data Processor - Extract insights from AI conversation exports

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
REPO_PATH="/Users/emmanuelhaddad/Downloads/business-knowledge-repo"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

usage() {
    echo "Usage: $0 [command] [file_path]"
    echo ""
    echo "Commands:"
    echo "  find-conversations     Locate conversation files in Downloads"
    echo "  process-claude [file]  Process Claude conversation export"
    echo "  process-grok [file]    Process Grok conversation export"
    echo "  extract-insights [file] Extract business insights from conversations"
    echo ""
    echo "Supported formats: JSON, TXT, CSV, RTF, PDF"
    exit 1
}

extract_business_insights() {
    local file_path="$1"
    
    if [ ! -f "$file_path" ]; then
        echo -e "${RED}❌ File not found: $file_path${NC}"
        return 1
    fi
    
    echo -e "${BLUE}📊 Extracting business insights from: $file_path${NC}"
    
    local filename=$(basename "$file_path")
    local extension="${filename##*.}"
    local date_prefix=$(date -u +"%Y-%m-%d")
    
    # Create insight document
    local insight_file="$REPO_PATH/insights/${date_prefix}_conversation-insights-${filename%.*}.md"
    
    echo -e "${GREEN}📝 Creating insight document: $insight_file${NC}"
    
    cat > "$insight_file" << EOF
# Conversation Insights - $filename

---
**Created:** $TIMESTAMP  
**Last Updated:** $TIMESTAMP  
**Type:** insight  
**Source:** AI Conversation Export  
**Original File:** $file_path  
**Tags:** [conversation, ai-insights, business-intelligence]  
---

## Source Information
- **File Name:** $filename
- **File Type:** $extension
- **Processing Date:** $TIMESTAMP
- **AI Platform:** [Detected from content analysis]

## Extracted Business Insights

### Key Decisions Identified
[Business decisions mentioned in conversations]

### Process Improvements
[Workflow optimizations discussed]

### Strategic Insights
[High-level business strategy conversations]

### Technical Solutions
[Technology implementations and solutions]

### Contact Information
[People, companies, or services mentioned]

### Action Items Generated
[Tasks and follow-ups identified]

## Content Analysis Summary

### Conversation Topics
[Main themes and subjects discussed]

### Business Value Assessment
- **High Value:** [Critical business information]
- **Medium Value:** [Useful operational insights]  
- **Low Value:** [General discussions]

### Implementation Opportunities
[Actionable items that could be implemented]

## Next Steps
- [ ] Review extracted insights for accuracy
- [ ] Create decision documents for major choices
- [ ] Add contacts to business database
- [ ] Schedule follow-up actions

---
**Processing Complete:** $TIMESTAMP  
**Airtable Record:** [To be created]
EOF

    echo -e "${GREEN}✅ Insight document created successfully${NC}"
    echo -e "${BLUE}📋 Next steps:${NC}"
    echo "  1. Review: $insight_file"
    echo "  2. Edit with specific insights from the conversation"
    echo "  3. Create Airtable record for tracking"
    
    return 0
}

case "${1:-}" in
    "find-conversations")
        echo -e "${BLUE}🔍 Searching for conversation files...${NC}"
        find /Users/emmanuelhaddad/Downloads -type f \( -name "*claude*" -o -name "*grok*" -o -name "*conversation*" \) 2>/dev/null
        ;;
    "extract-insights")
        extract_business_insights "$2"
        ;;
    "process-claude")
        echo -e "${BLUE}🤖 Processing Claude conversation...${NC}"
        extract_business_insights "$2"
        ;;
    "process-grok")
        echo -e "${BLUE}🤖 Processing Grok conversation...${NC}"
        extract_business_insights "$2"
        ;;
    *)
        usage
        ;;
esac
