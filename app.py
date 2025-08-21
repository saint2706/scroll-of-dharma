import streamlit as st
from pathlib import Path
import re
import base64
from narrative import NARRATIVES

# --- Base Directory ---
BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(
    page_title="Scroll of Dharma",
    page_icon="🕉️",
    layout="wide"
)
st.title("🕉️ The Scroll of Dharma")

# --- Asset Loading Functions ---
def get_asset_path(subfolder: str, filename: str) -> Path:
    """Constructs an absolute path to an asset."""
    return BASE_DIR / "assets" / subfolder / filename

@st.cache_data
def load_asset_as_base64(path: Path) -> str:
    """Loads a binary file and returns its base64 encoded string."""
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return ""

def load_animated_svg(filename: str, css_class: str, alt_text: str):
    """Loads an SVG, injects a CSS class for animation, and returns it as a string with alt text for accessibility."""
    svg_path = get_asset_path("svg", filename)
    try:
        with open(svg_path, "r", encoding="utf-8") as f:
            svg_content = f.read()
            # Add class and accessibility
            svg_content = re.sub(r"<svg", f'<svg class="{css_class}" role="img" aria-label="{alt_text}"', svg_content, count=1)
        return svg_content
    except FileNotFoundError:
        return None

# --- Theme and CSS Injection ---
parchment_base64 = load_asset_as_base64(get_asset_path("textures", "parchment_bg.png"))
font_base64 = load_asset_as_base64(get_asset_path("fonts", "UncialAntiqua.ttf"))

# --- UI State ---
if "show_about" not in st.session_state:
    st.session_state["show_about"] = False


st.markdown(f"""
<style>
@font-face {{
    font-family: 'UncialAntiqua';
    src: url(data:font/ttf;base64,{font_base64}) format('truetype');
}}
.stApp {{
    background-image: url('data:image/png;base64,{parchment_base64}');
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
.meditation-highlight {{
    font-family: 'UncialAntiqua', serif !important;
    color: #111 !important;
    font-weight: bold !important;
    font-size: 1.35rem;
    border: 2px solid #FFD700;
    border-radius: 12px;
    padding: 0.5em 1em;
    box-shadow: 0 2px 16px rgba(76, 60, 30, 0.18);
    text-shadow: 0 0 2px #fffbe6, 0 2px 12px rgba(76, 60, 30, 0.18);
    background: rgba(255, 255, 224, 0.08);
    display: inline-block;
}}
.lotus-animated, .chakra-animated, .sword-animated {{
    width: 100%;
    max-width: 400px;
    height: auto;
    display: block;
    margin: auto;
    aspect-ratio: 1 / 1;
    overflow: hidden;
}}
.lotus-animated {{ animation: bloom 4s ease-in-out infinite; }}
.chakra-animated {{ animation: spin 12s linear infinite; }}
.sword-animated {{ animation: rise 4s ease-in-out infinite; }}
@keyframes bloom {{ 0% {{ transform: scale(1); opacity: 0.8; }} 50% {{ transform: scale(1.05); opacity: 1; }} 100% {{ transform: scale(1); opacity: 0.8; }} }}
@keyframes spin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
@keyframes rise {{ 0% {{ transform: translateY(0); opacity: 0.8; }} 50% {{ transform: translateY(-5px); opacity: 1; }} 100% {{ transform: translateY(0); opacity: 0.8; }} }}
</style>
""", unsafe_allow_html=True)

import streamlit.components.v1 as components


scene_options = {
    "lotus_of_doubt": "The Lotus of Doubt",
    "chakra_of_dharma": "The Chakra of Dharma",
    "spiral_of_vision": "The Spiral of Vision",
    "sword_of_resolve": "The Sword of Resolve"
}
scene_assets = {
    "lotus_of_doubt": {"svg": "lotus.svg", "anim_class": "lotus-animated", "alt": "Lotus flower icon representing doubt"},
    "chakra_of_dharma": {"svg": "dharma_wheel.svg", "anim_class": "chakra-animated", "alt": "Dharma wheel icon representing counsel"},
    "spiral_of_vision": {"svg": "lotus_outline.svg", "anim_class": "lotus-animated", "alt": "Lotus outline icon representing vision"},
    "sword_of_resolve": {"svg": "trident.svg", "anim_class": "sword-animated", "alt": "Trident icon representing resolve"}
}

# Progress tracking: store last selected scroll in session state
if "last_scroll" not in st.session_state:
    st.session_state["last_scroll"] = None

selected_key = st.selectbox(
    "Choose a scroll to unfold:",
    options=list(scene_options.keys()),
    format_func=lambda key: scene_options[key],
    help="Use arrow keys to navigate and Enter to select."
)

if st.session_state["last_scroll"] != selected_key:
    st.session_state["last_scroll"] = selected_key

st.markdown(f"<small style='color:#FFD700;'>Bookmarked: {scene_options[st.session_state['last_scroll']]}</small>", unsafe_allow_html=True)


if selected_key:
    st.header(scene_options[selected_key])
    st.markdown('<div id="main-content"></div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1.2, 1])

    with col1:
        asset_info = scene_assets[selected_key]
        animated_svg = load_animated_svg(asset_info["svg"], asset_info["anim_class"], asset_info["alt"])
        if animated_svg:
            st.markdown(f'<div role="img" aria-label="{asset_info["alt"]}" class="fadein" style="width:100%;max-width:400px;margin:auto;">{animated_svg}</div>', unsafe_allow_html=True)
        else:
            st.error(f"SVG not found: {asset_info['svg']}")

    with col2:
        st.subheader("Meditation")
        st.markdown(f'<blockquote class="fadein meditation-highlight">{NARRATIVES.get(selected_key, "Narrative not found.")}</blockquote>', unsafe_allow_html=True)
        st.subheader("Chant")
        fadein_audio_path = get_asset_path("audio/fadein", f"{selected_key}_fadein.mp3")
        ambient_audio_path = get_asset_path("audio/ambient", f"{selected_key}_ambient_loop.mp3")

        try:
            st.markdown("**Introduction:**")
            st.audio(str(fadein_audio_path), format='audio/mp3')
        except FileNotFoundError:
            st.warning(f"Audio not found. Please run `python setup.py`.")

        try:
            st.markdown("**Ambient Loop:**")
            st.audio(str(ambient_audio_path), format='audio/mp3')
        except FileNotFoundError:
            st.warning(f"Ambient audio not found. Please run `python setup.py`.")



st.info("Remember to run `python setup.py` first to download and process all the necessary audio files.")
st.caption("Crafted with reverence • Powered by Streamlit")