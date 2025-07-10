# 🚀 Deployment Guide - LSMAC QR Generator Chromebook Package

This guide provides step-by-step instructions for deploying the LSMAC QR Generator web package on Chromebook and other platforms.

## 📦 Package Contents

The Chromebook web package includes:

```
web_qr_generator_package/
├── web_qr_generator.py      # Main Flask application
├── run_web_app.py           # Chromebook launcher script
├── launch_chromebook.sh     # Shell script launcher
├── install.sh               # Automated installation script
├── test_package.py          # Package testing script
├── requirements.txt         # Python dependencies
├── package_info.json        # Package metadata
├── README.md               # Detailed documentation
├── QUICK_START.md          # Quick start guide
├── DEPLOYMENT_GUIDE.md     # This file
└── templates/
    └── index.html          # Web interface template
```

## 🎯 Target Platforms

### Primary: Chromebook
- ✅ Optimized for Chrome OS
- ✅ Touch-friendly interface
- ✅ Chrome browser integration
- ✅ Linux container support

### Secondary: Other Platforms
- ✅ Windows (with Python 3.7+)
- ✅ macOS (with Python 3.7+)
- ✅ Linux (Ubuntu, Debian, etc.)

## 🛠️ Installation Methods

### Method 1: Automated Installation (Recommended)

1. **Download the package** to your Chromebook
2. **Open Terminal** (Ctrl+Alt+T)
3. **Navigate to package directory**:
   ```bash
   cd ~/Downloads/lsmac_qr_generator_chromebook/web_qr_generator_package
   ```
4. **Run the installer**:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

### Method 2: Manual Installation

1. **Install Python dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Make scripts executable**:
   ```bash
   chmod +x launch_chromebook.sh
   chmod +x run_web_app.py
   ```

3. **Test the installation**:
   ```bash
   python3 test_package.py
   ```

4. **Start the application**:
   ```bash
   python3 run_web_app.py
   ```

### Method 3: Quick Launch

1. **Run the shell script**:
   ```bash
   ./launch_chromebook.sh
   ```

## 🔧 Configuration Options

### Database Configuration
Edit `web_qr_generator.py` to change Supabase settings:

```python
SUPABASE_URL = "your-supabase-url"
API_KEY = "your-api-key"
```

### Server Configuration
Modify server settings in `web_qr_generator.py`:

```python
# Change port
app.run(host='0.0.0.0', port=8080, debug=False)

# Enable debug mode (development only)
app.run(host='0.0.0.0', port=5000, debug=True)
```

### QR Code Settings
Adjust QR code generation parameters:

```python
def generate_qr_code(member_id, size=10, border=4):
    # size: Controls QR code pixel size (8-12 recommended)
    # border: Controls white space around QR code (2-6 recommended)
```

## 🧪 Testing the Installation

### Run the Test Suite
```bash
python3 test_package.py
```

The test suite checks:
- ✅ Python version compatibility
- ✅ Required dependencies
- ✅ Supabase database connection
- ✅ QR code generation
- ✅ Flask application loading
- ✅ Port availability

### Manual Testing
1. **Start the application**:
   ```bash
   python3 run_web_app.py
   ```

2. **Open browser** to `http://localhost:5000`

3. **Test functionality**:
   - Add a test member
   - Generate a QR code
   - Download/print the QR code
   - Search for members

## 🚀 Production Deployment

### Option 1: Local Production
```bash
# Install production WSGI server
pip3 install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web_qr_generator:app
```

### Option 2: Docker Deployment
Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "web_qr_generator.py"]
```

Build and run:
```bash
docker build -t lsmac-qr-generator .
docker run -p 5000:5000 lsmac-qr-generator
```

### Option 3: Cloud Deployment

#### Heroku
1. Create `Procfile`:
   ```
   web: gunicorn web_qr_generator:app
   ```

2. Deploy:
   ```bash
   heroku create lsmac-qr-generator
   git push heroku main
   ```

#### Google Cloud Run
1. Create `Dockerfile` (see above)
2. Deploy:
   ```bash
   gcloud run deploy lsmac-qr-generator --source .
   ```

## 🔒 Security Considerations

### Development Environment
- ✅ Localhost-only access
- ✅ No external network exposure
- ✅ API keys in code (acceptable for development)

### Production Environment
- 🔒 Use environment variables for API keys
- 🔒 Enable HTTPS
- 🔒 Implement user authentication
- 🔒 Set up proper firewall rules
- 🔒 Regular security updates

### Environment Variables
Create `.env` file for production:
```bash
SUPABASE_URL=your-supabase-url
SUPABASE_API_KEY=your-api-key
FLASK_ENV=production
```

## 📱 Chromebook-Specific Features

### Touch Interface
- Large, touch-friendly buttons
- Responsive design for all screen sizes
- Optimized for Chrome browser

### Chrome OS Integration
- Desktop shortcut creation
- Terminal integration
- Print service integration

### Performance Optimization
- Lightweight Flask application
- Minimal dependencies
- Fast QR code generation

## 🐛 Troubleshooting

### Common Issues

**"Python not found"**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

**"Port 5000 in use"**
```bash
# Find the process
lsof -i :5000
# Kill the process
sudo pkill -f "python.*web_qr_generator"
```

**"Dependencies not installing"**
```bash
# Upgrade pip first
pip3 install --upgrade pip
# Install with user flag
pip3 install -r requirements.txt --user
```

**"Supabase connection failed"**
- Check internet connection
- Verify API key is correct
- Ensure Supabase project is active

**"Browser doesn't open"**
- Manually navigate to `http://localhost:5000`
- Check if server is running in terminal
- Verify no firewall blocking port 5000

### Debug Mode
Enable debug mode for troubleshooting:
```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

## 📊 Monitoring and Logs

### Application Logs
Check terminal output for:
- Server startup messages
- Database connection status
- QR code generation errors
- API request logs

### Performance Monitoring
- Monitor memory usage
- Check CPU usage during QR generation
- Track database response times

## 🔄 Updates and Maintenance

### Updating the Package
1. Download the latest package
2. Replace existing files
3. Restart the application
4. Test functionality

### Database Maintenance
- Regular backups via Supabase
- Monitor database size
- Clean up old member records

### System Maintenance
- Keep Python updated
- Update dependencies regularly
- Monitor disk space

## 📞 Support and Documentation

### Documentation Files
- `README.md` - Complete documentation
- `QUICK_START.md` - Quick start guide
- `package_info.json` - Package metadata

### Testing
- `test_package.py` - Comprehensive test suite
- Manual testing procedures
- Performance benchmarks

### Troubleshooting
- Common issues and solutions
- Debug procedures
- Error message explanations

---

**Package Version**: 1.0.0  
**Last Updated**: January 2025  
**Compatibility**: Chrome OS, Windows, macOS, Linux  
**Support**: Check README.md for detailed instructions 