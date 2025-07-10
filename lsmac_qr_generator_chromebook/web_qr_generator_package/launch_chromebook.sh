#!/bin/bash

# LSMAC QR Generator - Chromebook Launcher Script
# This script sets up and runs the web QR generator on Chromebook

echo "🎯 LSMAC QR Generator - Chromebook Edition"
echo "=============================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Installing..."
    sudo apt update
    sudo apt install -y python3 python3-pip
fi

# Check Python version
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✅ Python $PYTHON_VERSION detected"

# Upgrade pip
echo "📦 Upgrading pip..."
python3 -m pip install --upgrade pip

# Install requirements
echo "📦 Installing required packages..."
if python3 -m pip install -r requirements.txt; then
    echo "✅ Packages installed successfully"
else
    echo "❌ Failed to install packages. Trying alternative method..."
    python3 -m pip install Flask qrcode[pil] requests Pillow
fi

# Check if port 5000 is in use
if lsof -i :5000 &> /dev/null; then
    echo "⚠️  Port 5000 is already in use. Stopping existing process..."
    sudo pkill -f "python.*web_qr_generator"
    sleep 2
fi

# Start the web server
echo "🚀 Starting LSMAC QR Generator Web Server..."
echo "🌐 Server will be available at: http://localhost:5000"
echo "📱 Optimized for Chromebook browser"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the web application
python3 run_web_app.py 