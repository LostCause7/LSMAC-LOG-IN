import cv2
import numpy as np
from pyzbar import pyzbar
from typing import Optional, Tuple
import threading
import time
import requests

SUPABASE_URL = "https://xbqunvlxqvpmacjcrasc.supabase.co"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhicXVudmx4cXZwbWFjamNyYXNjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTIwMjQ0MjUsImV4cCI6MjA2NzYwMDQyNX0.DcGWWatFg2faO6g7iBEiyjKb4pxlKwHrya005nZ4Pns"
headers = {
    "apikey": API_KEY,
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def check_in_member(member_id):
    # Check if member exists
    r = requests.get(f"{SUPABASE_URL}/rest/v1/members?member_id=eq.{member_id}", headers=headers)
    if r.status_code == 200 and r.json():
        # Update checked_in to true
        update = requests.patch(f"{SUPABASE_URL}/rest/v1/members?member_id=eq.{member_id}", headers=headers, json={"checked_in": True})
        return update.status_code == 204
    else:
        print("Member not found in Supabase.")
        return False

class BarcodeScanner:
    def __init__(self, camera_index: int = 0):
        self.camera_index = camera_index
        self.camera = None
        self.is_scanning = False
        self.last_scanned_code = None
        self.scan_callback = None
        
    def start_camera(self) -> bool:
        """Initialize and start the camera"""
        try:
            self.camera = cv2.VideoCapture(self.camera_index)
            if not self.camera.isOpened():
                return False
            
            # Set camera properties for better barcode detection
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            self.camera.set(cv2.CAP_PROP_FPS, 30)
            
            return True
        except Exception as e:
            print(f"Error starting camera: {e}")
            return False
    
    def stop_camera(self):
        """Stop and release the camera"""
        self.is_scanning = False
        if self.camera:
            self.camera.release()
            self.camera = None
    
    def scan_barcode(self) -> Optional[str]:
        """Scan a single barcode from the camera"""
        if not self.camera or not self.camera.isOpened():
            return None
        
        ret, frame = self.camera.read()
        if not ret:
            return None
        
        # Convert to grayscale for better barcode detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect barcodes
        barcodes = pyzbar.decode(gray)
        
        for barcode in barcodes:
            barcode_data = barcode.data.decode('utf-8')
            barcode_type = barcode.type
            
            # Draw rectangle around barcode
            points = barcode.polygon
            if len(points) > 4:
                hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                points = hull
            
            npts = np.array(points, np.int32)
            npts = npts.reshape((-1, 1, 2))
            cv2.polylines(frame, [npts], True, (0, 255, 0), 3)
            
            # Add text label
            cv2.putText(frame, f"{barcode_type}: {barcode_data}", 
                       (barcode.rect.left, barcode.rect.top - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            return barcode_data
        
        return None
    
    def start_continuous_scanning(self, callback=None):
        """Start continuous barcode scanning in a separate thread"""
        self.scan_callback = callback
        self.is_scanning = True
        
        def scan_loop():
            while self.is_scanning:
                barcode_data = self.scan_barcode()
                if barcode_data and barcode_data != self.last_scanned_code:
                    self.last_scanned_code = barcode_data
                    if self.scan_callback:
                        self.scan_callback(barcode_data)
                    time.sleep(1)  # Prevent multiple scans of the same code
                time.sleep(0.1)  # Small delay to prevent excessive CPU usage
        
        self.scan_thread = threading.Thread(target=scan_loop, daemon=True)
        self.scan_thread.start()
    
    def stop_continuous_scanning(self):
        """Stop continuous barcode scanning"""
        self.is_scanning = False
        if hasattr(self, 'scan_thread'):
            self.scan_thread.join(timeout=1)
    
    def get_frame(self) -> Optional[np.ndarray]:
        """Get current frame from camera for display"""
        if not self.camera or not self.camera.isOpened():
            return None
        
        ret, frame = self.camera.read()
        if not ret:
            return None
        
        # Add scanning overlay
        height, width = frame.shape[:2]
        cv2.rectangle(frame, (width//4, height//4), (3*width//4, 3*height//4), (0, 255, 0), 2)
        cv2.putText(frame, "Position barcode in the green box", 
                   (width//4, height//4 - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        return frame 