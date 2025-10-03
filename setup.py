"""
Setup script for the Scroll of Dharma project.

This script orchestrates the entire setup process required to run the application.
It is designed to be run once by the user before launching the Streamlit app for
the first time. Its primary goal is to automate the preparation of the project
environment, including asset creation and dependency installation.

The setup process includes:
1.  **Ensuring Directory Structure**: Creates all necessary 'assets' subdirectories
    to ensure that generated files have a place to go.
2.  **Installing Dependencies**: Installs all required Python packages from
    `requirements.txt` using pip.
3.  **Checking for FFmpeg**: Verifies that FFmpeg is installed and available in the
    system's PATH, as it is a crucial dependency for audio processing with Pydub.
4.  **Running Asset Pipelines**: Executes the `download_fonts.py` and
    `audio_builder.py` scripts to download and generate all required font and
    audio assets.
5.  **Writing a Configuration File**: Creates a `config.json` file that summarizes
    the setup process, including which assets were created and whether dependencies
    like FFmpeg were found. This file is for user reference and debugging.
"""

import importlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

# A list of all directories that the application expects to exist.
EXPECTED_DIRS = [
    "assets/audio/raw",
    "assets/audio/fadein",
    "assets/audio/ambient",
    "assets/audio/composite",
    "assets/audio/birth",
    "assets/audio/forest/celestial_audience",
    "assets/audio/forest/forest_of_austerity",
    "assets/audio/forest/shiva_and_the_hunter",
    "assets/audio/forest/trial_of_heaven",
    "assets/fonts",
    "assets/audio/karna",
    "assets/textures",
    "assets/svg",
]

# The path for the final configuration file.
CONFIG_PATH = Path("config.json")


def ensure_structure():
    """
    Creates the necessary directory structure under the 'assets' folder.

    This function iterates through the `EXPECTED_DIRS` list and creates each
    directory if it doesn't already exist, preventing errors when other scripts
    try to write files to these locations.
    """
    print("📁 Ensuring folder structure...")
    for folder in EXPECTED_DIRS:
        Path(folder).mkdir(parents=True, exist_ok=True)
    print("✅ Folder structure verified.")


def install_dependencies():
    """
    Installs Python dependencies from the `requirements.txt` file.

    This function uses the current Python executable to run pip, ensuring that
    dependencies are installed in the correct environment.
    """
    print("📦 Installing dependencies...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True,
            capture_output=True,
            text=True,
        )
        print("✅ Dependencies installed.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e.stderr}")
        sys.exit(1)


def check_ffmpeg() -> bool:
    """
    Checks if FFmpeg is installed and accessible in the system's PATH.

    Pydub, which is used for audio processing in `audio_builder.py`, requires
    FFmpeg for handling different audio formats. This function verifies its
    presence and provides guidance if it's missing.

    Returns:
        True if FFmpeg is found and executable, False otherwise.
    """
    print("🔎 Checking ffmpeg availability...")
    exe = shutil.which("ffmpeg")
    if exe:
        try:
            # Run `ffmpeg -version` to confirm it's a working installation.
            subprocess.run(
                [exe, "-version"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
            print(f"✅ ffmpeg found: {exe}")
            return True
        except Exception:
            pass  # The found executable is not working.
    print("⚠️ ffmpeg not found or not working. Pydub requires ffmpeg to process audio.")
    print(
        "   Install from https://ffmpeg.org/ and ensure it's on your PATH,\n"
        "   then rerun setup if audio fails."
    )
    return False


def run_fonts_pipeline() -> int:
    """
    Executes the font download pipeline by running the `download_fonts.py` script.

    This function runs the font downloader as a separate process and captures its
    exit code to report success or failure.

    Returns:
        The exit code of the subprocess. An exit code of 0 indicates success.
    """
    print("🔤 Downloading webfonts via Google Fonts API...")
    try:
        res = subprocess.run([sys.executable, "download_fonts.py"], check=False)
        code = res.returncode or 0
        if code == 0:
            print("✅ Fonts downloaded.")
        else:
            print(f"⚠️ Font download finished with code {code}.")
        return code
    except FileNotFoundError:
        print("⚠️ download_fonts.py not found; skipping font download.")
        return 0


def run_audio_pipeline() -> None:
    """
    Executes the full audio generation pipeline from `audio_builder.py`.

    This function dynamically imports the `audio_builder` module and calls the
    builder function for each chapter. Each call is wrapped in a try-except
    block to make the pipeline fault-tolerant, allowing it to continue even if
    one part fails (e.g., due to a download error for a specific audio file).
    """
    print("🎼 Running consolidated audio pipeline...")
    try:
        ab = importlib.import_module("audio_builder")
    except Exception as e:
        print(f"❌ Failed to import audio_builder: {e}")
        return

    # Run each chapter's build process independently to be robust against failures.
    try:
        ab.build_chant_and_ambient()
    except Exception as e:
        print(f"⚠️ build_chant_and_ambient failed: {e}")
    try:
        ab.build_trilogy()
    except Exception as e:
        print(f"⚠️ build_trilogy failed: {e}")
    try:
        ab.build_forest_stories()
    except Exception as e:
        print(f"⚠️ build_forest_stories failed: {e}")
    try:
        if hasattr(ab, "build_birth_of_dharma"):
            ab.build_birth_of_dharma()
    except Exception as e:
        print(f"⚠️ build_birth_of_dharma failed: {e}")
    try:
        if hasattr(ab, "build_trials_of_karna"):
            ab.build_trials_of_karna()
    except Exception as e:
        print(f"⚠️ build_trials_of_karna failed: {e}")
    print("✅ Audio assets generation attempted.")


def scan_audio_outputs() -> dict:
    """
    Scans the 'assets/audio' directory to create a summary of generated files.

    This function helps verify the output of the audio pipeline by collecting
    the paths of all generated MP3 files, categorized by their type or chapter.
    This summary is then included in the final `config.json`.

    Returns:
        A dictionary summarizing the paths of all found MP3 files.
    """
    base = Path("assets/audio")

    def _collect(directory: Path, pattern: str) -> list[str]:
        if not directory.exists():
            return []
        return [str(p) for p in directory.glob(pattern)]

    def _collect_nested(directory: Path) -> dict:
        if not directory.exists():
            return {}
        result = {}
        for sub in directory.iterdir():
            if sub.is_dir():
                files = [str(p) for p in sub.glob("*.mp3")]
                if files:
                    result[sub.name] = files
        return result

    return {
        "fadein": _collect(base / "fadein", "*_fadein.mp3"),
        "ambient": _collect(base / "ambient", "*_ambient_loop.mp3"),
        "composite": _collect(base / "composite", "*_composite.mp3"),
        "forest": _collect_nested(base / "forest"),
        "birth": _collect_nested(base / "birth"),
        "karna": _collect_nested(base / "karna"),
    }


def write_config(audio_summary: dict, ffmpeg_ok: bool, font_status: int):
    """
    Writes a final `config.json` file with a summary of the setup process.

    This file serves as a record of the setup, confirming which assets were
    created and whether key dependencies were found. It's useful for debugging
    and verifying that the setup completed successfully.

    Args:
        audio_summary: The dictionary of found audio files from `scan_audio_outputs`.
        ffmpeg_ok: A boolean indicating if FFmpeg was found and is operational.
        font_status: The exit code from the font download pipeline.
    """
    print("🧾 Writing config.json...")
    config = {
        "audio_assets": audio_summary,
        "status": "Setup complete",
        "verified_folders": EXPECTED_DIRS,
        "ffmpeg_ok": ffmpeg_ok,
        "font_downloader_exit_code": font_status,
    }
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)
    print("✅ config.json created.")


def main():
    """
    The main function that runs the entire setup orchestration.

    This function calls all the necessary setup steps in the correct order,
    from creating directories to installing dependencies and building assets.
    """
    print("🌸 Dharma Scroll Setup Initiated 🌸")
    ensure_structure()
    install_dependencies()
    ffmpeg_ok = check_ffmpeg()
    font_status = run_fonts_pipeline()
    run_audio_pipeline()
    audio_summary = scan_audio_outputs()
    write_config(audio_summary, ffmpeg_ok, font_status)
    print("🕉️ Setup complete. Your scroll is ready to unfold.")


if __name__ == "__main__":
    main()
