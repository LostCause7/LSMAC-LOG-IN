# LSMAC Check-In System - Chromebook Edition v2.0

A comprehensive web-based member check-in system designed specifically for Chromebooks, featuring member check-in, admin management, and QR code generation.

## Features

- **Landing Page**: Clean interface with Member Check-In and Admin Login options
- **Member Check-In**: Camera-based barcode scanning for quick member check-ins
- **Admin Dashboard**: Complete administrative control panel
- **Date-Based Viewing**: View check-ins for any selected date
- **Manual Check-In**: Admin can manually check in members
- **Member Management**: Add, view, and delete members
- **QR Code Generation**: Automatic QR code generation for new members
- **Local Data Storage**: All data stored locally in the browser
- **Export Functionality**: Export data as JSON files
- **Responsive Design**: Works on various screen sizes
- **Offline Capable**: Works without internet connection

## Chromebook Setup Instructions

### Method 1: Direct File Access (Recommended)

1. **Download the Files**
   - Download all HTML files to your Chromebook
   - Save them to your Downloads folder or any accessible location

2. **Launch the Application**
   - Open Chrome browser on your Chromebook
   - Press `Ctrl + O` to open file browser
   - Navigate to where you saved the files
   - Select `index.html` and click "Open"

3. **Grant Camera Permissions**
   - When prompted, click "Allow" to grant camera access
   - This is required for barcode scanning functionality

### Method 2: Using the Launcher (Windows)

If you're transferring from a Windows machine:

1. Copy all files to your Chromebook
2. Double-click `launch_chromebook.bat` (if you have access to Windows compatibility)
3. Follow the prompts to open the web interface

## Usage Instructions

### Landing Page

The application starts with a clean landing page featuring two main options:

1. **Member Check-In**: For members to check themselves in
2. **Admin Login**: For administrators to access management functions

### Member Check-In Process

1. Click "Member Check-In" from the landing page
2. Click "Start Camera" to enable camera access
3. Click "Start Scanning" to begin barcode detection
4. Position the barcode within the green scanning box
5. The system will automatically detect and process the barcode
6. Click "CHECK IN MEMBER" to complete the check-in

### Admin Functions

#### Login
- Click "Admin Login" from the landing page
- Use credentials: Username: `admin`, Password: `admin123`
- Access the comprehensive admin dashboard

#### Date Selection & Check-ins
- Select any date to view check-ins for that specific date
- Use the dropdown to manually check in members
- Remove incorrect check-ins if needed

#### Member Management
- **Add New Member**: Create new members with automatic QR code generation
- **View All Members**: See complete member list with management options
- **Generate QR Codes**: Print QR codes for new or existing members
- **Delete Members**: Remove members from the system

#### Data Export
- Export all member data and check-in history as JSON files
- Files are automatically named with the current date

## File Structure

```
LSMAC Check-In System/
├── index.html              # Landing page
├── member_checkin.html     # Member check-in interface
├── admin_login.html        # Admin authentication
├── admin_dashboard.html    # Admin management dashboard
├── launch_chromebook.bat   # Windows launcher (optional)
├── migrate_to_chromebook.py # Data migration tool
└── README_CHROMEBOOK.md    # This file
```

## Admin Credentials

**Default Login:**
- Username: `admin`
- Password: `admin123`

**Security Note:** In a production environment, change these credentials and implement proper authentication.

## Data Management

### Local Storage
- All member data and check-in history is stored in the browser's local storage
- Data persists between browser sessions
- No internet connection required

### Exporting Data
- Click "Export Data" in the admin dashboard
- Download all data as a JSON file
- Files include member information and complete check-in history

### Sample Data
The system comes pre-loaded with sample members for testing:
- M001: John Smith
- M002: Jane Doe  
- M003: Bob Johnson

## QR Code System

### Automatic Generation
- New members automatically receive unique QR codes
- QR codes contain the member ID for scanning
- Codes can be printed directly from the system

### Printing QR Codes
- QR codes include member information and the unique ID
- Print-friendly format for easy distribution
- Each QR code is unique to the member

## Troubleshooting

### Camera Not Working
- Ensure you've granted camera permissions to the website
- Try refreshing the page and granting permissions again
- Check that no other applications are using the camera

### Barcode Not Detecting
- Ensure good lighting conditions
- Hold the barcode steady within the green scanning box
- Try different angles if the barcode isn't being detected

### Admin Login Issues
- Verify you're using the correct credentials
- Check that JavaScript is enabled
- Try clearing browser cache and cookies

### Page Not Loading
- Ensure you're using Chrome browser
- Try refreshing the page
- Check that the HTML files are not corrupted

### Data Not Saving
- Ensure you have sufficient storage space on your Chromebook
- Try clearing browser cache and cookies
- Check that JavaScript is enabled

## Technical Requirements

- **Browser**: Google Chrome (recommended) or any modern web browser
- **Camera**: Built-in or external camera for barcode scanning
- **Storage**: At least 10MB free space for data storage
- **Permissions**: Camera access permission

## Security Notes

- All data is stored locally on your Chromebook
- No data is transmitted to external servers
- Camera access is only used for barcode scanning
- Export files contain all stored data - handle securely
- Change default admin credentials in production

## Support

For technical support or questions:
1. Check the troubleshooting section above
2. Ensure you're using the latest version of Chrome
3. Try clearing browser cache and cookies
4. Restart the browser if issues persist

## Updates

To update the system:
1. Download the latest version of all HTML files
2. Replace the existing files
3. Refresh the browser page
4. Your existing data will be preserved

## Migration from Previous Version

If you have data from the previous version:
1. Run `migrate_to_chromebook.py` to convert your data
2. Import the generated JSON file into the new system
3. All existing check-in history will be preserved

---

**Note**: This system is designed specifically for Chromebooks and uses web technologies for maximum compatibility. All functionality works offline and data is stored locally for privacy and security. 