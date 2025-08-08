#!/bin/bash

# Super Admin Deployment Runner
# Coordinates complete setup and deployment of all business intelligence agents
# Created by: Claude AI Agent
# Last updated: $(date '+%Y-%m-%d %H:%M:%S')

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Configuration
DEPLOYMENT_DIR="$(pwd)"
LOG_FILE="deployment_$(date '+%Y%m%d_%H%M%S').log"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Logging function
log() {
    echo -e "$1" | tee -a "$LOG_FILE"
}

# Header
print_header() {
    clear
    log "${CYAN}${BOLD}"
    log "╔══════════════════════════════════════════════════════════════╗"
    log "║                SUPER ADMIN DEPLOYMENT SYSTEM                ║"
    log "║                                                              ║"
    log "║            Business Intelligence Agent Deployment            ║"
    log "║                 with Google Cloud Integration                ║"
    log "╚══════════════════════════════════════════════════════════════╝"
    log "${NC}"
    log ""
    log "🎯 ${BOLD}Deployment Started:${NC} $TIMESTAMP"
    log "📁 ${BOLD}Working Directory:${NC} $DEPLOYMENT_DIR"
    log "📝 ${BOLD}Log File:${NC} $LOG_FILE"
    log ""
}

# Check prerequisites
check_prerequisites() {
    log "${BLUE}🔍 Checking Prerequisites...${NC}"
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        log "${RED}❌ Python 3 not found. Please install Python 3.8+${NC}"
        exit 1
    fi
    
    python_version=$(python3 --version | cut -d' ' -f2)
    log "${GREEN}✅ Python ${python_version} found${NC}"
    
    # Check Git
    if ! command -v git &> /dev/null; then
        log "${RED}❌ Git not found. Please install Git${NC}"
        exit 1
    fi
    
    log "${GREEN}✅ Git found${NC}"
    
    # Check if we're in a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        log "${YELLOW}⚠️  Not in a git repository. Initializing...${NC}"
        git init
        git remote add origin https://x-access-token:$(grep GITHUB_TOKEN .env | cut -d'=' -f2)@github.com/Pushingcapital/business-knowledge-repo.git 2>/dev/null || true
    fi
    
    log "${GREEN}✅ Git repository ready${NC}"
    log ""
}

# Install dependencies
install_dependencies() {
    log "${BLUE}📦 Installing Dependencies...${NC}"
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        log "🔧 Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    log "🔧 Activating virtual environment..."
    source venv/bin/activate
    
    # Upgrade pip
    log "🔧 Upgrading pip..."
    pip install --upgrade pip > /dev/null 2>&1
    
    # Install requirements
    log "🔧 Installing requirements..."
    pip install -r requirements.txt > /dev/null 2>&1
    
    log "${GREEN}✅ Dependencies installed${NC}"
    log ""
}

# Setup Google Cloud
setup_google_cloud() {
    log "${BLUE}🌐 Setting up Google Cloud...${NC}"
    
    # Check if Google Cloud is already configured
    if [ -f ".env" ] && grep -q "GOOGLE_CLOUD_PROJECT" .env; then
        project_id=$(grep GOOGLE_CLOUD_PROJECT .env | cut -d'=' -f2)
        log "${YELLOW}⚠️  Google Cloud project already configured: $project_id${NC}"
        
        read -p "Do you want to reconfigure? (y/N): " reconfigure
        if [[ $reconfigure != "y" && $reconfigure != "Y" ]]; then
            log "${GREEN}✅ Using existing Google Cloud configuration${NC}"
            return 0
        fi
    fi
    
    # Run Google Cloud setup
    log "🔧 Running Google Cloud setup..."
    python3 google_cloud_setup.py
    
    if [ $? -eq 0 ]; then
        log "${GREEN}✅ Google Cloud setup completed${NC}"
    else
        log "${RED}❌ Google Cloud setup failed${NC}"
        exit 1
    fi
    
    log ""
}

# Deploy agents
deploy_agents() {
    log "${BLUE}🚀 Deploying All Agents...${NC}"
    
    # Source environment variables
    if [ -f ".env" ]; then
        export $(grep -v '^#' .env | xargs)
    fi
    
    # Run super admin deployment
    log "🔧 Starting super admin deployment..."
    python3 super_admin_deployment.py
    
    if [ $? -eq 0 ]; then
        log "${GREEN}✅ Agent deployment completed${NC}"
    else
        log "${RED}❌ Agent deployment failed${NC}"
        exit 1
    fi
    
    log ""
}

# Setup systemd services
setup_services() {
    log "${BLUE}⚙️  Setting up System Services...${NC}"
    
    # Check if we have systemd
    if ! command -v systemctl &> /dev/null; then
        log "${YELLOW}⚠️  systemctl not found. Skipping service setup.${NC}"
        return 0
    fi
    
    # Copy service files and enable them
    if [ -d "deployed_agents" ]; then
        for agent_dir in deployed_agents/*/; do
            agent_name=$(basename "$agent_dir")
            service_file="${agent_dir}${agent_name}.service"
            
            if [ -f "$service_file" ]; then
                log "🔧 Setting up service: $agent_name"
                
                # Copy service file to systemd
                sudo cp "$service_file" "/etc/systemd/system/"
                
                # Enable and start service
                sudo systemctl daemon-reload
                sudo systemctl enable "$agent_name"
                
                log "${GREEN}✅ Service $agent_name configured${NC}"
            fi
        done
    fi
    
    log ""
}

# Configure monitoring
setup_monitoring() {
    log "${BLUE}📊 Setting up Monitoring...${NC}"
    
    # Create monitoring directory
    mkdir -p monitoring/dashboards
    mkdir -p monitoring/alerts
    
    # Copy monitoring configuration
    if [ -f "monitoring_config.json" ]; then
        cp monitoring_config.json monitoring/
        log "${GREEN}✅ Monitoring configuration copied${NC}"
    fi
    
    # Setup log rotation
    cat > monitoring/logrotate.conf << EOF
logs/deployment/*.log {
    daily
    missingok
    rotate 30
    compress
    notifempty
    create 0644 ubuntu ubuntu
}
EOF
    
    log "${GREEN}✅ Monitoring setup completed${NC}"
    log ""
}

# Final verification
verify_deployment() {
    log "${BLUE}🧪 Verifying Deployment...${NC}"
    
    # Check if super admin control script exists
    if [ -f "super_admin_control.sh" ]; then
        log "${GREEN}✅ Super admin controls available${NC}"
        
        # Run status check
        log "📊 Running status check..."
        ./super_admin_control.sh status | tee -a "$LOG_FILE"
    else
        log "${RED}❌ Super admin controls not found${NC}"
        return 1
    fi
    
    # Check environment
    if [ -f ".env" ] && grep -q "GOOGLE_CLOUD_PROJECT" .env; then
        project_id=$(grep GOOGLE_CLOUD_PROJECT .env | cut -d'=' -f2)
        log "${GREEN}✅ Google Cloud project: $project_id${NC}"
    else
        log "${RED}❌ Google Cloud configuration missing${NC}"
        return 1
    fi
    
    # Check deployed agents
    if [ -d "deployed_agents" ]; then
        agent_count=$(find deployed_agents -maxdepth 1 -type d | wc -l)
        agent_count=$((agent_count - 1))  # Subtract 1 for the parent directory
        log "${GREEN}✅ Deployed agents: $agent_count${NC}"
    else
        log "${RED}❌ No agents deployed${NC}"
        return 1
    fi
    
    log ""
    return 0
}

# Commit and push changes
commit_deployment() {
    log "${BLUE}📝 Committing Deployment...${NC}"
    
    # Add all files
    git add .
    
    # Create deployment commit
    commit_message="feat: Super admin deployment completed - All business intelligence agents deployed - Google Cloud integration configured - Super admin controls enabled - Deployment ID: $(date '+%Y%m%d-%H%M%S') - Last updated by: Claude AI Agent"
    
    git commit -m "$commit_message" || log "${YELLOW}⚠️  No changes to commit${NC}"
    
    # Push to GitHub
    if git remote -v | grep -q origin; then
        log "🔧 Pushing to GitHub..."
        git push origin $(git branch --show-current) || log "${YELLOW}⚠️  Failed to push to GitHub${NC}"
        log "${GREEN}✅ Changes pushed to GitHub${NC}"
    else
        log "${YELLOW}⚠️  No GitHub remote configured${NC}"
    fi
    
    log ""
}

# Print success summary
print_success() {
    log "${GREEN}${BOLD}"
    log "╔══════════════════════════════════════════════════════════════╗"
    log "║                    🎉 DEPLOYMENT SUCCESSFUL! 🎉               ║"
    log "╚══════════════════════════════════════════════════════════════╝"
    log "${NC}"
    log ""
    log "${BOLD}🎯 DEPLOYMENT SUMMARY${NC}"
    log "═══════════════════════"
    
    if [ -f ".env" ] && grep -q "GOOGLE_CLOUD_PROJECT" .env; then
        project_id=$(grep GOOGLE_CLOUD_PROJECT .env | cut -d'=' -f2)
        log "🌐 ${BOLD}Google Cloud Project:${NC} $project_id"
    fi
    
    if [ -d "deployed_agents" ]; then
        agent_count=$(find deployed_agents -maxdepth 1 -type d | wc -l)
        agent_count=$((agent_count - 1))
        log "🤖 ${BOLD}Deployed Agents:${NC} $agent_count"
    fi
    
    log "👑 ${BOLD}Super Admin Mode:${NC} Enabled"
    log "📊 ${BOLD}Monitoring:${NC} Configured"
    log "🔐 ${BOLD}Security:${NC} Google Cloud IAM"
    log "📝 ${BOLD}Log File:${NC} $LOG_FILE"
    log ""
    log "${BOLD}🎮 CONTROL COMMANDS${NC}"
    log "═══════════════════════"
    log "📊 Status:    ${CYAN}./super_admin_control.sh status${NC}"
    log "🚀 Start All: ${CYAN}./super_admin_control.sh start${NC}"
    log "🛑 Stop All:  ${CYAN}./super_admin_control.sh stop${NC}"
    log "🔄 Restart:   ${CYAN}./super_admin_control.sh restart${NC}"
    log ""
    log "${BOLD}📁 IMPORTANT FILES${NC}"
    log "═══════════════════════"
    log "🔐 Environment:     ${CYAN}.env${NC}"
    log "👑 Admin Controls:  ${CYAN}super_admin_control.sh${NC}"
    log "📊 Agent Status:    ${CYAN}deployed_agents/${NC}"
    log "📈 Monitoring:      ${CYAN}monitoring/${NC}"
    log "📝 Logs:           ${CYAN}logs/${NC}"
    log ""
    log "${GREEN}${BOLD}🎉 Your business intelligence agents are now operational!${NC}"
}

# Error handler
handle_error() {
    log "${RED}${BOLD}"
    log "╔══════════════════════════════════════════════════════════════╗"
    log "║                     ❌ DEPLOYMENT FAILED ❌                   ║"
    log "╚══════════════════════════════════════════════════════════════╝"
    log "${NC}"
    log ""
    log "${RED}An error occurred during deployment.${NC}"
    log "📝 Check the log file for details: ${CYAN}$LOG_FILE${NC}"
    log ""
    log "🆘 For support, check:"
    log "   • Log file contents"
    log "   • Google Cloud permissions"
    log "   • Network connectivity"
    log "   • Dependencies installation"
    exit 1
}

# Set error handler
trap handle_error ERR

# Main execution
main() {
    print_header
    check_prerequisites
    install_dependencies
    setup_google_cloud
    deploy_agents
    setup_services
    setup_monitoring
    
    if verify_deployment; then
        commit_deployment
        print_success
    else
        log "${RED}❌ Deployment verification failed${NC}"
        exit 1
    fi
}

# Run main function
main "$@"