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
from narrative import NARRATIVES

# --- Base Directory ---
BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(page_title="Scroll of Dharma", page_icon="🕉️", layout="wide")
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


# --- Theme and CSS Injection ---
parchment_base64 = load_asset_as_base64(get_asset_path("textures", "parchment_bg.png"))

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


st.markdown(
    f"""
<style>
/* Local webfonts (base64 preferred) */
{font_face_css}
.stApp {{
    background-image: url('data:image/png;base64,{parchment_base64}');
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
    "gita_scroll": "gita_scroll.png",
    "fall_of_dharma": "fall_of_dharma.png",
    "weapon_quest": "weapon_quest.png",
    "birth_of_dharma": "birth_of_dharma.png",
    "trials_of_karna": "trials_of_karna.png",
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


def display_title(key: str) -> str:
    return STORY_DISPLAY_TITLES.get(key, key.replace("_", " ").title())


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
if "selected_chapter" not in st.session_state:
    st.session_state["selected_chapter"] = chapter_options[0]
selected_chapter = st.selectbox(
    "Choose a chapter:",
    options=chapter_options,
    format_func=lambda key: key.replace("_", " ").title(),
    help="Select a chapter from the epic.",
)
st.session_state["selected_chapter"] = selected_chapter
story_options = list(NARRATIVES[selected_chapter].keys())
if "last_scroll" not in st.session_state:
    st.session_state["last_scroll"] = story_options[0]
selected_key = st.selectbox(
    "Choose a scroll to unfold:",
    options=story_options,
    format_func=lambda key: display_title(key),
    help="Use arrow keys to navigate and Enter to select.",
)
st.session_state["last_scroll"] = selected_key
st.markdown(
    f"<small style='color:#FFD700;'>Bookmarked: {display_title(selected_key)} ({CHAPTER_TITLES.get(selected_chapter, selected_chapter.replace('_', ' ').title())})</small>",
    unsafe_allow_html=True,
)

# Override background based on selected chapter
chapter_bg_file = CHAPTER_BACKGROUNDS.get(selected_chapter)
if chapter_bg_file:
    chapter_bg_base64 = load_asset_as_base64(
        get_asset_path("textures", chapter_bg_file)
    )
    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url('data:image/png;base64,{chapter_bg_base64}');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
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

        # Soundscape section (lazy-load on click)
        st.subheader("Soundscape")
        primary_audio_path, ambient_audio_path = get_audio_for_story(
            selected_chapter, selected_key
        )
        autoplay_src = (
            ambient_audio_path
            if selected_chapter == "gita_scroll"
            else primary_audio_path
        )
        loop_attr = " loop" if selected_chapter == "gita_scroll" else ""
        load_key = f"_audio_loaded::{selected_chapter}::{selected_key}"
        cols = st.columns([1, 3])
        with cols[0]:
            if st.button("Load soundscape", key=load_key + "::btn"):
                st.session_state[load_key] = True
        if st.session_state.get(load_key):
            try:
                audio_b64 = load_asset_as_base64(autoplay_src)
                if not audio_b64:
                    raise FileNotFoundError(str(autoplay_src))
                st.markdown(
                    f"""<audio controls preload="none" playsinline{loop_attr} src="data:audio/mpeg;base64,{audio_b64}" style="width:100%"></audio>""",
                    unsafe_allow_html=True,
                )
            except FileNotFoundError:
                st.warning("Audio not found. Please run `python setup.py`.")
        else:
            st.caption("Click ‘Load soundscape’ to fetch audio for this scroll.")


st.info(
    "Remember to run `python setup.py` first to download and process all the necessary audio files."
)
st.caption("Crafted with reverence • Powered by Streamlit")
