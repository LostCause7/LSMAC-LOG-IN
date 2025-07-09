# Chromebook Setup Guide

## Prerequisites

1. **Enable Linux on Chromebook:**
   - Go to Settings → Advanced → Developers
   - Turn on "Linux (Beta)"
   - Wait for installation to complete

2. **Open Terminal:**
   - Press `Ctrl + Alt + T` to open Crosh
   - Type `shell` and press Enter

## Option 1: Desktop App (Recommended)

### Step 1: Install Python
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-tk
```

### Step 2: Install Dependencies
```bash
pip3 install qrcode[pil] pillow requests
```

### Step 3: Run the App
```bash
python3 qr_generator_chromebook.py
```

**Features:**
- ✅ Native GUI interface
- ✅ Saves QR codes to Downloads folder
- ✅ Uses Chrome OS print dialog
- ✅ Touch-friendly interface
- ✅ No browser required

## Option 2: Web App

### Step 1: Install Python
```bash
sudo apt update
sudo apt install -y python3 python3-pip
```

### Step 2: Install Flask
```bash
pip3 install flask qrcode[pil] requests
```

### Step 3: Run Web Server
```bash
python3 web_qr_generator.py
```

### Step 4: Open in Browser
- Browser opens automatically to `http://localhost:5000`
- Or manually open Chrome and go to `http://localhost:5000`

**Features:**
- ✅ Browser-based interface
- ✅ Responsive design for touchscreens
- ✅ Download QR codes directly
- ✅ Works on any device with browser

## Option 3: Easy Launcher (Alternative)

### Step 1: Install Dependencies
```bash
sudo apt update
sudo apt install -y python3 python3-pip
```

### Step 2: Run Launcher
```bash
python3 run_web_app.py
```

This automatically:
- ✅ Checks if dependencies are installed
- ✅ Installs missing dependencies
- ✅ Starts the web server
- ✅ Opens browser automatically

## Troubleshooting

### Common Issues:

1. **"Linux not available"**
   - Update Chrome OS to latest version
   - Ensure your Chromebook supports Linux

2. **"Python not found"**
   - Use `python3` instead of `python`
   - Install with: `sudo apt install python3`

3. **"Module not found"**
   - Install dependencies: `pip3 install -r requirements.txt`

4. **"Permission denied"**
   - Make script executable: `chmod +x qr_generator_chromebook.py`

5. **"Display issues"**
   - Ensure Linux has display access
   - Try web version if GUI doesn't work

### Debug Commands:
```bash
# Check Linux environment
uname -a

# Check Python version
python3 --version

# Check installed packages
pip3 list

# Test network connection
ping google.com
```

## File Locations

- **QR Codes**: Saved to `~/Downloads/` folder
- **App Files**: Wherever you extracted the app
- **Desktop Shortcut**: `~/Desktop/LSMAC-QR-Generator.desktop` (if using setup script)

## Keyboard Shortcuts

- **Ctrl + Alt + T**: Open terminal
- **Ctrl + C**: Stop web server
- **F5**: Refresh web app
- **Ctrl + P**: Print QR code (web app)

## Recommendation

**Use Option 1 (Desktop App)** for the best experience on Chromebook:
- More reliable
- Better performance
- Native Chrome OS integration
- No browser dependencies 