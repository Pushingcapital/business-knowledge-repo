# JSON Formatting Standards for Business Knowledge Repository

## Overview
This document establishes consistent JSON formatting standards across all files in the business-knowledge-repo project. Proper formatting ensures readability, maintainability, and automated processing capability.

## General Formatting Rules

### 1. Indentation and Spacing
- **Indentation**: Use 2 spaces (no tabs)
- **Object Properties**: One property per line
- **Array Elements**: One element per line for complex objects
- **No trailing commas**: Ensure JSON is valid

### 2. Property Ordering
For consistency, arrange properties in this order:
1. `id` (if present)
2. `name` / `title`
3. `description`
4. `timestamp` / `created_at` / `updated_at`
5. `version`
6. Core data properties
7. `metadata` (always last)

### 3. Timestamp Format
All timestamps must use ISO 8601 UTC format:
```json
{
  "timestamp": "2025-01-30T15:30:45Z",
  "created_at": "2025-01-30T15:30:45Z",
  "updated_at": "2025-01-30T15:30:45Z"
}
```

### 4. Required Metadata
Every JSON file should include a metadata section:
```json
{
  "metadata": {
    "version": "1.0",
    "created_at": "2025-01-30T15:30:45Z",
    "updated_at": "2025-01-30T15:30:45Z",
    "last_modified_by": "Claude AI Assistant",
    "file_type": "configuration|data|blueprint|manifest",
    "encoding": "UTF-8"
  }
}
```

## File-Specific Standards

### Make.com Blueprints (`make_*.json`)
```json
{
  "name": "Descriptive Blueprint Name",
  "description": "Clear description of automation purpose",
  "version": "1.0",
  "flow": [
    {
      "id": 1,
      "module": "webhook:customWebhook",
      "version": 1,
      "parameters": {
        "name": "descriptive_webhook_name"
      },
      "metadata": {
        "designer": {
          "x": 0,
          "y": 0
        }
      }
    }
  ],
  "metadata": {
    "instant": true,
    "version": 1,
    "scenario": {
      "roundtrips": 1,
      "maxErrors": 3,
      "autoCommit": true,
      "sequential": false
    },
    "created_at": "2025-01-30T15:30:45Z",
    "updated_at": "2025-01-30T15:30:45Z"
  }
}
```

### Configuration Files (`.cursor-settings.json`, etc.)
```json
{
  "cursor.ai.enabled": true,
  "cursor.ai.model": "claude-3.5-sonnet",
  "cursor.ai.systemPrompt": "Multi-line strings should be properly escaped",
  "cursor.ai.codebaseContext": [
    "insights/",
    "decisions/",
    "scripts/"
  ],
  "metadata": {
    "version": "1.0",
    "created_at": "2025-01-30T15:30:45Z",
    "updated_at": "2025-01-30T15:30:45Z"
  }
}
```

### Business Data Files
```json
{
  "entity_type": "user|deal|communication|escalation",
  "entity_id": "unique_identifier",
  "name": "Entity Name",
  "description": "Entity description",
  "status": "active|inactive|pending",
  "created_at": "2025-01-30T15:30:45Z",
  "updated_at": "2025-01-30T15:30:45Z",
  "data": {
    // Entity-specific data properties
  },
  "metadata": {
    "version": "1.0",
    "source": "system|user|import",
    "last_modified_by": "Claude AI Assistant"
  }
}
```

### AI Agent Profiles
```json
{
  "agent_id": "unique_agent_identifier",
  "name": "Agent Name",
  "description": "Agent purpose and capabilities",
  "version": "1.0",
  "status": "active|inactive|development",
  "capabilities": [
    "capability1",
    "capability2"
  ],
  "configuration": {
    // Agent-specific configuration
  },
  "memory": {
    // Agent memory structure
  },
  "metadata": {
    "created_at": "2025-01-30T15:30:45Z",
    "updated_at": "2025-01-30T15:30:45Z",
    "last_modified_by": "Claude AI Assistant"
  }
}
```

## Validation Rules

### 1. JSON Syntax
- Valid JSON syntax (use `jq` or online validators)
- No trailing commas
- Proper quote escaping
- Balanced brackets and braces

### 2. Required Fields
- Every file must have a `metadata` section
- Timestamps must be in ISO 8601 UTC format
- Version numbers must be semantic (e.g., "1.0", "2.1.3")

### 3. String Formatting
- Use double quotes for all strings
- Escape special characters properly
- Multi-line strings should use `\n` for line breaks

### 4. Numeric Values
- Use numbers for numeric values (not strings)
- No leading zeros except for decimals
- Use consistent decimal places for monetary values

## File Naming Conventions

### JSON Files
- Use lowercase with underscores: `make_business_hub.json`
- Include date stamps for logs: `active_communications_2025-01-30.json`
- Be descriptive and specific: `finance_lead_profile.json`

### Directory Structure
```
business_repo_knowledge/
├── ai_agents/
│   ├── profiles/
│   └── configurations/
├── communications/
│   ├── active/
│   └── archived/
├── finance/
│   ├── profiles/
│   └── configurations/
└── services/
    ├── credit_strategy/
    └── vehicle_transport/
```

## Automation and Tools

### JSON Validation Script
Create `scripts/validate_json.py` to automatically validate all JSON files:
- Check syntax validity
- Verify required metadata
- Validate timestamp formats
- Ensure property ordering

### Pre-commit Hooks
Set up git pre-commit hooks to:
- Validate JSON syntax
- Format JSON files automatically
- Check for required metadata

## Implementation Checklist

- [ ] Format all root-level JSON files
- [ ] Standardize business_repo_knowledge JSON files
- [ ] Update organized directory JSON files
- [ ] Add metadata to all files
- [ ] Create validation script
- [ ] Set up automated formatting
- [ ] Document any exceptions or special cases

---

**Last Updated:** 2025-01-30T15:30:45Z  
**Version:** 1.0  
**Modified By:** Claude AI Assistant