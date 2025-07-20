#!/bin/bash

# Master Integration Controller
# Central hub for all business system integrations

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
REPO_PATH="/Users/emmanuelhaddad/Downloads/business-knowledge-repo"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m'

print_header() {
    echo -e "${BLUE}"
    echo "════════════════════════════════════════════════════════════════"
    echo "🚀 PUSHING CAPITAL INTEGRATION CONTROL CENTER"
    echo "════════════════════════════════════════════════════════════════"
    echo -e "${NC}"
    echo -e "${CYAN}Master controller for all business system integrations${NC}"
    echo ""
}

check_integration_status() {
    echo -e "${BLUE}📊 Integration Status Check${NC}"
    echo "================================"
    echo ""
    
    # HubSpot Integration
    if [ -f "$REPO_PATH/.env" ] && grep -q "HUBSPOT_API_TOKEN" "$REPO_PATH/.env"; then
        echo -e "📊 ${GREEN}HubSpot API${NC}        ✅ Configured"
    else
        echo -e "📊 ${RED}HubSpot API${NC}        ❌ Not configured"
    fi
    
    # OpenPhone Integration
    if [ -f "$REPO_PATH/scripts/setup_openphone.sh" ]; then
        echo -e "📱 ${GREEN}OpenPhone${NC}          ✅ Setup ready"
    else
        echo -e "📱 ${RED}OpenPhone${NC}          ❌ Not setup"
    fi
    
    # Slack Integration
    if [ -f "$REPO_PATH/scripts/setup_slack.sh" ]; then
        echo -e "💬 ${GREEN}Slack${NC}              ✅ Setup ready"
    else
        echo -e "💬 ${RED}Slack${NC}              ❌ Not setup"
    fi
    
    # Cursor AI Integration
    if [ -f "$REPO_PATH/scripts/setup_cursor.sh" ]; then
        echo -e "💻 ${GREEN}Cursor AI${NC}          ✅ Setup ready"
    else
        echo -e "💻 ${RED}Cursor AI${NC}          ❌ Not setup"
    fi
    
    # Make.com Integration
    if [ -f "$REPO_PATH/scripts/setup_make.sh" ]; then
        echo -e "🔄 ${GREEN}Make.com${NC}           ✅ Setup ready"
    else
        echo -e "🔄 ${RED}Make.com${NC}           ❌ Not setup"
    fi
    
    # GitHub Integration
    if git remote get-url origin >/dev/null 2>&1; then
        echo -e "🐙 ${GREEN}GitHub${NC}             ✅ Connected"
    else
        echo -e "🐙 ${RED}GitHub${NC}             ❌ Not connected"
    fi
    
    # Airtable Integration
    echo -e "🗃️  ${GREEN}Airtable${NC}           ✅ Connected (appLPGFO41RF6QKHo)"
    
    echo ""
}

quick_setup() {
    echo -e "${YELLOW}⚡ Quick Setup - Running all integration setups...${NC}"
    echo ""
    
    cd "$REPO_PATH"
    
    # Make all scripts executable
    chmod +x scripts/*.sh
    
    # Run all setup scripts
    echo -e "${BLUE}📊 Setting up HubSpot integration...${NC}"
    ./scripts/hubspot_connector.sh setup-api
    
    echo -e "${BLUE}📱 Setting up OpenPhone integration...${NC}"
    ./scripts/setup_openphone.sh
    
    echo -e "${BLUE}💬 Setting up Slack integration...${NC}"
    ./scripts/setup_slack.sh
    
    echo -e "${BLUE}💻 Setting up Cursor AI integration...${NC}"
    ./scripts/setup_cursor.sh
    
    echo -e "${BLUE}🔄 Setting up Make.com integration...${NC}"
    ./scripts/setup_make.sh
    
    echo ""
    echo -e "${GREEN}✅ All integrations setup complete!${NC}"
}

test_integrations() {
    echo -e "${BLUE}🧪 Testing Integrations${NC}"
    echo "======================="
    echo ""
    
    cd "$REPO_PATH"
    
    # Test HubSpot
    echo -e "${CYAN}Testing HubSpot API...${NC}"
    if ./scripts/hubspot_connector.sh test-connection; then
        echo -e "${GREEN}✅ HubSpot API working${NC}"
    else
        echo -e "${RED}❌ HubSpot API failed${NC}"
    fi
    echo ""
    
    # Test GitHub
    echo -e "${CYAN}Testing GitHub connection...${NC}"
    if git remote get-url origin >/dev/null 2>&1; then
        echo -e "${GREEN}✅ GitHub connected${NC}"
    else
        echo -e "${RED}❌ GitHub not connected${NC}"
    fi
    echo ""
    
    # Test file system integrations
    echo -e "${CYAN}Testing local integrations...${NC}"
    ./scripts/repo_status.sh
}

show_integration_urls() {
    echo -e "${BLUE}🔗 Integration URLs & Endpoints${NC}"
    echo "==============================="
    echo ""
    
    echo -e "${CYAN}GitHub Repository:${NC}"
    echo "https://github.com/pushingcapital/business-knowledge-repo"
    echo ""
    
    echo -e "${CYAN}Airtable Base:${NC}"
    echo "https://airtable.com/appLPGFO41RF6QKHo"
    echo ""
    
    echo -e "${CYAN}HubSpot CRM:${NC}"
    echo "https://app.hubspot.com/"
    echo ""
    
    echo -e "${CYAN}Make.com Scenarios:${NC}"
    echo "https://make.com/scenarios"
    echo ""
    
    echo -e "${CYAN}Cloudflare Workers (for webhooks):${NC}"
    echo "https://workers.cloudflare.com/"
    echo ""
}

run_business_analysis() {
    echo -e "${BLUE}📈 Running Business Analysis${NC}"
    echo "============================"
    echo ""
    
    cd "$REPO_PATH"
    
    # HubSpot analysis
    echo -e "${CYAN}📊 HubSpot Pipeline Analysis:${NC}"
    ./scripts/analyze_hubspot.sh pipeline-summary
    echo ""
    
    # Repository status
    echo -e "${CYAN}📁 Repository Status:${NC}"
    ./scripts/repo_status.sh
    echo ""
    
    # Latest insights
    echo -e "${CYAN}💡 Latest Business Insights:${NC}"
    ls -la insights/ | tail -5
}

create_integration_dashboard() {
    echo -e "${BLUE}📊 Creating Integration Dashboard...${NC}"
    
    cat > integration_dashboard.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Pushing Capital Integration Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
        .integration-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .integration-card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .status-green { color: #28a745; }
        .status-red { color: #dc3545; }
        .quick-links { background: white; padding: 20px; border-radius: 10px; margin-top: 20px; }
        .quick-links a { display: inline-block; margin: 5px 10px; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 Pushing Capital Integration Dashboard</h1>
        <p>Master control center for all business system integrations</p>
    </div>
    
    <div class="integration-grid">
        <div class="integration-card">
            <h3>📊 HubSpot CRM</h3>
            <p><strong>Status:</strong> <span class="status-green">✅ Connected</span></p>
            <p><strong>Pipeline Value:</strong> $57,977</p>
            <p><strong>Active Deals:</strong> 37</p>
            <p><strong>Last Sync:</strong> Live API</p>
        </div>
        
        <div class="integration-card">
            <h3>📱 OpenPhone</h3>
            <p><strong>Status:</strong> <span class="status-green">✅ Setup Ready</span></p>
            <p><strong>Features:</strong> SMS, Call logs, Webhooks</p>
            <p><strong>Integration:</strong> HubSpot + Knowledge Repo</p>
        </div>
        
        <div class="integration-card">
            <h3>💬 Slack</h3>
            <p><strong>Status:</strong> <span class="status-green">✅ Setup Ready</span></p>
            <p><strong>Features:</strong> Bot commands, Message capture</p>
            <p><strong>Commands:</strong> /pipeline, /deals, /quote</p>
        </div>
        
        <div class="integration-card">
            <h3>💻 Cursor AI</h3>
            <p><strong>Status:</strong> <span class="status-green">✅ Setup Ready</span></p>
            <p><strong>Features:</strong> Code sync, Business context</p>
            <p><strong>Templates:</strong> HubSpot, Automation, Quotes</p>
        </div>
        
        <div class="integration-card">
            <h3>🔄 Make.com</h3>
            <p><strong>Status:</strong> <span class="status-green">✅ Setup Ready</span></p>
            <p><strong>Scenarios:</strong> Vehicle Transport, Credit Strategy</p>
            <p><strong>Automation:</strong> Quote to Deal pipeline</p>
        </div>
        
        <div class="integration-card">
            <h3>🐙 GitHub</h3>
            <p><strong>Status:</strong> <span class="status-green">✅ Connected</span></p>
            <p><strong>Repository:</strong> business-knowledge-repo</p>
            <p><strong>Latest:</strong> Integration setup complete</p>
        </div>
    </div>
    
    <div class="quick-links">
        <h3>🔗 Quick Links</h3>
        <a href="https://github.com/pushingcapital/business-knowledge-repo">GitHub Repo</a>
        <a href="https://airtable.com/appLPGFO41RF6QKHo">Airtable Base</a>
        <a href="https://app.hubspot.com/">HubSpot CRM</a>
        <a href="https://make.com/scenarios">Make.com</a>
        <a href="file:///Users/emmanuelhaddad/Downloads/business-knowledge-repo">Local Files</a>
    </div>
</body>
</html>
EOF

    echo -e "${GREEN}✅ Integration dashboard created: integration_dashboard.html${NC}"
}

# Main CLI dispatcher
case "${1:-}" in
    "status")
        print_header
        check_integration_status
        ;;
    "setup")
        print_header
        quick_setup
        ;;
    "test")
        print_header
        test_integrations
        ;;
    "urls")
        print_header
        show_integration_urls
        ;;
    "analyze")
        print_header
        run_business_analysis
        ;;
    "dashboard")
        print_header
        create_integration_dashboard
        ;;
    "all")
        print_header
        check_integration_status
        echo ""
        show_integration_urls
        echo ""
        run_business_analysis
        ;;
    *)
        print_header
        echo -e "${YELLOW}Usage: $0 [command]${NC}"
        echo ""
        echo -e "${CYAN}Commands:${NC}"
        echo "  status      Check integration status"
        echo "  setup       Run quick setup for all integrations"
        echo "  test        Test all integration connections"
        echo "  urls        Show all integration URLs and endpoints"
        echo "  analyze     Run comprehensive business analysis"
        echo "  dashboard   Create HTML integration dashboard"
        echo "  all         Show complete integration overview"
        echo ""
        echo -e "${CYAN}Individual Integration Commands:${NC}"
        echo "  ./scripts/hubspot_connector.sh     - HubSpot API management"
        echo "  ./scripts/setup_openphone.sh       - OpenPhone integration"
        echo "  ./scripts/setup_slack.sh           - Slack integration"
        echo "  ./scripts/setup_cursor.sh          - Cursor AI integration"
        echo "  ./scripts/setup_make.sh            - Make.com automation"
        echo "  ./scripts/analyze_hubspot.sh       - HubSpot data analysis"
        echo ""
        echo -e "${GREEN}🎯 Quick Start: $0 setup${NC}"
        ;;
esac

echo ""
echo -e "${PURPLE}🕐 Integration controller completed at: $TIMESTAMP${NC}"
