# LSMAC Member Check-In System

A comprehensive barcode scanning check-in system for managing member attendance with local database storage, camera integration, and QR code generation capabilities. Now includes a **futuristic web-based interface** with animated designs and modern UI.

## 🌟 New: Web-Based Check-In System

Experience the future of member check-in with our new **futuristic HTML interface** featuring:
- **Animated Design**: Glowing effects, floating particles, and smooth animations
- **Modern UI**: Sleek, sci-fi inspired interface with gradient backgrounds
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Real-time Camera**: Direct browser camera access for barcode scanning
- **Interactive Elements**: Hover effects, button animations, and visual feedback
- **No Installation Required**: Runs directly in any modern web browser

### Quick Web Access
- **Windows**: Double-click `launch_web_checkin.bat` or open `web_checkin.html` in your browser
- **All Platforms**: Open `web_checkin.html` directly in any web browser
- **Features**: Camera integration, member database, check-in tracking, and animated notifications

## Features

- **Barcode Scanning**: Real-time barcode detection using your system's camera
- **QR Code Generation**: Create QR codes for member IDs with customizable options
- **Member Management**: Add, edit, remove, and manage member information
- **Check-in Tracking**: Record daily check-ins with timestamps
- **Local Database**: SQLite database for reliable local data storage
- **Modern GUI**: Clean, intuitive interface built with tkinter
- **History Tracking**: View individual member check-in history
- **Duplicate Prevention**: Prevents multiple check-ins on the same day
- **System Launcher**: Easy access to both check-in system and QR generator

## System Requirements

- **Operating System**: Windows 10/11, macOS, or Linux
- **Python**: 3.7 or higher
- **Camera**: Built-in or USB camera for barcode scanning
- **Memory**: Minimum 4GB RAM
- **Storage**: 100MB free space

## Installation

1. **Clone or download the project files**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the launcher**:
   ```bash
   python launcher.py
   ```

## Quick Start

### 🌐 Web-Based Interface (Recommended)
1. **Windows**: Double-click `launch_web_checkin.bat`
2. **All Platforms**: Open `web_checkin.html` in your web browser
3. **Features**: 
   - Click "Start Camera" to access your device camera
   - Click "Start Scanning" to begin barcode detection
   - View member information and complete check-ins
   - Enjoy the futuristic animated interface

### Using the Launcher (Desktop Applications)
1. Run `python launcher.py`
2. Choose between:
   - **Member Check-In System**: For scanning barcodes and recording check-ins
   - **QR Code Generator**: For creating QR codes and managing members
   - **Test System**: To verify all components are working

### Direct Application Launch
- **Check-in System**: `python main.py`
- **QR Generator**: `python qr_generator.py`
- **System Test**: `python test_system.py`

## Usage Guide

### Member Check-In System

#### Starting the System
1. Launch the application using `python main.py` or the launcher
2. Click "Start Camera" to initialize your system's camera
3. Click "Start Scanning" to begin barcode detection

#### Adding Members
1. Click "Add Member" in the admin panel
2. Fill in the required information:
   - **Member ID**: Unique identifier (can be barcode number)
   - **Name**: Member's full name
   - **Email**: Optional email address
   - **Phone**: Optional phone number
3. Click "Save" to add the member to the database

#### Check-in Process
1. **Scan Member Barcode**: Position the member's barcode within the green scanning box
2. **Verify Member Info**: The system will display member information and check-in status
3. **Complete Check-in**: Click "Check In Member" to record the attendance
4. **View Results**: Check-ins appear in the "Today's Check-Ins" list

### QR Code Generator & Member Management

#### Member Management Features
The QR Code Generator now includes complete member management capabilities:

- **Add Members**: Create new member records with ID, name, email, and phone
- **Edit Members**: Update member information (name, email, phone)
- **Remove Members**: Delete members and their associated check-in history
- **Search Members**: Find members quickly using the search function
- **Member List**: Browse all registered members in an organized table

#### Creating QR Codes
1. Launch the QR Generator using `python qr_generator.py` or the launcher
2. **Manage Members**: Use the member management buttons to add, edit, or remove members
3. **Select a Member**: Choose from the member list or use the search function
4. **Generate QR Code**: Click "Generate QR Code" to create a QR code for the selected member
5. **Customize Options**: Adjust QR size and border settings as needed
6. **Save or Print**: Use "Save QR Code" to save as PNG file or "Print QR Code" to print

#### QR Code Features
- **Member Selection**: Browse or search through all registered members
- **Customizable Options**: Adjust QR code size and border width
- **Preview**: Real-time preview of generated QR codes
- **Save Options**: Save as PNG files with automatic naming
- **Print Support**: Direct printing through system image viewer

#### QR Code Usage
- Generated QR codes contain the member's ID
- Can be printed and given to members for easy check-in
- Compatible with the check-in system's barcode scanner
- High-quality PNG format for professional printing

#### Member Management Workflow
1. **Add New Members**: Click "Add Member" and fill in the required information
2. **Edit Existing Members**: Select a member and click "Edit Member" to update information
3. **Remove Members**: Select a member and click "Remove Member" (with confirmation)
4. **Generate QR Codes**: Select any member and generate their QR code
5. **Search Functionality**: Use the search box to quickly find specific members

### Viewing History
1. Click "View History" in the admin panel
2. Enter the Member ID when prompted
3. View the member's complete check-in history with dates and times

### Managing Data
- **Refresh List**: Updates the today's check-ins display
- **Database**: All data is stored locally in `checkin_system.db`
- **Backup**: Regularly backup the database file for data safety

## Supported Barcode Formats

The system supports all major barcode formats:
- Code 128
- Code 39
- EAN-13
- EAN-8
- UPC-A
- UPC-E
- QR Codes
- Data Matrix

## File Structure

```
LSMAC-LOG-IN/
├── web_checkin.html         # 🌟 Futuristic web-based check-in interface
├── launch_web_checkin.bat   # Windows launcher for web interface
├── launcher.py              # Main system launcher
├── main.py                  # Check-in system entry point
├── qr_generator.py          # QR code generator & member management
├── gui.py                   # Check-in system GUI
├── database.py              # Database operations
├── barcode_scanner.py       # Camera and barcode scanning
├── test_system.py           # System testing script
├── setup.py                 # Automated setup script
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── checkin_system.db       # SQLite database (created automatically)
```

## Database Schema

### Members Table
- `id`: Primary key
- `member_id`: Unique member identifier
- `name`: Member's full name
- `email`: Email address (optional)
- `phone`: Phone number (optional)
- `created_date`: Member registration date

### Check-ins Table
- `id`: Primary key
- `member_id`: Foreign key to members table
- `check_in_date`: Date of check-in
- `check_in_time`: Timestamp of check-in

## Troubleshooting

### Camera Issues
- Ensure your camera is connected and not in use by other applications
- Try different camera indices if multiple cameras are available
- Check camera permissions in your operating system

### Barcode Scanning Problems
- Ensure good lighting conditions
- Hold barcode steady within the green scanning box
- Clean barcode surface if scanning fails
- Try different barcode formats if issues persist

### QR Code Generation Issues
- Ensure the qrcode library is properly installed
- Check that the selected member exists in the database
- Verify write permissions for saving QR code files

### Member Management Issues
- Member IDs must be unique - check for duplicates
- Member names are required fields
- Email and phone are optional but recommended
- Removing a member will also delete their check-in history

### Database Issues
- Ensure write permissions in the application directory
- Check available disk space
- Restore from backup if database becomes corrupted

### Import Errors
- Run `python setup.py` to automatically fix common Windows compatibility issues
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Try using the test script to identify specific issues

## Security Considerations

- **Local Storage**: All data is stored locally on your system
- **No Network**: The application doesn't require internet connection
- **Data Privacy**: Member information is kept private and local
- **Backup**: Regularly backup the database file

## Support

For technical support or feature requests, please contact your system administrator or refer to the troubleshooting section above.

## License

This software is provided as-is for internal use by LSMAC organization.

---

**Version**: 1.2.0  
**Last Updated**: December 2024 