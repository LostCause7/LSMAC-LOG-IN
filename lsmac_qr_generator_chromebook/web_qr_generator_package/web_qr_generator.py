#!/usr/bin/env python3
"""
LSMAC QR Generator - Web Version for Chromebook
Optimized for Chrome OS deployment
"""

from flask import Flask, render_template, request, jsonify, send_file
import qrcode
import requests
import datetime
import os
import io
import base64

app = Flask(__name__)

# Supabase configuration
SUPABASE_URL = "https://xbqunvlxqvpmacjcrasc.supabase.co"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhicXVudmx4cXZwbWFjamNyYXNjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTIwMjQ0MjUsImV4cCI6MjA2NzYwMDQyNX0.DcGWWatFg2faO6g7iBEiyjKb4pxlKwHrya005nZ4Pns"

headers = {
    "apikey": API_KEY,
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def fetch_all_members():
    """Fetch all members from Supabase"""
    try:
        response = requests.get(f"{SUPABASE_URL}/rest/v1/members?select=member_id,name,email,phone,member_since", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error fetching members:", response.status_code, response.text)
            return []
    except Exception as e:
        print("Error:", e)
        return []

def add_member(member_data):
    """Add a new member to Supabase"""
    try:
        response = requests.post(f"{SUPABASE_URL}/rest/v1/members", headers=headers, json=member_data)
        return response.status_code in (200, 201)
    except Exception as e:
        print("Error adding member:", e)
        return False

def update_member(member_id, member_data):
    """Update an existing member"""
    try:
        response = requests.patch(f"{SUPABASE_URL}/rest/v1/members?member_id=eq.{member_id}", headers=headers, json=member_data)
        return response.status_code in (200, 204)
    except Exception as e:
        print("Error updating member:", e)
        return False

def delete_member(member_id):
    """Delete a member"""
    try:
        response = requests.delete(f"{SUPABASE_URL}/rest/v1/members?member_id=eq.{member_id}", headers=headers)
        return response.status_code in (200, 204)
    except Exception as e:
        print("Error deleting member:", e)
        return False

def generate_qr_code(member_id, size=10, border=4):
    """Generate QR code for a member"""
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=size,
            border=border
        )
        qr.add_data(member_id)
        qr.make(fit=True)
        
        # Create image
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64 for web display
        img_buffer = io.BytesIO()
        qr_image.save(img_buffer, format='PNG')
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    except Exception as e:
        print("Error generating QR code:", e)
        return None

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/members')
def get_members():
    """API endpoint to get all members"""
    members = fetch_all_members()
    return jsonify(members)

@app.route('/api/members', methods=['POST'])
def create_member():
    """API endpoint to create a new member"""
    data = request.json
    data['member_since'] = datetime.date.today().strftime('%Y-%m-%d')
    
    if add_member(data):
        return jsonify({"success": True, "message": "Member added successfully"})
    else:
        return jsonify({"success": False, "message": "Failed to add member"}), 400

@app.route('/api/members/<member_id>', methods=['PUT'])
def update_member_api(member_id):
    """API endpoint to update a member"""
    data = request.json
    
    if update_member(member_id, data):
        return jsonify({"success": True, "message": "Member updated successfully"})
    else:
        return jsonify({"success": False, "message": "Failed to update member"}), 400

@app.route('/api/members/<member_id>', methods=['DELETE'])
def delete_member_api(member_id):
    """API endpoint to delete a member"""
    if delete_member(member_id):
        return jsonify({"success": True, "message": "Member deleted successfully"})
    else:
        return jsonify({"success": False, "message": "Failed to delete member"}), 400

@app.route('/api/qr/<member_id>')
def generate_qr_api(member_id):
    """API endpoint to generate QR code"""
    size = request.args.get('size', 10, type=int)
    border = request.args.get('border', 4, type=int)
    
    qr_data = generate_qr_code(member_id, size, border)
    if qr_data:
        return jsonify({"success": True, "qr_code": qr_data})
    else:
        return jsonify({"success": False, "message": "Failed to generate QR code"}), 400

if __name__ == '__main__':
    import webbrowser
    import threading
    import time
    
    print("🚀 Starting LSMAC QR Generator Web Server...")
    print("🌐 Server will be available at: http://localhost:5000")
    print("📱 Optimized for Chromebook browser")
    
    # Open browser after a short delay
    def open_browser():
        time.sleep(2)  # Wait for server to start
        try:
            webbrowser.open('http://localhost:5000')
            print("✅ Browser opened automatically")
        except Exception as e:
            print(f"⚠️  Could not open browser automatically: {e}")
            print("📋 Please manually navigate to: http://localhost:5000")
    
    # Start browser in a separate thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    app.run(host='0.0.0.0', port=5000, debug=False) 