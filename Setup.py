"""
Setup script for ERP Automation Dashboard
Initializes directories and configuration
"""

import os
from pathlib import Path

def create_directory_structure():
    """Create necessary directories for the application"""
    directories = [
        'logs',
        'reports',
        'reports/csv',
        'templates',
    ]
    
    for directory in directories:
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}")
        
        # Create .gitkeep files to preserve empty directories
        if directory.startswith('reports'):
            gitkeep = path / '.gitkeep'
            gitkeep.touch(exist_ok=True)

def create_template_file():
    """Ensure dashboard.html is in templates directory"""
    template_dir = Path('templates')
    template_file = template_dir / 'dashboard.html'
    
    if not template_file.exists():
        print("⚠ Warning: templates/dashboard.html not found!")
        print("  Please copy the dashboard.html file to the templates directory")
    else:
        print("✓ Dashboard template found")

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = [
        'flask',
        'pandas',
        'numpy',
        'openpyxl',
        'schedule'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} is NOT installed")
    
    if missing_packages:
        print("\n⚠ Missing packages detected!")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def create_sample_env():
    """Create a sample .env.example file"""
    env_example = Path('.env.example')
    
    if not env_example.exists():
        content = """# ERP Automation Configuration
# Copy this file to .env and update with your settings

# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development

# Database Configuration (for production)
# DB_SERVER=your-sql-server
# DB_NAME=ERP_DB
# DB_USER=your-username
# DB_PASSWORD=your-password

# Scheduling
DAILY_REPORT_TIME=08:00
REFRESH_INTERVAL_HOURS=1

# Reports
KEEP_REPORTS_DAYS=30
"""
        env_example.write_text(content)
        print("✓ Created .env.example file")
    else:
        print("✓ .env.example already exists")

def main():
    """Main setup function"""
    print("=" * 50)
    print("ERP Automation Dashboard - Setup")
    print("=" * 50)
    print()
    
    print("1. Creating directory structure...")
    create_directory_structure()
    print()
    
    print("2. Checking template files...")
    create_template_file()
    print()
    
    print("3. Creating sample environment file...")
    create_sample_env()
    print()
    
    print("4. Checking dependencies...")
    dependencies_ok = check_dependencies()
    print()
    
    if dependencies_ok:
        print("=" * 50)
        print("✓ Setup completed successfully!")
        print("=" * 50)
        print()
        print("Next steps:")
        print("1. Copy .env.example to .env and configure settings")
        print("2. Update database connection in config.py (if needed)")
        print("3. Run the application: python app.py")
        print("4. Open browser: http://localhost:5000")
    else:
        print("=" * 50)
        print("⚠ Setup incomplete - please install missing packages")
        print("=" * 50)
        print()
        print("Run: pip install -r requirements.txt")

if __name__ == '__main__':
    main()
