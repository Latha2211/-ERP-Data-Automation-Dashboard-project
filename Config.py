"""
Configuration settings for ERP Automation System
"""

import os
from pathlib import Path

class Config:
    """Application configuration"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database settings (for real ERP connection)
    # Uncomment and configure when connecting to actual SQL Server
    # DB_SERVER = os.environ.get('DB_SERVER', 'localhost')
    # DB_NAME = os.environ.get('DB_NAME', 'ERP_DB')
    # DB_USER = os.environ.get('DB_USER', 'erp_user')
    # DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
    # DB_DRIVER = '{ODBC Driver 17 for SQL Server}'
    
    # Report settings
    REPORT_DIR = Path('reports')
    CSV_DIR = Path('reports/csv')
    LOG_DIR = Path('logs')
    
    # Schedule settings
    DAILY_REPORT_TIME = "08:00"
    REFRESH_INTERVAL_HOURS = 1
    
    # Data retention
    KEEP_REPORTS_DAYS = 30
    
    # Dashboard settings
    ITEMS_PER_PAGE = 50
    CHART_COLORS = {
        'purchase': '#3498db',
        'production': '#2ecc71',
        'packing': '#f39c12',
        'shipment': '#e74c3c'
    }
