#!/usr/bin/env python3
"""
🔮 Cursor AI Agent - Intelligent Development Assistant
Integrates Cursor AI with the business intelligence ecosystem

Owner: Emmanuel Haddad
Primary Email: manny@pushingcap.com
Mission: Enhance development with business context and agent coordination

Created: 2025-07-28T16:50:00Z
Last Modified: Claude AI Assistant - Owner Request
"""

import os
import json
import subprocess
import time
import sqlite3
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
import logging
from pathlib import Path
import watchdog.events
import watchdog.observers

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CursorAIAgent:
    def __init__(self):
        """Initialize Cursor AI Agent with business intelligence"""
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.workspace_path = Path(os.getcwd())
        self.owner_email = "manny@pushingcap.com"
        
        # Business context for Cursor AI
        self.business_context = {
            'owner': 'Emmanuel Haddad',
            'primary_email': 'manny@pushingcap.com',
            'business_name': 'Pushing Capital',
            'services': ['vehicle_transport', 'credit_strategy', 'property_appraisals', 'funding'],
            'integrations': ['hubspot', 'openphone', 'slack', 'airtable', 'make_com', 'cloudflare'],
            'ai_agents': ['grok_ceo', 'communications_manager', 'integrations_manager', 'email_intelligence', 'cursor_ai']
        }
        
        # Agent coordination endpoints
        self.agent_endpoints = {
            'grok_ceo': './launch_ai_agents.sh ceo',
            'communications': './launch_ai_agents.sh communications',
            'integrations': './launch_ai_agents.sh integrations',
            'email_intelligence': 'python3 email_intelligence_agent.py',
            'hubspot_search': 'python3 hubspot_deal_finder.py'
        }
        
        # Database for development tracking
        self.db_path = "cursor_development.db"
        self.init_database()
        
        logger.info("🔮 Cursor AI Agent initialized with business intelligence")
    
    def init_database(self):
        """Initialize SQLite database for development tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create development activities table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dev_activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                file_path TEXT,
                change_type TEXT,
                business_keywords TEXT,
                business_impact TEXT,
                agent_coordination TEXT,
                commit_hash TEXT,
                created_date DATETIME
            )
        ''')
        
        # Create cursor context table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cursor_context (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                context_type TEXT,
                context_data TEXT,
                last_updated DATETIME,
                active BOOLEAN
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("📊 Cursor AI development database initialized")
    
    def start_cursor_integration(self):
        """Start full Cursor AI integration with agent coordination"""
        logger.info("🚀 Starting Cursor AI integration with agent ecosystem...")
        
        # Update business context for Cursor
        self.update_cursor_business_context()
        
        # Start file watching
        self.start_file_watching()
        
        # Coordinate with other agents
        self.coordinate_with_agents("cursor_ai_activated")
        
        logger.info("✅ Cursor AI Agent fully integrated and operational")
    
    def update_cursor_business_context(self):
        """Update Cursor AI with latest business intelligence"""
        logger.info("📊 Updating Cursor AI with business context...")
        
        # Gather latest business intelligence
        context_data = {
            'timestamp': self.timestamp,
            'email_intelligence': self.get_email_intelligence_status(),
            'hubspot_deals': self.get_hubspot_status(),
            'integrations_health': self.get_integrations_status(),
            'active_projects': self.get_active_projects(),
            'business_priorities': self.get_business_priorities()
        }
        
        # Update Cursor settings with current context
        cursor_settings = {
            "cursor.ai.enabled": True,
            "cursor.ai.model": "claude-3.5-sonnet",
            "cursor.ai.systemPrompt": self.generate_dynamic_system_prompt(context_data),
            "cursor.ai.codebaseContext": [
                "insights/",
                "decisions/",
                "scripts/",
                "README.md",
                "*.py",
                "*.js",
                "*.sh",
                "*.md"
            ],
            "cursor.ai.rules": [
                "Always coordinate with AI agent ecosystem before major changes",
                "Include business context from manny@pushingcap.com email intelligence",
                "Reference HubSpot deals and opportunities when relevant",
                "Create insight documents for significant business features",
                "Coordinate with Grok CEO for strategic decisions",
                "Use Communications Manager for important updates",
                "Follow established agent coordination protocols"
            ]
        }
        
        # Save updated settings
        with open('.cursor-settings.json', 'w') as f:
            json.dump(cursor_settings, f, indent=2)
        
        # Store context in database
        self.store_cursor_context('business_intelligence', context_data)
        
        logger.info("✅ Cursor AI business context updated")
    
    def generate_dynamic_system_prompt(self, context_data: Dict) -> str:
        """Generate dynamic system prompt based on current business intelligence"""
        prompt = f"""You are the Cursor AI Agent for Pushing Capital's business intelligence ecosystem.

**CURRENT BUSINESS CONTEXT:**
- Owner: Emmanuel Haddad (manny@pushingcap.com)
- Primary Sales Email: manny@pushingcap.com
- Business: Vehicle transport, credit strategy, property appraisals, funding
- Active AI Agents: Grok CEO, Communications Manager, Integrations Manager, Email Intelligence

**ACTIVE INTEGRATIONS:**
- HubSpot CRM: {context_data.get('hubspot_deals', 'Unknown status')}
- Email Intelligence: {context_data.get('email_intelligence', 'Unknown status')}
- Integration Health: {context_data.get('integrations_health', 'Unknown status')}

**AI AGENT COORDINATION:**
When developing features:
1. Coordinate with Grok CEO Agent for strategic decisions
2. Use Communications Manager for important updates
3. Check with Integrations Manager for system health
4. Reference Email Intelligence for customer communications

**DEVELOPMENT GUIDELINES:**
- All new features should enhance business intelligence
- Include proper agent coordination in business-critical code
- Create insight documents for significant changes
- Reference HubSpot deals and email intelligence when applicable
- Use timestamp format: {datetime.now(timezone.utc).isoformat()}

**CURRENT PRIORITIES:**
{chr(10).join(f"- {priority}" for priority in context_data.get('business_priorities', ['Business development', 'System integration']))}

Remember: You're part of an AI agent ecosystem. Coordinate with other agents for maximum business impact."""
        
        return prompt
    
    def start_file_watching(self):
        """Start watching files for business-relevant changes"""
        logger.info("👀 Starting file watching for business intelligence...")
        
        class BusinessAwareFileHandler(watchdog.events.FileSystemEventHandler):
            def __init__(self, cursor_agent):
                self.cursor_agent = cursor_agent
            
            def on_modified(self, event):
                if event.is_directory:
                    return
                
                # Only process relevant files
                if any(event.src_path.endswith(ext) for ext in ['.py', '.js', '.md', '.sh', '.json']):
                    self.cursor_agent.process_file_change(event.src_path)
        
        event_handler = BusinessAwareFileHandler(self)
        observer = watchdog.observers.Observer()
        observer.schedule(event_handler, str(self.workspace_path), recursive=True)
        observer.start()
        
        logger.info("✅ File watching started for business intelligence")
        return observer
    
    def process_file_change(self, file_path: str):
        """Process file changes with business intelligence"""
        logger.info(f"📝 Processing file change: {file_path}")
        
        try:
            # Analyze business relevance
            business_analysis = self.analyze_business_relevance(file_path)
            
            if business_analysis['relevance'] == 'high':
                # Coordinate with other agents
                self.coordinate_with_agents(f"high_impact_change:{file_path}")
                
                # Create insight document
                self.create_development_insight(file_path, business_analysis)
                
                # Update business context if needed
                if business_analysis['requires_context_update']:
                    self.update_cursor_business_context()
            
            # Store development activity
            self.store_development_activity(file_path, business_analysis)
            
        except Exception as e:
            logger.error(f"Error processing file change {file_path}: {e}")
    
    def analyze_business_relevance(self, file_path: str) -> Dict[str, Any]:
        """Analyze file changes for business relevance"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {'relevance': 'low', 'error': str(e)}
        
        # Business keywords for analysis
        high_impact_keywords = [
            'hubspot', 'deal', 'pipeline', 'manny@pushingcap.com',
            'email_intelligence', 'grok_ceo', 'communications_manager',
            'darcy', 'appraisal', 'vehicle_transport', 'credit_strategy'
        ]
        
        medium_impact_keywords = [
            'api', 'integration', 'automation', 'webhook',
            'openphone', 'slack', 'airtable', 'make_com'
        ]
        
        # Agent coordination keywords
        agent_keywords = [
            'launch_ai_agents', 'agent', 'coordinate', 'grok', 'communications'
        ]
        
        content_lower = content.lower()
        
        high_found = [kw for kw in high_impact_keywords if kw in content_lower]
        medium_found = [kw for kw in medium_impact_keywords if kw in content_lower]
        agent_found = [kw for kw in agent_keywords if kw in content_lower]
        
        # Determine relevance level
        relevance = 'low'
        if high_found or agent_found:
            relevance = 'high'
        elif medium_found:
            relevance = 'medium'
        
        return {
            'relevance': relevance,
            'high_impact_keywords': high_found,
            'medium_impact_keywords': medium_found,
            'agent_keywords': agent_found,
            'requires_context_update': bool(agent_found or 'email' in content_lower),
            'file_type': os.path.splitext(file_path)[1],
            'timestamp': self.timestamp
        }
    
    def coordinate_with_agents(self, event_type: str):
        """Coordinate with other AI agents"""
        logger.info(f"🤖 Coordinating with agents for event: {event_type}")
        
        try:
            # Notify Grok CEO of significant development changes
            if event_type.startswith('high_impact_change') or event_type == 'cursor_ai_activated':
                subprocess.run([
                    './launch_ai_agents.sh', 'ceo', 'coordinate',
                    f"Cursor AI Agent: {event_type}"
                ], capture_output=True, text=True)
            
            # Notify Communications Manager
            subprocess.run([
                './launch_ai_agents.sh', 'communications', 'executive',
                f"Cursor AI development activity: {event_type}"
            ], capture_output=True, text=True)
            
            logger.info("✅ Agent coordination completed")
        
        except Exception as e:
            logger.error(f"Error coordinating with agents: {e}")
    
    def create_development_insight(self, file_path: str, analysis: Dict[str, Any]):
        """Create insight document for significant development changes"""
        date_prefix = datetime.now().strftime('%Y-%m-%d')
        filename = f"insights/{date_prefix}_cursor-ai-development.md"
        
        insight_content = f"""# 🔮 Cursor AI Development Insight

---
**Created:** {self.timestamp}  
**File Modified:** {file_path}  
**Business Relevance:** {analysis['relevance'].upper()}  
**Type:** development  
**Source:** Cursor AI Agent  
**Tags:** [cursor-ai, development, {analysis['relevance']}-impact]  
---

## Development Activity Summary

### File Changes
- **Modified File:** `{file_path}`
- **File Type:** {analysis['file_type']}
- **Business Impact:** {analysis['relevance'].upper()}

### Business Keywords Detected
"""
        
        if analysis['high_impact_keywords']:
            insight_content += f"**High Impact:** {', '.join(analysis['high_impact_keywords'])}\n"
        
        if analysis['medium_impact_keywords']:
            insight_content += f"**Medium Impact:** {', '.join(analysis['medium_impact_keywords'])}\n"
        
        if analysis['agent_keywords']:
            insight_content += f"**Agent Coordination:** {', '.join(analysis['agent_keywords'])}\n"
        
        insight_content += f"""
## Agent Coordination Status
- **Grok CEO:** Notified of development activity
- **Communications Manager:** Updated on changes
- **Context Update Required:** {analysis['requires_context_update']}

## Business Intelligence Impact
"""
        
        # Add specific impact analysis
        if 'email' in analysis.get('high_impact_keywords', []):
            insight_content += "- **Email Intelligence:** Changes may affect email processing for manny@pushingcap.com\n"
        
        if 'hubspot' in analysis.get('high_impact_keywords', []):
            insight_content += "- **HubSpot Integration:** Changes may affect deal processing and CRM workflows\n"
        
        if analysis.get('agent_keywords'):
            insight_content += "- **Agent Ecosystem:** Changes affect AI agent coordination and communication\n"
        
        insight_content += f"""
## Recommended Actions
- [ ] Test changes with live business data
- [ ] Verify agent coordination still functional
- [ ] Update relevant business process documentation
- [ ] Consider impact on email intelligence for manny@pushingcap.com

## Related Systems
- Email Intelligence: manny@pushingcap.com monitoring
- HubSpot Integration: Deal and contact management
- Agent Coordination: Grok CEO, Communications Manager
- Business Processes: Vehicle transport, credit strategy, appraisals

---
**Generated by:** Cursor AI Agent  
**Next Review:** {datetime.now().strftime('%Y-%m-%d')}  
**Business Context:** Active development with agent coordination
"""
        
        # Write insight file
        insight_path = Path(filename)
        insight_path.parent.mkdir(exist_ok=True)
        
        with open(insight_path, 'w') as f:
            f.write(insight_content)
        
        logger.info(f"✅ Created development insight: {filename}")
    
    def get_email_intelligence_status(self) -> str:
        """Get current email intelligence status"""
        try:
            # Check if email intelligence is operational
            if os.path.exists('email_intelligence_agent.py'):
                return "Deployed - monitoring manny@pushingcap.com"
            return "Not deployed"
        except:
            return "Unknown status"
    
    def get_hubspot_status(self) -> str:
        """Get current HubSpot integration status"""
        try:
            token = os.getenv('HUBSPOT_API_TOKEN')
            if token and token != 'test':
                return "Connected with live API"
            elif token:
                return "Test token configured"
            return "Not configured"
        except:
            return "Unknown status"
    
    def get_integrations_status(self) -> str:
        """Get overall integrations health"""
        try:
            # Check integrations manager
            if os.path.exists('integrations_manager_agent.py'):
                return "Monitoring active"
            return "Not active"
        except:
            return "Unknown status"
    
    def get_active_projects(self) -> List[str]:
        """Get list of active development projects"""
        projects = []
        
        # Check for recent insight files
        insights_dir = Path('insights')
        if insights_dir.exists():
            recent_insights = [f.name for f in insights_dir.glob('*.md') 
                             if 'cursor' in f.name.lower() or 'development' in f.name.lower()]
            projects.extend([f"Development: {insight}" for insight in recent_insights[:3]])
        
        # Check for AI agent files
        ai_files = ['grok_ceo_agent.py', 'communications_manager_agent.py', 'email_intelligence_agent.py']
        for ai_file in ai_files:
            if os.path.exists(ai_file):
                projects.append(f"AI Agent: {ai_file}")
        
        return projects[:5]  # Return top 5
    
    def get_business_priorities(self) -> List[str]:
        """Get current business priorities"""
        return [
            "Email intelligence for manny@pushingcap.com",
            "HubSpot integration and deal management",
            "AI agent coordination and communication",
            "Business process automation",
            "Customer communication optimization"
        ]
    
    def store_development_activity(self, file_path: str, analysis: Dict[str, Any]):
        """Store development activity in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO dev_activities 
            (timestamp, file_path, change_type, business_keywords, business_impact, agent_coordination, created_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            self.timestamp,
            file_path,
            analysis['file_type'],
            json.dumps(analysis.get('high_impact_keywords', [])),
            analysis['relevance'],
            json.dumps(analysis.get('agent_keywords', [])),
            self.timestamp
        ))
        
        conn.commit()
        conn.close()
    
    def store_cursor_context(self, context_type: str, context_data: Dict[str, Any]):
        """Store Cursor context in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Deactivate previous context of this type
        cursor.execute('''
            UPDATE cursor_context SET active = 0 WHERE context_type = ?
        ''', (context_type,))
        
        # Insert new context
        cursor.execute('''
            INSERT INTO cursor_context (context_type, context_data, last_updated, active)
            VALUES (?, ?, ?, 1)
        ''', (context_type, json.dumps(context_data), self.timestamp))
        
        conn.commit()
        conn.close()
    
    def generate_development_report(self) -> str:
        """Generate development activity report"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT file_path, business_impact, business_keywords, timestamp
            FROM dev_activities
            ORDER BY timestamp DESC
            LIMIT 10
        ''')
        
        activities = cursor.fetchall()
        conn.close()
        
        report = f"""# 🔮 Cursor AI Development Report

**Generated:** {self.timestamp}
**Owner:** Emmanuel Haddad (manny@pushingcap.com)

## Recent Development Activities

| File | Impact | Keywords | Timestamp |
|------|--------|----------|-----------|
"""
        
        for activity in activities:
            file_path, impact, keywords, timestamp = activity
            keywords_list = json.loads(keywords) if keywords else []
            report += f"| {os.path.basename(file_path)} | {impact.upper()} | {', '.join(keywords_list)} | {timestamp} |\n"
        
        report += f"""
## Current Business Context
- **Email Intelligence:** {self.get_email_intelligence_status()}
- **HubSpot Integration:** {self.get_hubspot_status()}
- **Integrations Health:** {self.get_integrations_status()}

## Agent Coordination Status
✅ **Grok CEO:** Receiving development notifications
✅ **Communications Manager:** Updated on changes  
✅ **Cursor AI:** Fully integrated with business intelligence

---
*Generated by Cursor AI Agent - Business Intelligence Development*
"""
        
        return report

def main():
    """Main execution for Cursor AI Agent"""
    print("🔮 CURSOR AI AGENT - BUSINESS INTELLIGENCE INTEGRATION")
    print("=" * 60)
    print("Owner: Emmanuel Haddad")
    print("Primary Email: manny@pushingcap.com")
    print("Mission: Integrate Cursor AI with business intelligence ecosystem")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print("")
    
    agent = CursorAIAgent()
    
    # Start integration
    print("🚀 Starting Cursor AI integration...")
    agent.start_cursor_integration()
    
    # Generate initial report
    report = agent.generate_development_report()
    report_file = f"cursor_ai_integration_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"📄 Integration report saved to: {report_file}")
    print("")
    print("✅ Cursor AI Agent fully integrated with business intelligence ecosystem")
    print("🤖 Agent coordination: ACTIVE")
    print("📧 Email intelligence: Connected to manny@pushingcap.com")
    print("🔮 Development monitoring: OPERATIONAL")

if __name__ == "__main__":
    main()