import os
import base64
import streamlit as st
from src.generator import generate_rag_answer

# Page Configuration
st.set_page_config(
    page_title="Inha University Students Community Support",
    page_icon="🎓",
    layout="centered"
)

# Base directory & Asset paths
BASE_DIR = os.path.dirname(__file__)
LOGO_PATH = os.path.join(BASE_DIR, "assets", "logo.png")
BG_PATH = os.path.join(BASE_DIR, "assets", "background.jpg")

def get_base64_of_bin_file(bin_file):
    """Encodes a local binary file (image) to a base64 string."""
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Dynamic Background Setup
if os.path.exists(BG_PATH):
    bg_base64 = get_base64_of_bin_file(BG_PATH)
    bg_css = f'url("data:image/jpg;base64,{bg_base64}")'
else:
    bg_css = 'linear-gradient(180deg, #0e1117 0%, #161b22 100%)'

# Inject Glassmorphism & Custom Styling
custom_css = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    .stApp {{
        background: linear-gradient(180deg, rgba(14, 17, 23, 0.88) 0%, rgba(11, 15, 25, 0.95) 100%), {bg_css};
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    [data-testid="stSidebar"] {{
        background-color: rgba(15, 23, 42, 0.75) !important;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }}

    .header-card {{
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 20px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
    }}

    .main-title {{
        font-size: 2.1rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #FFFFFF 30%, #38BDF8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.25 !important;
        letter-spacing: -0.02em !important;
        margin-bottom: 6px !important;
    }}

    .sub-title {{
        color: #CBD5E1 !important;
        font-size: 0.95rem !important;
        font-weight: 400 !important;
        line-height: 1.4 !important;
    }}

    .status-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(14, 165, 233, 0.12);
        border: 1px solid rgba(14, 165, 233, 0.3);
        color: #38BDF8;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 20px;
        margin-top: 10px;
    }}
    .status-dot {{
        width: 7px;
        height: 7px;
        background-color: #38BDF8;
        border-radius: 50%;
    }}

    .stChatInputContainer {{
        border-radius: 14px !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        background: rgba(15, 23, 42, 0.85) !important;
        backdrop-filter: blur(10px) !important;
    }}

    .stExpander {{
        background: rgba(15, 23, 42, 0.5) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=160)
        st.divider()

    st.subheader("⚙️ System Settings")
    top_k_val = st.slider(
        "Retrieved Matches (top_k)",
        min_value=1,
        max_value=5,
        value=1
    )
    threshold_val = st.slider(
        "Distance Cutoff Threshold",
        min_value=0.5,
        max_value=2.0,
        value=1.15,
        step=0.05,
        help="Lower values enforce strict matching; higher values allow broader matching."
    )
    st.divider()
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Header Card Component
if os.path.exists(LOGO_PATH):
    logo_b64 = get_base64_of_bin_file(LOGO_PATH)
    header_html = f"""
    <div class="header-card">
        <div style="display: flex; align-items: center; gap: 20px;">
            <img src="data:image/png;base64,{logo_b64}" width="95" style="border-radius: 12px; filter: drop-shadow(0 4px 10px rgba(0,0,0,0.3));">
            <div>
                <div class="main-title">Inha University Students Community Support</div>
                <div class="sub-title">Your central knowledge hub for campus procedures, course registration, IT support, and WiFi setup.</div>
                <div class="status-badge">
                    <span class="status-dot"></span> Production RAG System Active
                </div>
            </div>
        </div>
    </div>
    """
else:
    header_html = """
    <div class="header-card">
        <div>
            <div class="main-title">Inha University Students Community Support</div>
            <div class="sub-title">Your central knowledge hub for campus procedures, course registration, IT support, and WiFi setup.</div>
            <div class="status-badge">
                <span class="status-dot"></span> Production RAG System Active
            </div>
        </div>
    </div>
    """

st.markdown(header_html, unsafe_allow_html=True)

# Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render Conversation Messages & Retrieved Context
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("📄 View Retrieved Source Context"):
                for idx, src in enumerate(msg["sources"], 1):
                    st.caption(f"**Match #{idx}** (Distance Metric: `{src['distance']}`)")
                    st.info(src["text"])

# Process Search Input
if prompt := st.chat_input("Ask a question about Inha University..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching knowledge base..."):
            ans, sources = generate_rag_answer(prompt, top_k=top_k_val, threshold=threshold_val)
            st.markdown(ans)
            if sources:
                with st.expander("📄 View Retrieved Source Context"):
                    for idx, src in enumerate(sources, 1):
                        st.caption(f"**Match #{idx}** (Distance Metric: `{src['distance']}`)")
                        st.info(src["text"])

    st.session_state.messages.append({"role": "assistant", "content": ans, "sources": sources})