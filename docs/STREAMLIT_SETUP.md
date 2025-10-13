# Streamlit Version Setup (Legacy)

> **Note:** The Streamlit version is maintained for reference but the project has migrated to Astro for better performance. See the main [README.md](../README.md) for the current version.

## Prerequisites

*   Python 3.11+
*   `ffmpeg` on your system PATH ([Download here](https://ffmpeg.org))
*   Optional: `cookies.txt` in the project root for authenticated audio downloads

## Setup (PowerShell)

```powershell
# Create a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies, download fonts, and build audio assets
python setup.py

# Launch the app
streamlit run app.py
```

## Setup (Linux/macOS)

```bash
# Create a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies, download fonts, and build audio assets
python setup.py

# Launch the app
streamlit run app.py
```

## What `setup.py` Does

- Creates asset directories for audio, fonts, SVGs, and textures
- Installs Python dependencies from `requirements.txt`
- Confirms `ffmpeg` is available
- Downloads the required fonts
- Mixes the chapter soundscapes
- Writes a `config.json` manifest summarizing the generated assets

## Troubleshooting

*   **`ffmpeg` not found:** Install it from [ffmpeg.org](https://ffmpeg.org) and ensure it is in your system's PATH.
*   **Audio fails to download:** Some sources may be protected. A `cookies.txt` file from your browser, placed in the project root, may help.
*   **Autoplay is silent:** Some browsers require an interaction before they will play audio. A simple click or selection will awaken the soundscape.

## Files

The Streamlit version uses these files:

- `app.py` - Main Streamlit application
- `narrative.py` - Python narrative data
- `ui_constants.py` - UI configuration
- `audio_builder.py` - Audio processing scripts
- `download_fonts.py` - Font download utilities
- `requirements.txt` - Python dependencies
- `setup.py` - Setup script

These files are preserved for reference but are not used in the Astro version.
