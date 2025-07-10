# 🚀 Quick Start Guide - Chromebook

Get the LSMAC QR Generator running on your Chromebook in under 5 minutes!

## ⚡ Super Quick Start

### Option 1: One-Command Setup
```bash
# Download and run everything in one command
curl -sSL https://raw.githubusercontent.com/your-repo/lsmac-qr-generator/main/install.sh | bash
```

### Option 2: Manual Setup (3 steps)

1. **Open Terminal** (Ctrl+Alt+T)
2. **Navigate to package directory**:
   ```bash
   cd ~/Downloads/lsmac_qr_generator_chromebook/web_qr_generator_package
   ```
3. **Run the launcher**:
   ```bash
   chmod +x launch_chromebook.sh
   ./launch_chromebook.sh
   ```

## 🎯 What Happens Next

1. ✅ Python dependencies install automatically
2. 🌐 Web server starts on port 5000
3. 📱 Browser opens to `http://localhost:5000`
4. 🎉 You're ready to generate QR codes!

## 📱 Using the System

### First Time Setup
1. **Add a test member**:
   - Click "➕ Add New Member"
   - Enter: Name: "Test User", Email: "test@example.com", Phone: "555-1234"
   - Click "Add Member"

2. **Generate your first QR code**:
   - Click on the test member in the list
   - QR code generates automatically
   - Try downloading or printing it

### Daily Usage
1. **Add members** as they join
2. **Select members** to generate QR codes
3. **Download or print** QR codes as needed
4. **Search members** using the search box

## 🔧 Troubleshooting

### "Python not found"
```bash
sudo apt update && sudo apt install python3 python3-pip
```

### "Port 5000 in use"
```bash
sudo pkill -f "python.*web_qr_generator"
```

### "Browser doesn't open"
- Manually go to: `http://localhost:5000`

### "Can't install packages"
```bash
python3 -m pip install --user Flask qrcode[pil] requests Pillow
```

## 📋 System Requirements

- ✅ Chromebook with Linux support
- ✅ Internet connection (for initial setup)
- ✅ Chrome browser
- ✅ Terminal access (Ctrl+Alt+T)

## 🎉 Success Indicators

You'll know it's working when you see:
- ✅ "Packages installed successfully"
- ✅ "Starting LSMAC QR Generator Web Server"
- ✅ Browser opens to the web interface
- ✅ Member list loads (even if empty)

## 🆘 Need Help?

1. **Check the terminal output** for error messages
2. **Verify Python version**: `python3 --version`
3. **Test internet connection**: `ping google.com`
4. **Restart the script**: `./launch_chromebook.sh`

## 🔄 Stopping the Server

- **In terminal**: Press `Ctrl+C`
- **Or close the terminal window**

---

**Time to get started**: ~5 minutes  
**Difficulty**: Beginner-friendly  
**Support**: Check README.md for detailed instructions 