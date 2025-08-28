import sys
import shutil
import subprocess
import json
from pathlib import Path

# Consolidated builders
import importlib

# Expected folders
EXPECTED_DIRS = [
    "assets/audio/raw",
    "assets/audio/fadein",
    "assets/audio/ambient",
    "assets/audio/composite",
    "assets/audio/forest/celestial_audience",
    "assets/audio/forest/forest_of_austerity",
    "assets/audio/forest/shiva_and_the_hunter",
    "assets/audio/forest/trial_of_heaven",
    "assets/fonts",
    "assets/textures",
    "assets/svg",
]

CONFIG_PATH = Path("config.json")

def ensure_structure():
    print("📁 Ensuring folder structure...")
    for folder in EXPECTED_DIRS:
        Path(folder).mkdir(parents=True, exist_ok=True)
    print("✅ Folder structure verified.")

def install_dependencies():
    print("📦 Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    print("✅ Dependencies installed.")

def check_ffmpeg() -> bool:
    print("🔎 Checking ffmpeg availability...")
    exe = shutil.which("ffmpeg")
    if exe:
        try:
            subprocess.run([exe, "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            print(f"✅ ffmpeg found: {exe}")
            return True
        except Exception:
            pass
    print("⚠️ ffmpeg not found or not working. Pydub requires ffmpeg to process audio.")
    print("   Install from https://ffmpeg.org/ and ensure it's on your PATH, then rerun setup if audio fails.")
    return False

def run_fonts_pipeline() -> int:
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
    print("🎼 Running consolidated audio pipeline...")
    try:
        ab = importlib.import_module("audio_builder")
    except Exception as e:
        print(f"❌ Failed to import audio_builder: {e}")
        return
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
    print("✅ Audio assets generation attempted.")

def scan_audio_outputs() -> dict:
    base = Path("assets/audio")
    out = {
        "fadein": [],
        "ambient": [],
        "composite": [],
        "forest": {},
    }
    for p in (base / "fadein").glob("*_fadein.mp3"):
        out["fadein"].append(str(p))
    for p in (base / "ambient").glob("*_ambient_loop.mp3"):
        out["ambient"].append(str(p))
    for p in (base / "composite").glob("*_composite.mp3"):
        out["composite"].append(str(p))
    forest_dir = base / "forest"
    if forest_dir.exists():
        for story_dir in forest_dir.iterdir():
            if story_dir.is_dir():
                files = [str(p) for p in story_dir.glob("*.mp3")]
                if files:
                    out["forest"][story_dir.name] = files
    return out

def write_config(audio_summary, moved_assets, ffmpeg_ok: bool, font_status: int):
    print("🧾 Writing config.json...")
    config = {
    "audio_assets": audio_summary,
        "relocated_assets": moved_assets,
        "status": "Setup complete",
    "verified_folders": EXPECTED_DIRS,
    "ffmpeg_ok": ffmpeg_ok,
    "font_downloader_exit_code": font_status,
    }
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)
    print("✅ config.json created.")

def main():
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