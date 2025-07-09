#!/bin/bash

# LSMAC QR Generator - Complete Chrome OS Setup Script
# This script sets up everything needed to run the QR generator on Chrome OS

echo "================================================"
echo "LSMAC QR Generator - Chrome OS Setup"
echo "================================================"
echo

# Check if we're in the right directory
if [ ! -f "qr_generator_chromebook.py" ]; then
    echo "❌ Error: qr_generator_chromebook.py not found"
    echo "Please run this script from the lsmac_qr_generator_chromebook directory"
    exit 1
fi

# Update package list
echo "📦 Updating package list..."
sudo apt update

# Install Python and required packages
echo "🐍 Installing Python and dependencies..."
sudo apt install -y python3 python3-pip python3-tk

# Install Python dependencies
echo "📚 Installing Python packages..."
pip3 install qrcode[pil] pillow requests flask

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x run_desktop_app.sh
chmod +x run_web_app.sh
chmod +x setup_chromebook.sh

# Create desktop shortcut
echo "🖥️ Creating desktop shortcut..."
cat > ~/Desktop/LSMAC-QR-Generator.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=LSMAC QR Generator
Comment=Generate QR codes for LSMAC members
Exec=python3 $(pwd)/qr_generator_chromebook.py
Icon=applications-graphics
Terminal=false
Categories=Graphics;Office;
EOF

chmod +x ~/Desktop/LSMAC-QR-Generator.desktop

# Create web app shortcut
cat > ~/Desktop/LSMAC-QR-Web.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=LSMAC QR Web
Comment=Web-based QR code generator
Exec=python3 $(pwd)/web_qr_generator.py
Icon=applications-internet
Terminal=true
Categories=Network;Graphics;
EOF

chmod +x ~/Desktop/LSMAC-QR-Web.desktop

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To run the desktop app:"
echo "   • Double-click the desktop shortcut, or"
echo "   • Run: ./run_desktop_app.sh"
echo "   • Run: python3 qr_generator_chromebook.py"
echo ""
echo "🌐 To run the web app:"
echo "   • Double-click the web shortcut, or"
echo "   • Run: ./run_web_app.sh"
echo "   • Run: python3 web_qr_generator.py"
echo ""
echo "📁 QR codes will be saved to your Downloads folder"
echo "🖨️ You can print QR codes using Chrome OS print dialog"
echo ""
echo "📖 For help, see: README.md or CHROMEBOOK_SETUP.md" 