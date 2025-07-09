#!/bin/bash

# LSMAC QR Generator - Chrome OS Setup Script
# This script sets up the environment for running the QR generator on Chrome OS

echo "Setting up LSMAC QR Generator for Chrome OS..."

# Update package list
echo "Updating package list..."
sudo apt update

# Install Python and pip if not already installed
echo "Installing Python and pip..."
sudo apt install -y python3 python3-pip python3-tk

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Create desktop shortcut
echo "Creating desktop shortcut..."
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

# Make the main script executable
chmod +x qr_generator_chromebook.py

echo ""
echo "Setup complete!"
echo ""
echo "To run the QR generator:"
echo "1. Double-click the desktop shortcut, or"
echo "2. Open terminal and run: python3 qr_generator_chromebook.py"
echo ""
echo "The app will save QR codes to your Downloads folder."
echo "You can print QR codes using Chrome OS's print dialog." 