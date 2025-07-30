#!/bin/bash

# Repository Status Checker
echo "🔍 Business Knowledge Repository Status"
echo "======================================"
echo ""

# Git status
echo "📋 Git Repository Status:"
echo "  Branch: $(git branch --show-current 2>/dev/null || echo 'Not initialized')"
echo "  Remote: $(git remote get-url origin 2>/dev/null || echo 'No remote configured')"
echo "  Last commit: $(git log -1 --format='%h - %s (%cr)' 2>/dev/null || echo 'No commits')"
echo "  Modified files: $(git status --porcelain | wc -l | tr -d ' ')"
echo ""

# Directory structure
echo "📁 Repository Structure:"
find . -type d -not -path "./.git*" | sort | head -20 | sed 's/^/  /'
echo ""

# File counts
echo "📊 Content Statistics:"
echo "  Decisions: $(find decisions/ -name "*.md" 2>/dev/null | wc -l | tr -d ' ')"
echo "  Insights: $(find insights/ -name "*.md" 2>/dev/null | wc -l | tr -d ' ')"
echo "  Meetings: $(find meetings/ -name "*.md" 2>/dev/null | wc -l | tr -d ' ')"
echo "  Projects: $(find projects/ -name "*.md" 2>/dev/null | wc -l | tr -d ' ')"
echo "  Processes: $(find processes/ -name "*.md" 2>/dev/null | wc -l | tr -d ' ')"
echo "  Templates: $(find templates/ -name "*.md" 2>/dev/null | wc -l | tr -d ' ')"
echo "  Scripts: $(find scripts/ -name "*.sh" 2>/dev/null | wc -l | tr -d ' ')"
echo ""

# Recent activity
echo "⏰ Recent Files (Last 24 hours):"
find . -name "*.md" -mtime -1 2>/dev/null | head -10 | sed 's/^/  /'
echo ""

# Security check
echo "🔐 Security Status:"
if [ -f ".gitignore" ]; then
    echo "  ✅ .gitignore present"
else
    echo "  ❌ .gitignore missing"
fi

if grep -q "\.env" .gitignore 2>/dev/null; then
    echo "  ✅ Environment files protected"
else
    echo "  ⚠️  Environment protection needs review"
fi

echo ""
echo "🎯 Next Actions:"
echo "  1. git status - Check for uncommitted changes"
echo "  2. git push - Sync with GitHub (if remote configured)"
echo "  3. ./scripts/new_entry.sh - Create new documents"
echo "  4. ./scripts/process_conversations.sh find-conversations - Find AI conversations"
