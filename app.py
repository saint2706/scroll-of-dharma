"""
The main application file for the Scroll of Dharma.

This script uses Streamlit to create an interactive, narrative-driven web app.
It serves as the central "loom" that weaves together all the project's elements:
narrative text, animated SVG glyphs, themed soundscapes, and custom typography.

The application's structure includes:
1.  **Asset Loading**: Functions to load and cache assets like fonts, images,
    and SVGs, often encoding them in base64 to be embedded directly in the HTML.
2.  **Theming and Styling**: A large CSS block that defines the visual appearance,
    including background textures, typography, and custom animations for the SVGs.
    The theme (fonts, background) changes dynamically based on the selected chapter.
3.  **Content Mapping**: Dictionaries that map narrative chapters and stories to
    their corresponding assets (e.g., which SVG, audio file, and background to use).
4.  **UI Layout**: The main Streamlit layout, which includes dropdowns for chapter
    and story selection, and a two-column display for the animated glyph and the
    narrative/meditation text.
5.  **State Management**: Uses Streamlit's session state to keep track of the
    current selections and UI state (e.g., whether audio has been loaded).
"""

import streamlit as st
from pathlib import Path
import re
import base64

import time
import mimetypes


from typing import Optional
from narrative import NARRATIVES

# --- Base Directory ---
BASE_DIR = Path(__file__).resolve().parent
TEXTURE_CACHE_KEY = "_texture_url_cache"
_local_texture_cache: dict[str, str] = {}

st.set_page_config(page_title="Scroll of Dharma", page_icon="🕉️", layout="wide")
st.title("🕉️ The Scroll of Dharma")


# --- Asset Loading Functions ---
def get_asset_path(subfolder: str, filename: str) -> Path:
    """Constructs an absolute path to an asset."""
    return BASE_DIR / "assets" / subfolder / filename


PROLOGUE_TEXT = """
<p><strong>The scroll stirs awake.</strong> Amber glyphs rise from parchment, inviting you to breathe and listen before the teachings unfold.</p>
<p>This illuminated manuscript will guide you through chapters of devotion, trial, and awakening. Let the prologue center your senses:</p>
<ul>
    <li>Choose a chapter to attune the scroll's tapestry and typography.</li>
    <li>Unfurl a story to reveal its glyph, meditation, and chant.</li>
    <li>Invite the soundscape when you are ready to let the ambience resonate.</li>
</ul>
<p>When your intention feels steady, begin your journey through the Scroll of Dharma.</p>
"""

PROLOGUE_GLYPH = {
    "svg": "lotus.svg",
    "anim_class": "lotus-animated",
    "alt": "Lotus glyph introducing the scroll",
}

PROLOGUE_AUDIO = get_asset_path("audio/raw", "ambient_loop.mp3")


@st.cache_data
def load_asset_as_base64(path: Path) -> str:
    """Loads a binary file and returns its base64 encoded string."""
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return ""


@st.cache_data
def load_animated_svg(filename: str, css_class: str, alt_text: str):
    """Loads an SVG, injects a CSS class for animation, and returns it as a string with alt text for accessibility."""
    svg_path = get_asset_path("svg", filename)
    try:
        with open(svg_path, "r", encoding="utf-8") as f:
            svg_content = f.read()
            # Add class and accessibility
            svg_content = re.sub(
                r"<svg",
                f'<svg class="{css_class}" role="img" aria-label="{alt_text}"',
                svg_content,
                count=1,
            )
        return svg_content
    except FileNotFoundError:
        return None


def show_prologue_modal():
    """Display a modal or fullscreen introduction using the shared show_about flag."""
    glyph_html = load_animated_svg(
        PROLOGUE_GLYPH["svg"], PROLOGUE_GLYPH["anim_class"], PROLOGUE_GLYPH["alt"]
    )
    audio_url = register_audio(PROLOGUE_AUDIO)

    title_block = "<h3 class='prologue-title'>Prologue of the Scroll</h3>"
    glyph_block = f"<div class='prologue-glyph'>{glyph_html or ''}</div>"
    text_block = (
        f"<div class='meditation-highlight prologue-text'>{PROLOGUE_TEXT}</div>"
    )
    audio_html = (
        "<audio autoplay muted loop playsinline controls class='prologue-audio' src="
        f"{audio_url}">"
        "</audio>"
        if audio_url
        else ""
    )

    if hasattr(st, "modal"):
        with st.modal("Prologue of the Scroll", key="scroll-prologue"):
            st.markdown(title_block, unsafe_allow_html=True)
            st.markdown(glyph_block, unsafe_allow_html=True)
            st.markdown(text_block, unsafe_allow_html=True)
            if audio_html:
                st.markdown(audio_html, unsafe_allow_html=True)
                st.caption(
                    "Unmute the ambience to let the drone of the court hum beneath your reading."
                )
            if st.button(
                "Begin your journey", use_container_width=True, type="primary"
            ):
                st.session_state["show_about"] = False
    else:
        fallback = st.container()
        with fallback:
            st.markdown("<div id='prologue-anchor'></div>", unsafe_allow_html=True)
            st.markdown(title_block, unsafe_allow_html=True)
            st.markdown(glyph_block, unsafe_allow_html=True)
            st.markdown(text_block, unsafe_allow_html=True)
            if audio_html:
                st.markdown(audio_html, unsafe_allow_html=True)
                st.caption(
                    "Unmute the ambience to let the drone of the court hum beneath your reading."
                )
            if st.button(
                "Begin your journey", use_container_width=True, type="primary"
            ):
                st.session_state["show_about"] = False


# --- Theme and CSS Injection ---

def _resolve_media_file_manager():
    """Return the active Streamlit media file manager when available."""

    try:
        from streamlit.runtime.runtime import Runtime

        if Runtime.exists():
            return Runtime.instance().media_file_mgr
    except Exception:
        return None

    return None


def _get_texture_cache() -> dict[str, str]:
    """Return the persistent cache used for texture URLs."""

    try:
        return st.session_state.setdefault(TEXTURE_CACHE_KEY, {})
    except Exception:
        return _local_texture_cache


def get_texture_url(filename: str) -> str:
    """Register a texture with Streamlit's media manager and cache the resulting URL."""

    if not filename:
        return ""

    texture_path = get_asset_path("textures", filename)
    if not texture_path.exists():
        return ""

    cache = _get_texture_cache()
    cached_value = cache.get(filename, "")
    mimetype = mimetypes.guess_type(str(texture_path))[0] or "application/octet-stream"

    manager = _resolve_media_file_manager()
    if manager is not None:
        if cached_value and not cached_value.startswith("data:"):
            return cached_value

        try:
            served_url = manager.add(
                str(texture_path),
                mimetype,
                coordinates=f"texture::{filename}",
                file_name=texture_path.name,
            )
        except FileNotFoundError:
            served_url = ""
        except Exception:
            served_url = ""

        if served_url:
            cache[filename] = served_url
            return served_url

    if cached_value:
        return cached_value

    texture_b64 = load_asset_as_base64(texture_path)
    if texture_b64:
        data_uri = f"data:{mimetype};base64,{texture_b64}"
        cache[filename] = data_uri
        return data_uri

    return ""

# Build @font-face CSS with base64 data URIs (fallback to file URLs if missing)
FONT_SPECS = [
    ("Cormorant Garamond", "CormorantGaramond-400.woff2", 400, "normal"),
    ("Cormorant Garamond", "CormorantGaramond-700.woff2", 700, "normal"),
    ("Cormorant Garamond", "CormorantGaramond-Italic-400.woff2", 400, "italic"),
    ("EB Garamond", "EBGaramond-400.woff2", 400, "normal"),
    ("EB Garamond", "EBGaramond-700.woff2", 700, "normal"),
    ("EB Garamond", "EBGaramond-Italic-400.woff2", 400, "italic"),
    ("Cinzel", "Cinzel-400.woff2", 400, "normal"),
    ("Cinzel", "Cinzel-700.woff2", 700, "normal"),
    ("Spectral", "Spectral-400.woff2", 400, "normal"),
    ("Spectral", "Spectral-700.woff2", 700, "normal"),
    ("Spectral", "Spectral-Italic-400.woff2", 400, "italic"),
    ("Cormorant Unicase", "CormorantUnicase-400.woff2", 400, "normal"),
    ("Cormorant Unicase", "CormorantUnicase-700.woff2", 700, "normal"),
    ("Alegreya", "Alegreya-400.woff2", 400, "normal"),
    ("Alegreya", "Alegreya-700.woff2", 700, "normal"),
    ("Alegreya", "Alegreya-Italic-400.woff2", 400, "italic"),
    ("Noto Serif Devanagari", "NotoSerifDevanagari-400.woff2", 400, "normal"),
    ("Noto Serif Devanagari", "NotoSerifDevanagari-700.woff2", 700, "normal"),
    ("Tiro Devanagari Sanskrit", "TiroDevanagariSanskrit-400.woff2", 400, "normal"),
]


def _font_src(filename: str) -> str:
    """Call upon the scribe to weave a @font-face source, embedding base64 ink when found and pointing to the parchment file when not."""
    b64 = load_asset_as_base64(get_asset_path("fonts", filename))
    if b64:
        return f"url('data:font/woff2;base64,{b64}') format('woff2')"
    else:
        return f"url('assets/fonts/{filename}') format('woff2')"


font_face_css = "\n".join(
    [
        "@font-face { font-family:'%s'; src:%s; font-weight:%s; font-style:%s; font-display:swap; }"
        % (family, _font_src(file), weight, style)
        for (family, file, weight, style) in FONT_SPECS
    ]
)

# --- UI State ---
if "show_about" not in st.session_state:
    st.session_state["show_about"] = False


with st.sidebar:
    about_toggle = st.toggle(
        "Show introduction",
        value=st.session_state["show_about"],
        help="Learn how to explore the scroll, listen to its soundscapes, and chant along.",
    )
    if about_toggle != st.session_state["show_about"]:
        st.session_state["show_about"] = about_toggle

    if st.session_state["show_about"]:
        with st.expander("About the Scroll of Dharma", expanded=True):
            st.markdown(
                """
                **Welcome to the Scroll of Dharma.**

                • **Reading the Scroll:** Choose a chapter and story to reveal illuminated glyphs and meditative narratives. Let the parchment unfold as you scroll through the teachings.
                • **Immersive Audio:** Activate the accompanying soundscape to fill the space with ambient instruments tuned to each story's mood. Headphones are encouraged for the full experience.
                • **Chant Invocations:** When chants are available, listen, then repeat the syllables aloud or silently. Allow the rhythm to guide your breath and intention.

                Take your time with each section, pausing to reflect when the glyphs animate or the audio shifts. May this journey bring insight and serenity.
                """
            )
            if st.button("Dismiss introduction", use_container_width=True):
                st.session_state["show_about"] = False

parchment_texture_url = get_texture_url("parchment_bg.webp")

st.markdown(
    f"""
<style>
/* Local webfonts (base64 preferred) */
{font_face_css}
.stApp {{
    background-image: url('{parchment_texture_url}');
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    font-family: var(--story-body, serif);
}}
.meditation-highlight {{
    font-family: var(--story-body, serif) !important;
    color: #1b130a !important; /* dark ink on parchment */
    font-weight: 400 !important;
    font-size: 1.18rem;
    line-height: 1.7;
    letter-spacing: 0.2px;
    white-space: pre-wrap; /* preserve paragraph breaks from text */
    background: rgba(255, 250, 235, 0.93); /* solid, light backdrop for readability */
    border: 1px solid rgba(212, 175, 55, 0.6); /* soft gold */
    border-left: 6px solid #D4AF37; /* accent */
    border-radius: 12px;
    padding: 1rem 1.25rem;
    box-shadow: 0 6px 24px rgba(76, 60, 30, 0.18);
    backdrop-filter: blur(2px) saturate(110%);
    display: block;
    max-width: 70ch;
    margin: 0.5rem auto 0;
}}
.prologue-glyph {{
    display: flex;
    justify-content: center;
    margin: 0 0 1rem;
}}
.prologue-title {{
    font-family: var(--story-head, 'Cormorant Garamond', serif);
    color: #5b3f2b;
    font-weight: 600;
    text-align: center;
    margin-bottom: 1rem;
}}
.prologue-glyph svg {{
    max-width: 320px;
    width: 100%;
    height: auto;
}}
.prologue-text {{
    margin-bottom: 1rem !important;
}}
.prologue-audio {{
    width: 100%;
    margin-bottom: 0.5rem;
}}
div[data-testid="stVerticalBlock"]:has(> div#prologue-anchor) {{
    position: relative;
    z-index: 2;
    background: rgba(255, 250, 235, 0.94);
    border: 1px solid rgba(212, 175, 55, 0.45);
    border-radius: 16px;
    box-shadow: 0 20px 40px rgba(76, 60, 30, 0.25);
    padding: 3rem 2.75rem;
    margin: 0 auto 2.5rem;
    max-width: 720px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: calc(100vh - 6rem);
}}
div[data-testid="stVerticalBlock"]:has(> div#prologue-anchor) .stCaption {{
    text-align: center;
    color: #5b3f2b;
}}
div[data-testid="stVerticalBlock"]:has(> div#prologue-anchor) .stButton button {{
    width: 100%;
    margin-top: 0.75rem;
}}

.parchment-card {{
    position: relative;
    padding: 1.25rem 1rem 1.1rem;
    border-radius: 18px;
    border: 2px solid rgba(112, 78, 28, 0.35);
    background: rgba(255, 249, 235, 0.82);
    overflow: hidden;
    margin-bottom: 1.25rem;
    transition: transform 0.35s ease, box-shadow 0.35s ease, border-color 0.35s ease;
}}
.parchment-card::before {{
    content: "";
    position: absolute;
    inset: 0;
    background-image: url('{parchment_texture_url}');
    background-size: cover;
    background-repeat: no-repeat;
    opacity: 0.35;
    pointer-events: none;
    z-index: 0;
}}
.parchment-card::after {{
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at top, rgba(255, 255, 255, 0.35), transparent 65%);
    opacity: 0;
    transition: opacity 0.35s ease;
    pointer-events: none;
    z-index: 0;
}}
.parchment-card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 18px 36px rgba(72, 46, 12, 0.18);
    border-color: rgba(212, 175, 55, 0.65);
}}
.parchment-card:hover::after {{
    opacity: 1;
}}
.parchment-card.active-card {{
    border-color: #d4af37;
    box-shadow: 0 16px 40px rgba(212, 175, 55, 0.28);
}}
.parchment-card.active-card::after {{
    opacity: 0.9;
}}
.chapter-card-visual, .scroll-card-visual {{
    position: relative;
    min-height: 140px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0.25rem;
    z-index: 1;
}}
.chapter-card-visual svg, .scroll-card-visual svg {{
    max-width: 160px;
    filter: drop-shadow(0 6px 18px rgba(0, 0, 0, 0.18));
}}
.chapter-card-body, .scroll-card-body {{
    position: relative;
    z-index: 1;
    text-align: center;
}}
.chapter-card-meta {{
    font-size: 0.85rem;
    color: rgba(51, 33, 16, 0.85);
    margin: 0.35rem 0 0;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}}
.parchment-card div[data-testid="stButton"] {{
    margin: 0;
    position: relative;
    z-index: 1;
}}
.parchment-card div[data-testid="stButton"] > button {{
    width: 100%;
    background: rgba(255, 252, 244, 0.75);
    border: 1px solid rgba(120, 80, 32, 0.35);
    border-radius: 12px;
    color: #2d1c0a;
    font-size: 1.1rem;
    font-family: var(--story-head, "Cormorant Garamond", serif);
    font-weight: 600;
    letter-spacing: 0.05em;
    padding: 0.6rem 0.8rem;
    text-transform: uppercase;
    cursor: pointer;
    transition: background 0.35s ease, color 0.35s ease, border-color 0.35s ease, box-shadow 0.35s ease;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.45);
}}
.parchment-card div[data-testid="stButton"] > button:hover {{
    background: rgba(255, 255, 245, 0.95);
    color: #1b130a;
    border-color: rgba(212, 175, 55, 0.65);
}}
.parchment-card.active-card div[data-testid="stButton"] > button {{
    border-color: rgba(212, 175, 55, 0.85);
    color: #1b130a;
    background: rgba(255, 253, 245, 0.95);
}}
.scroll-card-body div[data-testid="stButton"] > button {{
    font-size: 1rem;
    text-transform: none;
    font-family: var(--story-body, serif);

}}
/* Base sizing for all story SVGs */
svg[role='img'] {{
    width: 100%;
    max-width: 420px;
    height: auto;
    display: block;
    margin: auto;
    aspect-ratio: 1 / 1;
    overflow: hidden;
    filter: drop-shadow(0 4px 16px rgba(0,0,0,0.15));
}}

/* Backward-compat: keep sizing for animated class names as well */
svg[class*='-animated'] {{
        width: 100%;
        max-width: 420px;
        height: auto;
        display: block;
        margin: auto;
        aspect-ratio: 1 / 1;
        overflow: hidden;
        filter: drop-shadow(0 4px 16px rgba(0,0,0,0.15));
}}

/* Story-specific animation bindings */
/* These classes are applied to the SVGs to trigger specific keyframe animations. */
.lotus-animated {{ animation: bloom 6s ease-in-out infinite; }}
.lotus-outline-animated {{ animation: outlinePulse 5.5s ease-in-out infinite; }}
.chakra-animated {{ animation: spin 20s linear infinite; }}
.trident-animated {{ animation: riseGlow 6s ease-in-out infinite; }}
.dice-animated {{ animation: rock 3.6s ease-in-out infinite; transform-origin: 50% 60%; }}
.collapse-animated {{ animation: shiver 8s ease-in-out infinite; }}
.restore-animated {{ animation: restoreBloom 7s ease-in-out infinite; }}
.forest-animated {{ animation: sway 6s ease-in-out infinite alternate; transform-origin: 50% 90%; }}
.bow-animated {{ animation: draw 5s ease-in-out infinite; transform-origin: 20% 50%; }}
.galaxy-animated {{ animation: orbit 40s linear infinite; }}
.bell-animated {{ animation: swing 4.2s ease-in-out infinite; transform-origin: 50% 6%; }}
/* Birth of Dharma animations */
/* Note: SVGs for 'Birth of Dharma' and 'Trials of Karna' are static and have no animations. */

/* Keyframes define the animations used by the classes above. */
/* A gentle pulsing/breathing effect. */
@keyframes bloom {{
    0% {{ transform: scale(1); filter: drop-shadow(0 2px 8px rgba(255,215,0,0.2)); }}
    50% {{ transform: scale(1.06); filter: drop-shadow(0 6px 18px rgba(255,215,0,0.35)); }}
    100% {{ transform: scale(1); filter: drop-shadow(0 2px 8px rgba(255,215,0,0.2)); }}
}}

@keyframes outlinePulse {{
    0% {{ transform: scale(1) rotate(0.2deg); opacity: 0.92; }}
    50% {{ transform: scale(1.04) rotate(-0.2deg); opacity: 1; }}
    100% {{ transform: scale(1) rotate(0.2deg); opacity: 0.92; }}
}}

@keyframes spin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}

@keyframes riseGlow {{
    0% {{ transform: translateY(0); filter: drop-shadow(0 2px 8px rgba(255,215,0,0.15)); }}
    50% {{ transform: translateY(-6px); filter: drop-shadow(0 10px 24px rgba(255,215,0,0.35)); }}
    100% {{ transform: translateY(0); filter: drop-shadow(0 2px 8px rgba(255,215,0,0.15)); }}
}}

@keyframes rock {{
    0% {{ transform: rotate(-3deg) translateY(0); }}
    50% {{ transform: rotate(3deg) translateY(-2px); }}
    100% {{ transform: rotate(-3deg) translateY(0); }}
}}

@keyframes shiver {{
    0% {{ transform: translateX(0) rotate(0deg); opacity: 0.95; }}
    15% {{ transform: translateX(-0.6px) rotate(-0.4deg); }}
    30% {{ transform: translateX(0.6px) rotate(0.4deg); }}
    45% {{ transform: translateX(-0.4px) rotate(-0.2deg); }}
    60% {{ transform: translateX(0.4px) rotate(0.2deg); }}
    75% {{ transform: translateX(0) rotate(0deg); }}
    100% {{ transform: translateX(0) rotate(0deg); opacity: 0.95; }}
}}

@keyframes restoreBloom {{
    0% {{ transform: scale(0.98); filter: drop-shadow(0 2px 6px rgba(80,200,120,0.2)); }}
    50% {{ transform: scale(1.05); filter: drop-shadow(0 10px 20px rgba(80,200,120,0.35)); }}
    100% {{ transform: scale(0.98); filter: drop-shadow(0 2px 6px rgba(80,200,120,0.2)); }}
}}

@keyframes sway {{
    0% {{ transform: rotate(-1.2deg); }}
    50% {{ transform: rotate(1.2deg); }}
    100% {{ transform: rotate(-1.2deg); }}
}}

@keyframes draw {{
    0% {{ transform: skewX(0deg) scaleX(1); }}
    50% {{ transform: skewX(-2.2deg) scaleX(0.985); }}
    100% {{ transform: skewX(0deg) scaleX(1); }}
}}

@keyframes orbit {{
    from {{ transform: rotate(0deg) scale(1); }}
    to {{ transform: rotate(360deg) scale(1); }}
}}

@keyframes swing {{
    0% {{ transform: rotate(-5deg); }}
    50% {{ transform: rotate(5deg); }}
    100% {{ transform: rotate(-5deg); }}
}}

/* Styled select boxes to match the parchment theme */
select, .stSelectbox select, div[role="combobox"] select {{
    font-family: var(--story-body, serif) !important;
    background: rgba(255, 250, 235, 0.96) !important;
    color: #1b130a !important;
    border: 1px solid rgba(212, 175, 55, 0.6) !important;
    padding: 0.45rem 0.6rem !important;
    border-radius: 10px !important;
    box-shadow: 0 6px 18px rgba(76, 60, 30, 0.06) !important;
    -webkit-appearance: none !important;
    appearance: none !important;
}}

/* Improve select labels */
.stSelectbox label, label[for] {{
    font-family: var(--story-head, 'Cormorant Garamond', serif) !important;
    color: #5b3f2b !important;
    font-weight: 600 !important;
    margin-bottom: 0.25rem !important;
}}
</style>
""",
    unsafe_allow_html=True,
)

if st.session_state["show_about"]:
    show_prologue_modal()

# --- Content and Asset Mapping ---
# These dictionaries are the core of the content management system. They link
# the narrative keys from `narrative.py` to the various assets that should be
# displayed for them.

# `scene_assets` maps each story's unique key to its SVG icon, animation class,
# and accessibility alt text. This is the primary lookup for visual elements.
scene_assets = {
    # Gita Scroll
    "lotus_of_doubt": {
        "svg": "lotus.svg",
        "anim_class": "lotus-animated",
        "alt": "Lotus flower icon representing doubt",
    },
    "chakra_of_dharma": {
        "svg": "dharma_wheel.svg",
        "anim_class": "chakra-animated",
        "alt": "Dharma wheel icon representing counsel",
    },
    "spiral_of_vision": {
        "svg": "lotus_outline.svg",
        "anim_class": "lotus-outline-animated",
        "alt": "Lotus outline icon representing vision",
    },
    "sword_of_resolve": {
        "svg": "trident.svg",
        "anim_class": "trident-animated",
        "alt": "Trident icon representing resolve",
    },
    # Fall of Dharma
    "game_of_fate": {
        "svg": "dice.svg",
        "anim_class": "dice-animated",
        "alt": "Dice icon representing the game of fate",
    },
    "silence_of_protest": {
        "svg": "dharma_collapse.svg",
        "anim_class": "collapse-animated",
        "alt": "Collapsed dharma icon representing silent protest",
    },
    "divine_intervention": {
        "svg": "restore_flower.svg",
        "anim_class": "restore-animated",
        "alt": "Restored flower icon representing grace",
    },
    # Weapon Quest
    "forest_of_austerity": {
        "svg": "forest.svg",
        "anim_class": "forest-animated",
        "alt": "Forest icon representing austerity",
    },
    "shiva_and_the_hunter": {
        "svg": "bow_and_arrow.svg",
        "anim_class": "bow-animated",
        "alt": "Bow and arrow icon representing the hunter",
    },
    "celestial_audience": {
        "svg": "galaxy.svg",
        "anim_class": "galaxy-animated",
        "alt": "Galaxy icon representing celestial audience",
    },
    "trial_of_heaven": {
        "svg": "bell.svg",
        "anim_class": "bell-animated",
        "alt": "Bell icon representing the trial of heaven",
    },
    # Birth of Dharma
    "cosmic_egg": {
        "svg": "cosmic_egg.svg",
        "anim_class": "",
        "alt": "Cosmic egg icon representing the first breath",
    },
    "wheel_turns": {
        "svg": "wheel_turns.svg",
        "anim_class": "",
        "alt": "Turning wheel icon representing the golden parchment",
    },
    "river_oath": {
        "svg": "river_oath.svg",
        "anim_class": "",
        "alt": "River oath icon representing flowing wisdom",
    },
    "balance_restored": {
        "svg": "balance_restored.svg",
        "anim_class": "",
        "alt": "Balance restored icon representing sacred glyphs",
    },
    "first_flame": {
        "svg": "sacred_flame.svg",
        "anim_class": "",
        "alt": "Sacred flame icon representing the awakening scroll",
    },
    # Trials of Karna
    "suns_gift": {
        "svg": "suns_gift.svg",
        "anim_class": "",
        "alt": "Sun's gift icon representing Surya's boon",
    },
    "brahmin_curse": {
        "svg": "brahmins_curse.svg",
        "anim_class": "",
        "alt": "Brahmin's curse icon representing fated forgetfulness",
    },
    "friends_vow": {
        "svg": "friends_vow.svg",
        "anim_class": "",
        "alt": "Friend's vow icon representing loyalty",
    },
    "birth_revealed": {
        "svg": "birth_revealed.svg",
        "anim_class": "",
        "alt": "Birth revealed icon representing hidden lineage",
    },
    "final_arrow": {
        "svg": "final_arrow.svg",
        "anim_class": "",
        "alt": "Final arrow icon representing Karna's fate",
    },
}

# `CHAPTER_TITLES` provides user-friendly display names for the chapter keys.
CHAPTER_TITLES = {
    "gita_scroll": "Gita Scroll",
    "fall_of_dharma": "Fall of Dharma",
    "weapon_quest": "Weapon Quest",
    "birth_of_dharma": "Birth of Dharma",
    "trials_of_karna": "Trials of Karna",
}

# `CHAPTER_BACKGROUNDS` maps each chapter key to a specific background texture image.
CHAPTER_BACKGROUNDS = {
    "gita_scroll": "gita_scroll.webp",
    "fall_of_dharma": "fall_of_dharma.webp",
    "weapon_quest": "weapon_quest.webp",
    "birth_of_dharma": "birth_of_dharma.webp",
    "trials_of_karna": "trials_of_karna.webp",
}

# Each chapter's soundscape card references a specific artwork and poetic description.
SOUNDSCAPE_ARTWORK = {
    "gita_scroll": "gita_scroll.webp",
    "fall_of_dharma": "fall_of_dharma.webp",
    "weapon_quest": "weapon_quest.webp",
    "birth_of_dharma": "birth_of_dharma.webp",
    "trials_of_karna": "trials_of_karna.webp",
}

SOUNDSCAPE_DESCRIPTIONS = {
    "gita_scroll": "Crimson dusk settles over Kurukshetra while Krishna's counsel shimmers between the strings and tambura drones.",
    "fall_of_dharma": "Echoes of judgement halls and solemn vows weave with temple bells to honor the gravity of the court.",
    "weapon_quest": "Forest breezes rustle beside the seeker—flutes, drums, and distant thunder accompany each trial.",
    "birth_of_dharma": "Cosmic breaths, cradle songs, and gentle chimes cradle the origin spark of righteousness.",
    "trials_of_karna": "Sunlit brass and low murmurings follow Karna's vow, balancing valor with the ache of destiny.",
}

# `STORY_DISPLAY_TITLES` allows overriding the default, auto-generated story titles
# for specific stories that need a more customized name.
STORY_DISPLAY_TITLES = {
    "sword_of_resolve": "Trident of Resolve",
}

# `CHANT_LINES` provides the text for the "Chant" section for each story.
# It's a nested dictionary: chapter -> story -> list of mantra lines.
CHANT_LINES = {
    "gita_scroll": {
        "lotus_of_doubt": [
            "Om Shanti Shanti Shanti",
            "Om Shanti Shanti Shanti",
            "Om Shanti Shanti Shanti",
            "Om Shanti Shanti Shanti",
        ],
        "chakra_of_dharma": [
            "Om Namo Bhagavate Vasudevaya",
            "Om Namo Bhagavate Vasudevaya",
            "Om Namo Bhagavate Vasudevaya",
            "Om Namo Bhagavate Vasudevaya",
        ],
        "spiral_of_vision": [
            "Om Namo Narayanaya",
            "Om Namo Narayanaya",
            "Om Namo Narayanaya",
            "Om Namo Narayanaya",
        ],
        "sword_of_resolve": [
            "Om Tat Sat",
            "Om Tat Sat",
            "Om Tat Sat",
            "Om Tat Sat",
        ],
    },
    "fall_of_dharma": {
        "game_of_fate": [
            "Asato maa sadgamaya",
            "Tamaso maa jyotirgamaya",
            "Mrityor maa amritam gamaya",
            "Om Shanti Shanti Shanti",
        ],
        "silence_of_protest": [
            "Om Shanti Shanti Shanti",
            "Om Shanti Shanti Shanti",
            "Om Shanti Shanti Shanti",
            "Om Shanti Shanti Shanti",
        ],
        "divine_intervention": [
            "Hare Krishna Hare Krishna",
            "Krishna Krishna Hare Hare",
            "Hare Rama Hare Rama",
            "Rama Rama Hare Hare",
        ],
    },
    "weapon_quest": {
        "forest_of_austerity": [
            "Om Bhur Bhuvah Swaha",
            "Tat Savitur Varenyam",
            "Bhargo Devasya Dhimahi",
            "Dhiyo Yo Nah Prachodayat",
        ],
        "shiva_and_the_hunter": [
            "Om Namah Shivaya",
            "Om Namah Shivaya",
            "Om Namah Shivaya",
            "Om Namah Shivaya",
        ],
        "celestial_audience": [
            "Om Indraya Namah",
            "Om Indraya Namah",
            "Om Indraya Namah",
            "Om Indraya Namah",
        ],
        "trial_of_heaven": [
            "Tryambakam yajamahe",
            "Sugandhim Pushtivardhanam",
            "Urvarkam iva bandhanan",
            "Mrityor mukshiya mamritat",
        ],
    },
    "birth_of_dharma": {
        "cosmic_breath": [
            "Om Pranaya Namah",
            "Om Pranaya Namah",
            "Om Pranaya Namah",
            "Om Pranaya Namah",
        ],
        "golden_parchment": [
            "Om Saraswatyai Namah",
            "Om Saraswatyai Namah",
            "Om Saraswatyai Namah",
            "Om Saraswatyai Namah",
        ],
        "flowing_wisdom": [
            "Om Namo Narayanaya",
            "Om Namo Narayanaya",
            "Om Namo Narayanaya",
            "Om Namo Narayanaya",
        ],
        "glyphs_of_dharma": [
            "Om Gam Ganapataye Namah",
            "Om Gam Ganapataye Namah",
            "Om Gam Ganapataye Namah",
            "Om Gam Ganapataye Namah",
        ],
        "awakening_scroll": [
            "Om Sri Gurubhyo Namah",
            "Om Sri Gurubhyo Namah",
            "Om Sri Gurubhyo Namah",
            "Om Sri Gurubhyo Namah",
        ],
        # narrative-key aliases
        "cosmic_egg": [
            "Om Pranaya Namah",
            "Om Pranaya Namah",
            "Om Pranaya Namah",
            "Om Pranaya Namah",
        ],
        "wheel_turns": [
            "Om Saraswatyai Namah",
            "Om Saraswatyai Namah",
            "Om Saraswatyai Namah",
            "Om Saraswatyai Namah",
        ],
        "river_oath": [
            "Om Namo Narayanaya",
            "Om Namo Narayanaya",
            "Om Namo Narayanaya",
            "Om Namo Narayanaya",
        ],
        "balance_restored": [
            "Om Gam Ganapataye Namah",
            "Om Gam Ganapataye Namah",
            "Om Gam Ganapataye Namah",
            "Om Gam Ganapataye Namah",
        ],
        "first_flame": [
            "Om Sri Gurubhyo Namah",
            "Om Sri Gurubhyo Namah",
            "Om Sri Gurubhyo Namah",
            "Om Sri Gurubhyo Namah",
        ],
    },
    "trials_of_karna": {
        "suns_gift": [
            "Om Suryaya Namah",
            "Om Suryaya Namah",
            "Om Suryaya Namah",
            "Om Suryaya Namah",
        ],
        "brahmin_curse": [
            "Asato maa sadgamaya",
            "Tamaso maa jyotirgamaya",
            "Mrityor maa amritam gamaya",
            "Om Shanti Shanti Shanti",
        ],
        "friends_vow": [
            "Om Mitraya Namah",
            "Om Mitraya Namah",
            "Om Mitraya Namah",
            "Om Mitraya Namah",
        ],
        "birth_revealed": [
            "Om Kuntidevyai Namah",
            "Om Kuntidevyai Namah",
            "Om Kuntidevyai Namah",
            "Om Kuntidevyai Namah",
        ],
        "final_arrow": [
            "Tryambakam yajamahe",
            "Sugandhim Pushtivardhanam",
            "Urvarkam iva bandhanan",
            "Mrityor mukshiya mamritat",
        ],
    },
}

# `BIRTH_STORY_AUDIO_MAP` is a special mapping required for the 'Birth of Dharma'
# chapter. It connects the narrative story keys (which are semantic, e.g., 'cosmic_egg')
# to the specific audio folder keys used in `audio_builder.py` (e.g., 'cosmic_breath'),
# as they do not share the same names.
BIRTH_STORY_AUDIO_MAP = {
    "cosmic_egg": "cosmic_breath",
    "wheel_turns": "awakening_scroll",
    "river_oath": "flowing_wisdom",
    "balance_restored": "glyphs_of_dharma",
    "first_flame": "golden_parchment",
}


def display_title(key: Optional[str]) -> str:
    """Translate a story key into the illuminated title seen by readers, or hush with an empty string when the key is missing."""
    if not isinstance(key, str) or not key:
        return ""
    return STORY_DISPLAY_TITLES.get(key, key.replace("_", " ").title())


@st.cache_data(show_spinner=False)
def register_audio(path: Optional[Path]) -> Optional[str]:
    """Register an audio asset with Streamlit's media manager and return its URL."""

    if path is None:
        return None

    resolved_path = path.resolve()
    if not resolved_path.exists():
        return None

    try:
        from streamlit import runtime

        if runtime.exists():
            return runtime.get_instance().media_file_mgr.add(
                str(resolved_path),
                "audio/mpeg",
                coordinates=f"audio::{resolved_path}",
                file_name=resolved_path.name,
            )
    except Exception:
        # Fall back to base64 registration when the runtime isn't available.
        pass

    data_uri = load_asset_as_base64(resolved_path)
    if not data_uri:
        return None

    return f"data:audio/mpeg;base64,{data_uri}"


def get_audio_for_story(chapter_key: str, story_key: str):
    """Return tuple (primary_url, ambient_url) based on chapter/story, using standardized outputs."""
    # Defaults for safety
    primary_url = None
    ambient_url = None

    if chapter_key == "gita_scroll":
        primary_url = get_asset_path("audio/fadein", f"{story_key}_fadein.mp3")
        ambient_url = get_asset_path("audio/ambient", f"{story_key}_ambient_loop.mp3")
    elif chapter_key == "fall_of_dharma":
        primary_url = get_asset_path("audio/composite", f"{story_key}_composite.mp3")
        # Use the global ambient bed for the court scenes
        ambient_url = get_asset_path("audio/raw", "ambient_loop.mp3")
    elif chapter_key == "weapon_quest":
        primary_url = get_asset_path(
            f"audio/forest/{story_key}", f"{story_key}_mix.mp3"
        )
        ambient_url = get_asset_path(f"audio/forest/{story_key}", "ambient.mp3")
    elif chapter_key == "birth_of_dharma":
        mapped = BIRTH_STORY_AUDIO_MAP.get(story_key, story_key)
        primary_url = get_asset_path(f"audio/birth/{mapped}", f"{mapped}_mix.mp3")
    elif chapter_key == "trials_of_karna":
        primary_url = get_asset_path(f"audio/karna/{story_key}", f"{story_key}_mix.mp3")

    return primary_url, ambient_url


# Build chapter and story options from NARRATIVES
chapter_options = list(NARRATIVES.keys())
stored_chapter = st.session_state.get("selected_chapter", chapter_options[0])
if stored_chapter not in chapter_options:
    stored_chapter = chapter_options[0]
    st.session_state["selected_chapter"] = stored_chapter

selected_chapter = stored_chapter
chapter_cards_per_row = max(1, min(3, len(chapter_options)))
for idx, chapter in enumerate(chapter_options):
    if idx % chapter_cards_per_row == 0:
        chapter_cols = st.columns(chapter_cards_per_row)
    col = chapter_cols[idx % chapter_cards_per_row]
    chapter_story_keys = list(NARRATIVES[chapter].keys())
    primary_story = chapter_story_keys[0] if chapter_story_keys else None
    asset_info = scene_assets.get(primary_story) if primary_story else None
    icon_html = ""
    if asset_info:
        icon_html = (
            load_animated_svg(
                asset_info["svg"], asset_info["anim_class"], asset_info["alt"]
            )
            or ""
        )

    with col:
        st.markdown(
            f"""
            <div class="chapter-card parchment-card {'active-card' if stored_chapter == chapter else ''}">
                <div class="chapter-card-visual">
                    {icon_html}
                </div>
                <div class="chapter-card-body">
            """,
            unsafe_allow_html=True,
        )
        clicked = st.button(
            CHAPTER_TITLES.get(chapter, chapter.replace("_", " ").title()),
            key=f"chapter_btn_{chapter}",
            use_container_width=True,
            help="Reveal this chapter's illuminated scrolls.",
        )
        st.markdown(
            f"""
                <p class="chapter-card-meta">{len(chapter_story_keys)} scrolls to explore</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if clicked:
            selected_chapter = chapter
            st.session_state["selected_chapter"] = chapter
            if chapter_story_keys:
                st.session_state["last_scroll"] = chapter_story_keys[0]

st.session_state["selected_chapter"] = selected_chapter

story_options = list(NARRATIVES[selected_chapter].keys())
stored_scroll = (
    st.session_state.get("last_scroll", story_options[0]) if story_options else None
)
if stored_scroll not in story_options:
    stored_scroll = story_options[0] if story_options else None
    if stored_scroll:
        st.session_state["last_scroll"] = stored_scroll

selected_key = stored_scroll
story_cards_per_row = max(1, min(3, len(story_options))) if story_options else 1
for idx, story_key in enumerate(story_options):
    if idx % story_cards_per_row == 0:
        story_cols = st.columns(story_cards_per_row)
    col = story_cols[idx % story_cards_per_row]
    asset_info = scene_assets.get(story_key, scene_assets.get("lotus_of_doubt"))
    icon_html = ""
    if asset_info:
        icon_html = (
            load_animated_svg(
                asset_info["svg"], asset_info["anim_class"], asset_info["alt"]
            )
            or ""
        )

    with col:
        st.markdown(
            f"""
            <div class="scroll-card parchment-card {'active-card' if stored_scroll == story_key else ''}">
                <div class="scroll-card-visual">
                    {icon_html}
                </div>
                <div class="scroll-card-body">
            """,
            unsafe_allow_html=True,
        )
        clicked = st.button(
            display_title(story_key),
            key=f"story_btn_{story_key}",
            use_container_width=True,
            help="Unfurl this illuminated scroll.",
        )
        st.markdown("</div></div>", unsafe_allow_html=True)
        if clicked:
            selected_key = story_key
            st.session_state["last_scroll"] = story_key

if not selected_key and story_options:
    selected_key = story_options[0]
    st.session_state["last_scroll"] = selected_key

if selected_key:
    st.session_state["last_scroll"] = selected_key

if selected_key:
    bookmarked_chapter = CHAPTER_TITLES.get(
        selected_chapter, selected_chapter.replace("_", " ").title()
    )
    st.markdown(
        f"<small style='color:#FFD700;'>Bookmarked: {display_title(selected_key)} ({bookmarked_chapter})</small>",
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        "<small style='color:#FFD700;'>No scrolls available yet.</small>",
        unsafe_allow_html=True,
    )

# Override background based on selected chapter
chapter_bg_file = CHAPTER_BACKGROUNDS.get(selected_chapter)
chapter_bg_url = get_texture_url(chapter_bg_file) if chapter_bg_file else ""
if chapter_bg_url:
    overlay_presets = {
        "default": {
            "background": (
                "radial-gradient(circle at 20% 15%, rgba(250, 230, 180, 0.22), rgba(250, 230, 180, 0) 55%), "
                "radial-gradient(circle at 80% 30%, rgba(255, 196, 140, 0.16), rgba(255, 196, 140, 0) 60%), "
                "linear-gradient(140deg, rgba(60, 38, 15, 0.25), rgba(32, 18, 8, 0.38)), "
                "radial-gradient(circle at 50% 50%, rgba(0, 0, 0, 0) 62%, rgba(0, 0, 0, 0.42) 100%)"
            ),
            "size": "160% 160%, 180% 180%, 100% 100%, 100% 100%",
            "position": "10% 10%, 90% 20%, center, center",
            "blend_layers": "screen, screen, soft-light, multiply",
            "mix": "soft-light",
            "animation": "none",
            "opacity": "0.85",
        },
        "gita_scroll": {
            "background": (
                "radial-gradient(circle at 15% 18%, rgba(102, 197, 255, 0.32), rgba(102, 197, 255, 0) 55%), "
                "radial-gradient(circle at 85% 25%, rgba(255, 255, 255, 0.24), rgba(255, 255, 255, 0) 60%), "
                "linear-gradient(115deg, rgba(15, 52, 96, 0.35), rgba(71, 113, 158, 0.25) 55%, rgba(200, 224, 255, 0.35)), "
                "radial-gradient(circle at 50% 55%, rgba(255, 255, 255, 0.05) 0%, rgba(0, 5, 15, 0.52) 100%)"
            ),
            "size": "200% 200%, 220% 220%, 100% 100%, 100% 100%",
            "position": "0% 15%, 80% 5%, center, center",
            "blend_layers": "screen, screen, soft-light, multiply",
            "mix": "soft-light",
            "animation": "waterShimmer 42s ease-in-out infinite",
            "opacity": "0.9",
        },
        "fall_of_dharma": {
            "background": (
                "radial-gradient(circle at 18% 22%, rgba(255, 163, 102, 0.32), rgba(255, 163, 102, 0) 58%), "
                "radial-gradient(circle at 78% 18%, rgba(255, 89, 48, 0.26), rgba(255, 89, 48, 0) 55%), "
                "linear-gradient(135deg, rgba(73, 22, 7, 0.45), rgba(25, 8, 3, 0.55)), "
                "radial-gradient(circle at 50% 52%, rgba(40, 5, 0, 0.05) 0%, rgba(7, 0, 0, 0.55) 100%)"
            ),
            "size": "190% 190%, 210% 210%, 100% 100%, 100% 100%",
            "position": "0% 0%, 100% 0%, center, center",
            "blend_layers": "screen, screen, soft-light, multiply",
            "mix": "soft-light",
            "animation": "emberDrift 34s linear infinite",
            "opacity": "0.92",
        },
        "weapon_quest": {
            "background": (
                "radial-gradient(circle at 16% 24%, rgba(126, 217, 87, 0.28), rgba(126, 217, 87, 0) 55%), "
                "radial-gradient(circle at 82% 28%, rgba(255, 241, 176, 0.22), rgba(255, 241, 176, 0) 60%), "
                "linear-gradient(130deg, rgba(25, 78, 32, 0.42), rgba(10, 36, 18, 0.45)), "
                "radial-gradient(circle at 50% 50%, rgba(10, 18, 7, 0.08) 0%, rgba(4, 9, 2, 0.5) 100%)"
            ),
            "size": "200% 200%, 220% 220%, 100% 100%, 100% 100%",
            "position": "5% 0%, 95% 10%, center, center",
            "blend_layers": "screen, screen, soft-light, multiply",
            "mix": "soft-light",
            "animation": "forestMotes 38s ease-in-out infinite",
            "opacity": "0.88",
        },
        "birth_of_dharma": {
            "background": (
                "radial-gradient(circle at 22% 24%, rgba(255, 214, 153, 0.32), rgba(255, 214, 153, 0) 58%), "
                "radial-gradient(circle at 78% 26%, rgba(255, 177, 194, 0.22), rgba(255, 177, 194, 0) 55%), "
                "linear-gradient(125deg, rgba(214, 127, 61, 0.38), rgba(133, 76, 19, 0.4)), "
                "radial-gradient(circle at 50% 52%, rgba(255, 255, 255, 0.02) 0%, rgba(41, 14, 0, 0.48) 100%)"
            ),
            "size": "190% 190%, 210% 210%, 100% 100%, 100% 100%",
            "position": "0% 5%, 90% 5%, center, center",
            "blend_layers": "screen, screen, soft-light, multiply",
            "mix": "soft-light",
            "animation": "dawnBloom 46s ease-in-out infinite",
            "opacity": "0.9",
        },
        "trials_of_karna": {
            "background": (
                "radial-gradient(circle at 20% 20%, rgba(255, 206, 102, 0.32), rgba(255, 206, 102, 0) 55%), "
                "radial-gradient(circle at 80% 22%, rgba(255, 112, 67, 0.26), rgba(255, 112, 67, 0) 60%), "
                "linear-gradient(140deg, rgba(108, 43, 10, 0.48), rgba(45, 12, 0, 0.48)), "
                "radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.04) 0%, rgba(18, 0, 0, 0.55) 100%)"
            ),
            "size": "200% 200%, 220% 220%, 100% 100%, 100% 100%",
            "position": "0% 10%, 90% 0%, center, center",
            "blend_layers": "screen, screen, soft-light, multiply",
            "mix": "soft-light",
            "animation": "solarPulse 36s ease-in-out infinite",
            "opacity": "0.93",
        },
    }
    overlay_config = overlay_presets.get(selected_chapter, overlay_presets["default"])
    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url('{chapter_bg_url}');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        position: relative;
        overflow: hidden;
    }}
    .stApp::before {{
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 0;
        opacity: {overlay_config['opacity']};
        background-image: {overlay_config['background']};
        background-size: {overlay_config['size']};
        background-position: {overlay_config['position']};
        background-repeat: no-repeat;
        background-blend-mode: {overlay_config['blend_layers']};
        mix-blend-mode: {overlay_config['mix']};
        animation: {overlay_config['animation']};
        transition: background-image 0.6s ease, opacity 1.2s ease;
    }}
    .stApp > header,
    .stApp > div,
    .stApp .block-container {{
        position: relative;
        z-index: 1;
    }}
    @keyframes emberDrift {{
        0% {{ background-position: 0% 0%, 100% 0%, center, center; opacity: 0.92; }}
        50% {{ background-position: 40% 60%, 10% 50%, center, center; opacity: 1; }}
        100% {{ background-position: 100% 80%, 0% 100%, center, center; opacity: 0.92; }}
    }}
    @keyframes waterShimmer {{
        0% {{ background-position: 0% 20%, 80% 0%, center, center; opacity: 0.9; }}
        50% {{ background-position: 45% 55%, 55% 50%, center, center; opacity: 1; }}
        100% {{ background-position: 100% 80%, 20% 100%, center, center; opacity: 0.9; }}
    }}
    @keyframes forestMotes {{
        0% {{ background-position: 5% 0%, 95% 10%, center, center; opacity: 0.88; }}
        50% {{ background-position: 40% 60%, 60% 40%, center, center; opacity: 0.97; }}
        100% {{ background-position: 95% 100%, 5% 90%, center, center; opacity: 0.88; }}
    }}
    @keyframes dawnBloom {{
        0% {{ background-position: 0% 5%, 90% 5%, center, center; opacity: 0.86; }}
        50% {{ background-position: 45% 55%, 55% 45%, center, center; opacity: 0.98; }}
        100% {{ background-position: 90% 95%, 10% 85%, center, center; opacity: 0.86; }}
    }}
    @keyframes solarPulse {{
        0% {{ background-position: 0% 10%, 90% 0%, center, center; opacity: 0.9; }}
        50% {{ background-position: 50% 55%, 50% 45%, center, center; opacity: 1; }}
        100% {{ background-position: 100% 90%, 0% 100%, center, center; opacity: 0.9; }}
    }}
    /* Per-chapter typography */
    :root {{
        {('--story-head: "Cormorant Garamond", serif;' if selected_chapter == 'gita_scroll' else '')}
        {('--story-body: "EB Garamond", "Noto Serif Devanagari", "Tiro Devanagari Sanskrit", serif;' if selected_chapter == 'gita_scroll' else '')}
        {('--story-head: "Cinzel", serif;' if selected_chapter == 'fall_of_dharma' else '')}
        {('--story-body: "Spectral", "Noto Serif Devanagari", "Tiro Devanagari Sanskrit", serif;' if selected_chapter == 'fall_of_dharma' else '')}
        {('--story-head: "Cormorant Unicase", serif;' if selected_chapter == 'weapon_quest' else '')}
        {('--story-body: "Alegreya", "Noto Serif Devanagari", "Tiro Devanagari Sanskrit", serif;' if selected_chapter == 'weapon_quest' else '')}
    {('--story-head: "Cormorant Garamond", serif;' if selected_chapter == 'birth_of_dharma' else '')}
    {('--story-body: "EB Garamond", "Noto Serif Devanagari", "Tiro Devanagari Sanskrit", serif;' if selected_chapter == 'birth_of_dharma' else '')}
    {('--story-head: "Cinzel", serif;' if selected_chapter == 'trials_of_karna' else '')}
    {('--story-body: "Spectral", "Noto Serif Devanagari", "Tiro Devanagari Sanskrit", serif;' if selected_chapter == 'trials_of_karna' else '')}
    }}
    /* Apply to content */
    h2, h3 {{ font-family: var(--story-head, serif) !important; }}
    .meditation-highlight, .stMarkdown p, .stMarkdown li {{ font-family: var(--story-body, serif) !important; }}
    .soundscape-panel {{
        border: 1px solid rgba(255, 215, 0, 0.35);
        background: rgba(15, 10, 5, 0.55);
        padding: 1.5rem;
        border-radius: 18px;
        box-shadow: 0 0 25px rgba(255, 215, 0, 0.08);
        backdrop-filter: blur(3px);
        margin-bottom: 1.2rem;
    }}
    .soundscape-panel img {{
        border-radius: 12px;
        border: 1px solid rgba(255, 215, 0, 0.45);
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.25);
    }}
    .soundscape-description {{
        font-size: 1.05rem;
        line-height: 1.6;
        color: rgba(255, 248, 230, 0.92);
        margin-bottom: 0.75rem;
    }}
    .soundscape-divider {{
        border: none;
        height: 1px;
        margin: 1.25rem 0;
        background: linear-gradient(90deg, rgba(255, 215, 0, 0), rgba(255, 215, 0, 0.5), rgba(255, 215, 0, 0));
    }}
    .soundscape-audio-label {{
        font-variant: small-caps;
        letter-spacing: 0.08em;
        color: rgba(255, 223, 128, 0.9);
        margin-top: 0.5rem;
        margin-bottom: 0.35rem;
    }}
    .mantra-pulse {{
        position: relative;
        width: 120px;
        height: 120px;
        margin: 1.5rem auto 0.75rem;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #d4af37;
        font-size: 2.35rem;
        font-family: var(--story-head, 'Cormorant Garamond', serif);
        letter-spacing: 0.25rem;
        text-transform: uppercase;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.45), 0 0 45px rgba(255, 215, 0, 0.3);
    }}
    .mantra-pulse::before,
    .mantra-pulse::after {{
        content: "";
        position: absolute;
        inset: 0;
        border-radius: 50%;
        border: 2px solid rgba(212, 175, 55, 0.55);
        box-shadow: 0 0 25px rgba(212, 175, 55, 0.35);
        animation: mantraPulseRing 6s ease-in-out infinite;
    }}
    .mantra-pulse::after {{
        animation-delay: 3s;
    }}
    .mantra-pulse .mantra-syllable {{
        position: relative;
        animation: mantraPulseInner 3s ease-in-out infinite;
        display: inline-block;
    }}
    @keyframes mantraPulseRing {{
        0% {{ transform: scale(0.7); opacity: 0; }}
        25% {{ opacity: 0.55; }}
        55% {{ transform: scale(1.05); opacity: 0.38; }}
        100% {{ transform: scale(1.25); opacity: 0; }}
    }}
    @keyframes mantraPulseInner {{
        0%, 100% {{
            transform: scale(1);
            text-shadow: 0 0 18px rgba(255, 215, 0, 0.35), 0 0 38px rgba(255, 215, 0, 0.25);
        }}
        50% {{
            transform: scale(0.9);
            text-shadow: 0 0 8px rgba(255, 215, 0, 0.2), 0 0 20px rgba(255, 215, 0, 0.15);
        }}
    }}
    @media (max-width: 768px) {{
        div[data-testid="stVerticalBlock"]:has(> div#prologue-anchor) {{
            padding: 2rem 1.25rem;
            margin: 0 auto 1.75rem;
        }}
        .parchment-card {{
            padding: 1rem 0.85rem 0.95rem;
            margin-bottom: 1rem;
        }}
        .chapter-card-visual svg, .scroll-card-visual svg {{
            max-width: 120px;
        }}
        .parchment-card div[data-testid="stButton"] > button {{
            font-size: 1rem;
            padding: 0.5rem 0.7rem;
        }}
        .meditation-highlight {{
            padding: 0.85rem 1rem;
            font-size: 1.05rem;
            line-height: 1.55;
            margin: 0.75rem 0;
            max-width: unset;
        }}
        .soundscape-panel {{
            padding: 1.05rem;
            border-radius: 16px;
        }}
        .soundscape-description {{
            font-size: 0.98rem;
            line-height: 1.55;
        }}
        .soundscape-panel img {{
            margin-bottom: 0.75rem;
        }}
        .soundscape-audio-label {{
            margin-top: 0.35rem;
            font-size: 0.95rem;
        }}
        div[data-testid="stHorizontalBlock"] {{
            flex-direction: column !important;
            align-items: stretch !important;
            gap: 0.75rem !important;
        }}
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {{
            width: 100% !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
        }}
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"] + div[data-testid="column"] {{
            margin-top: 0.5rem;
        }}
        div[data-testid="column"] div[data-testid="stVerticalBlock"] {{
            width: 100%;
        }}
    }}
    </style>
    """,
        unsafe_allow_html=True,
    )


if selected_key:
    st.header(
        CHAPTER_TITLES.get(selected_chapter, selected_chapter.replace("_", " ").title())
    )
    st.subheader(display_title(selected_key))
    st.markdown('<div id="main-content"></div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1.2, 1])

    with col1:
        asset_info = scene_assets.get(selected_key, scene_assets.get("lotus_of_doubt"))
        animated_svg = load_animated_svg(
            asset_info["svg"], asset_info["anim_class"], asset_info["alt"]
        )
        if animated_svg:
            st.markdown(
                f'<div role="img" aria-label="{asset_info["alt"]}" class="fadein" style="width:100%;max-width:420px;margin:auto;">{animated_svg}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.error(f"SVG not found: {asset_info['svg']}")

    with col2:
        st.subheader("Meditation")
        narrative_text = NARRATIVES[selected_chapter].get(
            selected_key, "Narrative not found."
        )
        st.markdown(
            f'<blockquote class="fadein meditation-highlight">{narrative_text}</blockquote>',
            unsafe_allow_html=True,
        )

        # Chant section
        st.subheader("Chant")
        chant_lines = CHANT_LINES.get(selected_chapter, {}).get(selected_key, [])
        if chant_lines:
            st.markdown(
                '<blockquote class="fadein meditation-highlight">'
                + "<br>".join(chant_lines)
                + "</blockquote>",
                unsafe_allow_html=True,
            )

        # Soundscape section with ambient/narrative toggles and rhythm visualization
        st.subheader("Soundscape")
        primary_audio_path, ambient_audio_path = get_audio_for_story(
            selected_chapter, selected_key
        )
        load_key = f"_audio_loaded::{selected_chapter}::{selected_key}"
        narrative_toggle_key = load_key + "::narrative_toggle"
        ambient_toggle_key = load_key + "::ambient_toggle"
        narrative_available = primary_audio_path is not None
        ambient_available = ambient_audio_path is not None

        artwork_file = SOUNDSCAPE_ARTWORK.get(
            selected_chapter, CHAPTER_BACKGROUNDS.get(selected_chapter)
        )
        artwork_url = ""
        if artwork_file:
            artwork_url = get_texture_url(artwork_file)
        soundscape_story = SOUNDSCAPE_DESCRIPTIONS.get(
            selected_chapter,
            "Let the unseen choir swell softly around the unfolding tale.",
        )

        with st.container():
            st.markdown('<div class="soundscape-panel">', unsafe_allow_html=True)
            art_col, info_col = st.columns([1.05, 1.6])
            with art_col:
                if artwork_url:
                    st.markdown(
                        f"<img src=\"{artwork_url}\" alt=\"Soundscape artwork\" style=\"width:100%;\" />",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        "<div style='font-size:3rem;text-align:center;'>🕉️</div>",
                        unsafe_allow_html=True,
                    )
                st.caption("Artwork from the illuminated scroll.")
            with info_col:
                st.markdown(
                    f"<p class='soundscape-description'>{soundscape_story}</p>",
                    unsafe_allow_html=True,
                )
                toggle_cols = st.columns(2)
                with toggle_cols[0]:
                    narrative_enabled = st.toggle(
                        "Narrative voice",
                        value=True,
                        key=narrative_toggle_key,
                        disabled=not narrative_available,
                        help="Recitations and storytelling that guide the meditation.",
                    )
                with toggle_cols[1]:
                    ambient_enabled = st.toggle(
                        "Ambient drones",
                        value=selected_chapter == "gita_scroll",
                        key=ambient_toggle_key,
                        disabled=not ambient_available,
                        help="Sustained pads and temple atmospheres that cradle the chant.",
                    )
                st.caption("Choose which rivers of sound accompany your contemplation.")
                if st.button(
                    "Unveil the mantra",
                    key=load_key + "::btn",
                    use_container_width=True,
                    help="Lazy-load the audio only when you are ready to listen.",
                ):
                    st.session_state[load_key] = True

            st.markdown('<hr class="soundscape-divider" />', unsafe_allow_html=True)

            if st.session_state.get(load_key):
                try:
                    players_rendered = False
                    with st.spinner("Kindling the sacred frequencies…"):
                        if narrative_enabled and narrative_available:
                            narrative_url = register_audio(primary_audio_path)
                            if not narrative_url:
                                raise FileNotFoundError(str(primary_audio_path))
                            st.markdown(
                                "<div class='soundscape-audio-label'>Narrative incantation</div>",
                                unsafe_allow_html=True,
                            )
                            st.markdown(
                                f'<audio controls preload="none" playsinline src="{narrative_url}" style="width:100%"></audio>',
                                unsafe_allow_html=True,
                            )
                            players_rendered = True
                        if ambient_enabled and ambient_available:
                            ambient_url = register_audio(ambient_audio_path)
                            if not ambient_url:
                                raise FileNotFoundError(str(ambient_audio_path))
                            st.markdown(
                                "<div class='soundscape-audio-label'>Ambient atmosphere</div>",
                                unsafe_allow_html=True,
                            )
                            st.markdown(
                                f'<audio controls preload="none" playsinline loop src="{ambient_url}" style="width:100%"></audio>',
                                unsafe_allow_html=True,
                            )
                            players_rendered = True

                    if not players_rendered:
                        st.info(
                            "Select at least one stream to invite sacred sound into the space."
                        )
                    else:
                        st.markdown(
                            """
                            <div class="mantra-pulse" role="img" aria-label="Mantra pulse animation">
                                <span class="mantra-syllable">ॐ</span>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        st.caption(
                            "Breathe with the glowing cadence as the mantra flows."
                        )
                except FileNotFoundError:
                    st.warning("Audio not found. Please run `python setup.py`.")
            else:
                st.caption(
                    "Press the mantra seal above to awaken this scroll's sacred soundscape."
                )

            st.markdown("</div>", unsafe_allow_html=True)


st.info(
    "Remember to run `python setup.py` first to download and process all the necessary audio files."
)
st.caption("Crafted with reverence • Powered by Streamlit")
