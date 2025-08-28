"""
The main Streamlit application for the Scroll of Dharma.

This script weaves together narrative text, animated SVG glyphs, custom fonts,
and dynamically generated audio soundscapes to create an immersive, meditative
experience. It allows users to select a chapter and a specific story within
it, and the application dynamically updates the displayed content, styling,
and audio to match the chosen theme.

Key functionalities:
- Sets up the Streamlit page configuration and title.
- Loads and injects custom CSS for styling, including fonts and animations.
- Defines data structures that map stories to their assets (SVGs, audio, etc.).
- Creates the user interface with select boxes for chapter and story selection.
- Displays the narrative text, animated SVG, and an audio player.
- Dynamically changes the background and typography based on the selected chapter.
"""
import streamlit as st
from pathlib import Path
import re
import base64
from narrative import NARRATIVES

# --- Base Directory ---
BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(page_title="Scroll of Dharma", page_icon="🕉️", layout="wide")
st.title("🕉️ The Scroll of Dharma")


# --- Asset Loading Functions ---
def get_asset_path(subfolder: str, filename: str) -> Path:
    """
    Constructs an absolute path to an asset in the 'assets' directory.

    Args:
        subfolder: The name of the subfolder within 'assets' (e.g., 'svg', 'audio').
        filename: The name of the asset file.

    Returns:
        An absolute Path object to the asset.
    """
    return BASE_DIR / "assets" / subfolder / filename


@st.cache_data
def load_asset_as_base64(path: Path) -> str:
    """
    Loads a binary file and returns its base64 encoded string.

    This is used for embedding images and audio directly into the HTML,
    avoiding the need for separate file requests. The result is cached
    to prevent re-reading files from disk on every interaction.

    Args:
        path: The absolute path to the binary file.

    Returns:
        A base64 encoded string of the file's content, or an empty string
        if the file is not found.
    """
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return ""


def load_animated_svg(filename: str, css_class: str, alt_text: str) -> str | None:
    """
    Loads an SVG file, injects a CSS class for animation, and adds accessibility attributes.

    Args:
        filename: The SVG filename in the 'assets/svg' directory.
        css_class: The CSS class to inject into the <svg> tag for animations.
        alt_text: The alternative text for screen readers.

    Returns:
        The modified SVG content as a string, or None if the file is not found.
    """
    svg_path = get_asset_path("svg", filename)
    try:
        with open(svg_path, "r", encoding="utf-8") as f:
            svg_content = f.read()
            # Use regex to add class and accessibility attributes to the <svg> tag
            svg_content = re.sub(
                r"<svg",
                f'<svg class="{css_class}" role="img" aria-label="{alt_text}"',
                svg_content,
                count=1,
            )
        return svg_content
    except FileNotFoundError:
        return None


# --- Theme and CSS Injection ---
# Load the default parchment background texture. This will be overridden by chapter-specific textures later.
parchment_base64 = load_asset_as_base64(get_asset_path("textures", "parchment_bg.png"))

# Initialize session state for UI elements.
if "show_about" not in st.session_state:
    st.session_state["show_about"] = False


# Inject custom CSS for fonts, animations, and overall styling.
st.markdown(
    f"""
<style>
/* Local webfonts (woff2) downloaded via download_fonts.py */
@font-face {{ font-family:'Cormorant Garamond'; src:url('assets/fonts/CormorantGaramond-400.woff2') format('woff2'); font-weight:400; font-style:normal; font-display:swap; }}
@font-face {{ font-family:'Cormorant Garamond'; src:url('assets/fonts/CormorantGaramond-700.woff2') format('woff2'); font-weight:700; font-style:normal; font-display:swap; }}
@font-face {{ font-family:'Cormorant Garamond'; src:url('assets/fonts/CormorantGaramond-Italic-400.woff2') format('woff2'); font-weight:400; font-style:italic; font-display:swap; }}

@font-face {{ font-family:'EB Garamond'; src:url('assets/fonts/EBGaramond-400.woff2') format('woff2'); font-weight:400; font-style:normal; font-display:swap; }}
@font-face {{ font-family:'EB Garamond'; src:url('assets/fonts/EBGaramond-700.woff2') format('woff2'); font-weight:700; font-style:normal; font-display:swap; }}
@font-face {{ font-family:'EB Garamond'; src:url('assets/fonts/EBGaramond-Italic-400.woff2') format('woff2'); font-weight:400; font-style:italic; font-display:swap; }}

@font-face {{ font-family:'Cinzel'; src:url('assets/fonts/Cinzel-400.woff2') format('woff2'); font-weight:400; font-style:normal; font-display:swap; }}
@font-face {{ font-family:'Cinzel'; src:url('assets/fonts/Cinzel-700.woff2') format('woff2'); font-weight:700; font-style:normal; font-display:swap; }}

@font-face {{ font-family:'Spectral'; src:url('assets/fonts/Spectral-400.woff2') format('woff2'); font-weight:400; font-style:normal; font-display:swap; }}
@font-face {{ font-family:'Spectral'; src:url('assets/fonts/Spectral-700.woff2') format('woff2'); font-weight:700; font-style:normal; font-display:swap; }}
@font-face {{ font-family:'Spectral'; src:url('assets/fonts/Spectral-Italic-400.woff2') format('woff2'); font-weight:400; font-style:italic; font-display:swap; }}

@font-face {{ font-family:'Cormorant Unicase'; src:url('assets/fonts/CormorantUnicase-400.woff2') format('woff2'); font-weight:400; font-style:normal; font-display:swap; }}
@font-face {{ font-family:'Cormorant Unicase'; src:url('assets/fonts/CormorantUnicase-700.woff2') format('woff2'); font-weight:700; font-style:normal; font-display:swap; }}

@font-face {{ font-family:'Alegreya'; src:url('assets/fonts/Alegreya-400.woff2') format('woff2'); font-weight:400; font-style:normal; font-display:swap; }}
@font-face {{ font-family:'Alegreya'; src:url('assets/fonts/Alegreya-700.woff2') format('woff2'); font-weight:700; font-style:normal; font-display:swap; }}
@font-face {{ font-family:'Alegreya'; src:url('assets/fonts/Alegreya-Italic-400.woff2') format('woff2'); font-weight:400; font-style:italic; font-display:swap; }}

@font-face {{ font-family:'Noto Serif Devanagari'; src:url('assets/fonts/NotoSerifDevanagari-400.woff2') format('woff2'); font-weight:400; font-style:normal; font-display:swap; }}
@font-face {{ font-family:'Noto Serif Devanagari'; src:url('assets/fonts/NotoSerifDevanagari-700.woff2') format('woff2'); font-weight:700; font-style:normal; font-display:swap; }}

@font-face {{ font-family:'Tiro Devanagari Sanskrit'; src:url('assets/fonts/TiroDevanagariSanskrit-400.woff2') format('woff2'); font-weight:400; font-style:normal; font-display:swap; }}

/* Base application styling */
.stApp {{
    background-image: url('data:image/png;base64,{parchment_base64}');
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    font-family: var(--story-body, serif);
}}

/* Styling for the narrative text blocks */
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
/* Note: Birth of Dharma icons are static and have no animations. */

/* CSS Keyframes for animations */
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

/* Improve select box labels */
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


# --- Data Mappings ---

# Maps story keys (from narrative.py) to their corresponding SVG assets and animation classes.
# This allows the app to dynamically select the correct visual for each story.
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
        "anim_class": "",  # Static SVG
        "alt": "Cosmic egg icon representing the first breath",
    },
    "wheel_turns": {
        "svg": "wheel_turns.svg",
        "anim_class": "",  # Static SVG
        "alt": "Turning wheel icon representing the golden parchment",
    },
    "river_oath": {
        "svg": "river_oath.svg",
        "anim_class": "",  # Static SVG
        "alt": "River oath icon representing flowing wisdom",
    },
    "balance_restored": {
        "svg": "balance_restored.svg",
        "anim_class": "",  # Static SVG
        "alt": "Balance restored icon representing sacred glyphs",
    },
    "first_flame": {
        "svg": "sacred_flame.svg",
        "anim_class": "",  # Static SVG
        "alt": "Sacred flame icon representing the awakening scroll",
    },
}

# Defines user-friendly display titles for the chapter selection dropdown.
CHAPTER_TITLES = {
    "gita_scroll": "Gita Scroll",
    "fall_of_dharma": "Fall of Dharma",
    "weapon_quest": "Weapon Quest",
    "birth_of_dharma": "Birth of Dharma",
}

# Maps chapter keys to their specific background texture image files.
CHAPTER_BACKGROUNDS = {
    "gita_scroll": "gita_scroll.png",
    "fall_of_dharma": "fall_of_dharma.png",
    "weapon_quest": "weapon_quest.png",
    "birth_of_dharma": "birth_of_dharma.png",
}

# Provides custom, user-friendly display titles for specific stories in the dropdowns.
# If a story key is not in this map, a titleized version of the key is used as a fallback.
STORY_DISPLAY_TITLES = {
    "sword_of_resolve": "Trident of Resolve",
}

# Contains the lines of chants (public domain mantras) for each story.
# The structure is {chapter_key: {story_key: [line1, line2, ...]}}.
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
        # Aliases for 'Birth of Dharma' to map narrative keys (used for SVGs)
        # to the same chants as the audio keys.
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
}

# The 'Birth of Dharma' chapter uses different keys for its narrative/SVG assets
# versus its audio assets. This map translates the narrative/SVG key (e.g., 'cosmic_egg')
# to the corresponding audio folder key (e.g., 'cosmic_breath').
BIRTH_STORY_AUDIO_MAP = {
    "cosmic_egg": "cosmic_breath",
    "wheel_turns": "awakening_scroll",
    "river_oath": "flowing_wisdom",
    "balance_restored": "glyphs_of_dharma",
    "first_flame": "golden_parchment",
}


def display_title(key: str) -> str:
    """
    Generates a user-friendly title for a story key.

    Uses STORY_DISPLAY_TITLES for custom titles, otherwise formats the key
    by replacing underscores with spaces and capitalizing words.

    Args:
        key: The story key (e.g., 'sword_of_resolve').

    Returns:
        A formatted, user-friendly string for display.
    """
    return STORY_DISPLAY_TITLES.get(key, key.replace("_", " ").title())


def get_audio_for_story(chapter_key: str, story_key: str) -> tuple[Path | None, Path | None]:
    """
    Determines the correct primary and ambient audio files for a given story.

    The audio structure varies by chapter. This function abstracts away the
    logic of finding the correct file paths based on the selected chapter
    and story.

    Args:
        chapter_key: The key of the selected chapter (e.g., 'gita_scroll').
        story_key: The key of the selected story (e.g., 'lotus_of_doubt').

    Returns:
        A tuple containing the Path objects for the primary audio and the
        ambient audio, respectively. Either can be None if not applicable.
    """
    primary_url = None
    ambient_url = None

    if chapter_key == "gita_scroll":
        primary_url = get_asset_path("audio/fadein", f"{story_key}_fadein.mp3")
        ambient_url = get_asset_path("audio/ambient", f"{story_key}_ambient_loop.mp3")
    elif chapter_key == "fall_of_dharma":
        primary_url = get_asset_path("audio/composite", f"{story_key}_composite.mp3")
        ambient_url = get_asset_path("audio/raw", "ambient_loop.mp3")  # Shared ambient track
    elif chapter_key == "weapon_quest":
        primary_url = get_asset_path(f"audio/forest/{story_key}", f"{story_key}_mix.mp3")
        ambient_url = get_asset_path(f"audio/forest/{story_key}", "ambient.mp3")
    elif chapter_key == "birth_of_dharma":
        # Use the mapping to find the correct audio folder for the story
        mapped_audio_key = BIRTH_STORY_AUDIO_MAP.get(story_key, story_key)
        primary_url = get_asset_path(f"audio/birth/{mapped_audio_key}", f"{mapped_audio_key}_mix.mp3")
        # This chapter has no separate ambient track.

    return primary_url, ambient_url


# --- Main Application Logic ---

# Build chapter and story options from the NARRATIVES data
chapter_options = list(NARRATIVES.keys())
if "selected_chapter" not in st.session_state:
    st.session_state["selected_chapter"] = chapter_options[0]

# Chapter selection dropdown
selected_chapter = st.selectbox(
    "Choose a chapter:",
    options=chapter_options,
    format_func=lambda key: CHAPTER_TITLES.get(key, key.replace("_", " ").title()),
    help="Select a chapter from the epic.",
)
st.session_state["selected_chapter"] = selected_chapter

# Story selection dropdown, dynamically updated based on the chosen chapter
story_options = list(NARRATIVES[selected_chapter].keys())
if "last_scroll" not in st.session_state:
    st.session_state["last_scroll"] = story_options[0]

selected_key = st.selectbox(
    "Choose a scroll to unfold:",
    options=story_options,
    format_func=display_title,
    help="Use arrow keys to navigate and Enter to select.",
)
st.session_state["last_scroll"] = selected_key

# Display a small "bookmark" of the current selection
st.markdown(
    f"<small style='color:#FFD700;'>Bookmarked: {display_title(selected_key)} ({CHAPTER_TITLES.get(selected_chapter, selected_chapter.replace('_', ' ').title())})</small>",
    unsafe_allow_html=True,
)

# Dynamically override the background and typography based on the selected chapter
chapter_bg_file = CHAPTER_BACKGROUNDS.get(selected_chapter)
if chapter_bg_file:
    chapter_bg_base64 = load_asset_as_base64(
        get_asset_path("textures", chapter_bg_file)
    )
    # Inject CSS to set the background image and define chapter-specific font variables
    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url('data:image/png;base64,{chapter_bg_base64}');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    /* Per-chapter typography using CSS variables */
    :root {{
        {('--story-head: "Cormorant Garamond", serif;' if selected_chapter == 'gita_scroll' else '')}
        {('--story-body: "EB Garamond", "Noto Serif Devanagari", "Tiro Devanagari Sanskrit", serif;' if selected_chapter == 'gita_scroll' else '')}
        {('--story-head: "Cinzel", serif;' if selected_chapter == 'fall_of_dharma' else '')}
        {('--story-body: "Spectral", "Noto Serif Devanagari", "Tiro Devanagari Sanskrit", serif;' if selected_chapter == 'fall_of_dharma' else '')}
        {('--story-head: "Cormorant Unicase", serif;' if selected_chapter == 'weapon_quest' else '')}
        {('--story-body: "Alegreya", "Noto Serif Devanagari", "Tiro Devanagari Sanskrit", serif;' if selected_chapter == 'weapon_quest' else '')}
        {('--story-head: "Cormorant Garamond", serif;' if selected_chapter == 'birth_of_dharma' else '')}
        {('--story-body: "EB Garamond", "Noto Serif Devanagari", "Tiro Devanagari Sanskrit", serif;' if selected_chapter == 'birth_of_dharma' else '')}
    }}
    /* Apply fonts to content */
    h2, h3 {{ font-family: var(--story-head, serif) !important; }}
    .meditation-highlight, .stMarkdown p, .stMarkdown li {{ font-family: var(--story-body, serif) !important; }}
    </style>
    """,
        unsafe_allow_html=True,
    )

# --- Content Display ---

if selected_key:
    # Display titles and create the main layout
    st.header(CHAPTER_TITLES.get(selected_chapter, selected_chapter.replace("_", " ").title()))
    st.subheader(display_title(selected_key))
    st.markdown('<div id="main-content"></div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1.2, 1])

    # Left column: Animated SVG
    with col1:
        # Get the SVG info, with a fallback to the default 'lotus_of_doubt'
        asset_info = scene_assets.get(selected_key, scene_assets["lotus_of_doubt"])
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

    # Right column: Narrative, Chant, and Soundscape
    with col2:
        # Meditation (Narrative Text)
        st.subheader("Meditation")
        narrative_text = NARRATIVES[selected_chapter].get(selected_key, "Narrative not found.")
        st.markdown(
            f'<blockquote class="fadein meditation-highlight">{narrative_text}</blockquote>',
            unsafe_allow_html=True,
        )

        # Chant Section
        st.subheader("Chant")
        chant_lines = CHANT_LINES.get(selected_chapter, {}).get(selected_key, [])
        if chant_lines:
            st.markdown(
                '<blockquote class="fadein meditation-highlight">'
                + "<br>".join(chant_lines)
                + "</blockquote>",
                unsafe_allow_html=True,
            )

        # Soundscape Section
        st.subheader("Soundscape")
        primary_audio_path, ambient_audio_path = get_audio_for_story(selected_chapter, selected_key)

        # Determine which audio to autoplay and whether it should loop
        autoplay_src = primary_audio_path
        loop_attr = ""
        # The 'gita_scroll' chapter has a special case where the ambient track is the primary autoplay source.
        if selected_chapter == "gita_scroll":
            autoplay_src = ambient_audio_path
            loop_attr = " loop"

        if autoplay_src:
            try:
                audio_b64 = load_asset_as_base64(autoplay_src)
                if not audio_b64:
                    raise FileNotFoundError(f"Audio file is empty: {autoplay_src}")
                st.markdown(
                    f"""<audio controls preload="auto" playsinline{loop_attr} src="data:audio/mpeg;base64,{audio_b64}" style="width:100%"></audio>""",
                    unsafe_allow_html=True,
                )
            except FileNotFoundError:
                st.warning(f"Audio not found at '{autoplay_src}'. Please run `python setup.py`.")
        else:
            st.info("No primary soundscape for this story.")


# --- Footer ---
st.info(
    "Remember to run `python setup.py` first to download and process all the necessary audio files."
)
st.caption("Crafted with reverence • Powered by Streamlit")
