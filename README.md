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

## ✍️ The Scribe's Tools (Configuration)

Should you feel the call to contribute to the Scroll, your path is clear.

*   **Narratives:** The heart of the scroll lies in `narrative.py`. Edit this file to alter the stories.
*   **Glyphs & Animations:** Add your own animated SVGs to `assets/svg/` and bind them to the narrative in `app.py`.
*   **Soundscapes:** The sources of the soundscapes are listed in `audio_builder.py`. Change the URLs and re-run `python setup.py` to forge new audio.
*   **Fonts:** The fonts are chosen in `download_fonts.py`. Add or remove families as you see fit.

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
