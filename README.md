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

The Scroll of Dharma is an interactive story lab built with Streamlit. Animated glyphs, reactive themes, and scored soundscapes bring epic turning points into a focused reading flow. Pick a chapter, inspect the pressure on every hero, and track the consequences of each choice.

## ✨ The Experience

Load the app, make a call, and watch the interface respond.

*   **Story-first reading:** Each narrative foregrounds the stakes, the conflict, and the payoff—no filler, just the pivotal beats.
*   **Instant visual shifts:** Chapter swaps trigger new typography, textures, and animated glyphs tuned to the scenario.
*   **Sound on demand:** Optional soundscapes add weight to the moment without forcing autoplay.
*   **Built for focus:** Minimal controls, fast loading assets, and a clean layout keep attention on the choice in front of you.

## 📜 The Chapters

Five chapters cover the critical pivots of the epic. Each one surfaces a decision that tilts the world.

*   **Gita Scroll:** Arjuna halts a war, interrogates duty, and chooses how to fight.
*   **Fall of Dharma:** A fixed dice game topples a kingdom while a court watches in silence.
*   **Weapon Quest:** Training, divine trials, and discipline decide who earns celestial weapons.
*   **Birth of Dharma:** Creation itself balances promises between fire, water, and motion.
*   **Trials of Karna:** Loyalty, secrecy, and a fatal curse lock a hero into his final stand.

*“To wield the divine, you must first dissolve the self.”*

## 🚀 Quick Start

Spin up the project with a standard Python workflow.

**Prerequisites:**
*   Python 3.11+
*   `ffmpeg` on your system PATH ([Download here](https://ffmpeg.org))
*   Optional: `cookies.txt` in the project root for authenticated audio downloads

**Setup (PowerShell):**

```powershell
# Create a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies, download fonts, and build audio assets
python setup.py

# Launch the app
streamlit run app.py
```

`setup.py` handles environment prep:
- Creates asset directories for audio, fonts, SVGs, and textures.
- Installs Python dependencies.
- Confirms `ffmpeg` is available.
- Downloads the required fonts.
- Mixes the chapter soundscapes.
- Writes a `config.json` manifest summarizing the generated assets.

## ✍️ The Scribe's Tools (A Guide for Contributors)

Should you feel the call to contribute a new story to the Scroll, your path is clear. The process is a meditation in three parts: composing the narrative, forging the soundscape, and weaving the elements together.

> **Keep your scroll aligned.** Before pushing your changes, rebase your branch onto the latest `main` so that the automated merge check in CI can complete without conflict.

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

### Development workflow and quality gates

The scroll now follows a shared rhythm for code style and quality checks, codified in `pyproject.toml`. Before opening a pull request, invoke the following guardians:

```bash
black --check .
ruff check .
mypy app.py narrative.py audio_builder.py setup.py
pytest
pip-audit --strict
```

These same commands run automatically on GitHub Actions for both Linux and Windows environments, so keeping them green locally will help your contribution sail smoothly through the review current.

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
