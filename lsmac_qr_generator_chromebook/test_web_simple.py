#!/usr/bin/env python3
"""
Simple test version of the web app to debug 500 errors
"""

from flask import Flask, jsonify
import requests

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

@app.route('/')
def index():
    """Simple test page"""
    return """
    <html>
    <head><title>LSMAC QR Generator - Test</title></head>
    <body>
        <h1>LSMAC QR Generator</h1>
        <p>Web server is running!</p>
        <p><a href="/api/members">Test API</a></p>
    </body>
    </html>
    """

@app.route('/api/members')
def get_members():
    """API endpoint to get all members"""
    try:
        response = requests.get(f"{SUPABASE_URL}/rest/v1/members?select=member_id,name,email,phone,member_since", headers=headers)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": f"API Error: {response.status_code}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/test')
def test():
    """Simple test endpoint"""
    return jsonify({"status": "ok", "message": "Server is working"})

if __name__ == '__main__':
    print("Starting simple test server...")
    print("Go to: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True) 