@echo off
echo Starting LSMAC Check-In System for Chromebook...
echo.
echo Opening web interface in your default browser...
echo.
echo If the browser doesn't open automatically, please:
echo 1. Open your web browser
echo 2. Navigate to: file:///%CD%/index.html
echo.
echo Press any key to open the web interface...
pause >nul

start "" "index.html"

echo.
echo The check-in system should now be running in your browser.
echo.
echo Features:
echo - Member Check-In with barcode scanning
echo - Admin login and dashboard
echo - Date-based check-in viewing
echo - Manual member check-in
echo - Member management and QR code generation
echo - Local data storage and export
echo.
echo Press any key to exit...
pause >nul 