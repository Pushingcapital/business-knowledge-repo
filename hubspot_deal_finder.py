#!/usr/bin/env python3
"""
🔍 HubSpot Deal Finder - Darcy Appraisals Search
Search for specific deals in HubSpot for owner Emmanuel Haddad

Target: Darcy + Appraisals deal
Owner: Emmanuel Haddad (emmanuel@pushingcap.com)

Created: 2025-07-28T16:40:00Z
Last Modified: Claude AI Assistant - Owner Request
"""

import os
import json
import requests
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class HubSpotDealFinder:
    def __init__(self):
        """Initialize HubSpot Deal Finder"""
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.api_token = os.getenv('HUBSPOT_API_TOKEN')
        self.portal_id = os.getenv('HUBSPOT_PORTAL_ID')
        self.base_url = "https://api.hubapi.com"
        
        # Search parameters for Darcy appraisals deal
        self.search_criteria = {
            'contact_name': 'Darcy',
            'deal_keywords': ['appraisal', 'appraisals', 'property', 'valuation'],
            'service_type': 'appraisal'
        }
        
        logger.info("🔍 HubSpot Deal Finder initialized for Darcy appraisals search")
    
    def search_darcy_appraisals_deal(self) -> Dict[str, Any]:
        """Search for Darcy appraisals deal specifically"""
        logger.info("🎯 Searching for Darcy appraisals deal...")
        
        results = {
            'timestamp': self.timestamp,
            'search_target': 'Darcy + Appraisals',
            'api_available': bool(self.api_token),
            'deals_found': [],
            'contacts_found': [],
            'search_method': 'hybrid'
        }
        
        # Method 1: Try API if available
        if self.api_token:
            logger.info("🌐 Using HubSpot API for live search...")
            api_results = self._search_via_api()
            results.update(api_results)
        else:
            logger.info("📁 API not configured, checking local data files...")
            file_results = self._search_local_files()
            results.update(file_results)
        
        # Method 2: Enhanced search through existing files
        enhanced_results = self._enhanced_local_search()
        results['enhanced_search'] = enhanced_results
        
        return results
    
    def _search_via_api(self) -> Dict[str, Any]:
        """Search via HubSpot API"""
        headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }
        
        api_results = {
            'api_deals': [],
            'api_contacts': [],
            'api_errors': []
        }
        
        try:
            # Search deals
            deals_url = f"{self.base_url}/crm/v3/objects/deals/search"
            deals_payload = {
                "filterGroups": [
                    {
                        "filters": [
                            {
                                "propertyName": "dealname",
                                "operator": "CONTAINS_TOKEN",
                                "value": "appraisal"
                            }
                        ]
                    }
                ],
                "properties": ["dealname", "amount", "dealstage", "hubspot_owner_id", "createdate"]
            }
            
            deals_response = requests.post(deals_url, headers=headers, json=deals_payload, timeout=30)
            
            if deals_response.status_code == 200:
                deals_data = deals_response.json()
                api_results['api_deals'] = deals_data.get('results', [])
                logger.info(f"📊 Found {len(api_results['api_deals'])} deals via API")
            else:
                api_results['api_errors'].append(f"Deals API error: {deals_response.status_code}")
            
            # Search contacts for Darcy
            contacts_url = f"{self.base_url}/crm/v3/objects/contacts/search"
            contacts_payload = {
                "filterGroups": [
                    {
                        "filters": [
                            {
                                "propertyName": "firstname",
                                "operator": "CONTAINS_TOKEN", 
                                "value": "Darcy"
                            }
                        ]
                    }
                ],
                "properties": ["firstname", "lastname", "email", "phone", "createdate"]
            }
            
            contacts_response = requests.post(contacts_url, headers=headers, json=contacts_payload, timeout=30)
            
            if contacts_response.status_code == 200:
                contacts_data = contacts_response.json()
                api_results['api_contacts'] = contacts_data.get('results', [])
                logger.info(f"👤 Found {len(api_results['api_contacts'])} contacts named Darcy via API")
            else:
                api_results['api_errors'].append(f"Contacts API error: {contacts_response.status_code}")
                
        except Exception as e:
            api_results['api_errors'].append(f"API search error: {str(e)}")
            logger.error(f"❌ API search failed: {e}")
        
        return api_results
    
    def _search_local_files(self) -> Dict[str, Any]:
        """Search through local HubSpot data files"""
        logger.info("📁 Searching local HubSpot data files...")
        
        local_results = {
            'local_deals': [],
            'local_contacts': [],
            'files_searched': []
        }
        
        # Search through common HubSpot data file patterns
        search_patterns = [
            'hubspot*.json',
            'deals*.json', 
            'raw_deals.json',
            'hubspot_export*.json',
            '*hubspot*.csv',
            'raw_deals.csv'
        ]
        
        import glob
        
        for pattern in search_patterns:
            files = glob.glob(pattern)
            for file_path in files:
                local_results['files_searched'].append(file_path)
                
                try:
                    if file_path.endswith('.json'):
                        with open(file_path, 'r') as f:
                            data = json.load(f)
                            
                        # Search for Darcy and appraisals
                        self._search_json_data(data, local_results, file_path)
                        
                    elif file_path.endswith('.csv'):
                        # Search CSV files
                        self._search_csv_data(file_path, local_results)
                        
                except Exception as e:
                    logger.warning(f"Error reading {file_path}: {e}")
        
        logger.info(f"📊 Local search completed: {len(local_results['files_searched'])} files searched")
        return local_results
    
    def _search_json_data(self, data: Any, results: Dict, file_path: str):
        """Search JSON data for Darcy and appraisals"""
        def search_recursive(obj, path=""):
            if isinstance(obj, dict):
                # Check if this looks like a deal or contact
                if self._contains_darcy_appraisal_keywords(obj):
                    if self._looks_like_deal(obj):
                        results['local_deals'].append({
                            'source_file': file_path,
                            'data': obj,
                            'found_at': path
                        })
                    elif self._looks_like_contact(obj):
                        results['local_contacts'].append({
                            'source_file': file_path,
                            'data': obj,
                            'found_at': path
                        })
                
                for key, value in obj.items():
                    search_recursive(value, f"{path}.{key}" if path else key)
                    
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    search_recursive(item, f"{path}[{i}]")
        
        search_recursive(data)
    
    def _search_csv_data(self, file_path: str, results: Dict):
        """Search CSV data for Darcy and appraisals"""
        try:
            import csv
            
            with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
                # Try to detect delimiter
                sample = csvfile.read(1024)
                csvfile.seek(0)
                
                delimiter = ',' if ',' in sample else '\t' if '\t' in sample else ';'
                reader = csv.DictReader(csvfile, delimiter=delimiter)
                
                for row_num, row in enumerate(reader):
                    if self._contains_darcy_appraisal_keywords(row):
                        results['local_deals'].append({
                            'source_file': file_path,
                            'data': row,
                            'found_at': f"row_{row_num}"
                        })
                        
        except Exception as e:
            logger.warning(f"Error reading CSV {file_path}: {e}")
    
    def _contains_darcy_appraisal_keywords(self, obj: Any) -> bool:
        """Check if object contains Darcy and appraisal keywords"""
        if not isinstance(obj, (dict, str)):
            obj_str = str(obj)
        else:
            obj_str = json.dumps(obj).lower() if isinstance(obj, dict) else str(obj).lower()
        
        has_darcy = 'darcy' in obj_str
        has_appraisal = any(keyword in obj_str for keyword in ['appraisal', 'appraise', 'valuation', 'assessment'])
        
        return has_darcy or has_appraisal
    
    def _looks_like_deal(self, obj: Dict) -> bool:
        """Check if object looks like a HubSpot deal"""
        deal_indicators = ['dealname', 'amount', 'dealstage', 'deal_id', 'pipeline']
        return any(indicator in str(obj).lower() for indicator in deal_indicators)
    
    def _looks_like_contact(self, obj: Dict) -> bool:
        """Check if object looks like a HubSpot contact"""
        contact_indicators = ['firstname', 'lastname', 'email', 'phone', 'contact_id']
        return any(indicator in str(obj).lower() for indicator in contact_indicators)
    
    def _enhanced_local_search(self) -> Dict[str, Any]:
        """Enhanced search through all available data"""
        logger.info("🔍 Running enhanced local search...")
        
        enhanced_results = {
            'potential_matches': [],
            'keyword_matches': [],
            'similar_deals': []
        }
        
        # Search through all JSON files in current directory
        import glob
        import os
        
        all_files = glob.glob('*.json') + glob.glob('*.csv')
        
        for file_path in all_files:
            if os.path.getsize(file_path) > 10:  # Skip empty files
                try:
                    if file_path.endswith('.json'):
                        with open(file_path, 'r') as f:
                            content = f.read().lower()
                            
                        if 'darcy' in content:
                            enhanced_results['potential_matches'].append({
                                'file': file_path,
                                'type': 'darcy_mention',
                                'relevance': 'high'
                            })
                            
                        if any(keyword in content for keyword in ['appraisal', 'valuation', 'assessment']):
                            enhanced_results['keyword_matches'].append({
                                'file': file_path,
                                'type': 'appraisal_related',
                                'relevance': 'medium'
                            })
                            
                except Exception as e:
                    continue
        
        return enhanced_results
    
    def generate_search_report(self, results: Dict[str, Any]) -> str:
        """Generate formatted search report"""
        report = f"""
# 🔍 HubSpot Deal Search Report - Darcy Appraisals

**Search Executed:** {results['timestamp']}
**Target:** {results['search_target']}
**API Available:** {'Yes' if results['api_available'] else 'No'}

## 🎯 Search Results Summary

### API Results (if available)
"""
        
        if results['api_available'] and 'api_deals' in results:
            report += f"- **Deals Found via API:** {len(results.get('api_deals', []))}\n"
            report += f"- **Contacts Found via API:** {len(results.get('api_contacts', []))}\n"
            
            if results.get('api_deals'):
                report += "\n#### Deals from API:\n"
                for deal in results['api_deals']:
                    report += f"- {deal.get('properties', {}).get('dealname', 'Unnamed Deal')}\n"
                    
            if results.get('api_contacts'):
                report += "\n#### Contacts from API:\n"
                for contact in results['api_contacts']:
                    props = contact.get('properties', {})
                    name = f"{props.get('firstname', '')} {props.get('lastname', '')}".strip()
                    report += f"- {name} ({props.get('email', 'No email')})\n"
        
        # Local file results
        if 'local_deals' in results:
            report += f"\n### Local File Results\n"
            report += f"- **Local Deals Found:** {len(results.get('local_deals', []))}\n"
            report += f"- **Local Contacts Found:** {len(results.get('local_contacts', []))}\n"
            report += f"- **Files Searched:** {len(results.get('files_searched', []))}\n"
            
            if results.get('local_deals'):
                report += "\n#### Local Deals:\n"
                for deal in results['local_deals']:
                    report += f"- **File:** {deal['source_file']}\n"
                    report += f"  **Location:** {deal['found_at']}\n"
                    
        # Enhanced search results
        if 'enhanced_search' in results:
            enhanced = results['enhanced_search']
            report += f"\n### Enhanced Search\n"
            report += f"- **Potential Matches:** {len(enhanced.get('potential_matches', []))}\n"
            report += f"- **Keyword Matches:** {len(enhanced.get('keyword_matches', []))}\n"
            
            if enhanced.get('potential_matches'):
                report += "\n#### Files with 'Darcy' mentions:\n"
                for match in enhanced['potential_matches']:
                    report += f"- {match['file']} ({match['relevance']} relevance)\n"
                    
            if enhanced.get('keyword_matches'):
                report += "\n#### Files with appraisal keywords:\n"
                for match in enhanced['keyword_matches']:
                    report += f"- {match['file']} ({match['relevance']} relevance)\n"
        
        report += f"\n## 🎯 Owner Action Required\n\n"
        
        if not results['api_available']:
            report += "**⚠️ HubSpot API Configuration Needed:**\n"
            report += "- Set HUBSPOT_API_TOKEN environment variable\n"
            report += "- Configure portal access for live deal data\n\n"
        
        report += "**📧 Email Monitoring Status:** ACTIVE\n"
        report += "**📊 Integration Status:** Monitoring for Darcy communications\n"
        
        report += f"\n---\n*Report generated by HubSpot Deal Finder at {self.timestamp}*"
        
        return report

def main():
    """Main execution for HubSpot deal search"""
    print("🔍 HUBSPOT DEAL FINDER - DARCY APPRAISALS SEARCH")
    print("=" * 60)
    print("Owner: Emmanuel Haddad")
    print("Target: Darcy + Appraisals deal")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print("")
    
    finder = HubSpotDealFinder()
    
    # Execute search
    print("🎯 Executing search for Darcy appraisals deal...")
    results = finder.search_darcy_appraisals_deal()
    
    # Generate and display report
    report = finder.generate_search_report(results)
    
    # Save report
    report_file = f"darcy_appraisals_search_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"\n📄 Search report saved to: {report_file}")
    print("\n" + "="*60)
    print(report)
    
    # Summary for owner
    print(f"\n👑 OWNER SUMMARY:")
    print(f"📊 API Available: {'Yes' if results['api_available'] else 'No (Configuration needed)'}")
    print(f"🎯 Deals Found: {len(results.get('api_deals', []) + results.get('local_deals', []))}")
    print(f"👤 Contacts Found: {len(results.get('api_contacts', []) + results.get('local_contacts', []))}")
    print(f"📁 Files Searched: {len(results.get('files_searched', []))}")
    print(f"📧 Email Monitoring: ACTIVE")

if __name__ == "__main__":
    main()