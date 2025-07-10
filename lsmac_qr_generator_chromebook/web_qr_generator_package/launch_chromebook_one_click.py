#!/usr/bin/env python3
"""
LSMAC QR Generator - One-Click Chromebook Launcher
Handles everything automatically: dependencies, setup, and launch
"""

import os
import sys
import subprocess
import webbrowser
import threading
import time
import platform
import shutil
from pathlib import Path

def print_banner():
    """Print the application banner"""
    print("=" * 60)
    print("🎯 LSMAC QR Generator - Chromebook Edition")
    print("=" * 60)
    print("📱 One-Click Setup & Launch")
    print("🌐 Web-based QR Code Generation System")
    print("=" * 60)
    print()

def check_system():
    """Check if running on Chromebook"""
    print("🔍 Checking system compatibility...")
    
    # Check OS
    system = platform.system()
    print(f"✅ Operating System: {system}")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major >= 3 and python_version.minor >= 7:
        print(f"✅ Python Version: {python_version.major}.{python_version.minor}")
    else:
        print(f"❌ Python Version: {python_version.major}.{python_version.minor} (Need 3.7+)")
        return False
    
    # Check if we're on Chromebook
    if os.path.exists('/etc/chrome_dev.conf'):
        print("✅ Chromebook detected")
    else:
        print("⚠️  Not running on Chromebook (will still work)")
    
    return True

def install_dependencies():
    """Install all required Python packages"""
    print("📦 Installing dependencies...")
    
    try:
        # Upgrade pip first
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ Pip upgraded")
        
        # Install requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ Dependencies installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        print("🔄 Trying alternative installation method...")
        
        try:
            # Install packages individually
            packages = ["Flask==2.3.3", "qrcode[pil]==7.4.2", "requests==2.31.0", "Pillow==10.0.1"]
            for package in packages:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("✅ Dependencies installed via alternative method")
            return True
        except subprocess.CalledProcessError as e2:
            print(f"❌ Failed to install dependencies: {e2}")
            return False

def check_port_availability():
    """Check if port 5000 is available"""
    print("🔌 Checking port availability...")
    
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 5000))
        sock.close()
        
        if result == 0:
            print("⚠️  Port 5000 is already in use")
            print("🔄 Attempting to stop existing processes...")
            
            # Try to kill existing processes
            try:
                if platform.system() == "Windows":
                    subprocess.run(["taskkill", "/f", "/im", "python.exe"], 
                                 capture_output=True, text=True)
                else:
                    subprocess.run(["pkill", "-f", "web_qr_generator"], 
                                 capture_output=True, text=True)
                time.sleep(2)
                print("✅ Existing processes stopped")
            except:
                print("⚠️  Could not stop existing processes")
                return False
        else:
            print("✅ Port 5000 is available")
        
        return True
    except Exception as e:
        print(f"❌ Error checking port: {e}")
        return False

def test_installation():
    """Test if all components are working"""
    print("🧪 Testing installation...")
    
    try:
        # Test imports
        import flask
        import qrcode
        import requests
        from PIL import Image
        print("✅ All Python packages imported successfully")
        
        # Test QR code generation
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data("TEST")
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        print("✅ QR code generation test passed")
        
        return True
    except Exception as e:
        print(f"❌ Installation test failed: {e}")
        return False

def create_desktop_shortcut():
    """Create a desktop shortcut for easy access"""
    try:
        desktop_path = os.path.expanduser("~/Desktop")
        shortcut_path = os.path.join(desktop_path, "LSMAC-QR-Generator.desktop")
        
        # Get the current script path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(current_dir, "launch_chromebook_one_click.py")
        
        shortcut_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=LSMAC QR Generator
Comment=Web-based QR code generation system
Exec=python3 "{script_path}"
Icon=applications-internet
Terminal=true
Categories=Office;Network;WebBrowser;
Keywords=QR;Code;Generator;Member;Management;
StartupNotify=true
StartupWMClass=LSMAC-QR-Generator
"""
        
        with open(shortcut_path, 'w') as f:
            f.write(shortcut_content)
        
        # Make executable
        os.chmod(shortcut_path, 0o755)
        print("✅ Desktop shortcut created")
        print("📱 You can now double-click the 'LSMAC QR Generator' icon on your desktop")
        
    except Exception as e:
        print(f"⚠️  Could not create desktop shortcut: {e}")

def start_web_server():
    """Start the Flask web server"""
    print("🚀 Starting LSMAC QR Generator Web Server...")
    print("🌐 Server will be available at: http://localhost:5000")
    print("📱 Optimized for Chromebook browser")
    print()
    print("💡 Tips:")
    print("   - Use Ctrl+C to stop the server")
    print("   - The browser should open automatically")
    print("   - If browser doesn't open, go to: http://localhost:5000")
    print("   - Double-click the desktop icon for future launches")
    print()
    
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
    
    # Import and run the web app
    try:
        from web_qr_generator import app
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    """Main launcher function"""
    print_banner()
    
    # Step 1: Check system compatibility
    if not check_system():
        print("❌ System compatibility check failed")
        return
    
    # Step 2: Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        return
    
    # Step 3: Check port availability
    if not check_port_availability():
        print("❌ Port 5000 is not available")
        return
    
    # Step 4: Test installation
    if not test_installation():
        print("❌ Installation test failed")
        return
    
    # Step 5: Create desktop shortcut (only on first run)
    desktop_shortcut_path = os.path.expanduser("~/Desktop/LSMAC-QR-Generator.desktop")
    if not os.path.exists(desktop_shortcut_path):
        create_desktop_shortcut()
    else:
        print("✅ Desktop shortcut already exists")
    
    # Step 6: Start the web server
    print("🎉 All checks passed! Starting the application...")
    print()
    start_web_server()

if __name__ == "__main__":
    main() 