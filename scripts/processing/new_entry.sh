#!/bin/bash

# Business Knowledge Repository - New Entry Script
# Creates a new timestamped document with proper headers

# Get current UTC timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
DATE_ONLY=$(date -u +"%Y-%m-%d")

# Function to display usage
usage() {
    echo "Usage: $0 <type> <filename> [title]"
    echo "Types: process, insight, decision, meeting, project"
    echo "Example: $0 decision quarterly-pricing-strategy 'Q3 Pricing Strategy Decision'"
    exit 1
}

# Check arguments
if [ $# -lt 2 ]; then
    usage
fi

TYPE=$1
FILENAME=$2
TITLE=${3:-$FILENAME}

# Validate type
case $TYPE in
    process|insight|decision|meeting|project)
        ;;
    *)
        echo "Error: Invalid type. Must be process, insight, decision, meeting, or project"
        usage
        ;;
esac

# Create filename with date prefix
FULL_FILENAME="${DATE_ONLY}_${FILENAME}.md"
FILEPATH="${TYPE}s/${FULL_FILENAME}"

# Check if file already exists
if [ -f "$FILEPATH" ]; then
    echo "Error: File $FILEPATH already exists"
    exit 1
fi

# Create the document with timestamp header
cat > "$FILEPATH" << EOF
# $TITLE

---
**Created:** $TIMESTAMP  
**Last Updated:** $TIMESTAMP  
**Type:** $TYPE  
**Author:** $(git config user.name 2>/dev/null || echo "Emmanuel Haddad")  
**Tags:** [$TYPE]  
---

## Summary
Brief description of this $TYPE...

## Details
Detailed information...

## Context
Background and reasoning...

## Stakeholders
- [ ] Person 1
- [ ] Person 2

## Action Items
- [ ] Item 1
- [ ] Item 2

## Follow-up
Next steps and timeline...

---
**Document ID:** ${DATE_ONLY}_${FILENAME}  
**Created:** $TIMESTAMP
EOF

echo "✅ Created new $TYPE document: $FILEPATH"
echo "📝 Edit with: vim $FILEPATH"
echo "🔗 Commit with: git add $FILEPATH && git commit -m '[$TIMESTAMP] $TYPE: $TITLE'"

# Optionally open in default editor
read -p "Open in editor now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    ${EDITOR:-vim} "$FILEPATH"
fi
