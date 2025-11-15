import streamlit as st
import streamlit.components.v1 as components
import os, re, base64

st.set_page_config(page_title="Embedded HTML (fixed)", layout="centered")

BASE = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE, "static")
INDEX_PATH = os.path.join(STATIC_DIR, "index.html")
EMBED_LIMIT_BYTES = 6 * 1024 * 1024  # 6 MB

if not os.path.exists(INDEX_PATH):
    st.error(f"index.html not found in: {STATIC_DIR}")
    st.stop()

html = open(INDEX_PATH, "r", encoding="utf-8").read()

def to_data_uri(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    mime_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".svg": "image/svg+xml",
        ".mp4": "video/mp4",
        ".webm": "video/webm",
        ".ogg": "video/ogg",
    }
    mime = mime_map.get(ext)
    if not mime:
        return None
    size = os.path.getsize(filepath)
    if size > EMBED_LIMIT_BYTES:
        return None
    with open(filepath, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:{mime};base64,{b64}"

def replace_assets(html_text):
    # We'll find src= or href= occurrences using a safe regex that does not confuse quotes.
    # This regex uses a verbose pattern and escapes quotes properly.
    pattern = re.compile(r'(?:src|href)\s*=\s*(?P<q>["\'])(?P<path>[^"\']+?\.(?:png|jpg|jpeg|gif|svg|mp4|webm|ogg))(?P=q)',
                         flags=re.IGNORECASE)
    video_fallbacks = []
    def repl(m):
        ref = m.group("path")
        quote = m.group("q")
        # ignore absolute URLs or data URIs
        if ref.startswith(("http://", "https://", "data:")):
            return m.group(0)
        candidate = os.path.join(STATIC_DIR, ref.lstrip("/"))
        if not os.path.exists(candidate):
            return m.group(0)
        data_uri = to_data_uri(candidate)
        if data_uri:
            return f'{m.group(0)[0:m.group(0).find("=")+1]}{quote}{data_uri}{quote}'
        else:
            # For large videos, remove src and record fallback
            if candidate.lower().endswith((".mp4", ".webm", ".ogg")):
                video_fallbacks.append(candidate)
                return f'{m.group(0)[0:m.group(0).find("=")+1]}{quote}#{quote}'
            return m.group(0)
    new_html = pattern.sub(repl, html_text)
    return new_html, video_fallbacks

adjusted_html, video_fbs = replace_assets(html)

st.markdown("## Preview of your site")
components.html(adjusted_html, height=700, scrolling=True)

if video_fbs:
    st.markdown("---")
    st.info("Large video(s) detected — playing below with Streamlit's player.")
    for vid in video_fbs:
        st.subheader(os.path.basename(vid))
        try:
            with open(vid, "rb") as f:
                st.video(f.read())
        except Exception as e:
            st.error(f"Could not load video {vid}: {e}")

st.caption("If you still see a blank area, open the Streamlit app's URL in your browser (not the in-app preview).")
