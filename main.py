"""
ERP Data Automation Dashboard
Main Application Entry Point
Author: Your Name
Description: Automated ERP data extraction and dashboard generation system
"""

import logging
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import pandas as pd
import schedule
from flask import Flask, render_template, jsonify, send_file
from data_extractor import ERPDataExtractor
from report_generator import ReportGenerator
from config import Config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/erp_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Global state
data_lock = threading.Lock()
latest_data = {
    'purchase': None,
    'production': None,
    'packing': None,
    'shipment': None,
    'last_updated': None
}

class ERPAutomationSystem:
    """Main automation system orchestrator"""
    
    def __init__(self):
        self.extractor = ERPDataExtractor()
        self.report_gen = ReportGenerator()
        self.running = False
        self.scheduler_thread = None
        logger.info("ERP Automation System initialized")
    
    def fetch_and_process_data(self):
        """Fetch data from ERP and process it"""
        global latest_data
        
        logger.info("Starting data fetch and processing...")
        try:
            # Extract data from ERP
            purchase_data = self.extractor.get_purchase_data()
            production_data = self.extractor.get_production_data()
            packing_data = self.extractor.get_packing_data()
            shipment_data = self.extractor.get_shipment_data()
            
            # Update global state
            with data_lock:
                latest_data['purchase'] = purchase_data
                latest_data['production'] = production_data
                latest_data['packing'] = packing_data
                latest_data['shipment'] = shipment_data
                latest_data['last_updated'] = datetime.now()
            
            # Generate reports
            self.report_gen.generate_excel_reports(
                purchase_data, production_data, packing_data, shipment_data
            )
            self.report_gen.generate_csv_exports(
                purchase_data, production_data, packing_data, shipment_data
            )
            
            logger.info("Data processing completed successfully")
            
        except Exception as e:
            logger.error(f"Error in data processing: {str(e)}", exc_info=True)
    
    def schedule_jobs(self):
        """Schedule automated jobs"""
        # Schedule daily report at 8 AM
        schedule.every().day.at("08:00").do(self.fetch_and_process_data)
        
        # Schedule hourly refresh
        schedule.every().hour.do(self.fetch_and_process_data)
        
        logger.info("Jobs scheduled: Daily at 8 AM and hourly refresh")
    
    def run_scheduler(self):
        """Run the scheduler in a separate thread"""
        self.running = True
        logger.info("Scheduler thread started")
        
        while self.running:
            schedule.run_pending()
            time.sleep(60)
        
        logger.info("Scheduler thread stopped")
    
    def start(self):
        """Start the automation system"""
        # Initial data fetch
        self.fetch_and_process_data()
        
        # Setup and start scheduler
        self.schedule_jobs()
        self.scheduler_thread = threading.Thread(target=self.run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        logger.info("Automation system started")
    
    def stop(self):
        """Stop the automation system"""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        logger.info("Automation system stopped")

# Initialize the system
erp_system = ERPAutomationSystem()

# Flask Routes
@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/summary')
def get_summary():
    """Get summary statistics"""
    with data_lock:
        if not latest_data['last_updated']:
            return jsonify({'error': 'No data available'}), 404
        
        summary = {
            'purchase': {
                'total_orders': len(latest_data['purchase']),
                'total_amount': latest_data['purchase']['amount'].sum(),
                'pending': len(latest_data['purchase'][latest_data['purchase']['status'] == 'Pending'])
            },
            'production': {
                'total_units': latest_data['production']['quantity'].sum(),
                'completed': len(latest_data['production'][latest_data['production']['status'] == 'Completed']),
                'in_progress': len(latest_data['production'][latest_data['production']['status'] == 'In Progress'])
            },
            'packing': {
                'total_packed': latest_data['packing']['quantity'].sum(),
                'completed': len(latest_data['packing'][latest_data['packing']['status'] == 'Completed'])
            },
            'shipment': {
                'total_shipments': len(latest_data['shipment']),
                'dispatched': len(latest_data['shipment'][latest_data['shipment']['status'] == 'Dispatched']),
                'pending': len(latest_data['shipment'][latest_data['shipment']['status'] == 'Pending'])
            },
            'last_updated': latest_data['last_updated'].strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return jsonify(summary)

@app.route('/api/department/<dept_name>')
def get_department_data(dept_name):
    """Get data for a specific department"""
    with data_lock:
        if not latest_data['last_updated']:
            return jsonify({'error': 'No data available'}), 404
        
        data_map = {
            'purchase': latest_data['purchase'],
            'production': latest_data['production'],
            'packing': latest_data['packing'],
            'shipment': latest_data['shipment']
        }
        
        if dept_name not in data_map:
            return jsonify({'error': 'Invalid department'}), 400
        
        df = data_map[dept_name]
        return jsonify({
            'data': df.to_dict(orient='records'),
            'count': len(df)
        })

@app.route('/api/refresh', methods=['POST'])
def refresh_data():
    """Manually trigger data refresh"""
    thread = threading.Thread(target=erp_system.fetch_and_process_data)
    thread.start()
    return jsonify({'status': 'Refresh initiated'})

@app.route('/api/download/<report_type>')
def download_report(report_type):
    """Download generated reports"""
    file_map = {
        'excel': 'reports/daily_report.xlsx',
        'purchase_csv': 'reports/csv/purchase_data.csv',
        'production_csv': 'reports/csv/production_data.csv',
        'packing_csv': 'reports/csv/packing_data.csv',
        'shipment_csv': 'reports/csv/shipment_data.csv'
    }
    
    if report_type not in file_map:
        return jsonify({'error': 'Invalid report type'}), 400
    
    file_path = Path(file_map[report_type])
    if not file_path.exists():
        return jsonify({'error': 'Report not found'}), 404
    
    return send_file(file_path, as_attachment=True)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'system_running': erp_system.running,
        'last_update': latest_data['last_updated'].isoformat() if latest_data['last_updated'] else None
    })

def create_directories():
    """Create necessary directories"""
    Path('logs').mkdir(exist_ok=True)
    Path('reports').mkdir(exist_ok=True)
    Path('reports/csv').mkdir(exist_ok=True)
    Path('templates').mkdir(exist_ok=True)

if __name__ == '__main__':
    try:
        logger.info("Starting ERP Automation Dashboard...")
        create_directories()
        
        # Start the automation system
        erp_system.start()
        
        # Start Flask app
        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
        
    except KeyboardInterrupt:
        logger.info("Shutdown requested...")
        erp_system.stop()
    except Exception as e:
        logger.error(f"Application error: {str(e)}", exc_info=True)
    finally:
        logger.info("Application shutdown complete")
