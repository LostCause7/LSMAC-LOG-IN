#!/usr/bin/env python3
"""
LSMAC QR Generator - Web App Launcher for Chrome OS
"""

import os
import sys
import subprocess
import webbrowser
import threading
import time

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import qrcode
        import requests
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Installing dependencies...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "flask", "qrcode[pil]", "requests"], check=True)
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            return False

def run_web_server():
    """Run the web server"""
    print("🚀 Starting LSMAC QR Generator Web Server...")
    print("📱 Opening browser automatically...")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Import and run the web app
        from web_qr_generator import app
        
        # Open browser after a short delay
        def open_browser():
            time.sleep(2)  # Wait for server to start
            webbrowser.open('http://localhost:5000')
        
        # Start browser in a separate thread
        threading.Thread(target=open_browser, daemon=True).start()
        
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    """Main function"""
    print("=" * 50)
    print("LSMAC QR Generator - Web App")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("web_qr_generator.py"):
        print("❌ Error: web_qr_generator.py not found")
        print("Please run this script from the lsmac_qr_generator_chromebook directory")
        return
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Run the web server
    run_web_server()

if __name__ == "__main__":
    main() 