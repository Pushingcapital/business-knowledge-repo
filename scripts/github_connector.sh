#!/bin/bash

# GitHub Connector Script for Business Knowledge Repository
# Created by: Claude AI Agent
# Last updated: $(date '+%Y-%m-%d %H:%M:%S')

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
CONFIG_FILE=".env"
REPO_NAME="Pushingcapital/business-knowledge-repo"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo -e "${CYAN}🐙 GitHub Connector for Business Knowledge Repository${NC}"
echo -e "${CYAN}=================================================${NC}"
echo ""

# Function to setup GitHub authentication
setup_github() {
    echo -e "${BLUE}🔧 Setting up GitHub connection...${NC}"
    echo ""
    
    if [ ! -f "$CONFIG_FILE" ]; then
        echo "# Business Knowledge Repository - Environment Configuration" > "$CONFIG_FILE"
        echo "# Created: $TIMESTAMP" >> "$CONFIG_FILE"
        echo "" >> "$CONFIG_FILE"
    fi
    
    echo "GitHub repository: https://github.com/$REPO_NAME"
    echo ""
    
    # Update git remote with token
    if [ -f "$CONFIG_FILE" ] && grep -q "GITHUB_TOKEN" "$CONFIG_FILE"; then
        TOKEN=$(grep "GITHUB_TOKEN" "$CONFIG_FILE" | cut -d'=' -f2)
        git remote set-url origin "https://x-access-token:$TOKEN@github.com/$REPO_NAME.git"
        echo -e "${GREEN}✅ GitHub authentication configured${NC}"
    else
        echo -e "${RED}❌ GitHub token not found in .env file${NC}"
        return 1
    fi
}

# Function to test GitHub connection
test_connection() {
    echo -e "${BLUE}🧪 Testing GitHub connection...${NC}"
    echo ""
    
    if git fetch origin > /dev/null 2>&1; then
        echo -e "${GREEN}✅ GitHub connection successful${NC}"
        echo -e "📍 Current branch: $(git branch --show-current)"
        echo -e "🔄 Last commit: $(git log -1 --pretty=format:'%h - %s (%cr)')"
    else
        echo -e "${RED}❌ GitHub connection failed${NC}"
        return 1
    fi
}

# Function to sync repository
sync_repo() {
    echo -e "${BLUE}🔄 Syncing with GitHub...${NC}"
    echo ""
    
    # Check for local changes
    if [ -n "$(git status --porcelain)" ]; then
        echo -e "${YELLOW}⚠️  Local changes detected${NC}"
        echo "Files to be committed:"
        git status --short
        echo ""
        
        read -p "Commit message: " commit_msg
        if [ -n "$commit_msg" ]; then
            git add .
            git commit -m "$commit_msg"
            echo -e "${GREEN}✅ Changes committed${NC}"
        else
            echo -e "${YELLOW}⚠️  No commit message provided, skipping commit${NC}"
            return 1
        fi
    fi
    
    # Push to GitHub
    if git push origin $(git branch --show-current); then
        echo -e "${GREEN}✅ Successfully synced with GitHub${NC}"
    else
        echo -e "${RED}❌ Failed to sync with GitHub${NC}"
        return 1
    fi
}

# Function to show repository status
show_status() {
    echo -e "${CYAN}📊 Repository Status${NC}"
    echo -e "${CYAN}==================${NC}"
    echo ""
    echo -e "🔗 Remote URL: $(git remote get-url origin | sed 's/x-access-token:[^@]*@/x-access-token:***@/')"
    echo -e "🌿 Current branch: $(git branch --show-current)"
    echo -e "📝 Last commit: $(git log -1 --pretty=format:'%h - %s (%cr)')"
    echo -e "📍 Repository: https://github.com/$REPO_NAME"
    echo ""
    
    if [ -n "$(git status --porcelain)" ]; then
        echo -e "${YELLOW}⚠️  Uncommitted changes:${NC}"
        git status --short
    else
        echo -e "${GREEN}✅ Working tree clean${NC}"
    fi
}

# Main menu
case "${1:-menu}" in
    "setup")
        setup_github
        ;;
    "test")
        test_connection
        ;;
    "sync")
        sync_repo
        ;;
    "status")
        show_status
        ;;
    "menu")
        echo "Available commands:"
        echo "  setup  - Configure GitHub authentication"
        echo "  test   - Test GitHub connection"
        echo "  sync   - Sync repository with GitHub"
        echo "  status - Show repository status"
        echo ""
        echo "Usage: $0 [setup|test|sync|status]"
        ;;
    *)
        echo -e "${RED}❌ Unknown command: $1${NC}"
        echo "Run '$0 menu' for available commands"
        exit 1
        ;;
esac