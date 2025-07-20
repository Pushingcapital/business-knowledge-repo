# Business Knowledge Repository

---
**Created:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")  
**Version:** 1.0.0  
---

## Overview
This repository serves as the central knowledge base for all business operations, decisions, and insights. Every entry is timestamped to the second for complete audit trail and historical context.

## Repository Structure

### 📋 `/processes`
Standard operating procedures, workflows, and repeatable business processes.

### 💡 `/insights` 
Market research, competitor analysis, customer feedback, and strategic insights.

### ⚖️ `/decisions`
Decision logs with context, rationale, stakeholders involved, and outcomes.

### 📄 `/templates`
Reusable documents, contracts, presentations, and standardized formats.

### 🤝 `/meetings`
Important meeting notes, action items, and follow-up documentation.

### 🚀 `/projects`
Project documentation, status updates, post-mortems, and lessons learned.

### 🔧 `/scripts`
Automation tools and utilities for timestamp management and data sync.

## Quick Start

### Create New Documents
```bash
# Navigate to repository
cd /Users/emmanuelhaddad/Downloads/business-knowledge-repo

# Make scripts executable
chmod +x scripts/*.sh

# Create new decision document
./scripts/new_entry.sh decision pricing-strategy "Q4 Pricing Strategy"

# Create new meeting notes
./scripts/new_entry.sh meeting client-review "Weekly Client Review"
```

### Process AI Conversations
```bash
# Find conversation files
./scripts/process_conversations.sh find-conversations

# Process Claude export
./scripts/process_conversations.sh process-claude /path/to/claude-export.json

# Process Grok report
./scripts/process_conversations.sh process-grok /path/to/grok-report.pdf
```

## Best Practices

1. **Always timestamp to the second** - Use provided scripts
2. **Link related documents** - Reference Airtable records and other files
3. **Tag consistently** - Use standardized tags for easy searching
4. **Commit with context** - Explain the "why" behind every change

---
**Repository Status:** Operational
