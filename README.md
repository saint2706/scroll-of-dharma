# 🕉️ The Scroll of Dharma

*“Dharma is not a rule. It is a rhythm.”*

<p align="center">
    <a href="LICENSE"><img alt="License" src="https://img.shields.io/github/license/saint2706/scroll-of-dharma"></a>
    <a href="https://www.python.org/"><img alt="Python" src="https://img.shields.io/badge/python-3.11%2B-blue?logo=python"></a>
    <a href="https://streamlit.io/"><img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-1.x-FF4B4B?logo=streamlit"></a>
    <a href="https://ffmpeg.org/"><img alt="ffmpeg required" src="https://img.shields.io/badge/ffmpeg-required-brightgreen"></a>
    <a href="https://github.com/saint2706/scroll-of-dharma/commits">
        <img alt="Last commit" src="https://img.shields.io/github/last-commit/saint2706/scroll-of-dharma">
    </a>
</p>

This is not just a project. It is a digital sanctuary, an interactive meditation on duty, doubt, and devotion. It is a place to witness ancient narratives come alive through animated glyphs, living soundscapes, and the timeless wisdom of the epics.

*“Doubt is not defeat, but the fertile soil of wisdom.”*

## ✨ The Experience

Unfurl the scroll and choose your path. Each chapter is a unique journey, a different facet of the diamond that is Dharma.

*   **Themed Narratives:** Immerse yourself in stories of conflict, choice, and transcendence, drawn from the heart of sacred texts.
*   **Animated Glyphs:** Watch as symbols of doubt, resolve, and cosmic balance gently move and breathe, each telling a story of its own.
*   **Living Soundscapes:** Let the curated audio guide your meditation. From the ambient chants of the Gita to the layered compositions of a kingdom's fall, each sound is a thread in the tapestry of the narrative.
*   **Evocative Typography:** Each chapter is rendered in a unique typeface, carefully chosen to reflect its tone and spirit.

## 📜 The Chapters

The Scroll of Dharma unfolds in four chapters, each a world unto itself.

*   **Gita Scroll:** Stand with Arjuna on the battlefield of Kurukshetra, where the whispers of doubt give way to the thunder of divine counsel.
*   **Fall of Dharma:** Witness the gilded court where a game of dice unravels an empire, and silence becomes the loudest cry of protest.
*   **Weapon Quest:** Journey into the wilderness of the self, where a warrior’s austerity earns him the weapons of the gods.
*   **Birth of Dharma:** Travel back to the cosmic dawn, where creation cracks open not with a bang, but with a breath of harmonious invocation.

*“To wield the divine, you must first dissolve the self.”*

## 🚀 Unfurling the Scroll (Quick Start)

To begin your journey, you must first prepare the vessel. These incantations, whispered into your terminal, will bring the Scroll to life.

**Prerequisites:**
*   Python 3.11+
*   `ffmpeg` must be on your system's PATH ([Download here](https://ffmpeg.org))
*   Optional: A `cookies.txt` file in the root of the project to aid in fetching audio from the ether.

**The Ritual (PowerShell):**

```powershell
# Create and enter the sacred space
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Invoke the setup scribe (installs dependencies, gathers fonts, and forges audio)
python setup.py

# Unfurl the scroll
streamlit run app.py
```

The `setup.py` scribe is a powerful incantation. It will:
- Ensure the sanctums for assets (audio, fonts, textures, svg) are prepared.
- Gather the necessary Python libraries.
- Verify the presence of `ffmpeg`.
- Summon the sacred fonts from the Google Fonts heavens.
- Forge the audio landscapes for each chapter.
- Leave a `config.json` file, a map of the assets it has created.

## ✍️ The Scribe's Tools (A Guide for Contributors)

Should you feel the call to contribute a new story to the Scroll, your path is clear. The process is a meditation in three parts: composing the narrative, forging the soundscape, and weaving the elements together.

Let us say you wish to add a new story called `"The River's Wisdom"` to the `"Birth of Dharma"` chapter.

### 1. Compose the Narrative

The heart of the scroll lies in `narrative.py`. Open this file and add your new story's text. Give it a unique key, like `the_rivers_wisdom`.

```python
# In narrative.py, within the "birth_of_dharma" chapter...
"the_rivers_wisdom": (
    "“The river does not carve the stone with force, but with persistence...”\n"
    "Your narrative continues here, a gentle stream of wisdom..."
),
```

### 2. Forge the Soundscape

The soul of the scroll echoes in `audio_builder.py`. Here, you must provide the sources for your new soundscape.

1.  **Add the Source:** Find the configuration dictionary for your chapter (e.g., `BIRTH_CHAPTERS`). Add a new entry for `the_rivers_wisdom` with URLs to your chosen audio from YouTube or Pixabay.

    ```python
    # In audio_builder.py, within BIRTH_CHAPTERS...
    "the_rivers_wisdom": [
        { "type": "pixabay", "url": "https://.../ambient_water.mp3" },
        { "type": "youtube", "url": "https://www.youtube.com/watch?v=..." },
    ],
    ```

2.  **Run the Forge:** After saving your changes, invoke the setup scribe again to create the audio asset.

    ```powershell
    python setup.py
    ```

    This will download, process, and mix your audio, placing the final file in `assets/audio/birth/the_rivers_wisdom/`.

### 3. Weave the Elements

The final thread is woven in `app.py`, the loom of the experience. Here, you will connect your new narrative to its visual glyph.

1.  **Add the Glyph:** Place your new SVG icon (e.g., `river.svg`) into the `assets/svg/` directory.

2.  **Bind the Assets:** In `app.py`, find the `scene_assets` dictionary. Add a new entry for `the_rivers_wisdom`, linking it to your SVG. If it has an animation, define its class.

    ```python
    # In app.py, within scene_assets...
    "the_rivers_wisdom": {
        "svg": "river.svg",
        "anim_class": "", # Add an animation class if you created one in the CSS
        "alt": "An icon of a flowing river representing wisdom",
    },
    ```
3. **Map the Audio (If Needed)**: Some chapters, like 'Birth of Dharma', require an extra step to map the narrative key to the audio key if they differ. In `app.py`, find the `BIRTH_STORY_AUDIO_MAP` and add your mapping if necessary. If your keys are identical, you can skip this.

That is all. Unfurl the scroll (`streamlit run app.py`) and behold your contribution. The river of Dharma flows on, enriched by your devotion.

## 🗺️ Anatomy of the Scroll (Structure)

```
.
├── app.py                     # The loom that weaves the experience
├── setup.py                   # The scribe that prepares the scroll
├── audio_builder.py           # The forge for the soundscapes
├── download_fonts.py          # The summoner of sacred fonts
├── narrative.py               # The heart of the scroll's wisdom
├── assets/
│   ├── audio/                 # The echoes of the narrative
│   ├── fonts/                 # The sacred characters
│   ├── svg/                   # The breathing glyphs
│   └── textures/              # The parchment of the scroll
├── requirements.txt
└── LICENSE
```

## ❓ Clearing the Path (Troubleshooting)

*   **`ffmpeg` not found:** You must install it from [ffmpeg.org](https://ffmpeg.org) and ensure it is in your system's PATH.
*   **Audio fails to download:** Some sources may be protected. A `cookies.txt` file from your browser, placed in the project root, may appease the guardians of the content.
*   **Autoplay is silent:** Some browsers require an interaction before they will play audio. A simple click or selection will awaken the soundscape.

---

*Crafted with reverence • Powered by Streamlit*
