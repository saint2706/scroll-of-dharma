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

# --- UI State ---
if "show_about" not in st.session_state:
    st.session_state["show_about"] = False


st.markdown(
    f"""
<style>
/* Local webfonts (woff2) */
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
/* Birth of Dharma: static icons, no animation */

/* Keyframes */
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

# components import was unused; removed obsolete import


# Story -> SVG mapping using newly added icons
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
}

# Friendly chapter titles
CHAPTER_TITLES = {
    "gita_scroll": "Gita Scroll",
    "fall_of_dharma": "Fall of Dharma",
    "weapon_quest": "Weapon Quest",
    "birth_of_dharma": "Birth of Dharma",
}

# Chapter -> background texture filename
CHAPTER_BACKGROUNDS = {
    "gita_scroll": "gita_scroll.png",
    "fall_of_dharma": "fall_of_dharma.png",
    "weapon_quest": "weapon_quest.png",
    "birth_of_dharma": "birth_of_dharma.png",
}

# Custom display titles for specific stories
STORY_DISPLAY_TITLES = {
    "sword_of_resolve": "Trident of Resolve",
}

# Chant lines per story for each chapter (public domain mantras)
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
}

# Map narrative keys to audio folder keys for Birth of Dharma
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

        # Soundscape section (kept as-is with single, autoplaying player)
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
        try:
            audio_b64 = load_asset_as_base64(autoplay_src)
            if not audio_b64:
                raise FileNotFoundError(str(autoplay_src))
            st.markdown(
                f"""<audio controls preload="auto" playsinline{loop_attr} src="data:audio/mpeg;base64,{audio_b64}" style="width:100%"></audio>""",
                unsafe_allow_html=True,
            )
        except FileNotFoundError:
            st.warning("Audio not found. Please run `python setup.py`.")


st.info(
    "Remember to run `python setup.py` first to download and process all the necessary audio files."
)
st.caption("Crafted with reverence • Powered by Streamlit")
