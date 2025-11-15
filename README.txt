README - simple static server (no Flask)

Problem you saw:
- ModuleNotFoundError: No module named 'flask'
  This happens when Flask is not installed in the environment.

Two easy fixes:
1) Install Flask (if you want to keep using the Flask app):
   - pip install flask
   - Or add a requirements.txt containing "Flask" to your project and deploy with that.

2) Use this replacement app.py which requires NO external packages:
   - Place this file next to a folder named 'static' that contains index.html and assets.
   - Run: python app.py
   - Open: http://127.0.0.1:8000/

Contents of this ZIP:
- app.py         (std-lib static server)
- README.txt
