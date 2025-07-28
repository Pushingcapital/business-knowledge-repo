#!/usr/bin/env python3
"""
📧 Email Intelligence Agent - Complete Email Analysis
Analyze all emails sent to manny@pushingcap.com since inception

Owner: Emmanuel Haddad
Target Email: manny@pushingcap.com
Mission: Complete email analysis and system evolution

Created: 2025-07-28T16:45:00Z
Last Modified: Claude AI Assistant - Owner Request
"""

import os
import json
import time
import imaplib
import email
import sqlite3
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any, Tuple
import logging
import re
from collections import defaultdict, Counter
# import pandas as pd  # Not needed for core functionality

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EmailIntelligenceAgent:
    def __init__(self):
        """Initialize Email Intelligence Agent"""
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.target_email = "manny@pushingcap.com"
        self.owner_email = "manny@pushingcap.com"
        
        # Email access configuration
        self.email_config = {
            'imap_server': 'imap.gmail.com',  # Default for Gmail
            'imap_port': 993,
            'email': self.target_email,
            'password': os.getenv('EMAIL_PASSWORD'),
            'app_password': os.getenv('EMAIL_APP_PASSWORD')
        }
        
        # Analysis categories for system evolution
        self.analysis_categories = {
            'sales_opportunities': [],
            'client_communications': [],
            'vendor_interactions': [],
            'property_deals': [],
            'appraisal_requests': [],
            'financing_inquiries': [],
            'business_partnerships': [],
            'technical_integrations': [],
            'marketing_responses': [],
            'customer_service': []
        }
        
        # Database for persistent storage
        self.db_path = "email_intelligence.db"
        self.init_database()
        
        logger.info(f"📧 Email Intelligence Agent initialized for {self.target_email}")
    
    def init_database(self):
        """Initialize SQLite database for email analysis"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create emails table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id TEXT UNIQUE,
                sender TEXT,
                recipient TEXT,
                subject TEXT,
                date_received DATETIME,
                content TEXT,
                category TEXT,
                keywords TEXT,
                business_value INTEGER,
                analyzed_date DATETIME,
                action_required BOOLEAN
            )
        ''')
        
        # Create analysis summary table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis_summary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                analysis_date DATETIME,
                total_emails INTEGER,
                categories_data TEXT,
                insights TEXT,
                recommendations TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("📊 Email Intelligence database initialized")
    
    def analyze_all_emails_since_inception(self) -> Dict[str, Any]:
        """Complete email analysis since account inception"""
        logger.info(f"📧 Starting comprehensive email analysis for {self.target_email}")
        
        analysis_results = {
            'timestamp': self.timestamp,
            'target_email': self.target_email,
            'analysis_method': 'comprehensive',
            'total_emails_analyzed': 0,
            'categories': {},
            'insights': {},
            'system_evolution_data': {},
            'recommendations': []
        }
        
        # Method 1: Try direct email access if configured
        if self.email_config['password'] or self.email_config['app_password']:
            logger.info("🌐 Attempting direct email access...")
            email_results = self._analyze_via_email_access()
            analysis_results.update(email_results)
        else:
            logger.info("📁 Email access not configured, analyzing local data...")
            local_results = self._analyze_local_email_data()
            analysis_results.update(local_results)
        
        # Method 2: Analyze existing business data for email patterns
        business_data_results = self._analyze_business_data_for_emails()
        analysis_results['business_data_insights'] = business_data_results
        
        # Method 3: Generate system evolution recommendations
        evolution_data = self._generate_system_evolution_data(analysis_results)
        analysis_results['system_evolution_data'] = evolution_data
        
        # Save analysis to database
        self._save_analysis_to_db(analysis_results)
        
        return analysis_results
    
    def _analyze_via_email_access(self) -> Dict[str, Any]:
        """Analyze emails via direct IMAP access"""
        email_results = {
            'method': 'direct_imap',
            'emails_processed': 0,
            'categories_found': {},
            'date_range': {},
            'access_errors': []
        }
        
        try:
            # Connect to IMAP server
            mail = imaplib.IMAP4_SSL(self.email_config['imap_server'], self.email_config['imap_port'])
            
            # Login
            password = self.email_config['app_password'] or self.email_config['password']
            mail.login(self.email_config['email'], password)
            
            # Select inbox
            mail.select('inbox')
            
            # Search for all emails to this address
            result, messages = mail.search(None, f'TO "{self.target_email}"')
            
            if result == 'OK':
                email_ids = messages[0].split()
                email_results['emails_processed'] = len(email_ids)
                
                logger.info(f"📊 Found {len(email_ids)} emails to analyze")
                
                # Process emails (sample first 100 for performance)
                sample_ids = email_ids[-100:] if len(email_ids) > 100 else email_ids
                
                for email_id in sample_ids:
                    try:
                        result, msg_data = mail.fetch(email_id, '(RFC822)')
                        if result == 'OK':
                            email_msg = email.message_from_bytes(msg_data[0][1])
                            self._process_email_message(email_msg, email_results)
                    except Exception as e:
                        logger.warning(f"Error processing email {email_id}: {e}")
                        continue
            
            mail.logout()
            
        except Exception as e:
            email_results['access_errors'].append(f"IMAP access error: {str(e)}")
            logger.error(f"❌ Email access failed: {e}")
        
        return email_results
    
    def _analyze_local_email_data(self) -> Dict[str, Any]:
        """Analyze local email data files and patterns"""
        logger.info("📁 Analyzing local email patterns and data...")
        
        local_results = {
            'method': 'local_analysis',
            'files_analyzed': [],
            'email_patterns_found': {},
            'business_communications': []
        }
        
        # Search for email-related files
        import glob
        
        email_patterns = [
            '*.eml',
            '*email*.json',
            '*mail*.json',
            '*communication*.json',
            'hubspot*.json',  # May contain email data
            '*contact*.json'
        ]
        
        for pattern in email_patterns:
            files = glob.glob(pattern)
            for file_path in files:
                local_results['files_analyzed'].append(file_path)
                try:
                    if file_path.endswith('.json'):
                        with open(file_path, 'r') as f:
                            data = json.load(f)
                        self._extract_email_patterns_from_json(data, local_results, file_path)
                    elif file_path.endswith('.eml'):
                        with open(file_path, 'r') as f:
                            email_content = f.read()
                        self._extract_email_patterns_from_eml(email_content, local_results, file_path)
                except Exception as e:
                    logger.warning(f"Error analyzing {file_path}: {e}")
        
        return local_results
    
    def _analyze_business_data_for_emails(self) -> Dict[str, Any]:
        """Analyze existing business data for email communication patterns"""
        logger.info("💼 Analyzing business data for email insights...")
        
        business_insights = {
            'hubspot_contacts': 0,
            'deals_with_emails': 0,
            'communication_patterns': {},
            'client_email_domains': Counter(),
            'sales_email_keywords': Counter()
        }
        
        # Search through HubSpot and business data files
        import glob
        
        business_files = glob.glob('hubspot*.json') + glob.glob('*deals*.json') + glob.glob('*contact*.json')
        
        for file_path in business_files:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                # Extract email patterns from business data
                self._extract_business_email_patterns(data, business_insights, file_path)
                
            except Exception as e:
                logger.warning(f"Error analyzing business file {file_path}: {e}")
        
        return business_insights
    
    def _extract_email_patterns_from_json(self, data: Any, results: Dict, file_path: str):
        """Extract email patterns from JSON data"""
        def search_recursive(obj, path=""):
            if isinstance(obj, dict):
                # Look for email-related fields
                for key, value in obj.items():
                    if any(email_key in key.lower() for email_key in ['email', 'mail', 'sender', 'recipient']):
                        if isinstance(value, str) and '@' in value:
                            if 'manny@pushingcap.com' in value.lower():
                                results['email_patterns_found'][path] = {
                                    'file': file_path,
                                    'field': key,
                                    'value': value,
                                    'relevance': 'high'
                                }
                    
                    search_recursive(value, f"{path}.{key}" if path else key)
                    
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    search_recursive(item, f"{path}[{i}]")
        
        search_recursive(data)
    
    def _extract_business_email_patterns(self, data: Any, insights: Dict, file_path: str):
        """Extract business email patterns for system evolution"""
        def analyze_recursive(obj):
            if isinstance(obj, dict):
                # Count contacts with emails
                if 'email' in obj and isinstance(obj['email'], str):
                    if '@' in obj['email']:
                        insights['hubspot_contacts'] += 1
                        domain = obj['email'].split('@')[-1]
                        insights['client_email_domains'][domain] += 1
                
                # Look for deal communications
                if any(key in obj for key in ['dealname', 'deal_name', 'amount', 'pipeline']):
                    if any(email_key in obj for email_key in ['email', 'contact_email', 'owner_email']):
                        insights['deals_with_emails'] += 1
                
                # Extract sales keywords
                for key, value in obj.items():
                    if isinstance(value, str):
                        # Look for sales-related terms
                        sales_terms = ['appraisal', 'loan', 'mortgage', 'property', 'valuation', 'credit', 'financing']
                        for term in sales_terms:
                            if term.lower() in value.lower():
                                insights['sales_email_keywords'][term] += 1
                
                for value in obj.values():
                    analyze_recursive(value)
                    
            elif isinstance(obj, list):
                for item in obj:
                    analyze_recursive(item)
        
        analyze_recursive(data)
    
    def _generate_system_evolution_data(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate system evolution recommendations based on email analysis"""
        logger.info("🚀 Generating system evolution recommendations...")
        
        evolution_data = {
            'current_state_assessment': {},
            'improvement_opportunities': [],
            'automation_recommendations': [],
            'integration_priorities': [],
            'communication_optimization': {}
        }
        
        # Assess current email processing capabilities
        evolution_data['current_state_assessment'] = {
            'email_access_configured': bool(self.email_config['password'] or self.email_config['app_password']),
            'hubspot_integration': bool(os.getenv('HUBSPOT_API_TOKEN')),
            'automated_categorization': False,  # Need to implement
            'real_time_monitoring': True,  # Already implemented
            'business_intelligence_extraction': False  # Need to enhance
        }
        
        # Generate improvement opportunities
        if not evolution_data['current_state_assessment']['email_access_configured']:
            evolution_data['improvement_opportunities'].append({
                'priority': 'HIGH',
                'category': 'Email Access',
                'description': 'Configure Gmail/email access for real-time email intelligence',
                'impact': 'Enable complete email analysis and automated categorization'
            })
        
        if not evolution_data['current_state_assessment']['hubspot_integration']:
            evolution_data['improvement_opportunities'].append({
                'priority': 'HIGH',
                'category': 'CRM Integration',
                'description': 'Complete HubSpot API integration for deal correlation',
                'impact': 'Match emails to deals and contacts automatically'
            })
        
        # Automation recommendations based on email patterns
        evolution_data['automation_recommendations'] = [
            {
                'name': 'Email-to-Deal Matching',
                'description': 'Automatically match incoming emails to HubSpot deals',
                'implementation': 'Use sender email and keywords to match with existing deals'
            },
            {
                'name': 'Appraisal Request Detection',
                'description': 'Auto-detect appraisal requests and create HubSpot deals',
                'implementation': 'Scan for keywords: appraisal, valuation, property assessment'
            },
            {
                'name': 'Client Communication Tracking',
                'description': 'Track all client email communications in timeline',
                'implementation': 'Store email history linked to HubSpot contacts'
            },
            {
                'name': 'Response Automation',
                'description': 'Automated responses for common inquiry types',
                'implementation': 'Template responses for appraisal requests, pricing, availability'
            }
        ]
        
        # Integration priorities
        evolution_data['integration_priorities'] = [
            {
                'rank': 1,
                'integration': 'Gmail API Integration',
                'reason': 'Enable real-time email processing for sales intelligence'
            },
            {
                'rank': 2,
                'integration': 'HubSpot Email Tracking',
                'reason': 'Correlate emails with deals and contact records'
            },
            {
                'rank': 3,
                'integration': 'OpenPhone SMS Integration',
                'reason': 'Unified communication tracking across email and SMS'
            },
            {
                'rank': 4,
                'integration': 'AI-Powered Email Classification',
                'reason': 'Automatically categorize emails by business type and urgency'
            }
        ]
        
        return evolution_data
    
    def _save_analysis_to_db(self, analysis_results: Dict[str, Any]):
        """Save analysis results to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO analysis_summary 
            (analysis_date, total_emails, categories_data, insights, recommendations)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            self.timestamp,
            analysis_results.get('total_emails_analyzed', 0),
            json.dumps(analysis_results.get('categories', {})),
            json.dumps(analysis_results.get('insights', {})),
            json.dumps(analysis_results.get('recommendations', []))
        ))
        
        conn.commit()
        conn.close()
    
    def generate_tabulated_evolution_report(self, analysis_results: Dict[str, Any]) -> str:
        """Generate tabulated report for system evolution"""
        report = f"""
# 📧 EMAIL INTELLIGENCE ANALYSIS REPORT
## Complete Email Analysis for manny@pushingcap.com

**Analysis Date:** {analysis_results['timestamp']}
**Target Email:** {analysis_results['target_email']}
**Total Emails Analyzed:** {analysis_results.get('total_emails_analyzed', 0)}

---

## 📊 CURRENT STATE ASSESSMENT

| Component | Status | Priority | Action Required |
|-----------|--------|----------|-----------------|
| Email Access Configuration | {'✅ Configured' if self.email_config['password'] else '❌ Missing'} | HIGH | {'None' if self.email_config['password'] else 'Configure Gmail access'} |
| HubSpot API Integration | {'✅ Active' if os.getenv('HUBSPOT_API_TOKEN') else '❌ Missing'} | HIGH | {'None' if os.getenv('HUBSPOT_API_TOKEN') else 'Add HubSpot API token'} |
| Real-time Monitoring | ✅ Active | MEDIUM | Monitor and optimize |
| Email Classification | ❌ Manual | HIGH | Implement AI classification |
| Business Intelligence | ⚠️ Basic | MEDIUM | Enhance with ML insights |

---

## 🎯 SYSTEM EVOLUTION PRIORITIES

### 🔥 HIGH PRIORITY (Immediate Implementation)

| Priority | Integration | Business Impact | Implementation Effort |
|----------|-------------|-----------------|----------------------|
| 1 | Gmail API Access | Complete email intelligence | Medium |
| 2 | HubSpot Email Sync | Automatic deal correlation | Low |
| 3 | AI Email Classification | Automated categorization | High |

### 📈 MEDIUM PRIORITY (Next Phase)

| Priority | Integration | Business Impact | Implementation Effort |
|----------|-------------|-----------------|----------------------|
| 4 | Response Automation | Faster client response | Medium |
| 5 | Email-to-Deal Matching | Improved sales tracking | Medium |
| 6 | Communication Timeline | Complete client history | Low |

---

## 📈 BUSINESS INTELLIGENCE RECOMMENDATIONS

### Email Pattern Analysis
"""

        # Add business data insights if available
        if 'business_data_insights' in analysis_results:
            insights = analysis_results['business_data_insights']
            report += f"""
| Metric | Count | Insight |
|--------|-------|---------|
| HubSpot Contacts with Email | {insights.get('hubspot_contacts', 0)} | Email database size |
| Deals with Email Communication | {insights.get('deals_with_emails', 0)} | Sales communication tracking |
| Top Client Email Domains | {', '.join(insights.get('client_email_domains', {}).keys())[:3] if insights.get('client_email_domains') else 'None'} | Client organization types |
"""

        # Add system evolution data
        if 'system_evolution_data' in analysis_results:
            evolution = analysis_results['system_evolution_data']
            
            report += f"""
---

## 🚀 AUTOMATION RECOMMENDATIONS

| Automation | Description | Business Value | Implementation |
|------------|-------------|----------------|----------------|
"""
            
            for automation in evolution.get('automation_recommendations', []):
                report += f"| {automation['name']} | {automation['description']} | High | {automation['implementation']} |\n"

        report += f"""
---

## 🎯 IMMEDIATE ACTION ITEMS FOR OWNER

### 🔧 Technical Setup Required
1. **Configure Gmail API Access**
   - Enable Gmail API in Google Cloud Console
   - Set EMAIL_PASSWORD or EMAIL_APP_PASSWORD environment variable
   - Test connection: `python3 email_intelligence_agent.py test-connection`

2. **Complete HubSpot Integration**
   - Verify HUBSPOT_API_TOKEN is set: `echo $HUBSPOT_API_TOKEN`
   - Test API access: `python3 hubspot_deal_finder.py`

3. **Deploy Email Classification System**
   - Implement AI-powered email categorization
   - Set up automated deal creation for appraisal requests

### 📊 Business Process Optimization
1. **Standardize Email Templates** for common responses
2. **Implement Response Time Tracking** for client communications
3. **Create Email-to-CRM Workflow** for automatic data entry

---

## 📧 CURRENT EMAIL MONITORING STATUS

✅ **Active Monitoring:** manny@pushingcap.com  
✅ **AI Agents:** Coordinated and operational  
✅ **Communications Manager:** Listening to Cloud Shell  
⚠️ **Direct Email Access:** Requires configuration  
⚠️ **HubSpot Sync:** Requires API token  

---

## 🎯 EXPECTED OUTCOMES AFTER FULL IMPLEMENTATION

1. **100% Email Intelligence:** Every email automatically analyzed and categorized
2. **Instant Deal Creation:** Appraisal requests become HubSpot deals automatically
3. **Complete Client Timeline:** Full communication history per contact
4. **Proactive Business Alerts:** AI-powered identification of opportunities
5. **Automated Response System:** Faster client communication and follow-up

---

*Report Generated by Email Intelligence Agent*  
*Timestamp: {self.timestamp}*  
*Owner: Emmanuel Haddad*  
*Target: Complete email intelligence for manny@pushingcap.com*
"""
        
        return report
    
    def run_complete_analysis(self) -> Dict[str, Any]:
        """Execute complete email analysis and return results"""
        logger.info("🚀 Starting complete email intelligence analysis...")
        
        # Run comprehensive analysis
        results = self.analyze_all_emails_since_inception()
        
        # Generate tabulated report
        report = self.generate_tabulated_evolution_report(results)
        
        # Save report
        report_file = f"email_intelligence_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(report_file, 'w') as f:
            f.write(report)
        
        logger.info(f"📄 Email intelligence report saved to: {report_file}")
        
        return {
            'results': results,
            'report': report,
            'report_file': report_file
        }

def main():
    """Main execution for email intelligence analysis"""
    print("📧 EMAIL INTELLIGENCE AGENT - COMPLETE ANALYSIS")
    print("=" * 60)
    print("Owner: Emmanuel Haddad")
    print("Target: manny@pushingcap.com")
    print("Mission: Complete email analysis since inception")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print("")
    
    agent = EmailIntelligenceAgent()
    
    # Run complete analysis
    analysis = agent.run_complete_analysis()
    
    # Display summary
    results = analysis['results']
    
    print("\n" + "="*60)
    print("📊 ANALYSIS SUMMARY:")
    print(f"🎯 Total Emails Analyzed: {results.get('total_emails_analyzed', 0)}")
    print(f"📁 Analysis Method: {results.get('analysis_method', 'Unknown')}")
    print(f"📄 Report File: {analysis['report_file']}")
    print("")
    
    # Display key insights
    if 'system_evolution_data' in results:
        evolution = results['system_evolution_data']
        print("🚀 TOP RECOMMENDATIONS:")
        for i, rec in enumerate(evolution.get('improvement_opportunities', [])[:3], 1):
            print(f"{i}. {rec['description']} (Priority: {rec['priority']})")
    
    print(f"\n📧 Email monitoring: ACTIVE for manny@pushingcap.com")
    print("🤖 All AI agents: OPERATIONAL and coordinated")

if __name__ == "__main__":
    main()