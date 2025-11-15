# streamlit_app.py
import streamlit as st
import streamlit.components.v1 as components
import os, re, base64

st.set_page_config(page_title="Embedded HTML", layout="centered")

BASE = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE, "static")
INDEX_PATH = os.path.join(STATIC_DIR, "index.html")
EMBED_LIMIT_BYTES = 6 * 1024 * 1024

if not os.path.exists(INDEX_PATH):
    st.error(f"index.html not found in: {STATIC_DIR}")
    st.stop()

html = open(INDEX_PATH, "r", encoding="utf-8").read()

def to_data_uri(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    mime = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".svg": "image/svg+xml",
        ".mp4": "video/mp4",
    }.get(ext, None)
    if mime is None: return None
    size = os.path.getsize(filepath)
    if size > EMBED_LIMIT_BYTES: return None
    with open(filepath, "rb") as f:
        data = f.read()
    import base64
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:{mime};base64,{b64}"

def replace_assets(html_text):
    modified = html_text
    video_fallbacks = []
    pattern = re.compile(r'(src|href)=(["'])([^"']+?\.(?:png|jpg|jpeg|gif|svg|mp4))\2', re.IGNORECASE)

    def repl(m):
        attr, quote, ref = m.group(1), m.group(2), m.group(3)
        if ref.startswith(("http://","https://","data:")): return m.group(0)
        candidate = os.path.join(STATIC_DIR, ref.lstrip("/"))
        if not os.path.exists(candidate): return m.group(0)
        data_uri = to_data_uri(candidate)
        if data_uri:
            return f'{attr}={quote}{data_uri}{quote}'
        else:
            if candidate.lower().endswith(".mp4"):
                video_fallbacks.append(candidate)
                return f'{attr}={quote}#{quote}'
            return m.group(0)

    new_html = pattern.sub(repl, modified)
    return new_html, video_fallbacks

adjusted_html, video_fbs = replace_assets(html)

st.markdown("## Preview")
components.html(adjusted_html, height=700, scrolling=True)

if video_fbs:
    st.markdown("---")
    for vid in video_fbs:
        st.write("Video too large to embed:", os.path.basename(vid))
        with open(vid, "rb") as f:
            st.video(f.read())
