
# ERP Data Automation Dashboard - Overview and Project Structure
    Built automated MIS and production dashboard system connecting directly to ERP SQL backend, replacing manual Excel-based reporting
    Integrated Power BI with ERP database for live dashboards tracking purchase, production, packing, and shipment metrics in real-time
    Automated data extraction and cleanup using Python (pyodbc, pandas) with scheduled report refreshes and CSV generation
    Reduced manual data handling errors and saved 2+ hours daily for management team
## 📁 Complete Directory Structure
    An automated ERP data extraction and visualization system built with Python, Flask, and Power BI integration capabilities. This system eliminates manual data handling, provides real-time dashboards, and generates    automated reports for purchase, production, packing, and shipment departments.
    ✨ Features
    
    Automated Data Extraction: Connects to ERP backend database and extracts data automatically
    Real-time Dashboard: Web-based dashboard showing key metrics and KPIs
    Multi-threaded Processing: Uses threading for efficient data processing
    Scheduled Reports: Automatic daily and hourly report generation
    Excel & CSV Exports: Generate formatted Excel reports and CSV files
    Department-wise Views: Separate views for Purchase, Production, Packing, and Shipment
    Comprehensive Logging: Full logging system for monitoring and debugging
    REST API: RESTful API endpoints for data access and integration
```
erp-automation/
│
├── app.py                      # Main application with Flask server and scheduler
├── config.py                   # Configuration settings
├── data_extractor.py           # ERP data extraction module
├── report_generator.py         # Excel and CSV report generation
├── setup.py                    # Setup and initialization script
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
├── .env.example               # Environment variables template
├── README.md                   # Project documentation
├── PROJECT_STRUCTURE.md        # This file
│
├── templates/
│   └── dashboard.html         # Main dashboard UI template
│
├── logs/
│   ├── .gitkeep
│   └── erp_automation.log     # Application logs (auto-generated)
│
└── reports/
    ├── .gitkeep
    ├── daily_report.xlsx      # Latest Excel report (auto-generated)
    ├── daily_report_*.xlsx    # Timestamped Excel reports
    └── csv/
        ├── .gitkeep
        ├── purchase_data.csv      # Latest CSV exports
        ├── production_data.csv
        ├── packing_data.csv
        ├── shipment_data.csv
        └── *_*.csv               # Timestamped CSV exports
```

## 📄 File Descriptions

### Core Application Files

#### `app.py`
**Purpose**: Main application entry point
**Key Components**:
- Flask application initialization
- ERPAutomationSystem class (orchestrator)
- Threaded scheduler for automated jobs
- REST API endpoints
- Global data state management with thread-safe locking

**Key Features**:
- Multi-threaded data processing
- Scheduled report generation (daily at 8 AM, hourly refresh)
- REST API for dashboard and integrations
- Health check endpoint

**Main Classes/Functions**:
```python
class ERPAutomationSystem:
    - fetch_and_process_data()    # Main data processing
    - schedule_jobs()              # Setup scheduled tasks
    - run_scheduler()              # Scheduler thread
    - start() / stop()             # Lifecycle management

Flask Routes:
    - / (dashboard)
    - /api/summary
    - /api/department/<dept_name>
    - /api/refresh
    - /api/download/<report_type>
    - /health
```

#### `config.py`
**Purpose**: Centralized configuration management
**Contains**:
- Flask settings (SECRET_KEY, etc.)
- Database connection parameters
- Report directory paths
- Scheduling configuration
- Dashboard customization

**Usage**:
```python
from config import Config
app.config.from_object(Config)
```

#### `data_extractor.py`
**Purpose**: Extract data from ERP database
**Key Components**:
- Database connection management
- SQL query execution
- Data transformation and cleaning
- Demo data generation (for development)

**Main Class**:
```python
class ERPDataExtractor:
    - get_purchase_data()     # Extract purchase orders
    - get_production_data()   # Extract production data
    - get_packing_data()      # Extract packing data
    - get_shipment_data()     # Extract shipment data
    - _execute_query()        # Execute SQL queries
```

**For Production**: Uncomment database connection code and replace demo data generation with actual SQL queries.

#### `report_generator.py`
**Purpose**: Generate formatted reports
**Key Components**:
- Excel report generation with multiple sheets
- CSV export functionality
- Professional Excel formatting
- Summary sheet creation
- Old report cleanup

**Main Class**:
```python
class ReportGenerator:
    - generate_excel_reports()       # Create Excel workbook
    - generate_csv_exports()         # Export CSV files
    - _format_excel_sheet()          # Apply Excel styling
    - _create_summary()              # Generate summary data
    - cleanup_old_reports()          # Remove old files
```

**Excel Features**:
- Professional formatting with colors
- Auto-adjusted column widths
- Header row freeze
- Multiple department sheets
- Summary dashboard sheet

#### `setup.py`
**Purpose**: Initialize project structure
**Features**:
- Create necessary directories
- Check dependencies
- Verify template files
- Create sample environment file

**Usage**:
```bash
python setup.py
```

### Frontend Files

#### `templates/dashboard.html`
**Purpose**: Web-based dashboard interface
**Features**:
- Responsive design
- Real-time data updates
- Department-wise data tables
- Summary statistics cards
- Download buttons for reports
- Auto-refresh functionality

**Main Sections**:
- Header with last update time
- Statistics grid (4 department cards)
- Tabbed department data view
- Download section
- JavaScript for API interaction

**Technologies Used**:
- Vanilla JavaScript (no frameworks)
- CSS3 with gradient backgrounds
- Fetch API for AJAX calls
- Responsive grid layout

## 🔄 Data Flow

```
1. Scheduler Thread (Background)
   └── Triggers fetch_and_process_data() every hour
       └── ERPDataExtractor.get_*_data()
           └── Executes SQL queries / Generates demo data
               └── Returns pandas DataFrames
                   └── Updates global latest_data (thread-safe)
                       └── ReportGenerator.generate_excel_reports()
                       └── ReportGenerator.generate_csv_exports()

2. Dashboard Request Flow
   └── User opens http://localhost:5000/
       └── Flask serves dashboard.html
           └── JavaScript calls /api/summary
               └── Returns summary statistics
                   └── JavaScript calls /api/department/purchase
                       └── Returns department data
                           └── Renders tables and charts

3. Manual Refresh Flow
   └── User clicks Refresh button
       └── POST /api/refresh
           └── Spawns thread to run fetch_and_process_data()
               └── Returns immediate response
                   └── Background process updates data
```

## 🧵 Threading Architecture

```
Main Thread
├── Flask Application
│   ├── API Endpoints (handles requests)
│   └── Template Rendering
│
└── Scheduler Thread (Daemon)
    ├── schedule.run_pending()
    └── Triggers data processing jobs
        └── fetch_and_process_data()
            ├── Data Extraction (sequential)
            └── Report Generation (sequential)
```

**Thread Safety**:
- `data_lock` (threading.Lock) protects `latest_data` dictionary
- All reads/writes to shared data use context manager: `with data_lock:`

## 📊 Data Models

### Purchase Data
```python
{
    'po_id': str,
    'vendor_name': str,
    'item_name': str,
    'quantity': int,
    'unit_price': float,
    'amount': float,
    'order_date': datetime,
    'delivery_date': datetime,
    'status': str  # 'Pending', 'Approved', 'Delivered'
}
```

### Production Data
```python
{
    'production_id': str,
    'product_name': str,
    'batch_no': str,
    'quantity': int,
    'unit': str,
    'start_date': datetime,
    'end_date': datetime,
    'status': str,  # 'Completed', 'In Progress', 'Pending'
    'department': str
}
```

### Packing Data
```python
{
    'packing_id': str,
    'product_name': str,
    'quantity': int,
    'package_type': str,
    'packing_date': datetime,
    'status': str,
    'operator': str
}
```

### Shipment Data
```python
{
    'shipment_id': str,
    'customer_name': str,
    'destination': str,
    'quantity': int,
    'shipment_date': datetime,
    'expected_delivery': datetime,
    'status': str,  # 'Dispatched', 'In Transit', 'Pending', 'Delivered'
    'transporter': str
}
```

## 🔌 API Reference

### GET /api/summary
Returns summary statistics for all departments.

**Response**:
```json
{
  "purchase": {
    "total_orders": 50,
    "total_amount": 125000.50,
    "pending": 15
  },
  "production": {
    "total_units": 15000,
    "completed": 30,
    "in_progress": 18
  },
  "packing": {...},
  "shipment": {...},
  "last_updated": "2024-11-10 14:30:00"
}
```

### GET /api/department/{dept_name}
Returns detailed data for specified department.

**Parameters**: 
- `dept_name`: purchase | production | packing | shipment

**Response**:
```json
{
  "data": [
    {
      "po_id": "PO0001",
      "vendor_name": "Vendor A",
      ...
    }
  ],
  "count": 50
}
```

### POST /api/refresh
Manually triggers data refresh.

**Response**:
```json
{
  "status": "Refresh initiated"
}
```

### GET /api/download/{report_type}
Downloads generated reports.

**Parameters**:
- `report_type`: excel | purchase_csv | production_csv | packing_csv | shipment_csv

**Returns**: File download

### GET /health
Health check endpoint.

**Response**:
```json
{
  "status": "healthy",
  "system_running": true,
  "last_update": "2024-11-10T14:30:00"
}
```

## 🔧 Customization Guide

### Adding New Departments

1. **Add extraction method in `data_extractor.py`**:
```python
def get_quality_data(self) -> pd.DataFrame:
    # Your SQL query or data generation
    pass
```

2. **Update `app.py` to include new department**:
```python
quality_data = self.extractor.get_quality_data()
latest_data['quality'] = quality_data
```

3. **Add to report generation**:
```python
quality_df.to_excel(writer, sheet_name='Quality', index=False)
```

4. **Update dashboard HTML** with new tab and data view

### Modifying Schedule

In `app.py`, modify `schedule_jobs()`:
```python
# Daily at specific time
schedule.every().day.at("06:00").do(self.fetch_and_process_data)

# Every X hours
schedule.every(2).hours.do(self.fetch_and_process_data)

# Every weekday
schedule.every().monday.at("09:00").do(self.fetch_and_process_data)
```

### Custom Report Formatting

In `report_generator.py`, modify `_format_excel_sheet()`:
```python
# Change header color
header_fill = PatternFill(start_color="YOUR_COLOR", ...)

# Modify font
header_font = Font(bold=True, size=12, ...)

# Conditional formatting
if cell.value > 1000:
    cell.fill = PatternFill(start_color="FF0000", ...)
```

## 🐛 Debugging

### Enable Debug Logging
```python
logging.basicConfig(level=logging.DEBUG)
```

### Check Scheduler Status
```python
# In app.py
print(f"Running: {erp_system.running}")
print(f"Jobs: {schedule.jobs}")
```

### Test Individual Components
```python
# Test data extraction
extractor = ERPDataExtractor()
df = extractor.get_purchase_data()
print(df.head())

# Test report generation
report_gen = ReportGenerator()
report_gen.generate_excel_reports(df1, df2, df3, df4)
```

## 📚 Dependencies Explanation

| Package | Purpose |
|---------|---------|
| Flask | Web framework for dashboard and API |
| pandas | Data manipulation and analysis |
| numpy | Numerical operations |
| openpyxl | Excel file generation and formatting |
| schedule | Job scheduling functionality |
| pyodbc | SQL Server database connectivity |

## 🚀 Quick Start Commands

```bash
# Setup
python setup.py

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py

# Access dashboard
open http://localhost:5000

# Check logs
tail -f logs/erp_automation.log
```

---

