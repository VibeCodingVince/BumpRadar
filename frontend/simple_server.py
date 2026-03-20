#!/usr/bin/env python3
"""
Simple HTTP server for BumpRadar frontend
No SSL - easier for mobile testing
"""
import http.server
import socketserver
import os

PORT = 3000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

if __name__ == '__main__':
    with socketserver.TCPServer(("0.0.0.0", PORT), MyHTTPRequestHandler) as httpd:
        print("")
        print("BumpRadar Frontend Server Started!")
        print("")
        print("On your phone, open your browser and go to:")
        print("   http://192.168.2.10:3000")
        print("")
        print("On this computer:")
        print("   http://localhost:3000")
        print("")
        print("Press Ctrl+C to stop the server")
        print("")
        httpd.serve_forever()
