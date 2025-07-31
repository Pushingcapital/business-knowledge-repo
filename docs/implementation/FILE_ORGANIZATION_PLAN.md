# File Organization Plan

## Current State Analysis

### 🗂️ **Root Directory Issues**
- 18 files scattered in root directory
- Mixed file types: Python scripts, JSON configs, shell scripts, JS files
- Documentation files mixed with configuration files
- No clear separation of concerns

### 📁 **Directory Structure Issues**
- Duplicate structures: `business_repo_knowledge` vs `organized`
- Inconsistent naming conventions
- Scripts in multiple locations
- Missing standardized directory structure

---

## 🎯 **Target Organization Structure**

```
/workspace/
├── 📄 README.md
├── 📄 LICENSE
├── 📄 .gitignore
├── 
├── 📁 config/                     # All configuration files
│   ├── cursor/
│   │   └── .cursor-settings.json
│   ├── integrations/
│   │   ├── make_business_hub.json
│   │   ├── make_credit_strategy.json
│   │   ├── make_vehicle_transport.json
│   │   ├── openphone_make_blueprint.json
│   │   └── slack_make_blueprint.json
│   └── system/
│
├── 📁 scripts/                    # All automation scripts
│   ├── automation/
│   │   ├── airtable_connector.sh
│   │   ├── hubspot_connector.sh
│   │   ├── integration_controller.sh
│   │   └── setup_*.sh files
│   ├── management/
│   │   ├── cursor_business_cli.sh
│   │   ├── make_management_cli.sh
│   │   └── repo_status.sh
│   ├── processing/
│   │   ├── process_conversations.sh
│   │   ├── process_openphone.sh
│   │   └── new_entry.sh
│   └── validation/
│       └── validate_json.py
│
├── 📁 src/                        # Source code
│   ├── api/
│   │   ├── openphone_api.py
│   │   └── slack_bot.py
│   ├── webhooks/
│   │   ├── openphone_webhook.js
│   │   └── slack_webhook.js
│   └── integrations/
│       └── cursor_ai_integration.py
│
├── 📁 docs/                       # All documentation
│   ├── standards/
│   │   ├── JSON_FORMATTING_STANDARDS.md
│   │   └── JSON_IMPLEMENTATION_SUMMARY.md
│   ├── decisions/
│   │   └── 2025-07-20_ai-conversation-system.md
│   ├── insights/
│   │   ├── 2025-07-20_conversation-insights-*.md
│   │   ├── 2025-07-20_grok4-implementation.md
│   │   ├── 2025-07-20_hubspot-analysis.md
│   │   └── integration-*.md files
│   └── implementation/
│       └── FILE_ORGANIZATION_PLAN.md
│
├── 📁 business/                   # Business data and configurations
│   ├── agents/
│   │   ├── communications_manager.json
│   │   └── profiles/
│   ├── finance/
│   │   └── finance_lead_profile.json
│   ├── escalations/
│   │   └── admin_escalation.json
│   ├── services/
│   │   ├── credit_strategy/
│   │   └── vehicle_transport/
│   └── communications/
│
├── 📁 system/                     # System configurations and data
│   ├── memory/
│   │   └── agent_knowledge_base.json
│   ├── deployments/
│   │   └── cloud_deployment_manifest.json
│   ├── databases/
│   ├── security/
│   ├── logs/
│   └── monitoring/
│
└── 📁 data/                      # Data storage
    ├── contacts/
    │   └── contacts.json
    ├── volatile/
    └── exports/
```

---

## 🚀 **Implementation Steps**

### Phase 1: Create Directory Structure
1. Create main directories: `config/`, `src/`, `docs/`, `business/`, `system/`, `data/`
2. Create subdirectories with specific purposes
3. Ensure proper permissions

### Phase 2: Move Configuration Files
1. Move JSON configs to `config/integrations/`
2. Move `.cursor-settings.json` to `config/cursor/`
3. Update any references

### Phase 3: Organize Scripts
1. Categorize scripts by purpose
2. Move to appropriate subdirectories in `scripts/`
3. Update execution permissions

### Phase 4: Organize Source Code
1. Move Python API files to `src/api/`
2. Move webhook files to `src/webhooks/`
3. Move integration code to `src/integrations/`

### Phase 5: Consolidate Documentation
1. Move all `.md` files to `docs/` with proper categorization
2. Organize by type: standards, decisions, insights, implementation

### Phase 6: Merge Business Data
1. Consolidate `business_repo_knowledge/` and relevant `organized/` files
2. Create unified `business/` structure
3. Remove duplicate directories

### Phase 7: System Data Organization
1. Move system files to `system/`
2. Organize by function: memory, deployments, databases, etc.

### Phase 8: Data Management
1. Move contact and data files to `data/`
2. Create proper data categorization

### Phase 9: Cleanup
1. Remove empty directories
2. Update file references
3. Validate all moves completed successfully

---

## 📋 **File Mapping**

### Root Files → New Locations
```
cursor_ai_integration.py        → src/integrations/
cursor_business_cli.sh          → scripts/management/
.cursor-settings.json           → config/cursor/
make_business_hub.json          → config/integrations/
make_credit_strategy.json       → config/integrations/
make_management_cli.sh          → scripts/management/
make_vehicle_transport.json     → config/integrations/
openphone_api.py               → src/api/
openphone_make_blueprint.json  → config/integrations/
openphone_webhook.js           → src/webhooks/
slack_bot.py                   → src/api/
slack_make_blueprint.json      → config/integrations/
slack_webhook.js               → src/webhooks/
JSON_FORMATTING_STANDARDS.md   → docs/standards/
JSON_IMPLEMENTATION_SUMMARY.md → docs/standards/
```

### Directory Consolidation
```
business_repo_knowledge/        → business/
organized/ai_memory/           → system/memory/
organized/deployments/         → system/deployments/
organized/people/              → data/contacts/
insights/                      → docs/insights/
decisions/                     → docs/decisions/
```

---

## ✅ **Success Criteria**

1. ✅ **Clean Root Directory**: Only essential files (README, LICENSE, .gitignore)
2. ✅ **Logical Grouping**: Files grouped by purpose and type
3. ✅ **Consistent Naming**: Standardized directory and file names
4. ✅ **No Duplicates**: Single source of truth for all files
5. ✅ **Proper Permissions**: Executable scripts, readable configs
6. ✅ **Updated References**: All file paths updated correctly
7. ✅ **Validation**: All files accounted for and functional

---

## 🔧 **Tools & Commands**

### Validation Commands
```bash
# Count files before/after
find /workspace -type f | wc -l

# Validate JSON files
python3 scripts/validation/validate_json.py validate

# Check for broken references
grep -r "scripts/" config/ src/ docs/ business/ system/ data/

# Verify executable permissions
find scripts/ -name "*.sh" -not -executable
```

---

**Implementation Priority**: High  
**Estimated Time**: 1-2 hours  
**Risk Level**: Low (with proper validation)  
**Dependencies**: None  

**Next Action**: Begin Phase 1 - Create Directory Structure