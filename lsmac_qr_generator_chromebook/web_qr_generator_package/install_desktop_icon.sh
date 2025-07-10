#!/bin/bash

# LSMAC QR Generator - Desktop Icon Installer
# This script creates a desktop icon for easy access

echo "🎯 LSMAC QR Generator - Desktop Icon Installer"
echo "================================================"
echo ""

# Get the current directory
CURRENT_DIR=$(pwd)
DESKTOP_FILE="LSMAC-QR-Generator.desktop"
DESKTOP_PATH="$HOME/Desktop"

echo "📁 Current directory: $CURRENT_DIR"
echo "🖥️  Desktop path: $DESKTOP_PATH"
echo ""

# Check if we're in the right directory
if [[ ! -f "launch_chromebook_one_click.py" ]]; then
    echo "❌ Error: Please run this script from the package directory"
    echo "   Current directory: $CURRENT_DIR"
    echo "   Expected files: launch_chromebook_one_click.py"
    exit 1
fi

# Create the desktop entry with the correct path
echo "📝 Creating desktop entry..."
cat > "$DESKTOP_PATH/$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=LSMAC QR Generator
Comment=Web-based QR code generation system for member management
Exec=python3 "$CURRENT_DIR/launch_chromebook_one_click.py"
Icon=applications-internet
Terminal=true
Categories=Office;Network;WebBrowser;
Keywords=QR;Code;Generator;Member;Management;
StartupNotify=true
StartupWMClass=LSMAC-QR-Generator
EOF

# Make the desktop file executable
chmod +x "$DESKTOP_PATH/$DESKTOP_FILE"

# Also make the launcher executable
chmod +x "$CURRENT_DIR/launch_chromebook_one_click.py"

echo "✅ Desktop icon created successfully!"
echo ""
echo "🎉 Installation Complete!"
echo "========================"
echo ""
echo "📱 You can now:"
echo "   1. Double-click the 'LSMAC QR Generator' icon on your desktop"
echo "   2. Or run: python3 launch_chromebook_one_click.py"
echo ""
echo "🌐 The application will:"
echo "   - Install dependencies automatically"
echo "   - Start the web server"
echo "   - Open your browser to the interface"
echo ""
echo "💡 Tips:"
echo "   - The icon will appear on your desktop"
echo "   - You can pin it to your taskbar for easy access"
echo "   - The application runs locally on your Chromebook"
echo ""
echo "🔧 If the icon doesn't work:"
echo "   - Right-click the icon and check 'Allow Launching'"
echo "   - Or run the launcher manually from terminal"
echo "" 