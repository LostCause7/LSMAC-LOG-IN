#!/bin/bash

# LSMAC QR Generator - Web App Launcher for Chrome OS
# This script runs the web version of the QR generator

echo "================================================"
echo "LSMAC QR Generator - Web App Launcher"
echo "================================================"
echo

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed"
    echo "Installing Python3..."
    sudo apt update
    sudo apt install -y python3 python3-pip
fi

# Check if Flask is installed
echo "📦 Checking dependencies..."
python3 -c "import flask, qrcode, requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing missing dependencies..."
    pip3 install flask qrcode[pil] requests
fi

echo "✅ Dependencies ready"
echo
echo "🚀 Starting LSMAC QR Generator Web Server..."
echo "📱 Opening browser automatically..."
echo "🛑 Press Ctrl+C to stop the server"
echo

# Run the web app
python3 web_qr_generator.py 