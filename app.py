
from flask import Flask, send_from_directory, safe_join, abort
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path="/static")

@app.route("/")
def index():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return send_from_directory(STATIC_DIR, "index.html")
    else:
        return "<h2>index.html not found in ./static</h2>", 404

@app.route("/<path:filename>")
def serve_file(filename):
    safe_path = safe_join(STATIC_DIR, filename)
    if safe_path and os.path.exists(safe_path):
        return send_from_directory(STATIC_DIR, filename)
    return abort(404)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
