# 🕉️ Scroll of Dharma

<p align="left">
    <a href="LICENSE"><img alt="License" src="https://img.shields.io/github/license/saint2706/scroll-of-dharma"></a>
    <a href="https://www.python.org/"><img alt="Python" src="https://img.shields.io/badge/python-3.11%2B-blue?logo=python"></a>
    <a href="https://streamlit.io/"><img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-1.x-FF4B4B?logo=streamlit"></a>
    <a href="https://ffmpeg.org/"><img alt="ffmpeg required" src="https://img.shields.io/badge/ffmpeg-required-brightgreen"></a>
    <a href="https://github.com/saint2706/scroll-of-dharma/commits">
        <img alt="Last commit" src="https://img.shields.io/github/last-commit/saint2706/scroll-of-dharma">
    </a>
    <a href="https://github.com/saint2706/scroll-of-dharma/issues">
        <img alt="Issues" src="https://img.shields.io/github/issues/saint2706/scroll-of-dharma">
    </a>
    <a href="https://github.com/saint2706/scroll-of-dharma">
        <img alt="Repo size" src="https://img.shields.io/github/repo-size/saint2706/scroll-of-dharma">
    </a>
  
</p>

An interactive meditation on duty, doubt, and devotion - experienced through themed narratives, animated glyphs, and living soundscapes.

Built with Python 3.11 and Streamlit. Audio is prepared with yt-dlp, ffmpeg, and pydub; fonts are fetched via the Google Fonts CSS API.

## ✨ Highlights

- Chapters and stories: choose a chapter (Gita Scroll, Fall of Dharma, Weapon Quest) and a story within it.
- Themed visuals: story-specific animated SVGs with gentle motion.
- Chant + Soundscape: a short chant text block per story, plus a single audio player that autoplays the right track for the chapter.
    - Gita Scroll: ambient loop autoplays (looping).
    - Fall of Dharma: composite mix autoplays.
    - Weapon Quest: forest mix autoplays.
- Per-chapter typography and textures: local webfonts and background textures set the tone for each chapter.
- One-step setup: fonts and audio are built with a single `setup.py` run.

## � Quick start (Windows PowerShell)

Prerequisites:
- Python 3.11+
- ffmpeg on your PATH (https://ffmpeg.org)
- Optional: `cookies.txt` in the project root to improve yt-dlp success

Commands (optional copy/paste):

```powershell
# create and activate venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# run setup (installs deps, downloads fonts, builds audio)
python setup.py

# launch the app
streamlit run app.py
```

What `setup.py` does:
- Ensures folders for assets (audio raw/fadein/ambient/composite/forest, fonts, textures, svg).
- Installs Python requirements with the current interpreter.
- Checks for ffmpeg and prints guidance if missing.
- Runs `download_fonts.py` to fetch local woff2 fonts via Google Fonts CSS API.
- Runs the consolidated `audio_builder.py`:
    - Gita chants: downloads, condenses to key moments (≤10 min), creates fade-in and ambient loop.
    - Fall of Dharma: builds 60s composites from layered sources with loudness targets and soft compression.
    - Weapon Quest: downloads ambient/instrument and optional layers, mixes a themed forest track per story.
- Writes `config.json` with a summary of generated assets.

## ▶️ Using the app

- Pick a chapter and story from the dropdowns.
- The chant block shows four short lines appropriate to the story.
- The Soundscape player autoplays the correct audio for the selected chapter.

Note: Some browsers may block autoplay with audio until you interact with the page (e.g., change a select or click Play).

## 📂 Structure (key files)

```
.
├── app.py                     # Streamlit UI (chapters/stories, SVG, chant, soundscape)
├── setup.py                   # One-step setup (deps, ffmpeg check, fonts, audio build)
├── download_fonts.py          # Google Fonts CSS API fetcher (woff2 -> assets/fonts)
├── audio_builder.py           # Consolidated audio pipeline (chants, composites, forest)
├── narrative.py               # Narrative text per chapter/story
├── assets/
│   ├── audio/
│   │   ├── raw/               # Source mp3s
│   │   ├── fadein/            # Gita intro tracks
│   │   ├── ambient/           # Gita ambient loops
│   │   ├── composite/         # Fall of Dharma composites
│   │   └── forest/<story>/    # Weapon Quest mixes and layers
│   ├── fonts/                 # Local webfonts (woff2)
│   ├── svg/                   # Story glyphs (animated via CSS)
│   └── textures/              # Per-chapter backgrounds
├── requirements.txt
└── LICENSE
```

## � Configuration & customization

- Narratives: edit `narrative.py` to update story text.
- SVGs and animations: add SVGs under `assets/svg/` and wire them in `app.py` (`scene_assets`).
- Audio sources: update URLs in `audio_builder.py` (`CHANTS`, `trilogy_sources`, `CHAPTERS`). Re-run `python setup.py`.
- Fonts: adjust families/weights in `download_fonts.py`’s `FAMILIES` map.

## ❓ Troubleshooting

- ffmpeg not found: install from https://ffmpeg.org and ensure `ffmpeg` is on your PATH (restart terminal afterward).
- yt-dlp 403/DRM/region blocks: place a browser-exported `cookies.txt` in the repo root; re-run setup. You can also update yt-dlp or manually download files into `assets/audio/...`.
- Autoplay blocked: click Play once; subsequent story changes usually autoplay.

## 📜 License & credits

See `LICENSE` for terms. Fonts via Google Fonts. Some ambient/instrument tracks from public-domain/CC sources; verify licenses for any replacements you add.

- Crafted with reverence • Powered by Streamlit
