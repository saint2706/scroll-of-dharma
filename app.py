"""
The main application file for the Scroll of Dharma, a Streamlit-based web app.

This script serves as the central "loom" that weaves together all the project's
elements: narrative text, animated SVG glyphs, themed soundscapes, and custom
typography. It is responsible for rendering the user interface, managing application
state, and orchestrating the dynamic loading of assets based on user selections.

The application's structure includes:
1.  **Asset Loading**: Functions to load and cache assets like fonts, images,
    and SVGs, often encoding them in base64 to be embedded directly in the HTML.
    This minimizes requests and improves performance.
2.  **Theming and Styling**: A large CSS block that defines the visual appearance,
    including background textures, typography, and custom animations for the SVGs.
    The theme (fonts, background) changes dynamically based on the selected chapter.
3.  **Content Mapping**: Dictionaries that map narrative chapters and stories to
    their corresponding assets (e.g., which SVG, audio file, and background to use).
4.  **UI Layout**: The main Streamlit layout, which includes dropdowns for chapter
    and story selection, and a two-column display for the animated glyph and the
    narrative/meditation text.
5.  **State Management**: Uses Streamlit's session state to keep track of the
    current selections and UI state (e.g., whether audio has been loaded), ensuring
    a persistent experience as the user interacts with the application.
"""

import streamlit as st
from pathlib import Path
import re
import base64
import html



import time
import mimetypes

from typing import Optional, Tuple
from narrative import NARRATIVES
from ui_constants import (
    BACKGROUND_OVERLAYS,
    BIRTH_STORY_AUDIO_MAP,
    CHANT_LINES,
    CHAPTER_BACKGROUNDS,
    CHAPTER_TITLES,
    FONT_SPECS,
    PARCHMENT_GRADIENT_LAYERS,
    PROLOGUE_AUDIO_ASSET,
    PROLOGUE_GLYPH,
    PROLOGUE_TEXT,
    SCENE_ASSETS,
    SOUNDSCAPE_ARTWORK,
    SOUNDSCAPE_DESCRIPTIONS,
    STORY_DISPLAY_TITLES,
)

# --- Base Directory ---
BASE_DIR = Path(__file__).resolve().parent
TEXTURE_CACHE_KEY = "_texture_url_cache"
_local_texture_cache: dict[str, str] = {}

st.set_page_config(page_title="Scroll of Dharma", page_icon="🕉️", layout="wide")
st.title("🕉️ The Scroll of Dharma")


# --- Asset Loading Functions ---
def get_asset_path(subfolder: str, filename: str) -> Path:
    """
    Constructs an absolute path to an asset in the 'assets' directory.

    Args:
        subfolder: The name of the subfolder within 'assets' (e.g., 'svg', 'fonts').
        filename: The name of the asset file.

    Returns:
        A Path object representing the absolute path to the asset.
    """
    return BASE_DIR / "assets" / subfolder / filename


PROLOGUE_AUDIO = get_asset_path(*PROLOGUE_AUDIO_ASSET)


@st.cache_data
def load_asset_as_base64(path: Path) -> str:
    """
    Loads a binary file and returns its base64 encoded string.

    This function is cached to avoid re-reading files from disk. It's used for
    embedding assets like fonts and images directly into the HTML, which can
    improve loading performance.

    Args:
        path: The absolute path to the binary file.

    Returns:
        A base64 encoded string representation of the file, or an empty string
        if the file is not found.
    """
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        st.error(f"Asset not found at path: {path}")
        return ""


@st.cache_data
def load_animated_svg(filename: str, css_class: str, alt_text: str) -> Optional[str]:
    """
    Loads an SVG file, injects a CSS class for animation, and adds accessibility attributes.

    This function is cached to prevent re-reading and processing the same SVG file
    multiple times. It modifies the SVG content to include a specified CSS class
    and an ARIA label for screen readers.

    Args:
        filename: The name of the SVG file in the 'assets/svg' directory.
        css_class: The CSS class to inject into the <svg> tag for styling and animation.
        alt_text: The alternative text for the SVG, used for the ARIA label.

    Returns:
        The modified SVG content as a string, or None if the file is not found.
    """
    svg_path = get_asset_path("svg", filename)
    try:
        with open(svg_path, "r", encoding="utf-8") as f:
            svg_content = f.read()
            # Use regex to inject the CSS class and accessibility role/label
            svg_content = re.sub(
                r"<svg",
                f'<svg class="{css_class}" role="img" aria-label="{alt_text}"',
                svg_content,
                count=1,
            )
        return svg_content
    except FileNotFoundError:
        st.error(f"SVG asset not found: {filename}")
        return None


def show_prologue_modal():
    """
    Displays a modal-like introduction screen for the application.

    This function constructs the HTML for the prologue, including an animated SVG,
    introductory text, and background audio. It is displayed when the user toggles
    the 'Show introduction' option in the sidebar.
    """
    # Load the animated SVG glyph for the prologue
    glyph_html = load_animated_svg(
        PROLOGUE_GLYPH["svg"], PROLOGUE_GLYPH["anim_class"], PROLOGUE_GLYPH["alt"]
    )
    # Register and get the URL for the prologue's background audio
    audio_url = register_audio(PROLOGUE_AUDIO)

    # Construct the HTML blocks for the prologue's content
    title_block = "<h3 class='prologue-title'>Prologue of the Scroll</h3>"
    glyph_block = f"<div class='prologue-glyph'>{glyph_html or ''}</div>"
    text_block = (
        f"<div class='meditation-highlight prologue-text'>{PROLOGUE_TEXT}</div>"
    )
    # The audio is muted by default to comply with browser autoplay policies
    audio_html = (
        (
            "<audio autoplay muted loop playsinline controls class='prologue-audio' src=\""
            f"{audio_url}\"></audio>"
        )
        if audio_url
        else ""
    )

    # Use a Streamlit container to render the prologue
    prologue_container = st.container()
    with prologue_container:
            # The 'prologue-wrapper' div acts as the modal container
            st.markdown(
                "<div class='prologue-wrapper' id='prologue-container'><div id='prologue-anchor'></div>",
                unsafe_allow_html=True,
            )
            st.markdown(title_block, unsafe_allow_html=True)
            st.markdown(glyph_block, unsafe_allow_html=True)
            st.markdown(text_block, unsafe_allow_html=True)

            # Display the audio player and a caption if audio is available
            if audio_html:
                st.markdown(audio_html, unsafe_allow_html=True)
                st.caption(
                    "Unmute the ambience to let the drone of the court hum beneath your reading."
                )

            # The button to dismiss the prologue and start the main experience
            if st.button(
                "Begin your journey", use_container_width=True, type="primary"
            ):
                st.session_state["show_about"] = False
                st.experimental_rerun()
            st.markdown("</div>", unsafe_allow_html=True)


# --- Theme and CSS Injection ---

def _resolve_media_file_manager():
    """
    Safely retrieves the active Streamlit media file manager instance.

    This function attempts to import and access Streamlit's runtime to get the
    media file manager. It handles cases where the runtime might not be available
    (e.g., during testing or in different deployment environments).

    Returns:
        The media file manager instance, or None if it cannot be resolved.
    """
    try:
        from streamlit.runtime.runtime import Runtime

        if Runtime.exists():
            return Runtime.instance().media_file_mgr
    except (ImportError, AttributeError):
        # Gracefully fail if Streamlit's internal structure changes or is unavailable
        return None

    return None


def _get_texture_cache() -> dict[str, str]:
    """
    Retrieves the cache for texture URLs, using session state if available.

    This function provides a caching mechanism for texture URLs to avoid redundant
    processing. It defaults to a local dictionary if Streamlit's session state
    is not accessible.

    Returns:
        A dictionary serving as the texture URL cache.
    """
    try:
        # Use Streamlit's session state for a persistent, per-session cache
        return st.session_state.setdefault(TEXTURE_CACHE_KEY, {})
    except Exception:
        # Fallback to a simple dictionary if session state is not available
        return _local_texture_cache


def get_texture_url(filename: str, subfolder: str = "textures") -> str:
    """
    Registers a texture with Streamlit's media manager and caches the resulting URL.

    This function first attempts to get a URL from the media manager for efficient
    serving. If the media manager is unavailable, it falls back to embedding the
    texture as a base64 data URI. Results are cached to improve performance.

    Args:
        filename: The name of the texture file.
        subfolder: The subfolder within 'assets' where the texture is located.

    Returns:
        A URL (either from the media manager or a data URI) for the texture,
        or an empty string if the file cannot be processed.
    """
    if not filename:
        return ""

    texture_path = get_asset_path(subfolder, filename)
    if not texture_path.exists():
        st.warning(f"Texture file not found: {texture_path}")
        return ""

    cache = _get_texture_cache()
    cache_key = f"{subfolder}/{filename}"

    # Return cached URL if it's already a valid media manager URL
    if cache_key in cache and not cache[cache_key].startswith("data:"):
        return cache[cache_key]

    manager = _resolve_media_file_manager()
    if manager:
        try:
            mimetype = mimetypes.guess_type(str(texture_path))[0] or "application/octet-stream"
            served_url = manager.add(
                str(texture_path),
                mimetype,
                coordinates=f"texture::{subfolder}::{filename}",
                file_name=texture_path.name,
            )
            if served_url:
                cache[cache_key] = served_url
                return served_url
        except Exception as e:
            st.warning(f"Could not register texture with media manager: {e}")

    # Fallback to base64 encoding if media manager fails or is unavailable
    if cache_key in cache:
        return cache[cache_key]  # Return cached base64 URI

    texture_b64 = load_asset_as_base64(texture_path)
    if texture_b64:
        mimetype = mimetypes.guess_type(str(texture_path))[0] or "application/octet-stream"
        data_uri = f"data:{mimetype};base64,{texture_b64}"
        cache[cache_key] = data_uri
        return data_uri

    return ""

# --- Artwork Helpers -------------------------------------------------------

def resolve_soundscape_artwork(
    chapter_key: str, story_key: Optional[str] = None
) -> Optional[Tuple[str, str]]:
    """
    Resolves the artwork for a soundscape, with a preference for story-specific assets.

    This function checks for artwork defined at the story level first, then falls
    back to chapter-level default artwork, and finally to the main chapter
    background if no specific artwork is found.

    Args:
        chapter_key: The key for the selected chapter.
        story_key: The key for the selected story (optional).

    Returns:
        A tuple containing the filename and subfolder of the artwork, or None if
        no suitable artwork can be found.
    """
    chapter_artwork = SOUNDSCAPE_ARTWORK.get(chapter_key)
    entry = None

    # Prioritize story-specific artwork if available
    if isinstance(chapter_artwork, dict):
        if story_key:
            entry = chapter_artwork.get(story_key)
        if not entry:
            entry = chapter_artwork.get("default")
    else:
        entry = chapter_artwork

    # Fallback to the main chapter background if no specific artwork is defined
    if entry is None:
        fallback_bg = CHAPTER_BACKGROUNDS.get(chapter_key)
        return (fallback_bg, "textures") if fallback_bg else None

    # Parse the artwork entry to get filename and subfolder
    if isinstance(entry, dict):
        filename = entry.get("filename")
        subfolder = entry.get("subfolder", "artworks")
    elif isinstance(entry, str):
        if "/" in entry:
            subfolder, filename = entry.split("/", 1)
        else:
            filename = entry
            subfolder = "artworks"
    else:
        return None

    return (filename, subfolder) if filename else None


# Build @font-face CSS with base64 data URIs (fallback to file URLs if missing)
def _font_src(filename: str) -> str:
    """
    Generates a CSS 'src' descriptor for a @font-face rule.

    This function prioritizes embedding the font as a base64 data URI for
    performance. If the font file cannot be loaded, it provides a fallback URL
    to the file in the 'assets/fonts' directory.

    Args:
        filename: The name of the font file (e.g., 'my-font.woff2').

    Returns:
        A CSS string for the 'src' property of a @font-face rule.
    """
    b64_font = load_asset_as_base64(get_asset_path("fonts", filename))
    if b64_font:
        # Embed the font directly into the CSS for faster loading
        return f"url('data:font/woff2;base64,{b64_font}') format('woff2')"
    else:
        # Provide a fallback URL if base64 encoding fails
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
if not parchment_texture_url:
    fallback_texture_url = get_texture_url("gita_scroll.webp")
    if fallback_texture_url:
        parchment_texture_url = fallback_texture_url

parchment_background_layers_css = (
    f"background-image: url('{parchment_texture_url}'), {PARCHMENT_GRADIENT_LAYERS};"
    if parchment_texture_url
    else f"background: {PARCHMENT_GRADIENT_LAYERS};"
)

parchment_card_background_css = (
    f"background-image: url('{parchment_texture_url}');"
    if parchment_texture_url
    else f"background: {PARCHMENT_GRADIENT_LAYERS};"
)

st.markdown(
    f"""
<style>
/* Local webfonts (base64 preferred) */
{font_face_css}
.stApp {{
    {parchment_background_layers_css}
    background-size: cover;
    background-repeat: no-repeat;
    font-family: var(--story-body, serif);
}}
.sr-only {{
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    border: 0;
}}
@media (min-width: 768px) {{
    .stApp {{
        background-attachment: fixed;
    }}
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
.prologue-wrapper {{
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
.prologue-wrapper .stCaption {{
    text-align: center;
    color: #5b3f2b;
}}
.prologue-wrapper .stButton button {{
    width: 100%;
    margin-top: 0.75rem;
}}
.prologue-wrapper .stButton button:focus-visible {{
    outline: 3px solid #1c3d5a;
    outline-offset: 3px;
    box-shadow: 0 0 0 4px rgba(255, 255, 255, 0.85), 0 0 12px rgba(28, 61, 90, 0.55);
}}

.parchment-card {{
    position: relative;
    padding: 1.25rem 1rem 1.1rem;
    border-radius: 18px;
    border: 2px solid rgba(112, 78, 28, 0.45);
    background: transparent;
    overflow: hidden;
    margin-bottom: 1.25rem;
    transition: transform 0.35s ease, box-shadow 0.35s ease, border-color 0.35s ease;
}}
.chapter-grid,
.scroll-grid {{
    display: grid;
    align-items: stretch;
    gap: 1.25rem;
    padding: 0.25rem 0.5rem 0.75rem;
    margin: 0 -0.5rem 1.75rem;
}}
.chapter-grid {{
    grid-template-columns: repeat(var(--chapter-count, 1), minmax(0, 1fr));
}}
.scroll-grid {{
    grid-template-columns: repeat(var(--scroll-count, 1), minmax(0, 1fr));
}}
.chapter-grid:focus-within .parchment-card,
.scroll-grid:focus-within .parchment-card {{
    outline: 2px solid rgba(212, 175, 55, 0.65);
    outline-offset: 4px;
}}
.chapter-card-wrapper,
.scroll-card-wrapper {{
    display: flex;
    min-width: 0;
}}
.chapter-card-wrapper .parchment-card,
.scroll-card-wrapper .parchment-card {{
    margin-bottom: 0;
    width: 100%;
}}
.parchment-card::before {{
    content: "";
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    top: clamp(120px, 44%, 200px);
    {parchment_card_background_css}
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center bottom;
    background-color: rgba(255, 248, 235, 0.92);
    background-blend-mode: multiply;
    box-shadow: inset 0 24px 42px rgba(106, 78, 34, 0.22);
    border-radius: 0 0 18px 18px;
    opacity: 0.95;
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
.parchment-card .stButton {{
    margin: 0;
    position: relative;
    z-index: 1;
}}
.parchment-card .stButton > button {{
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
.parchment-card .stButton > button:focus-visible {{
    outline: 3px solid #1c3d5a;
    outline-offset: 3px;
    box-shadow: 0 0 0 4px rgba(255, 255, 255, 0.85), 0 0 12px rgba(28, 61, 90, 0.55);
}}
.parchment-card .stButton > button:hover {{
    background: rgba(255, 255, 245, 0.95);
    color: #1b130a;
    border-color: rgba(212, 175, 55, 0.65);
}}
.parchment-card.active-card .stButton > button {{
    border-color: rgba(212, 175, 55, 0.85);
    color: #1b130a;
    background: rgba(255, 253, 245, 0.95);
}}
.scroll-card-body .stButton > button {{
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
.dice-animated {{ transform-origin: 50% 60%; }}
.forest-animated {{ transform-origin: 50% 90%; }}
.bow-animated {{ transform-origin: 20% 50%; }}
.bell-animated {{ transform-origin: 50% 6%; }}
.cosmic-egg-animated {{ transform-origin: 50% 50%; }}
.wheel-turns-animated {{ transform-origin: 50% 50%; }}
.river-oath-animated {{ transform-origin: 50% 85%; }}
.balance-restored-animated {{ transform-origin: 50% 55%; }}
.first-flame-animated {{ transform-origin: 50% 92%; }}
.suns-gift-animated {{ transform-origin: 50% 50%; }}
.brahmin-curse-animated {{ transform-origin: 50% 48%; }}
.friends-vow-animated {{ transform-origin: 50% 70%; }}
.birth-revealed-animated {{ transform-origin: 50% 45%; }}
.final-arrow-animated {{ transform-origin: 32% 50%; }}

@media (prefers-reduced-motion: no-preference) {{
    .lotus-animated {{ animation: bloom 6s ease-in-out infinite; }}
    .lotus-outline-animated {{ animation: outlinePulse 5.5s ease-in-out infinite; }}
    .chakra-animated {{ animation: spin 20s linear infinite; }}
    .trident-animated {{ animation: riseGlow 6s ease-in-out infinite; }}
    .dice-animated {{ animation: rock 3.6s ease-in-out infinite; }}
    .collapse-animated {{ animation: shiver 8s ease-in-out infinite; }}
    .restore-animated {{ animation: restoreBloom 7s ease-in-out infinite; }}
    .forest-animated {{ animation: sway 6s ease-in-out infinite alternate; }}
    .bow-animated {{ animation: draw 5s ease-in-out infinite; }}
    .galaxy-animated {{ animation: orbit 40s linear infinite; }}
    .bell-animated {{ animation: swing 4.2s ease-in-out infinite; }}
    .cosmic-egg-animated {{ animation: cosmicBreath 9s ease-in-out infinite; }}
    .wheel-turns-animated {{ animation: turnCycle 16s linear infinite; }}
    .river-oath-animated {{ animation: riverDrift 7s ease-in-out infinite; }}
    .balance-restored-animated {{ animation: balanceSway 8s ease-in-out infinite; }}
    .first-flame-animated {{ animation: flameFlicker 3.5s ease-in-out infinite; }}
    .suns-gift-animated {{ animation: solarPulse 6.5s ease-in-out infinite; }}
    .brahmin-curse-animated {{ animation: curseVeil 5.5s ease-in-out infinite; }}
    .friends-vow-animated {{ animation: vowPulse 6s ease-in-out infinite; }}
    .birth-revealed-animated {{ animation: revealGlow 7.5s ease-in-out infinite; }}
    .final-arrow-animated {{ animation: arrowRise 5s ease-in-out infinite; }}

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

    @keyframes cosmicBreath {{
        0% {{ transform: scale(0.98) rotate(-1deg); filter: drop-shadow(0 4px 12px rgba(120, 200, 255, 0.2)); }}
        40% {{ transform: scale(1.03) rotate(1deg); filter: drop-shadow(0 10px 22px rgba(120, 200, 255, 0.3)); }}
        70% {{ transform: scale(1.01) rotate(0deg); }}
        100% {{ transform: scale(0.98) rotate(-1deg); filter: drop-shadow(0 4px 12px rgba(120, 200, 255, 0.2)); }}
    }}

    @keyframes turnCycle {{
        from {{ transform: rotate(0deg); }}
        50% {{ transform: rotate(180deg); }}
        to {{ transform: rotate(360deg); }}
    }}

    @keyframes riverDrift {{
        0% {{ transform: translateX(0) rotate(-0.6deg); }}
        35% {{ transform: translateX(1.8px) rotate(0.4deg); }}
        65% {{ transform: translateX(-1.8px) rotate(-0.4deg); }}
        100% {{ transform: translateX(0) rotate(-0.6deg); }}
    }}

    @keyframes balanceSway {{
        0% {{ transform: rotate(-2deg) scale(0.995); }}
        50% {{ transform: rotate(2deg) scale(1.01); }}
        100% {{ transform: rotate(-2deg) scale(0.995); }}
    }}

    @keyframes flameFlicker {{
        0% {{ transform: scaleY(0.98) scaleX(0.99); filter: drop-shadow(0 4px 10px rgba(255, 140, 0, 0.35)); }}
        25% {{ transform: scaleY(1.05) scaleX(0.97); filter: drop-shadow(0 8px 16px rgba(255, 180, 0, 0.45)); }}
        50% {{ transform: scaleY(0.96) scaleX(1.02); filter: drop-shadow(0 5px 12px rgba(255, 120, 0, 0.3)); }}
        75% {{ transform: scaleY(1.08) scaleX(0.98); filter: drop-shadow(0 10px 20px rgba(255, 200, 60, 0.5)); }}
        100% {{ transform: scaleY(0.98) scaleX(0.99); filter: drop-shadow(0 4px 10px rgba(255, 140, 0, 0.35)); }}
    }}

    @keyframes solarPulse {{
        0% {{ transform: scale(0.97); filter: drop-shadow(0 4px 10px rgba(255, 215, 0, 0.25)); }}
        50% {{ transform: scale(1.05); filter: drop-shadow(0 8px 18px rgba(255, 240, 120, 0.4)); }}
        100% {{ transform: scale(0.97); filter: drop-shadow(0 4px 10px rgba(255, 215, 0, 0.25)); }}
    }}

    @keyframes curseVeil {{
        0% {{ transform: translateY(0) scale(1); opacity: 1; }}
        45% {{ transform: translateY(2px) scale(0.99); opacity: 0.85; }}
        55% {{ transform: translateY(-1px) scale(1.01); opacity: 0.75; }}
        100% {{ transform: translateY(0) scale(1); opacity: 1; }}
    }}

    @keyframes vowPulse {{
        0% {{ transform: scale(0.98); }}
        40% {{ transform: scale(1.02); }}
        70% {{ transform: scale(1); }}
        100% {{ transform: scale(0.98); }}
    }}

    @keyframes revealGlow {{
        0% {{ transform: translateY(2px) scale(0.98); filter: drop-shadow(0 2px 6px rgba(255, 255, 255, 0.2)); }}
        45% {{ transform: translateY(-2px) scale(1.02); filter: drop-shadow(0 8px 18px rgba(255, 255, 255, 0.35)); }}
        100% {{ transform: translateY(2px) scale(0.98); filter: drop-shadow(0 2px 6px rgba(255, 255, 255, 0.2)); }}
    }}

    @keyframes arrowRise {{
        0% {{ transform: translateX(0) translateY(0); }}
        30% {{ transform: translateX(-2px) translateY(-3px); }}
        60% {{ transform: translateX(1px) translateY(-6px); }}
        100% {{ transform: translateX(0) translateY(0); }}
    }}
}}

@media (prefers-reduced-motion: reduce) {{
    .lotus-animated,
    .lotus-outline-animated,
    .chakra-animated,
    .trident-animated,
    .dice-animated,
    .collapse-animated,
    .restore-animated,
    .forest-animated,
    .bow-animated,
    .galaxy-animated,
    .bell-animated,
    .cosmic-egg-animated,
    .wheel-turns-animated,
    .river-oath-animated,
    .balance-restored-animated,
    .first-flame-animated,
    .suns-gift-animated,
    .brahmin-curse-animated,
    .friends-vow-animated,
    .birth-revealed-animated,
    .final-arrow-animated {{
        animation: none !important;
    }}
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
# Core narrative metadata now lives in ui_constants.py to keep this module focused.
scene_assets = SCENE_ASSETS

def display_title(key: Optional[str]) -> str:
    """
    Translates a story's key into a human-readable title.

    This function looks up a predefined display title for a given story key.
    If a specific title is not found, it generates a default title by replacing
    underscores with spaces and capitalizing the words.

    Args:
        key: The key of the story (e.g., 'lotus_of_doubt').

    Returns:
        The display-friendly title for the story. Returns an empty string if the
        key is invalid.
    """
    if not isinstance(key, str) or not key:
        return ""
    return STORY_DISPLAY_TITLES.get(key, key.replace("_", " ").title())


@st.cache_data(show_spinner=False)
def register_audio(path: Optional[Path]) -> Optional[str]:
    """
    Registers an audio asset and returns a URL for it.

    This function first tries to use Streamlit's media manager for efficient serving.
    If that fails (e.g., in a non-standard environment), it falls back to embedding
    the audio as a base64 data URI. The result is cached to avoid reprocessing.

    Args:
        path: The absolute path to the audio file.

    Returns:
        A URL for the audio asset, or None if the file cannot be processed.
    """
    if path is None:
        return None

    resolved_path = path.resolve()
    if not resolved_path.exists():
        st.warning(f"Audio file not found: {resolved_path}")
        return None

    # Attempt to use Streamlit's media manager first
    try:
        from streamlit import runtime
        if runtime.exists():
            return runtime.get_instance().media_file_mgr.add(
                str(resolved_path),
                "audio/mpeg",
                coordinates=f"audio::{resolved_path.name}",
                file_name=resolved_path.name,
            )
    except (ImportError, AttributeError):
        # Fallback if runtime is not available
        pass

    # Fallback to base64 encoding
    data_uri = load_asset_as_base64(resolved_path)
    return f"data:audio/mpeg;base64,{data_uri}" if data_uri else None


def get_audio_for_story(chapter_key: str, story_key: str) -> Tuple[Optional[Path], Optional[Path]]:
    """
    Retrieves the audio file paths for a given story.

    This function acts as a router, determining the correct paths for a story's
    primary (narrative/chant) and ambient audio based on its chapter. It follows
    the standardized directory structure defined in `audio_builder.py`.

    Args:
        chapter_key: The key of the chapter the story belongs to.
        story_key: The key of the story.

    Returns:
        A tuple containing the Path objects for the primary and ambient audio files.
        Either or both can be None if not applicable for the story.
    """
    primary_path, ambient_path = None, None

    if chapter_key == "gita_scroll":
        primary_path = get_asset_path("audio/fadein", f"{story_key}_fadein.mp3")
        ambient_path = get_asset_path("audio/ambient", f"{story_key}_ambient_loop.mp3")
    elif chapter_key == "fall_of_dharma":
        primary_path = get_asset_path("audio/composite", f"{story_key}_composite.mp3")
        ambient_path = get_asset_path("audio/raw", "ambient_loop.mp3") # Shared ambient track
    elif chapter_key == "weapon_quest":
        primary_path = get_asset_path(f"audio/forest/{story_key}", f"{story_key}_mix.mp3")
        ambient_path = get_asset_path(f"audio/forest/{story_key}", "ambient.mp3")
    elif chapter_key == "birth_of_dharma":
        # Some stories in this chapter have unique audio mappings
        audio_key = BIRTH_STORY_AUDIO_MAP.get(story_key, story_key)
        primary_path = get_asset_path(f"audio/birth/{audio_key}", f"{audio_key}_mix.mp3")
    elif chapter_key == "trials_of_karna":
        primary_path = get_asset_path(f"audio/karna/{story_key}", f"{story_key}_mix.mp3")

    return primary_path, ambient_path


# --- UI Rendering: Chapter and Story Selection ---

# Retrieve chapter options from the narratives data
chapter_options = list(NARRATIVES.keys())
# Get the currently selected chapter from session state, defaulting to the first chapter
stored_chapter = st.session_state.get("selected_chapter", chapter_options[0])
if stored_chapter not in chapter_options:
    stored_chapter = chapter_options[0]
    st.session_state["selected_chapter"] = stored_chapter
selected_chapter = stored_chapter

# Create a container for the chapter selection grid
chapter_grid = st.container()
with chapter_grid:
    # Use custom CSS for a grid layout
    st.markdown("<div class='chapter-grid' role='list'>", unsafe_allow_html=True)

    # Iterate through each chapter to create a selection card
    for chapter in chapter_options:
        chapter_story_keys = list(NARRATIVES[chapter].keys())
        primary_story = chapter_story_keys[0] if chapter_story_keys else None

        # Load the icon for the chapter card (using the first story's icon)
        asset_info = scene_assets.get(primary_story) if primary_story else None
        icon_html = ""
        if asset_info:
            icon_html = load_animated_svg(
                asset_info["svg"], asset_info["anim_class"], asset_info["alt"]
            ) or ""

        # Determine if this is the active chapter for styling and accessibility
        is_active_chapter = (stored_chapter == chapter)
        active_class = "active-card" if is_active_chapter else ""
        aria_current_attr = " aria-current='true'" if is_active_chapter else ""
        sr_only_note = "<span class='sr-only'>Currently selected chapter</span>" if is_active_chapter else ""

        # Render the chapter card using st.markdown for custom HTML
        st.markdown("<div class='chapter-card-wrapper' role='listitem'>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="chapter-card parchment-card {active_class}" role="group"{aria_current_attr}>
                <div class="chapter-card-visual">{icon_html}</div>
                <div class="chapter-card-body">{sr_only_note}""",
            unsafe_allow_html=True,
        )

        # The button that selects the chapter
        if st.button(
            CHAPTER_TITLES.get(chapter, chapter.replace("_", " ").title()),
            key=f"chapter_btn_{chapter}",
            use_container_width=True,
            help="Reveal this chapter's illuminated scrolls.",
        ):
            selected_chapter = chapter
            st.session_state["selected_chapter"] = chapter
            # Default to the first story of the new chapter
            if chapter_story_keys:
                st.session_state["last_scroll"] = chapter_story_keys[0]
            st.experimental_rerun()

        st.markdown(
            f"""<p class="chapter-card-meta">{len(chapter_story_keys)} scrolls to explore</p>
               </div></div>""",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Ensure the selected chapter is stored in the session state
st.session_state["selected_chapter"] = selected_chapter

# Get the story options for the currently selected chapter
story_options = list(NARRATIVES[selected_chapter].keys())
# Determine the selected story, defaulting to the first story if necessary
if story_options:
    default_scroll = story_options[0]
    stored_scroll = st.session_state.get("last_scroll")
    if not stored_scroll or stored_scroll not in story_options:
        stored_scroll = default_scroll
    st.session_state["last_scroll"] = stored_scroll
else:
    stored_scroll = None

chapter_count = max(len(chapter_options), 1)
story_count = max(len(story_options), 1)

st.markdown(
    f"""
    <style>
        :root {{
            --chapter-count: {chapter_count};
            --scroll-count: {story_count};
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Create the story selection grid
selected_key = stored_scroll
scroll_grid = st.container()
with scroll_grid:
    st.markdown("<div class='scroll-grid' role='list'>", unsafe_allow_html=True)

    # Iterate through each story in the selected chapter
    for story_key in story_options:
        # Load the icon for the story card
        asset_info = scene_assets.get(story_key, scene_assets.get("lotus_of_doubt"))
        icon_html = ""
        if asset_info:
            icon_html = load_animated_svg(
                asset_info["svg"], asset_info["anim_class"], asset_info["alt"]
            ) or ""

        # Determine if this is the active story for styling and accessibility
        is_active_scroll = (stored_scroll == story_key)
        active_scroll_class = "active-card" if is_active_scroll else ""
        aria_selected_attr = " aria-selected='true'" if is_active_scroll else ""
        sr_only_scroll = "<span class='sr-only'>Currently selected scroll</span>" if is_active_scroll else ""

        # Render the story card
        st.markdown("<div class='scroll-card-wrapper' role='listitem'>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="scroll-card parchment-card {active_scroll_class}" role="group"{aria_selected_attr}>
                <div class="scroll-card-visual">{icon_html}</div>
                <div class="scroll-card-body">{sr_only_scroll}""",
            unsafe_allow_html=True,
        )

        # The button to select the story
        if st.button(
            display_title(story_key),
            key=f"story_btn_{story_key}",
            use_container_width=True,
            help="Unfurl this illuminated scroll.",
        ):
            selected_key = story_key
            st.session_state["last_scroll"] = story_key
            st.experimental_rerun()

        st.markdown("</div></div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Final check to ensure a story is selected if available
if not selected_key and story_options:
    selected_key = story_options[0]
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

# --- Dynamic Theming and Styling ---

# Dynamically set the page background and typography based on the selected chapter
chapter_bg_file = CHAPTER_BACKGROUNDS.get(selected_chapter)
chapter_bg_url = get_texture_url(chapter_bg_file) if chapter_bg_file else ""
if chapter_bg_url:
    overlay_presets = BACKGROUND_OVERLAYS
    overlay_config = overlay_presets.get(selected_chapter, overlay_presets["default"])

    # Inject CSS to update the background image and animated overlays
    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url('{chapter_bg_url}');
        background-size: cover;
        background-repeat: no-repeat;
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
    }}
    @media (min-width: 768px) {{
        .stApp {{
            background-attachment: fixed;
        }}
        .stApp::before {{
            position: fixed;
        }}
    }}
    @media (max-width: 767px) {{
        .stApp::before {{
            position: absolute;
            background-attachment: scroll;
        }}
    }}
    .stApp > header,
    .stApp > div,
    .stApp .block-container {{
        position: relative;
        z-index: 1;
    }}
    @media (prefers-reduced-motion: no-preference) {{
        .stApp::before {{
            animation: {overlay_config['animation']};
            transition: background-image 0.6s ease, opacity 1.2s ease;
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
    }}
    @media (prefers-reduced-motion: reduce) {{
        .stApp::before {{
            animation: none !important;
            transition: none !important;
        }}
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
    }}
    .mantra-pulse .mantra-syllable {{
        position: relative;
        display: inline-block;
    }}
    @media (prefers-reduced-motion: no-preference) {{
        .mantra-pulse::before,
        .mantra-pulse::after {{
            animation: mantraPulseRing 6s ease-in-out infinite;
        }}
        .mantra-pulse::after {{
            animation-delay: 3s;
        }}
        .mantra-pulse .mantra-syllable {{
            animation: mantraPulseInner 3s ease-in-out infinite;
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
    }}
    @media (prefers-reduced-motion: reduce) {{
        .mantra-pulse::before,
        .mantra-pulse::after,
        .mantra-pulse .mantra-syllable {{
            animation: none !important;
            transition: none !important;
        }}
    }}
    @media (max-width: 768px) {{
        .prologue-wrapper {{
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
        .parchment-card .stButton > button {{
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
        .chapter-grid,
        .scroll-grid {{
            margin: 0 -0.75rem 1.5rem;
            padding: 0.25rem 0.75rem 0.65rem;
            gap: 1rem;
        }}
        .chapter-card-wrapper,
        .scroll-card-wrapper {{
            flex: 0 0 clamp(240px, 80vw, 320px);
        }}
    }}
    </style>
    """,
        unsafe_allow_html=True,
    )


# --- Main Content Display ---

# This block renders the main content area if a story has been selected.
if selected_key:
    # Display the titles for the chapter and the selected story
    st.header(CHAPTER_TITLES.get(selected_chapter, selected_chapter.replace("_", " ").title()))
    st.subheader(display_title(selected_key))
    st.markdown('<div id="main-content"></div>', unsafe_allow_html=True)

    # Use a two-column layout for the SVG glyph and the text/audio content
    story_columns = st.container()
    with story_columns:
        col1, col2 = st.columns([1.2, 1])

        # Column 1: Animated SVG Glyph
        with col1:
            asset_info = scene_assets.get(selected_key, scene_assets.get("lotus_of_doubt"))
            if asset_info:
                animated_svg = load_animated_svg(
                    asset_info["svg"], asset_info["anim_class"], asset_info["alt"]
                )
                if animated_svg:
                    st.markdown(
                        f'<div role="img" aria-label="{asset_info["alt"]}" class="fadein" '
                        f'style="width:100%;max-width:420px;margin:auto;">{animated_svg}</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.error(f"SVG not found: {asset_info['svg']}")
            else:
                st.error("Asset info not found for the selected story.")

        # Column 2: Narrative, Chant, and Soundscape
        with col2:
            # Meditation/Narrative Text
            st.subheader("Meditation")
            narrative_text = NARRATIVES[selected_chapter].get(selected_key, "Narrative not found.")
            st.markdown(
                f'<blockquote class="fadein meditation-highlight">{narrative_text}</blockquote>',
                unsafe_allow_html=True,
            )

            # Chant Text
            st.subheader("Chant")
            chant_lines = CHANT_LINES.get(selected_chapter, {}).get(selected_key, [])
            if chant_lines:
                st.markdown(
                    '<blockquote class="fadein meditation-highlight">' + "<br>".join(chant_lines) + "</blockquote>",
                    unsafe_allow_html=True,
                )

            # Soundscape Player
            st.subheader("Soundscape")
            primary_audio_path, ambient_audio_path = get_audio_for_story(selected_chapter, selected_key)

            # Keys for managing state related to audio loading and toggles
            load_key = f"_audio_loaded::{selected_chapter}::{selected_key}"
            narrative_toggle_key = f"{load_key}::narrative_toggle"
            ambient_toggle_key = f"{load_key}::ambient_toggle"
            narrative_available = primary_audio_path is not None
            ambient_available = ambient_audio_path is not None

            # Resolve and display soundscape artwork
            artwork_info = resolve_soundscape_artwork(selected_chapter, selected_key)
            artwork_url = get_texture_url(artwork_info[0], artwork_info[1]) if artwork_info else ""
            soundscape_story = SOUNDSCAPE_DESCRIPTIONS.get(selected_chapter, "An immersive soundscape for your meditation.")

            # Accessibility attributes for the artwork
            chapter_title = CHAPTER_TITLES.get(selected_chapter, selected_chapter.replace("_", " ").title())
            soundscape_alt = f"Artwork for the {chapter_title} soundscape: {soundscape_story}"
            soundscape_alt_html = html.escape(soundscape_alt, quote=True)

            # Soundscape control panel
            with st.container():
                st.markdown('<div class="soundscape-panel">', unsafe_allow_html=True)
                art_col, info_col = st.columns([1.05, 1.6])
                with art_col:
                    if artwork_url:
                        st.markdown(f'<img src="{artwork_url}" alt="{soundscape_alt_html}" style="width:100%;" />', unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div role='img' aria-label='{soundscape_alt_html}' style='font-size:3rem;text-align:center;'>🕉️</div>", unsafe_allow_html=True)
                    st.caption("Artwork from the illuminated scroll.")

                with info_col:
                    st.markdown(f"<p class='soundscape-description'>{soundscape_story}</p>", unsafe_allow_html=True)
                    # Toggles for enabling/disabling audio streams
                    toggle_cols = st.columns(2)
                    narrative_enabled = toggle_cols[0].toggle(
                        "Narrative voice", value=True, key=narrative_toggle_key,
                        disabled=not narrative_available, help="Recitations and storytelling."
                    )
                    ambient_enabled = toggle_cols[1].toggle(
                        "Ambient drones", value=(selected_chapter == "gita_scroll"),
                        key=ambient_toggle_key, disabled=not ambient_available, help="Atmospheric sound beds."
                    )
                    st.caption("Choose which streams of sound to activate.")

                    # Button to lazy-load the audio
                    if st.button("Unveil the mantra", key=f"{load_key}::btn", use_container_width=True):
                        st.session_state[load_key] = True

                st.markdown("</div>", unsafe_allow_html=True)
            st.markdown('<hr class="soundscape-divider" />', unsafe_allow_html=True)

            # Audio player rendering (lazy-loaded)
            if st.session_state.get(load_key):
                try:
                    players_rendered = False
                    with st.spinner("Kindling the sacred frequencies…"):
                        # Render narrative audio player
                        if narrative_enabled and narrative_available:
                            narrative_url = register_audio(primary_audio_path)
                            if narrative_url:
                                st.markdown("<div class='soundscape-audio-label'>Narrative Incantation</div>", unsafe_allow_html=True)
                                st.audio(narrative_url, format="audio/mpeg")
                                players_rendered = True

                        # Render ambient audio player
                        if ambient_enabled and ambient_available:
                            ambient_url = register_audio(ambient_audio_path)
                            if ambient_url:
                                st.markdown("<div class='soundscape-audio-label'>Ambient Atmosphere</div>", unsafe_allow_html=True)
                                st.audio(ambient_url, format="audio/mpeg", loop=True)
                                players_rendered = True

                    if not players_rendered:
                        st.info("Select at least one audio stream to begin.")
                    else:
                        # Visual feedback that audio is active
                        st.markdown(
                            '<div class="mantra-pulse" role="img" aria-label="Mantra pulse animation"><span class="mantra-syllable">ॐ</span></div>',
                            unsafe_allow_html=True,
                        )
                        st.caption("Breathe with the glowing cadence as the mantra flows.")
                except FileNotFoundError:
                    st.warning("Audio files not found. Please run `python setup.py` to generate them.")
            else:
                st.caption("Press the mantra seal above to awaken this scroll's sacred soundscape.")


st.info(
    "Remember to run `python setup.py` first to download and process all the necessary audio files."
)
st.caption("Crafted with reverence • Powered by Streamlit")
