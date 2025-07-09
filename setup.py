#!/usr/bin/env python3
"""
Setup script for LSMAC Member Check-In System
Handles installation and common Windows compatibility issues.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a pip command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    print("=" * 60)
    print("LSMAC Member Check-In System - Setup")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("✗ Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    
    print(f"✓ Python version: {sys.version.split()[0]}")
    
    # Upgrade pip
    run_command("python -m pip install --upgrade pip", "Upgrading pip")
    
    # Install numpy first (required for OpenCV)
    if not run_command("pip install numpy>=1.21.2", "Installing numpy"):
        return False
    
    # Install OpenCV headless (more stable on Windows)
    if not run_command("pip install opencv-python-headless", "Installing OpenCV"):
        return False
    
    # Install other dependencies
    dependencies = [
        ("pyzbar", "Installing barcode scanner"),
        ("Pillow", "Installing image processing library")
    ]
    
    for package, description in dependencies:
        if not run_command(f"pip install {package}", description):
            return False
    
    print("\n" + "=" * 60)
    print("SETUP COMPLETE!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Run 'python test_system.py' to verify installation")
    print("2. Run 'python main.py' to start the application")
    print("\nIf you encounter any issues:")
    print("- Make sure your camera is connected and not in use")
    print("- Check that you have administrator privileges")
    print("- Try running the test script first")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nSetup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nSetup failed with error: {e}")
        sys.exit(1) 