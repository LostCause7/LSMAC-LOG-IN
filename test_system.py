#!/usr/bin/env python3
"""
Test script for LSMAC Member Check-In System
This script tests all major components to ensure they're working correctly.
"""

import sys
import importlib
import cv2
import sqlite3
from datetime import datetime

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing module imports...")
    
    modules = [
        'cv2',
        'pyzbar',
        'PIL',
        'tkinter',
        'sqlite3',
        'threading',
        'datetime'
    ]
    
    failed_imports = []
    
    for module in modules:
        try:
            importlib.import_module(module)
            print(f"✓ {module}")
        except ImportError as e:
            print(f"✗ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\nFailed to import: {', '.join(failed_imports)}")
        print("Please install missing dependencies: pip install -r requirements.txt")
        return False
    
    print("All modules imported successfully!\n")
    return True

def test_camera():
    """Test camera access"""
    print("Testing camera access...")
    
    try:
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"✓ Camera working - Frame size: {frame.shape}")
                cap.release()
                return True
            else:
                print("✗ Camera opened but couldn't read frame")
                cap.release()
                return False
        else:
            print("✗ Could not open camera")
            return False
    except Exception as e:
        print(f"✗ Camera test failed: {e}")
        return False

def test_database():
    """Test database operations"""
    print("Testing database operations...")
    
    try:
        from database import CheckInDatabase
        
        # Test database creation
        db = CheckInDatabase("test_checkin_system.db")
        print("✓ Database created successfully")
        
        # Test member operations
        success = db.add_member("TEST001", "Test Member", "test@example.com", "123-456-7890")
        if success:
            print("✓ Member added successfully")
        else:
            print("✗ Failed to add member")
            return False
        
        # Test member retrieval
        member = db.get_member("TEST001")
        if member:
            print(f"✓ Member retrieved: {member[1]}")
        else:
            print("✗ Failed to retrieve member")
            return False
        
        # Test check-in
        success = db.record_check_in("TEST001")
        if success:
            print("✓ Check-in recorded successfully")
        else:
            print("✗ Failed to record check-in")
            return False
        
        # Clean up test database
        import os
        if os.path.exists("test_checkin_system.db"):
            os.remove("test_checkin_system.db")
            print("✓ Test database cleaned up")
        
        return True
        
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        return False

def test_barcode_scanner():
    """Test barcode scanner initialization"""
    print("Testing barcode scanner...")
    
    try:
        from barcode_scanner import BarcodeScanner
        
        scanner = BarcodeScanner()
        print("✓ Barcode scanner initialized")
        
        # Test camera start
        if scanner.start_camera():
            print("✓ Scanner camera started")
            scanner.stop_camera()
            print("✓ Scanner camera stopped")
            return True
        else:
            print("✗ Scanner camera failed to start")
            return False
            
    except Exception as e:
        print(f"✗ Barcode scanner test failed: {e}")
        return False

def test_gui_components():
    """Test GUI components"""
    print("Testing GUI components...")
    
    try:
        import tkinter as tk
        from tkinter import ttk
        
        # Test basic tkinter functionality
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Test creating basic widgets
        frame = tk.Frame(root)
        label = tk.Label(frame, text="Test")
        button = tk.Button(frame, text="Test")
        
        print("✓ Basic GUI components created")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"✗ GUI test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("LSMAC Member Check-In System - System Test")
    print("=" * 50)
    print()
    
    tests = [
        ("Module Imports", test_imports),
        ("Camera Access", test_camera),
        ("Database Operations", test_database),
        ("Barcode Scanner", test_barcode_scanner),
        ("GUI Components", test_gui_components)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 30)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your system is ready to run the check-in application.")
        print("Run 'python main.py' to start the application.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the issues above.")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main() 