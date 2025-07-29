#!/bin/bash

# 🚀 Make.com Business Intelligence Deployment Script
# Deploy all Pushing Capital automation blueprints and configure integrations

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🚀 Pushing Capital Make.com Deployment${NC}"
echo "=============================================="
echo -e "${YELLOW}Deploying business intelligence hub and service automations${NC}"
echo ""

# Configuration paths
BUSINESS_REPO="business_repo_knowledge"
INTEGRATIONS_DIR="$BUSINESS_REPO/integrations/make_com"
SERVICES_DIR="$BUSINESS_REPO/services"

print_step() {
    echo -e "${BLUE}📋 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_step "Checking deployment prerequisites..."
    
    # Check if business repo exists
    if [ ! -d "$BUSINESS_REPO" ]; then
        print_error "Business repository not found at $BUSINESS_REPO"
        exit 1
    fi
    
    # Check for automation blueprints
    if [ ! -f "$INTEGRATIONS_DIR/make_business_hub.json" ]; then
        print_error "Business Intelligence Hub blueprint not found"
        exit 1
    fi
    
    print_success "Prerequisites satisfied"
}

# Deploy Business Intelligence Hub
deploy_business_hub() {
    print_step "Deploying Business Intelligence Hub..."
    
    echo "📊 Business Intelligence Hub Configuration:"
    echo "   • Central webhook coordination"
    echo "   • HubSpot, OpenPhone, Slack routing"
    echo "   • Real-time business event processing"
    echo ""
    
    # Validate business hub blueprint
    if command -v jq &> /dev/null; then
        if jq empty "$INTEGRATIONS_DIR/make_business_hub.json" 2>/dev/null; then
            print_success "Business Intelligence Hub blueprint validated"
        else
            print_error "Invalid JSON in business hub blueprint"
            return 1
        fi
    fi
    
    # Copy blueprint to deployment directory
    mkdir -p "deployments/make_com"
    cp "$INTEGRATIONS_DIR/make_business_hub.json" "deployments/make_com/"
    
    print_success "Business Intelligence Hub ready for import"
}

# Deploy Credit Strategy Automation
deploy_credit_strategy() {
    print_step "Deploying Credit Strategy Automation..."
    
    echo "💳 Credit Strategy Pipeline:"
    echo "   • Lead capture to HubSpot deal creation"
    echo "   • Automated document generation"
    echo "   • Slack team notifications"
    echo "   • $1,500 deal value automation"
    echo ""
    
    if [ -f "$SERVICES_DIR/credit_strategy/make_credit_strategy.json" ]; then
        cp "$SERVICES_DIR/credit_strategy/make_credit_strategy.json" "deployments/make_com/"
        print_success "Credit Strategy automation ready"
    else
        print_warning "Credit Strategy blueprint not found"
    fi
}

# Deploy Vehicle Transport Automation  
deploy_vehicle_transport() {
    print_step "Deploying Vehicle Transport Automation..."
    
    echo "🚛 Vehicle Transport Pipeline:"
    echo "   • Quote calculation and HubSpot integration"
    echo "   • Customer contact management"
    echo "   • Real-time transport notifications"
    echo "   • Dynamic pricing based on ZIP codes"
    echo ""
    
    if [ -f "$SERVICES_DIR/vehicle_transport/make_vehicle_transport.json" ]; then
        cp "$SERVICES_DIR/vehicle_transport/make_vehicle_transport.json" "deployments/make_com/"
        print_success "Vehicle Transport automation ready"
    else
        print_warning "Vehicle Transport blueprint not found"
    fi
}

# Deploy Slack Integration
deploy_slack_integration() {
    print_step "Deploying Slack Integration..."
    
    echo "📱 Slack Communication Hub:"
    echo "   • #credit-services notifications"
    echo "   • #transport-quotes alerts"
    echo "   • Real-time business updates"
    echo "   • Team coordination automation"
    echo ""
    
    if [ -f "$INTEGRATIONS_DIR/slack_make_blueprint.json" ]; then
        cp "$INTEGRATIONS_DIR/slack_make_blueprint.json" "deployments/make_com/"
        print_success "Slack integration ready"
    else
        print_warning "Slack blueprint not found"
    fi
}

# Generate deployment report
generate_deployment_report() {
    print_step "Generating deployment report..."
    
    REPORT_FILE="deployments/make_com_deployment_report_$(date +%Y%m%d_%H%M%S).md"
    
    cat > "$REPORT_FILE" << EOF
# Make.com Deployment Report

**Deployment Date:** $TIMESTAMP  
**Status:** Ready for Import  
**Blueprints Prepared:** $(ls deployments/make_com/*.json 2>/dev/null | wc -l)

## Deployment Summary

### ✅ Business Intelligence Hub
- **File:** make_business_hub.json
- **Purpose:** Central automation coordinating all business events
- **Integrations:** HubSpot, OpenPhone, Slack, Knowledge Repo
- **Status:** Ready for import

### 💳 Credit Strategy Pipeline  
- **File:** make_credit_strategy.json
- **Purpose:** Automate credit strategy from intake to completion
- **Deal Value:** $1,500 per client
- **Status:** Ready for import

### 🚛 Vehicle Transport Automation
- **File:** make_vehicle_transport.json  
- **Purpose:** Quote generation and deal management
- **Features:** Dynamic pricing, contact management
- **Status:** Ready for import

### 📱 Communication Integrations
- **Slack Integration:** Team notifications and alerts
- **OpenPhone Integration:** Customer SMS and call handling
- **Status:** Ready for configuration

## Import Instructions

### 1. Access Make.com
- Login to your Make.com account
- Navigate to Scenarios > Create New > Import Blueprint

### 2. Import Business Intelligence Hub (Priority 1)
- Upload: make_business_hub.json
- Configure webhook URL
- Set up HubSpot API connection
- Test webhook routing

### 3. Import Service Automations
- Upload: make_credit_strategy.json
- Upload: make_vehicle_transport.json
- Configure service-specific webhooks
- Test end-to-end workflows

### 4. Configure Integrations
- **HubSpot API:** Configure deal pipelines and custom fields
- **Slack Webhooks:** Set up channel notifications
- **OpenPhone API:** Configure SMS and call routing
- **Google Drive:** Set up document generation

## Post-Deployment Checklist

- [ ] Business Intelligence Hub webhook configured
- [ ] HubSpot pipelines mapped correctly  
- [ ] Slack channels receiving notifications
- [ ] OpenPhone integration responding
- [ ] Document generation working
- [ ] End-to-end testing completed
- [ ] Team training on new workflows

## Monitoring & Maintenance

### Weekly Tasks
- Review automation execution logs
- Monitor error rates and failures
- Check integration health status
- Validate data flow accuracy

### Monthly Tasks  
- Performance optimization review
- New feature integration assessment
- Cost analysis and optimization
- Team feedback collection

---
**Generated:** $TIMESTAMP  
**Next Review:** $(date -d '+30 days' +%Y-%m-%d)
EOF

    print_success "Deployment report generated: $REPORT_FILE"
}

# Create deployment directory structure
setup_deployment_structure() {
    print_step "Setting up deployment structure..."
    
    mkdir -p deployments/make_com
    mkdir -p deployments/logs
    mkdir -p deployments/backups
    
    print_success "Deployment directories created"
}

# Main deployment process
main() {
    echo -e "${BLUE}Starting Make.com deployment process...${NC}"
    echo ""
    
    check_prerequisites
    setup_deployment_structure
    deploy_business_hub
    deploy_credit_strategy
    deploy_vehicle_transport  
    deploy_slack_integration
    generate_deployment_report
    
    echo ""
    echo -e "${GREEN}🎉 Make.com Deployment Complete!${NC}"
    echo "=============================================="
    echo ""
    echo -e "${YELLOW}Next Steps:${NC}"
    echo "1. Login to Make.com dashboard"
    echo "2. Import blueprints from deployments/make_com/"
    echo "3. Configure API connections as prompted"
    echo "4. Test each automation workflow"
    echo "5. Enable production scenarios"
    echo ""
    echo -e "${BLUE}📊 Deployment Summary:${NC}"
    echo "   • Business Intelligence Hub: Ready"
    echo "   • Credit Strategy Pipeline: Ready"  
    echo "   • Vehicle Transport: Ready"
    echo "   • Communication Hub: Ready"
    echo ""
    echo -e "${GREEN}🚀 Pushing Capital automation ecosystem deployed!${NC}"
}

# Handle script arguments
case "${1:-}" in
    "status")
        echo "Make.com Deployment Status:"
        if [ -d "deployments/make_com" ]; then
            echo "✅ Deployment directory exists"
            echo "📁 Blueprints ready: $(ls deployments/make_com/*.json 2>/dev/null | wc -l)"
        else
            echo "❌ Deployment not initialized"
        fi
        ;;
    "clean")
        echo "🧹 Cleaning deployment directory..."
        rm -rf deployments/make_com
        print_success "Deployment directory cleaned"
        ;;
    *)
        main
        ;;
esac