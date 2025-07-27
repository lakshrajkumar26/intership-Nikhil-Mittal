#!/usr/bin/env python3
"""
Portfolio Analyzer Setup Script
Automatically installs dependencies and validates the setup
"""

import subprocess
import sys
import os

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required packages"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def check_files():
    """Check if required files exist"""
    required_files = [
        "portfolio_analyzer.py",
        "app.py", 
        "requirements.txt",
        "Stock_trading_2023.csv",
        "Stock_trading_2024.csv",
        "Stock_trading_2025.csv"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files found")
    return True

def main():
    """Main setup function"""
    print("🚀 Portfolio Analyzer Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Check required files
    if not check_files():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run: python -m streamlit run app.py --server.port 8501")
    print("2. Open: http://localhost:8501")
    print("3. Click 'Run Portfolio Analysis' in the sidebar")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 