#!/bin/bash

# 🚀 AI Agents Master Launcher
# Launch and manage all AI agents for Pushing Capital business operations

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m'

print_banner() {
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                🤖 AI AGENTS CONTROL CENTER                    ║"
    echo "║                   Pushing Capital Operations                    ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo -e "${CYAN}Intelligent business automation with AI agent coordination${NC}"
    echo ""
}

check_dependencies() {
    echo -e "${YELLOW}🔍 Checking dependencies...${NC}"
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python 3 not found${NC}"
        return 1
    fi
    
    # Check required Python packages
    if ! python3 -c "import requests" 2>/dev/null; then
        echo -e "${YELLOW}📦 Installing Python dependencies...${NC}"
        pip3 install requests flask gunicorn pyyaml python-dotenv 2>/dev/null || {
            echo -e "${RED}❌ Failed to install Python dependencies${NC}"
            return 1
        }
    fi
    
    # Check if agents exist
    local missing_agents=()
    if [ ! -f "integrations_manager_agent.py" ]; then
        missing_agents+=("Integrations Manager")
    fi
    if [ ! -f "grok_ceo_agent.py" ]; then
        missing_agents+=("Grok CEO")
    fi
    if [ ! -f "communications_manager_agent.py" ]; then
        missing_agents+=("Communications Manager")
    fi
    
    if [ ${#missing_agents[@]} -gt 0 ]; then
        echo -e "${RED}❌ Missing agents: ${missing_agents[*]}${NC}"
        return 1
    fi
    
    echo -e "${GREEN}✅ All dependencies satisfied${NC}"
    return 0
}

show_agent_status() {
    echo -e "${BLUE}📊 Agent Status Dashboard${NC}"
    echo "================================"
    
    # Integrations Manager
    if [ -f "integrations_manager_agent.py" ]; then
        echo -e "🔧 ${GREEN}Integrations Manager${NC}  ✅ Ready"
        echo "   • Monitors 7 business integrations"
        echo "   • Health checks and auto-fixing"
        echo "   • Real-time integration analytics"
    else
        echo -e "🔧 ${RED}Integrations Manager${NC}  ❌ Missing"
    fi
    
    echo ""
    
    # Grok CEO
    if [ -f "grok_ceo_agent.py" ]; then
        echo -e "🏛️ ${GREEN}Grok CEO${NC}              ✅ Ready"
        echo "   • Strategic decision making"
        echo "   • Executive reporting"
        echo "   • Multi-agent coordination"
    else
        echo -e "🏛️ ${RED}Grok CEO${NC}              ❌ Missing"
    fi
    
    echo ""
    
    # Communications Manager
    if [ -f "communications_manager_agent.py" ]; then
        echo -e "📡 ${GREEN}Communications Manager${NC} ✅ Ready"
        echo "   • Multi-channel messaging"
        echo "   • Business alerts & notifications"
        echo "   • Customer communications"
    else
        echo -e "📡 ${RED}Communications Manager${NC} ❌ Missing"
    fi
    
    echo ""
    
    # Cloud Deployment
    if [ -f "cloud_shell_deployment.py" ]; then
        echo -e "☁️ ${GREEN}Cloud Shell Deployment${NC} ✅ Ready"
        echo "   • Google Cloud Run deployment"
        echo "   • Container orchestration"
        echo "   • Auto-scaling & monitoring"
    else
        echo -e "☁️ ${RED}Cloud Shell Deployment${NC} ❌ Missing"
    fi
    
    echo ""
}

launch_integrations_manager() {
    echo -e "${BLUE}🔧 Launching Integrations Manager...${NC}"
    
    if [ ! -f "integrations_manager_agent.py" ]; then
        echo -e "${RED}❌ Integrations Manager agent not found${NC}"
        return 1
    fi
    
    echo -e "${GREEN}Commands available:${NC}"
    echo "  status    - Check all integration health"
    echo "  report    - Generate detailed report"
    echo "  fix       - Auto-fix integration issues"
    echo "  monitor   - Start continuous monitoring"
    echo ""
    
    if [ $# -gt 1 ]; then
        python3 integrations_manager_agent.py "${@:2}"
    else
        python3 integrations_manager_agent.py status
    fi
}

launch_grok_ceo() {
    echo -e "${BLUE}🏛️ Launching Grok CEO Agent...${NC}"
    
    if [ ! -f "grok_ceo_agent.py" ]; then
        echo -e "${RED}❌ Grok CEO agent not found${NC}"
        return 1
    fi
    
    echo -e "${GREEN}Commands available:${NC}"
    echo "  decision <type>  - Make strategic decision"
    echo "  report          - Generate executive report"
    echo "  coordinate      - Coordinate agent tasks"
    echo "  metrics         - Show business metrics"
    echo ""
    
    if [ $# -gt 1 ]; then
        python3 grok_ceo_agent.py "${@:2}"
    else
        python3 grok_ceo_agent.py report
    fi
}

launch_communications_manager() {
    echo -e "${BLUE}📡 Launching Communications Manager...${NC}"
    
    if [ ! -f "communications_manager_agent.py" ]; then
        echo -e "${RED}❌ Communications Manager agent not found${NC}"
        return 1
    fi
    
    echo -e "${GREEN}Commands available:${NC}"
    echo "  alert <severity> <message>    - Send business alert"
    echo "  executive <message>          - Send executive update"
    echo "  customer <service> <message> - Send customer notification"
    echo "  analytics                    - Show communication analytics"
    echo "  channels                     - Show channel status"
    echo ""
    
    if [ $# -gt 1 ]; then
        python3 communications_manager_agent.py "${@:2}"
    else
        python3 communications_manager_agent.py channels
    fi
}

launch_cursor_ai() {
    echo -e "${BLUE}🔮 Launching Cursor AI Agent...${NC}"
    
    if [ ! -f "cursor_ai_agent.py" ]; then
        echo -e "${RED}❌ Cursor AI agent not found${NC}"
        return 1
    fi
    
    echo -e "${GREEN}Commands available:${NC}"
    echo "  start                        - Start Cursor AI integration"
    echo "  context                      - Update business context"
    echo "  watch                        - Start file watching"
    echo "  report                       - Generate development report"
    echo "  status                       - Show integration status"
    echo ""
    
    if [ $# -gt 1 ]; then
        case "${2:-}" in
            "start")
                python3 cursor_ai_agent.py
                ;;
            "context")
                echo "🔮 Updating Cursor AI business context..."
                python3 -c "
from cursor_ai_agent import CursorAIAgent
agent = CursorAIAgent()
agent.update_cursor_business_context()
print('✅ Business context updated')
"
                ;;
            "watch")
                echo "👀 Starting Cursor AI file watching..."
                python3 -c "
from cursor_ai_agent import CursorAIAgent
agent = CursorAIAgent()
observer = agent.start_file_watching()
try:
    import time
    print('🔮 Cursor AI watching for file changes... (Press Ctrl+C to stop)')
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
    print('✅ File watching stopped')
    observer.join()
"
                ;;
            "report")
                python3 -c "
from cursor_ai_agent import CursorAIAgent
agent = CursorAIAgent()
report = agent.generate_development_report()
print(report)
"
                ;;
            "status")
                echo "🔮 Cursor AI Integration Status:"
                echo "  📧 Email Intelligence: $(python3 -c 'from cursor_ai_agent import CursorAIAgent; print(CursorAIAgent().get_email_intelligence_status())')"
                echo "  🎯 HubSpot Integration: $(python3 -c 'from cursor_ai_agent import CursorAIAgent; print(CursorAIAgent().get_hubspot_status())')"
                echo "  🔧 Integrations Health: $(python3 -c 'from cursor_ai_agent import CursorAIAgent; print(CursorAIAgent().get_integrations_status())')"
                echo "  🔮 Cursor Settings: $([ -f '.cursor-settings.json' ] && echo '✅ Configured' || echo '❌ Missing')"
                ;;
            *)
                echo "🔮 Running default Cursor AI integration..."
                python3 cursor_ai_agent.py
                ;;
        esac
    else
        echo "🔮 Running default Cursor AI integration..."
        python3 cursor_ai_agent.py
    fi
}

deploy_to_cloud() {
    echo -e "${BLUE}☁️ Deploying to Google Cloud Shell...${NC}"
    
    if [ ! -f "cloud_shell_deployment.py" ]; then
        echo -e "${RED}❌ Cloud Shell deployment manager not found${NC}"
        return 1
    fi
    
    echo -e "${YELLOW}📋 Pre-deployment checklist:${NC}"
    echo "  ✓ Google Cloud CLI installed"
    echo "  ✓ Project ID configured"
    echo "  ✓ Billing enabled"
    echo "  ✓ Required APIs enabled"
    echo ""
    
    echo -e "${GREEN}Available commands:${NC}"
    echo "  deploy     - Deploy all agents to cloud"
    echo "  health     - Check deployment health"
    echo "  scale      - Scale agent instances"
    echo "  status     - Show deployment status"
    echo "  dashboard  - Create management dashboard"
    echo ""
    
    if [ $# -gt 1 ]; then
        python3 cloud_shell_deployment.py "${@:2}"
    else
        python3 cloud_shell_deployment.py deploy
    fi
}

run_agent_coordination() {
    echo -e "${BLUE}🤖 Running Agent Coordination Demo...${NC}"
    
    echo -e "${CYAN}Simulating business workflow with all agents:${NC}"
    echo ""
    
    # Step 1: Check integrations
    echo -e "${YELLOW}Step 1: Checking integration health...${NC}"
    python3 integrations_manager_agent.py status
    echo ""
    
    # Step 2: CEO strategic decision
    echo -e "${YELLOW}Step 2: CEO making strategic decision...${NC}"
    python3 grok_ceo_agent.py decision service_expansion
    echo ""
    
    # Step 3: Send business alert
    echo -e "${YELLOW}Step 3: Sending business alert...${NC}"
    python3 communications_manager_agent.py alert high "New service expansion approved by CEO"
    echo ""
    
    echo -e "${GREEN}✅ Agent coordination workflow completed${NC}"
}

generate_deployment_report() {
    echo -e "${BLUE}📄 Generating Deployment Report...${NC}"
    
    local report_file="ai_agents_deployment_report_$(date +%Y%m%d_%H%M%S).md"
    
    cat > "$report_file" << EOF
# 🤖 AI Agents Deployment Report

**Generated:** $TIMESTAMP
**System:** $(uname -s) $(uname -r)
**Location:** $(pwd)

## Agent Status

### 🔧 Integrations Manager Agent
- **File:** integrations_manager_agent.py
- **Status:** $([ -f "integrations_manager_agent.py" ] && echo "✅ Ready" || echo "❌ Missing")
- **Purpose:** Monitor and manage all business system integrations
- **Capabilities:** Health checks, auto-fixing, analytics, monitoring

### 🏛️ Grok CEO Agent
- **File:** grok_ceo_agent.py
- **Status:** $([ -f "grok_ceo_agent.py" ] && echo "✅ Ready" || echo "❌ Missing")
- **Purpose:** Executive-level strategic decision making
- **Capabilities:** Strategic decisions, executive reporting, agent coordination

### 📡 Communications Manager Agent
- **File:** communications_manager_agent.py
- **Status:** $([ -f "communications_manager_agent.py" ] && echo "✅ Ready" || echo "❌ Missing")
- **Purpose:** Multi-channel business communications
- **Capabilities:** Alerts, notifications, customer communications, analytics

### ☁️ Cloud Shell Deployment Manager
- **File:** cloud_shell_deployment.py
- **Status:** $([ -f "cloud_shell_deployment.py" ] && echo "✅ Ready" || echo "❌ Missing")
- **Purpose:** Deploy and manage agents in Google Cloud
- **Capabilities:** Container deployment, scaling, monitoring, dashboards

## Deployment Commands

\`\`\`bash
# Launch individual agents
./launch_ai_agents.sh integrations
./launch_ai_agents.sh ceo
./launch_ai_agents.sh communications

# Deploy to cloud
./launch_ai_agents.sh cloud deploy

# Run coordination demo
./launch_ai_agents.sh coordinate

# Check status
./launch_ai_agents.sh status
\`\`\`

## Architecture Overview

The AI agents work together to provide comprehensive business automation:

1. **Integrations Manager** monitors system health and performance
2. **Grok CEO** makes strategic decisions based on business data
3. **Communications Manager** handles all business communications
4. **Cloud Deployment** ensures scalable, reliable infrastructure

## Next Steps

1. Configure environment variables (.env file)
2. Set up API keys for integrations
3. Deploy to Google Cloud for production use
4. Monitor agent performance and health

---
**Report generated by AI Agents Control Center**
EOF

    echo -e "${GREEN}✅ Report generated: $report_file${NC}"
}

show_help() {
    echo -e "${CYAN}🤖 AI Agents Control Center - Usage Guide${NC}"
    echo ""
    echo "Commands:"
    echo "  integrations [cmd]    - Launch Integrations Manager"
    echo "  ceo [cmd]            - Launch Grok CEO Agent"
    echo "  communications [cmd]  - Launch Communications Manager"
    echo "  cursor [cmd]         - Launch Cursor AI Agent"
    echo "  cloud [cmd]          - Deploy to Google Cloud Shell"
    echo "  coordinate           - Run agent coordination demo"
    echo "  status               - Show all agent status"
    echo "  report               - Generate deployment report"
    echo "  check                - Check dependencies"
    echo "  help                 - Show this help"
    echo ""
    echo "Examples:"
    echo "  ./launch_ai_agents.sh integrations status"
    echo "  ./launch_ai_agents.sh ceo report"
    echo "  ./launch_ai_agents.sh communications alert high 'System update'"
    echo "  ./launch_ai_agents.sh cursor start"
    echo "  ./launch_ai_agents.sh cloud deploy"
    echo "  ./launch_ai_agents.sh coordinate"
    echo ""
}

# Main execution
main() {
    print_banner
    
    if [ $# -eq 0 ]; then
        show_agent_status
        echo ""
        echo -e "${YELLOW}💡 Use './launch_ai_agents.sh help' for usage guide${NC}"
        return 0
    fi
    
    case "${1:-}" in
        "integrations")
            launch_integrations_manager "$@"
            ;;
        "ceo")
            launch_grok_ceo "$@"
            ;;
        "communications")
            launch_communications_manager "$@"
            ;;
        "cursor")
            launch_cursor_ai "$@"
            ;;
        "cloud")
            deploy_to_cloud "$@"
            ;;
        "coordinate")
            run_agent_coordination
            ;;
        "status")
            show_agent_status
            ;;
        "report")
            generate_deployment_report
            ;;
        "check")
            check_dependencies
            ;;
        "help"|"--help"|"-h")
            show_help
            ;;
        *)
            echo -e "${RED}❌ Unknown command: $1${NC}"
            echo ""
            show_help
            ;;
    esac
}

# Make sure we can handle interrupts gracefully
trap 'echo -e "\n${YELLOW}👋 AI Agents Control Center terminated${NC}"; exit 0' INT

# Run main function
main "$@"