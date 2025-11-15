Streamlit project (fixed)

Files included:
- streamlit_app.py
- static/index.html  (copied if available)
- static/journey_video.mp4  (copied if available)

Usage:
1) Unzip the folder.
2) Install Streamlit if needed: pip install streamlit
3) Run: streamlit run streamlit_app.py
4) Open the URL printed by Streamlit in your browser.

Notes:
- The app inlines small images/videos as data URIs so the iframe preview works.
- Large videos are played using st.video() to avoid iframe black screens.
