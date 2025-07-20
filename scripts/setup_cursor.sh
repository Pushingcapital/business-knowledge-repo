#!/bin/bash

# Cursor AI Integration for Business Knowledge Management
# Creates file-based sync and CLI automation

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "💻 Setting up Cursor AI Integration..."
echo "====================================="
echo ""

# Create Cursor project configuration
create_cursor_config() {
    echo "⚙️ Creating Cursor workspace configuration..."
    
    cat > .cursor-settings.json << 'EOF'
{
  "cursor.ai.enabled": true,
  "cursor.ai.model": "claude-3.5-sonnet",
  "cursor.ai.systemPrompt": "You are a business intelligence assistant for Pushing Capital. You have access to:\n- HubSpot CRM data with 37 active deals worth $57,977\n- 4 business pipelines: Customer ($45,500), Vehicle Transport ($6,500), Credit Analysis, Automation\n- Business knowledge repository with decisions, insights, and processes\n- Real-time conversation processing from Claude and Grok\n\nWhen writing code or documentation:\n1. Always include timestamps in UTC format\n2. Reference relevant HubSpot deal data when applicable\n3. Integrate with existing business-knowledge-repo structure\n4. Consider automation opportunities for vehicle transport and credit services\n5. Link new code to Airtable records when appropriate",
  "cursor.ai.codebaseContext": [
    "insights/",
    "decisions/", 
    "scripts/",
    "README.md"
  ],
  "cursor.ai.rules": [
    "Always use business context from HubSpot analysis",
    "Include proper error handling and logging",
    "Create markdown documentation for all new features",
    "Link code changes to relevant Airtable records",
    "Follow established timestamp format: YYYY-MM-DDTHH:MM:SSZ"
  ]
}
EOF

    echo "✅ Cursor workspace settings created"
}

# Create Cursor AI automation scripts
create_cursor_automation() {
    echo "🤖 Creating Cursor AI automation..."
    
    cat > cursor_ai_integration.py << 'EOF'
#!/usr/bin/env python3
"""
Cursor AI Integration for Business Intelligence
Syncs code changes with business knowledge repo
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

class CursorBusinessSync:
    def __init__(self, repo_path):
        self.repo_path = Path(repo_path)
        self.timestamp = datetime.utcnow().isoformat() + 'Z'
        
    def watch_code_changes(self):
        """Monitor Cursor for business-relevant code changes"""
        print("👀 Watching for Cursor AI code changes...")
        
        # Use file system events to monitor changes
        import watchdog.events
        import watchdog.observers
        
        class CodeChangeHandler(watchdog.events.FileSystemEventHandler):
            def __init__(self, sync_manager):
                self.sync = sync_manager
                
            def on_modified(self, event):
                if event.is_directory:
                    return
                    
                # Only process relevant file types
                if any(event.src_path.endswith(ext) for ext in ['.py', '.js', '.md', '.sh']):
                    self.sync.process_code_change(event.src_path)
        
        event_handler = CodeChangeHandler(self)
        observer = watchdog.observers.Observer()
        observer.schedule(event_handler, str(self.repo_path), recursive=True)
        observer.start()
        
        try:
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
    
    def process_code_change(self, file_path):
        """Process code changes from Cursor AI"""
        print(f"📝 Processing code change: {file_path}")
        
        # Extract business context from file
        context = self.extract_business_context(file_path)
        
        if context:
            # Create insight document
            self.create_code_insight(file_path, context)
            
            # Update git with business context
            self.commit_with_business_context(file_path, context)
    
    def extract_business_context(self, file_path):
        """Extract business-relevant information from code"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Look for business keywords
            business_keywords = [
                'hubspot', 'deal', 'pipeline', 'quote', 'revenue',
                'customer', 'client', 'payment', 'automation'
            ]
            
            found_keywords = [kw for kw in business_keywords if kw.lower() in content.lower()]
            
            if found_keywords:
                return {
                    'file': file_path,
                    'keywords': found_keywords,
                    'timestamp': self.timestamp,
                    'type': 'code_change',
                    'business_relevance': 'high' if len(found_keywords) > 2 else 'medium'
                }
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
        
        return None
    
    def create_code_insight(self, file_path, context):
        """Create insight document for code changes"""
        date_prefix = self.timestamp[:10]
        filename = f"insights/{date_prefix}_cursor-ai-code-insight.md"
        
        insight_content = f"""# Cursor AI Code Development Insight

---
**Created:** {self.timestamp}  
**Last Updated:** {self.timestamp}  
**Type:** insight  
**Source:** Cursor AI Development  
**Tags:** [cursor-ai, development, automation]  
---

## Code Change Summary
- **File Modified:** {file_path}
- **Business Keywords:** {', '.join(context['keywords'])}
- **Relevance Level:** {context['business_relevance']}
- **Timestamp:** {self.timestamp}

## Business Impact Analysis
"""
        
        # Add specific analysis based on keywords
        if 'hubspot' in context['keywords']:
            insight_content += "\n### HubSpot Integration\nCode changes related to HubSpot CRM integration. May affect pipeline management or deal processing.\n"
        
        if 'automation' in context['keywords']:
            insight_content += "\n### Automation Enhancement\nCode changes related to business process automation. Could impact operational efficiency.\n"
        
        insight_content += f"""
## Recommended Actions
- [ ] Test code changes with live HubSpot data
- [ ] Update business process documentation
- [ ] Verify integration with existing automation workflows
- [ ] Create Airtable record for significant changes

## Related Documents
- HubSpot Analysis: insights/2025-07-20_hubspot-analysis.md
- Business Decisions: decisions/
- Process Documentation: processes/

---
**Generated by:** Cursor AI Integration  
**Next Review:** {datetime.fromisoformat(self.timestamp[:-1]).strftime('%Y-%m-%d')}
"""
        
        # Write insight file
        insight_path = self.repo_path / filename
        insight_path.parent.mkdir(exist_ok=True)
        
        with open(insight_path, 'w') as f:
            f.write(insight_content)
        
        print(f"✅ Created code insight: {filename}")
    
    def commit_with_business_context(self, file_path, context):
        """Commit changes with business context"""
        try:
            # Add business context to git commit
            commit_message = f"[{self.timestamp}] Cursor AI: {os.path.basename(file_path)} - {context['business_relevance']} business impact\n\nBusiness keywords: {', '.join(context['keywords'])}\nFile: {file_path}"
            
            subprocess.run(['git', 'add', file_path], cwd=self.repo_path)
            subprocess.run(['git', 'commit', '-m', commit_message], cwd=self.repo_path)
            
            print(f"✅ Committed with business context: {file_path}")
        except Exception as e:
            print(f"Error committing: {e}")

# Create Cursor-specific business templates
def create_cursor_templates():
    """Create Cursor AI templates for business development"""
    
    templates = {
        'hubspot_integration.py': '''
# HubSpot Integration Template
# Use this template for HubSpot API integrations

import requests
from datetime import datetime

class HubSpotIntegration:
    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = "https://api.hubapi.com/crm/v3"
        self.headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        }
        
    def get_deals(self, pipeline_id=None):
        """Get deals from HubSpot with business context"""
        # Implementation here
        pass
        
    def log_business_activity(self, activity_data):
        """Log to business knowledge repo"""
        timestamp = datetime.utcnow().isoformat() + 'Z'
        # Log to insights/ directory
        pass
''',
        
        'business_automation.js': '''
// Business Automation Template
// Use for creating new automation workflows

class BusinessAutomation {
    constructor(config) {
        this.config = config;
        this.timestamp = new Date().toISOString();
    }
    
    async processBusinessEvent(event) {
        // Log to knowledge repo
        await this.logToKnowledgeRepo(event);
        
        // Update HubSpot if relevant
        if (this.isBusinessRelevant(event)) {
            await this.updateHubSpot(event);
        }
    }
    
    async logToKnowledgeRepo(event) {
        // Implementation for logging to business-knowledge-repo
    }
}
''',
        
        'quote_generator.py': '''
# Quote Generation Template
# For vehicle transport and service quotes

class QuoteGenerator:
    def __init__(self, service_type):
        self.service_type = service_type  # 'vehicle_transport', 'credit_strategy', etc.
        
    def generate_quote(self, parameters):
        """Generate quote based on business rules"""
        # Vehicle transport: distance, vehicle type, timeline
        # Credit strategy: credit score, services needed
        # Funding: amount, timeline, risk assessment
        pass
        
    def save_to_hubspot(self, quote_data):
        """Save quote as HubSpot deal"""
        pass
'''
    }
    
    # Create templates directory
    templates_dir = Path('templates/cursor-ai')
    templates_dir.mkdir(exist_ok=True)
    
    for filename, content in templates.items():
        with open(templates_dir / filename, 'w') as f:
            f.write(content)
    
    print("✅ Cursor AI business templates created")

if __name__ == "__main__":
    repo_path = "/Users/emmanuelhaddad/Downloads/business-knowledge-repo"
    
    # Create templates
    create_cursor_templates()
    
    # Start monitoring (optional - run in background)
    sync_manager = CursorBusinessSync(repo_path)
    print("🚀 Cursor AI integration ready!")
    print("Run sync_manager.watch_code_changes() to start monitoring")
EOF

    chmod +x cursor_ai_integration.py
    echo "✅ Cursor AI automation created"
}

# Create Cursor command line integration
create_cursor_cli() {
    echo "⌨️ Creating Cursor CLI integration..."
    
    cat > cursor_business_cli.sh << 'EOF'
#!/bin/bash

# Cursor Business CLI Integration
# Commands for Cursor AI business development

cursor_business_context() {
    echo "📊 Loading business context for Cursor AI..."
    
    # Load latest HubSpot data
    ./scripts/analyze_hubspot.sh pipeline-summary > /tmp/business_context.txt
    
    # Add to Cursor context
    echo "Business Context loaded:"
    echo "- 37 active deals worth $57,977"
    echo "- 4 pipelines: Customer, Vehicle Transport, Credit, Automation"
    echo "- Immediate opportunities: $22,650"
    echo ""
    echo "Use @business_context in Cursor AI for contextual assistance"
}

cursor_create_business_file() {
    local file_type=$1
    local name=$2
    
    case $file_type in
        "hubspot")
            cp templates/cursor-ai/hubspot_integration.py "$name.py"
            echo "✅ Created HubSpot integration: $name.py"
            ;;
        "automation")
            cp templates/cursor-ai/business_automation.js "$name.js"
            echo "✅ Created automation script: $name.js"
            ;;
        "quote")
            cp templates/cursor-ai/quote_generator.py "$name.py"
            echo "✅ Created quote generator: $name.py"
            ;;
        *)
            echo "❌ Unknown file type. Use: hubspot, automation, quote"
            ;;
    esac
}

cursor_sync_changes() {
    echo "🔄 Syncing Cursor changes with business repo..."
    
    # Run the Python integration
    python3 cursor_ai_integration.py &
    
    echo "✅ Background sync started"
}

# Main CLI dispatcher
case "${1:-}" in
    "context")
        cursor_business_context
        ;;
    "create")
        cursor_create_business_file "$2" "$3"
        ;;
    "sync")
        cursor_sync_changes
        ;;
    *)
        echo "Cursor Business CLI"
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  context          Load business context for Cursor AI"
        echo "  create [type] [name]  Create business file from template"
        echo "  sync             Start background sync with business repo"
        echo ""
        echo "File types: hubspot, automation, quote"
        ;;
esac
EOF

    chmod +x cursor_business_cli.sh
    echo "✅ Cursor CLI integration created"
}

# Execute setup functions
create_cursor_config
create_cursor_automation
create_cursor_cli

echo ""
echo "🎉 Cursor AI Integration Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Open business-knowledge-repo in Cursor AI"
echo "2. Install Python dependencies: pip install watchdog"
echo "3. Run: ./cursor_business_cli.sh context"
echo "4. Use @business_context in Cursor for AI assistance"
echo "5. Run: ./cursor_business_cli.sh sync (for automatic monitoring)"
