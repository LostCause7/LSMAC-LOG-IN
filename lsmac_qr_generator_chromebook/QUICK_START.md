# Quick Start Guide - Chrome OS

## Option 1: Desktop App (Recommended)

### Step 1: Enable Linux on Chromebook
1. Go to **Settings** → **Advanced** → **Developers**
2. Turn on **"Linux (Beta)"**
3. Wait for Linux to install (may take a few minutes)

### Step 2: Open Terminal
1. Press **Ctrl + Alt + T** to open Crosh
2. Type `shell` and press Enter
3. This opens the Linux terminal

### Step 3: Install Dependencies
```bash
# Update package list
sudo apt update

# Install Python and required packages
sudo apt install -y python3 python3-pip python3-tk

# Install Python dependencies
pip3 install qrcode[pil] pillow requests
```

### Step 4: Run the App
```bash
# Navigate to the app directory
cd /path/to/lsmac_qr_generator_chromebook

# Run the app
python3 qr_generator_chromebook.py
```

## Option 2: Web App (Alternative)

### Step 1: Install Flask
```bash
pip3 install flask
```

### Step 2: Run Web Server
```bash
python3 web_qr_generator.py
```

### Step 3: Open in Browser
1. Open Chrome browser
2. Go to: `http://localhost:5000`

## Features

### Desktop App Features:
- ✅ Native GUI interface
- ✅ Member management (Add/Edit/Delete)
- ✅ QR code generation with custom size/border
- ✅ Save QR codes to Downloads folder
- ✅ Print QR codes using Chrome OS print dialog
- ✅ Search members by name, ID, or email
- ✅ Real-time Supabase database sync

### Web App Features:
- ✅ Browser-based interface
- ✅ Same functionality as desktop app
- ✅ Works on any device with a browser
- ✅ Responsive design for touchscreens
- ✅ Download QR codes directly to browser

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
   - Run with: `chmod +x qr_generator_chromebook.py`

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
- **Desktop Shortcut**: `~/Desktop/LSMAC-QR-Generator.desktop`

## Keyboard Shortcuts

- **Ctrl + Alt + T**: Open terminal
- **Ctrl + C**: Stop web server
- **F5**: Refresh web app
- **Ctrl + P**: Print QR code (web app)

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Try the web version as an alternative
3. Ensure your Chromebook is up to date
4. Restart Linux environment if needed

## Next Steps

After setup:
1. Add your first member
2. Generate a test QR code
3. Save/print the QR code
4. Explore all features

The app will automatically sync with your Supabase database! 