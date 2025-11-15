# app.py
# Simple static file server using only Python standard library (no Flask required).
# Place this file next to a folder named 'static' containing your index.html, video, images, CSS, etc.
#
# Usage:
#   python app.py
# Then open http://127.0.0.1:8000/ in your browser.
#
# This avoids the ModuleNotFoundError for Flask by using http.server.

import http.server
import socketserver
import os
import sys

PORT = 8000
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

if not os.path.isdir(STATIC_DIR):
    print(f"Error: static directory not found at {STATIC_DIR}")
    print("Create a 'static' folder and put your index.html and assets inside it.")
    sys.exit(1)

class Handler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Serve files out of the static/ directory by default.
        # If path is '/', serve static/index.html
        if path == "/":
            path = "/index.html"
        # Remove leading slash
        rel_path = path.lstrip("/")
        full_path = os.path.join(STATIC_DIR, rel_path)
        return full_path

    def log_message(self, format, *args):
        # Override to be a bit quieter. Comment out this method to see access logs.
        pass

with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
    print(f"Serving at http://127.0.0.1:{PORT}/ (static folder: {STATIC_DIR})")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down server")
        httpd.server_close()
