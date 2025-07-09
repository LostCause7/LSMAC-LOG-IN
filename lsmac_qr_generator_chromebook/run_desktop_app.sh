#!/bin/bash

# LSMAC QR Generator - Desktop App Launcher for Chrome OS
# This script runs the desktop version of the QR generator

echo "================================================"
echo "LSMAC QR Generator - Desktop App Launcher"
echo "================================================"
echo

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed"
    echo "Installing Python3..."
    sudo apt update
    sudo apt install -y python3 python3-pip python3-tk
fi

# Check if required packages are installed
echo "📦 Checking dependencies..."
python3 -c "import tkinter, qrcode, requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing missing dependencies..."
    pip3 install qrcode[pil] pillow requests
fi

echo "✅ Dependencies ready"
echo
echo "🚀 Starting LSMAC QR Generator Desktop App..."
echo "🛑 Press Ctrl+C to stop the app"
echo

# Run the desktop app
python3 qr_generator_chromebook.py 