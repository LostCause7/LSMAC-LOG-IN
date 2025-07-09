# LSMAC QR Generator - Chrome OS Version

This is a Chrome OS compatible version of the LSMAC QR Code Generator that can run on your Acer Chromebook.

## Features

- **Chrome OS Compatible**: Runs on Chromebook's Linux environment
- **Desktop GUI Interface**: Native application with touch-friendly design
- **Web-Based Interface**: Access via Chrome browser (alternative)
- **Member Management**: Add, edit, and remove members from the Supabase database
- **QR Code Generation**: Generate QR codes for selected members with customizable size and border
- **QR Code Actions**: Save QR codes to Downloads folder or print them
- **Member Search**: Search through members by name, ID, or email
- **Supabase Integration**: Uses the same Supabase database as the desktop version

## 📋 **Step-by-Step Guide for Chromebook**

### **Step 1: Enable Linux on Chromebook**
1. Go to **Settings** (gear icon in bottom right)
2. Scroll down and click **"Advanced"**
3. Click **"Developers"**
4. Turn on **"Linux (Beta)"**
5. Click **"Turn On"** and wait for installation (may take 5-10 minutes)

### **Step 2: Download and Extract the App**
1. Download the `lsmac_qr_generator_chromebook` folder to your Chromebook
2. Extract the ZIP file (right-click → "Extract all")
3. Note where you extracted it (usually Downloads folder)

### **Step 3: Open Terminal**
1. Press **Ctrl + Alt + T** to open Crosh
2. Type `shell` and press **Enter**
3. This opens the Linux terminal

### **Step 4: Navigate to the App Folder**
```bash
cd ~/Downloads/lsmac_qr_generator_chromebook
```
*(If you extracted it elsewhere, use that path instead)*

### **Step 5: Run the Complete Setup (Recommended)**
```bash
chmod +x setup_chromebook_complete.sh
./setup_chromebook_complete.sh
```

This will:
- ✅ Install Python and all dependencies
- ✅ Create desktop shortcuts
- ✅ Make all scripts executable
- ✅ Set up everything automatically

### **Step 6: Launch the App**

**Option A: Desktop App (Recommended)**
```bash
python3 qr_generator_chromebook.py
```

**Option B: Use the Launcher Script**
```bash
./run_desktop_app.sh
```

**Option C: Double-click Desktop Shortcut**
- Look for "LSMAC QR Generator" on your desktop
- Double-click to launch

## 🚀 **Alternative Quick Start**

If you want to skip the setup script:

### **Manual Installation:**
```bash
# Install Python and dependencies
sudo apt update
sudo apt install -y python3 python3-pip python3-tk
pip3 install qrcode[pil] pillow requests flask

# Run the app
python3 qr_generator_chromebook.py
```

## 📱 **Using the App**

Once the app opens:
1. **Add Members**: Click "Add Member" to add new members
2. **Search**: Use the search box to find members
3. **Generate QR**: Select a member and click "Generate QR Code"
4. **Save/Print**: Use "Save QR Code" or "Print QR Code" buttons
5. **QR Options**: Adjust size and border in the options panel

## Installation Options

### Option 1: Complete Setup (Recommended)

1. **Enable Linux on Chromebook**:
   - Go to Settings → Advanced → Developers
   - Turn on "Linux (Beta)"
   - Wait for installation to complete

2. **Run Complete Setup**:
   ```bash
   chmod +x setup_chromebook_complete.sh
   ./setup_chromebook_complete.sh
   ```

3. **Launch the App**:
   - Double-click desktop shortcuts, or
   - Run: `python3 qr_generator_chromebook.py`

### Option 2: Desktop App Only

1. **Enable Linux on Chromebook**
2. **Run Desktop Setup**:
   ```bash
   chmod +x run_desktop_app.sh
   ./run_desktop_app.sh
   ```

### Option 3: Web App Only

1. **Enable Linux on Chromebook**
2. **Run Web Setup**:
   ```bash
   chmod +x run_web_app.sh
   ./run_web_app.sh
   ```

### Option 4: Manual Setup

1. **Install Python**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-tk
   ```

2. **Install Dependencies**:
   ```bash
   pip3 install qrcode[pil] pillow requests flask
   ```

3. **Run the App**:
   ```bash
   python3 qr_generator_chromebook.py
   ```

## Project Structure

```
lsmac_qr_generator_chromebook/
├── README.md                           # This file
├── qr_generator_chromebook.py         # Chrome OS compatible Python app
├── web_qr_generator.py                # Web-based version
├── requirements.txt                    # Python dependencies
├── setup_chromebook_complete.sh       # Complete setup script
├── run_desktop_app.sh                 # Desktop app launcher
├── run_web_app.sh                     # Web app launcher
├── run_web_app.py                     # Python web launcher
├── setup_chromebook.sh                # Basic setup script
├── CHROMEBOOK_SETUP.md                # Chrome OS specific guide
├── QUICK_START.md                     # Quick start guide
├── test_standalone.html               # CORS error explanation
└── web_templates/                     # HTML templates for web version
    └── index.html                     # Main web interface
```

## Features Comparison

| Feature | Desktop (Python) | Chrome OS Version |
|---------|------------------|-------------------|
| Member Management | ✅ | ✅ |
| QR Code Generation | ✅ | ✅ |
| QR Code Saving | ✅ | ✅ |
| QR Code Printing | ✅ | ✅ |
| Member Search | ✅ | ✅ |
| Supabase Integration | ✅ | ✅ |
| Modern UI | ✅ | ✅ (Adapted for Chrome OS) |
| Chrome OS Compatible | ❌ | ✅ |

## Chrome OS Specific Features

- **Linux Environment**: Runs in Chrome OS's Linux container
- **File System Access**: Saves files to Downloads folder
- **Print Integration**: Uses Chrome OS printing system
- **Web Interface**: Optional web-based version for browser access
- **Touch Support**: Optimized for Chromebook touchscreens

## Setup Instructions

### Quick Setup (Linux Environment)

1. **Enable Linux** on your Chromebook
2. **Open Terminal** in Linux environment
3. **Run Setup Script**:
   ```bash
   chmod +x setup_chromebook.sh
   ./setup_chromebook.sh
   ```
4. **Launch App**:
   ```bash
   python3 qr_generator_chromebook.py
   ```

### Web-Based Setup

1. **Install Flask**:
   ```bash
   pip3 install flask
   ```
2. **Run Web Server**:
   ```bash
   python3 web_qr_generator.py
   ```
3. **Open Browser**: Navigate to `http://localhost:5000`

## Configuration

The app uses the same Supabase configuration as the desktop version:
- **URL**: `https://xbqunvlxqvpmacjcrasc.supabase.co`
- **API Key**: Configured in the Python files

## 🛠️ **Troubleshooting**

### **If you get "Permission denied":**
```bash
chmod +x *.sh
```

### **If Python is not found:**
```bash
sudo apt install python3
```

### **If modules are missing:**
```bash
pip3 install qrcode[pil] pillow requests flask
```

### **If the GUI doesn't work:**
Try the web version:
```bash
python3 web_qr_generator.py
```
Then open Chrome and go to: `http://localhost:5000`

### **Common Issues**

1. **Linux Not Available**:
   - Ensure your Chromebook supports Linux
   - Update Chrome OS to latest version

2. **Python Installation**:
   - Use `python3` instead of `python`
   - Install pip if needed: `sudo apt install python3-pip`

3. **Permission Issues**:
   - Run with appropriate permissions
   - Check file permissions in Downloads folder

4. **Display Issues**:
   - Ensure Linux has display access
   - Try web-based version if GUI doesn't work

### **Debug Tips**

1. **Check Linux Environment**: `uname -a`
2. **Verify Python**: `python3 --version`
3. **Test Network**: `ping google.com`
4. **Check Dependencies**: `pip3 list`

## 📁 **Where Files Are Saved**

- **QR Codes**: Automatically saved to `~/Downloads/` folder
- **App Files**: Wherever you extracted the folder
- **Desktop Shortcuts**: `~/Desktop/` folder

## 🎯 **Pro Tips**

1. **Use the desktop app** - it's more reliable than the web version
2. **QR codes save automatically** to your Downloads folder
3. **Print using Chrome OS print dialog** - it's integrated
4. **Touch-friendly interface** - works great with touchscreen
5. **Search works in real-time** - just start typing

## ✅ **Success Indicators**

You'll know it's working when:
- ✅ The app window opens with a modern interface
- ✅ You can see the member management panel on the left
- ✅ QR code preview area is visible on the right
- ✅ Status bar shows "Ready" at the bottom

The app will connect to your Supabase database automatically, so all your member data will be available immediately!

**The main file that runs the app is:** `qr_generator_chromebook.py`

## Usage

### Desktop App (Linux Environment)
- **Launch**: `python3 qr_generator_chromebook.py`
- **Interface**: Native GUI similar to desktop version
- **File Operations**: Saves to Downloads folder
- **Printing**: Uses Chrome OS print dialog

### Web App (Browser)
- **Launch**: `python3 web_qr_generator.py`
- **Access**: Open browser to `http://localhost:5000`
- **Interface**: Web-based interface
- **File Operations**: Downloads to browser's download folder

## License

Same as the main LSMAC project. 