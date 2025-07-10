#!/usr/bin/env python3
"""
LSMAC QR Generator - Package Test Script
Tests the installation and basic functionality
"""

import sys
import importlib
import requests
import json

def test_python_version():
    """Test Python version compatibility"""
    print("🐍 Testing Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} is too old. Need 3.7+")
        return False

def test_dependencies():
    """Test if all required dependencies are installed"""
    print("📦 Testing dependencies...")
    
    dependencies = [
        ('flask', 'Flask'),
        ('qrcode', 'QRCode'),
        ('requests', 'requests'),
        ('PIL', 'Pillow')
    ]
    
    all_good = True
    for module_name, display_name in dependencies:
        try:
            importlib.import_module(module_name)
            print(f"✅ {display_name} is installed")
        except ImportError:
            print(f"❌ {display_name} is missing")
            all_good = False
    
    return all_good

def test_supabase_connection():
    """Test connection to Supabase database"""
    print("🌐 Testing Supabase connection...")
    
    SUPABASE_URL = "https://xbqunvlxqvpmacjcrasc.supabase.co"
    API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhicXVudmx4cXZwbWFjamNyYXNjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTIwMjQ0MjUsImV4cCI6MjA2NzYwMDQyNX0.DcGWWatFg2faO6g7iBEiyjKb4pxlKwHrya005nZ4Pns"
    
    headers = {
        "apikey": API_KEY,
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{SUPABASE_URL}/rest/v1/members?select=count", headers=headers)
        if response.status_code == 200:
            print("✅ Supabase connection successful")
            return True
        else:
            print(f"❌ Supabase connection failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Supabase connection error: {e}")
        return False

def test_qr_generation():
    """Test QR code generation functionality"""
    print("📱 Testing QR code generation...")
    
    try:
        import qrcode
        import io
        import base64
        
        # Create a test QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4
        )
        qr.add_data("TEST_MEMBER_123")
        qr.make(fit=True)
        
        # Create image
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        img_buffer = io.BytesIO()
        qr_image.save(img_buffer, format='PNG')
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        
        if img_str:
            print("✅ QR code generation successful")
            return True
        else:
            print("❌ QR code generation failed")
            return False
            
    except Exception as e:
        print(f"❌ QR code generation error: {e}")
        return False

def test_flask_app():
    """Test Flask app import and basic setup"""
    print("🌐 Testing Flask application...")
    
    try:
        # Import the web app
        from web_qr_generator import app
        
        # Test basic app properties
        if hasattr(app, 'routes') or hasattr(app, 'url_map'):
            print("✅ Flask app loaded successfully")
            return True
        else:
            print("❌ Flask app structure is invalid")
            return False
            
    except Exception as e:
        print(f"❌ Flask app error: {e}")
        return False

def test_port_availability():
    """Test if port 5000 is available"""
    print("🔌 Testing port availability...")
    
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 5000))
        sock.close()
        
        if result == 0:
            print("⚠️  Port 5000 is already in use")
            return False
        else:
            print("✅ Port 5000 is available")
            return True
            
    except Exception as e:
        print(f"❌ Port test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 LSMAC QR Generator - Package Test")
    print("=" * 40)
    print()
    
    tests = [
        ("Python Version", test_python_version),
        ("Dependencies", test_dependencies),
        ("Supabase Connection", test_supabase_connection),
        ("QR Generation", test_qr_generation),
        ("Flask App", test_flask_app),
        ("Port Availability", test_port_availability)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 Test Results Summary:")
    print("=" * 40)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Package is ready to use.")
        print("\nTo start the application:")
        print("  python3 run_web_app.py")
        print("  or")
        print("  ./launch_chromebook.sh")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\nCommon fixes:")
        print("  - Install missing dependencies: pip3 install -r requirements.txt")
        print("  - Check internet connection for Supabase test")
        print("  - Stop other applications using port 5000")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 