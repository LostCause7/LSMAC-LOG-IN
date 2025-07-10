#!/bin/bash

# LSMAC QR Generator - Automated Installation Script
# This script automatically installs and configures the web QR generator on Chromebook

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Header
echo "🎯 LSMAC QR Generator - Chromebook Installation"
echo "================================================"
echo ""

# Check if running on Chromebook
if ! grep -q "cros" /etc/os-release 2>/dev/null; then
    print_warning "This script is optimized for Chromebook. Some features may not work on other systems."
fi

# Check if script is run as root
if [[ $EUID -eq 0 ]]; then
    print_error "Please do not run this script as root. Run as a regular user."
    exit 1
fi

# Check if we're in the correct directory
if [[ ! -f "web_qr_generator.py" ]]; then
    print_error "Please run this script from the package directory containing web_qr_generator.py"
    exit 1
fi

print_status "Starting installation process..."

# Step 1: Check and install Python
print_status "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_status "Python 3 not found. Installing..."
    sudo apt update
    sudo apt install -y python3 python3-pip
    print_success "Python 3 installed successfully"
else
    PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    print_success "Python $PYTHON_VERSION found"
fi

# Step 2: Upgrade pip
print_status "Upgrading pip..."
python3 -m pip install --upgrade pip --user
print_success "Pip upgraded successfully"

# Step 3: Install Python dependencies
print_status "Installing Python dependencies..."
if python3 -m pip install -r requirements.txt --user; then
    print_success "Dependencies installed successfully"
else
    print_warning "Failed to install from requirements.txt. Installing packages individually..."
    python3 -m pip install Flask==2.3.3 qrcode[pil]==7.4.2 requests==2.31.0 Pillow==10.0.1 --user
    print_success "Dependencies installed successfully"
fi

# Step 4: Make scripts executable
print_status "Setting up executable permissions..."
chmod +x launch_chromebook.sh
chmod +x run_web_app.py
print_success "Permissions set successfully"

# Step 5: Check port availability
print_status "Checking port availability..."
if lsof -i :5000 &> /dev/null; then
    print_warning "Port 5000 is already in use. Stopping existing processes..."
    sudo pkill -f "python.*web_qr_generator" || true
    sleep 2
fi

# Step 6: Test the installation
print_status "Testing installation..."
if python3 -c "import flask, qrcode, requests, PIL" 2>/dev/null; then
    print_success "All dependencies are working correctly"
else
    print_error "Some dependencies failed to import. Please check the installation."
    exit 1
fi

# Step 7: Create desktop shortcut (optional)
print_status "Creating desktop shortcut..."
cat > ~/Desktop/LSMAC-QR-Generator.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=LSMAC QR Generator
Comment=Web-based QR code generation system
Exec=bash -c "cd $(pwd) && ./launch_chromebook.sh"
Icon=applications-internet
Terminal=true
Categories=Office;
EOF

chmod +x ~/Desktop/LSMAC-QR-Generator.desktop
print_success "Desktop shortcut created"

# Installation complete
echo ""
echo "🎉 Installation Complete!"
echo "========================"
echo ""
print_success "LSMAC QR Generator has been installed successfully!"
echo ""
echo "📱 To start the application:"
echo "   Option 1: Double-click the desktop shortcut"
echo "   Option 2: Run: ./launch_chromebook.sh"
echo "   Option 3: Run: python3 run_web_app.py"
echo ""
echo "🌐 The web interface will be available at: http://localhost:5000"
echo ""
echo "📚 For help and documentation, see:"
echo "   - README.md (detailed instructions)"
echo "   - QUICK_START.md (quick start guide)"
echo ""
print_status "Starting the application now..."
echo ""

# Start the application
./launch_chromebook.sh 