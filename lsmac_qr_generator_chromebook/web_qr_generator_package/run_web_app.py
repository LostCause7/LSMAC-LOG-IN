#!/usr/bin/env python3
"""
LSMAC QR Generator - Chromebook Web Launcher
Optimized for Chrome OS deployment
"""

import os
import sys
import subprocess
import webbrowser
import threading
import time
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def start_web_server():
    """Start the Flask web server"""
    print("🚀 Starting LSMAC QR Generator Web Server...")
    print("🌐 Server will be available at: http://localhost:5000")
    print("📱 Optimized for Chromebook browser")
    
    # Import and run the web app
    from web_qr_generator import app
    
    # Open browser after delay
    def open_browser():
        time.sleep(3)  # Wait for server to start
        try:
            webbrowser.open('http://localhost:5000')
            print("✅ Browser opened automatically")
        except Exception as e:
            print(f"⚠️  Could not open browser automatically: {e}")
            print("📋 Please manually navigate to: http://localhost:5000")
    
    # Start browser in background
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)

def main():
    """Main launcher function"""
    print("=" * 50)
    print("🎯 LSMAC QR Generator - Chromebook Edition")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install requirements
    if not install_requirements():
        return
    
    # Start web server
    try:
        start_web_server()
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    main() 