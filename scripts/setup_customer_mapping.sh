#!/bin/bash

# 🗺️ Pushing Capital Customer Mapping Setup
# Create visual maps of customers by service type and location

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🗺️ Pushing Capital Customer Mapping System${NC}"
echo "=============================================="
echo -e "${YELLOW}Setting up customer location visualization and tracking${NC}"
echo ""

# Create mapping directory structure
setup_mapping_structure() {
    echo -e "${BLUE}📁 Creating mapping directory structure...${NC}"
    
    mkdir -p customer_mapping
    mkdir -p customer_mapping/data
    mkdir -p customer_mapping/exports
    mkdir -p customer_mapping/templates
    
    echo -e "${GREEN}✅ Directory structure created${NC}"
}

# Create customer data template
create_data_template() {
    echo -e "${BLUE}📋 Creating customer data template...${NC}"
    
    cat > customer_mapping/templates/customer_data_template.csv << 'EOF'
Customer_Name,Service_Type,Deal_Value,Address,City,State,ZIP,Stage,Rep_Assigned,Date_Added,Phone,Email
John Smith,Credit Strategy,1500,123 Main St,Dallas,TX,75201,Onboarding,Agent_001,2025-01-29,(555) 123-4567,john@email.com
Sarah Johnson,Vehicle Transport,850,456 Oak Ave,Miami,FL,33101,Quote_Sent,Agent_002,2025-01-29,(555) 234-5678,sarah@email.com
Mike Wilson,Property Appraisal,650,789 Pine Rd,Denver,CO,80202,Completed,Agent_003,2025-01-29,(555) 345-6789,mike@email.com
Lisa Davis,Funding Services,2200,321 Elm St,Seattle,WA,98101,Approved,Agent_004,2025-01-29,(555) 456-7890,lisa@email.com
EOF

    echo -e "${GREEN}✅ Customer data template created${NC}"
}

# Create HubSpot export instructions
create_hubspot_export_guide() {
    echo -e "${BLUE}📊 Creating HubSpot export guide...${NC}"
    
    cat > customer_mapping/HubSpot_Export_Guide.md << 'EOF'
# HubSpot Customer Data Export for Mapping

## Required Fields for Customer Mapping

### Contact Properties
- First Name
- Last Name  
- Email
- Phone
- Address
- City
- State
- Postal Code

### Deal Properties
- Deal Name
- Deal Amount
- Deal Stage
- Pipeline
- Deal Owner
- Create Date
- Close Date

### Custom Properties (if available)
- Service Type
- Lead Source
- Customer Satisfaction Score

## Export Steps

1. **Navigate to Contacts**
   - Go to Contacts > Contacts in HubSpot

2. **Create Custom View**
   - Click "Create view"
   - Select "All contacts" or filter by service type
   - Add required properties to columns

3. **Export Data**
   - Click "Actions" > "Export"
   - Select "Export all" or "Export filtered"
   - Choose CSV format
   - Include all selected properties

4. **Export Deals**
   - Go to Sales > Deals
   - Create view with customer deal information
   - Export as CSV

## Data Mapping for Services

### Credit Strategy ($1,500/client)
- Pipeline: Customer Pipeline
- Stage: Onboarding, Analysis, Strategy, Implementation
- Color Code: Blue (#0066CC)

### Vehicle Transport (Variable pricing)
- Pipeline: Nationwide Vehicle Transport Solutions
- Stage: Quote, Booked, In Transit, Delivered
- Color Code: Green (#00AA44)

### Property Appraisal ($450-$650)
- Pipeline: Appraisal Services
- Stage: Requested, Scheduled, Completed, Delivered
- Color Code: Orange (#FF8800)

### Funding Services (Commission-based)
- Pipeline: Funding Pipeline
- Stage: Application, Review, Approved, Funded
- Color Code: Purple (#8800CC)
EOF

    echo -e "${GREEN}✅ HubSpot export guide created${NC}"
}

# Create Mapline setup instructions
create_mapline_instructions() {
    echo -e "${BLUE}🗺️ Creating Mapline setup instructions...${NC}"
    
    cat > customer_mapping/Mapline_Setup_Instructions.md << 'EOF'
# Mapline Customer Mapping Setup for Pushing Capital

## Account Setup
1. **Create Mapline Account**
   - Visit: https://mapline.com
   - Sign up for business account
   - Choose plan based on customer volume

## Import Customer Data

### Step 1: Prepare Data
- Use template: `templates/customer_data_template.csv`
- Export from HubSpot following export guide
- Ensure all addresses are complete

### Step 2: Upload to Mapline
- Click "Add" > "Pins" > "From Spreadsheet"
- Upload your customer CSV file
- Map columns: Address, City, State, ZIP

### Step 3: Color-Code by Service Type
**Credit Strategy Services**
- Color: Blue (#0066CC)
- Icon: Credit card or dollar sign
- Filter: Service_Type = "Credit Strategy"

**Vehicle Transport**
- Color: Green (#00AA44) 
- Icon: Truck or car
- Filter: Service_Type = "Vehicle Transport"

**Property Appraisal**
- Color: Orange (#FF8800)
- Icon: House or building
- Filter: Service_Type = "Property Appraisal"

**Funding Services**
- Color: Purple (#8800CC)
- Icon: Bank or money
- Filter: Service_Type = "Funding Services"

## Advanced Features

### Segmentation
- Right-click pin layer > "Segment"
- Segment by: Deal_Value, Stage, Rep_Assigned
- Create heat maps by revenue concentration

### Real-time Updates
- Connect Mapline to HubSpot via Zapier/Make.com
- Auto-update customer locations
- Track sales activity in real-time

### Reporting
- Generate territory reports
- Revenue by geographic region
- Customer density analysis
- Service penetration by market

## Revenue Visualization
- Size pins by deal value
- Large pins: $2,000+ (Funding Services)
- Medium pins: $1,500 (Credit Strategy)
- Small pins: <$1,000 (Transport/Appraisal)

## Market Analysis
- Identify high-density customer areas
- Plan marketing campaigns by region
- Optimize service delivery routes
- Track competitor presence
EOF

    echo -e "${GREEN}✅ Mapline setup instructions created${NC}"
}

# Create geocoding script for address conversion
create_geocoding_script() {
    echo -e "${BLUE}🌍 Creating geocoding utility script...${NC}"
    
    cat > customer_mapping/scripts/geocode_addresses.py << 'EOF'
#!/usr/bin/env python3
"""
Geocoding utility for Pushing Capital customer addresses
Converts addresses to latitude/longitude coordinates for mapping
"""

import csv
import requests
import time
import sys
from datetime import datetime

def geocode_address(address, city, state, zip_code):
    """
    Geocode a single address using OpenStreetMap Nominatim API
    Free alternative to Google Maps API
    """
    full_address = f"{address}, {city}, {state} {zip_code}"
    
    # Nominatim API endpoint
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': full_address,
        'format': 'json',
        'limit': 1,
        'countrycodes': 'us'
    }
    
    headers = {
        'User-Agent': 'PushingCapital-CustomerMapping/1.0'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
        else:
            print(f"No results found for: {full_address}")
            return None, None
            
    except requests.RequestException as e:
        print(f"Error geocoding {full_address}: {e}")
        return None, None

def process_customer_file(input_file, output_file):
    """
    Process customer CSV file and add geocoded coordinates
    """
    processed_count = 0
    error_count = 0
    
    with open(input_file, 'r', newline='', encoding='utf-8') as infile:
        with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            reader = csv.DictReader(infile)
            
            # Add latitude and longitude fields
            fieldnames = reader.fieldnames + ['Latitude', 'Longitude']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for row in reader:
                # Extract address components
                address = row.get('Address', '')
                city = row.get('City', '')
                state = row.get('State', '')
                zip_code = row.get('ZIP', '')
                
                if address and city and state:
                    lat, lon = geocode_address(address, city, state, zip_code)
                    row['Latitude'] = lat if lat else ''
                    row['Longitude'] = lon if lon else ''
                    
                    if lat and lon:
                        processed_count += 1
                        print(f"✅ Geocoded: {row['Customer_Name']} - {city}, {state}")
                    else:
                        error_count += 1
                        print(f"❌ Failed: {row['Customer_Name']} - {city}, {state}")
                else:
                    error_count += 1
                    print(f"⚠️  Incomplete address: {row['Customer_Name']}")
                
                writer.writerow(row)
                
                # Rate limiting - be respectful to free API
                time.sleep(1)
    
    print(f"\n📊 Geocoding Summary:")
    print(f"✅ Successfully processed: {processed_count}")
    print(f"❌ Errors: {error_count}")
    print(f"📁 Output file: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 geocode_addresses.py input.csv output.csv")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    print(f"🌍 Starting geocoding process...")
    print(f"📥 Input: {input_file}")
    print(f"📤 Output: {output_file}")
    print("")
    
    process_customer_file(input_file, output_file)
EOF

    chmod +x customer_mapping/scripts/geocode_addresses.py
    echo -e "${GREEN}✅ Geocoding script created${NC}"
}

# Create customer mapping dashboard config
create_dashboard_config() {
    echo -e "${BLUE}📊 Creating mapping dashboard configuration...${NC}"
    
    cat > customer_mapping/dashboard_config.json << 'EOF'
{
  "name": "Pushing Capital Customer Map Dashboard",
  "description": "Comprehensive customer location and service tracking",
  "map_layers": {
    "credit_strategy": {
      "name": "Credit Strategy Customers",
      "color": "#0066CC",
      "icon": "credit-card",
      "revenue_per_client": 1500,
      "pipeline": "Customer Pipeline"
    },
    "vehicle_transport": {
      "name": "Vehicle Transport",
      "color": "#00AA44",
      "icon": "truck",
      "revenue_variable": true,
      "pipeline": "Nationwide Vehicle Transport Solutions"
    },
    "property_appraisal": {
      "name": "Property Appraisals",
      "color": "#FF8800", 
      "icon": "home",
      "revenue_range": [450, 650],
      "pipeline": "Appraisal Services"
    },
    "funding_services": {
      "name": "Funding Services",
      "color": "#8800CC",
      "icon": "bank",
      "revenue_commission": true,
      "pipeline": "Funding Pipeline"
    }
  },
  "kpi_tracking": {
    "monthly_revenue_target": 75000,
    "quarterly_revenue_target": 225000,
    "annual_revenue_target": 900000,
    "customer_satisfaction_minimum": 4.5,
    "response_time_target": 15
  },
  "geographic_analysis": {
    "heat_maps": ["revenue", "customer_density", "service_type"],
    "territory_optimization": true,
    "competitor_tracking": true,
    "market_penetration": true
  }
}
EOF

    echo -e "${GREEN}✅ Dashboard configuration created${NC}"
}

# Generate setup report
generate_setup_report() {
    echo -e "${BLUE}📋 Generating setup report...${NC}"
    
    REPORT_FILE="customer_mapping/Customer_Mapping_Setup_Report_$(date +%Y%m%d_%H%M%S).md"
    
    cat > "$REPORT_FILE" << EOF
# Customer Mapping Setup Report - Pushing Capital

**Setup Date:** $TIMESTAMP  
**Status:** Ready for Implementation  
**System:** Customer location visualization and tracking

## 📁 Directory Structure Created

\`\`\`
customer_mapping/
├── data/                    # Customer data files
├── exports/                 # Map exports and reports
├── templates/               # Data templates
├── scripts/                 # Geocoding utilities
├── HubSpot_Export_Guide.md  # Data export instructions
├── Mapline_Setup_Instructions.md  # Mapping platform setup
└── dashboard_config.json    # Dashboard configuration
\`\`\`

## 🗺️ Mapping Platforms Available

### Option 1: Mapline (Recommended)
- **URL:** https://mapline.com
- **Features:** Real-time updates, segmentation, business analytics
- **Cost:** Varies by customer volume
- **Best For:** Business intelligence and team tracking

### Option 2: Mapbox
- **URL:** https://mapbox.com
- **Features:** Custom styling, embeddable maps, developer tools
- **Cost:** Pay-per-use API calls
- **Best For:** Website integration and custom solutions

## 📊 Service Type Mapping

### 💳 Credit Strategy (\$1,500/client)
- **Color:** Blue (#0066CC)
- **Pipeline:** Customer Pipeline
- **Stages:** Onboarding → Analysis → Strategy → Implementation

### 🚛 Vehicle Transport (Variable pricing)
- **Color:** Green (#00AA44)
- **Pipeline:** Nationwide Vehicle Transport Solutions
- **Stages:** Quote → Booked → In Transit → Delivered

### 🏠 Property Appraisal (\$450-\$650)
- **Color:** Orange (#FF8800)
- **Pipeline:** Appraisal Services
- **Stages:** Requested → Scheduled → Completed → Delivered

### 💰 Funding Services (Commission-based)
- **Color:** Purple (#8800CC)
- **Pipeline:** Funding Pipeline
- **Stages:** Application → Review → Approved → Funded

## 🚀 Implementation Steps

### Phase 1: Data Preparation (Day 1)
1. Export customer data from HubSpot CRM
2. Use provided template for data formatting
3. Geocode addresses using provided script

### Phase 2: Map Creation (Day 2-3)
1. Set up Mapline or Mapbox account
2. Import customer data
3. Configure color-coding by service type
4. Set up segmentation and filters

### Phase 3: Integration (Day 4-5)
1. Connect to HubSpot for real-time updates
2. Configure automated reporting
3. Set up team access and permissions
4. Train team on map usage

## 📈 Expected Benefits

### Customer Insights
- Geographic distribution of services
- Revenue concentration by region
- Market penetration analysis
- Customer density heat maps

### Operational Efficiency
- Territory optimization for sales reps
- Service delivery route planning
- Market expansion opportunities
- Competitor activity tracking

### Business Intelligence
- Real-time customer tracking
- Revenue visualization by location
- Performance metrics by region
- Strategic planning support

## 🎯 Next Actions

1. **Choose mapping platform** (Mapline recommended)
2. **Export HubSpot customer data** using provided guide
3. **Geocode addresses** using provided script
4. **Create initial map** with color-coded service types
5. **Set up real-time integration** with HubSpot
6. **Train team** on map usage and customer tracking

---
**Generated:** $TIMESTAMP  
**Contact:** manny@pushingcap.com for implementation support
EOF

    echo -e "${GREEN}✅ Setup report generated: $REPORT_FILE${NC}"
}

# Main setup function
main() {
    echo -e "${BLUE}Starting customer mapping setup...${NC}"
    echo ""
    
    setup_mapping_structure
    create_data_template
    create_hubspot_export_guide
    create_mapline_instructions
    create_geocoding_script
    create_dashboard_config
    generate_setup_report
    
    echo ""
    echo -e "${GREEN}🎉 Customer Mapping Setup Complete!${NC}"
    echo "=============================================="
    echo ""
    echo -e "${YELLOW}Quick Start:${NC}"
    echo "1. Export customer data from HubSpot"
    echo "2. Use customer_mapping/templates/customer_data_template.csv"
    echo "3. Choose Mapline (recommended) or Mapbox"
    echo "4. Follow setup instructions in customer_mapping/"
    echo ""
    echo -e "${BLUE}📊 Benefits:${NC}"
    echo "   • Real-time customer location tracking"
    echo "   • Service-based color coding and segmentation"
    echo "   • Revenue visualization by geographic region"
    echo "   • Territory optimization for sales team"
    echo ""
    echo -e "${GREEN}🗺️ Your customer mapping system is ready to deploy!${NC}"
}

# Run main setup
main