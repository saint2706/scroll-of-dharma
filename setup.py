import os
import shutil
import subprocess
import json
from pathlib import Path
from audio_utils import process_all_chants

# Expected folders
EXPECTED_DIRS = [
    "assets/audio/raw",
    "assets/audio/fadein",
    "assets/audio/ambient",
    "assets/fonts",
    "assets/textures",
    "assets/svg"
]

# Misplaced assets to relocate
MISPLACED_ASSETS = {
    "UncialAntiqua.ttf": "assets/fonts",
    "parchment_bg.png": "assets/textures",
    "lotus.svg": "assets/svg"
}

CONFIG_PATH = Path("config.json")

def ensure_structure():
    print("📁 Ensuring folder structure...")
    for folder in EXPECTED_DIRS:
        Path(folder).mkdir(parents=True, exist_ok=True)
    print("✅ Folder structure verified.")

def relocate_assets():
    print("📦 Checking for misplaced assets...")
    root = Path(".")
    moved = []
    for filename, target_dir in MISPLACED_ASSETS.items():
        for path in root.rglob(filename):
            if target_dir not in str(path.parent):
                dest = Path(target_dir) / filename
                shutil.move(str(path), str(dest))
                moved.append({"file": filename, "from": str(path), "to": str(dest)})
                print(f"🔄 Moved {filename} to {target_dir}")
    print("✅ Assets relocated.")
    return moved

def install_dependencies():
    print("📦 Installing dependencies...")
    subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
    print("✅ Dependencies installed.")

def run_audio_pipeline():
    print("🎼 Running audio processing pipeline...")
    results = process_all_chants()
    for name, paths in results.items():
        print(f"🎶 {name}:")
        print(f"   Fade-in: {paths['fadein']}")
        print(f"   Ambient: {paths['ambient']}")
    print("✅ Audio assets generated.")
    return results

def write_config(audio_results, moved_assets):
    print("🧾 Writing config.json...")
    config = {
        "audio_assets": audio_results,
        "relocated_assets": moved_assets,
        "status": "Setup complete",
        "verified_folders": EXPECTED_DIRS
    }
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)
    print("✅ config.json created.")

def main():
    print("🌸 Dharma Scroll Setup Initiated 🌸")
    ensure_structure()
    moved_assets = relocate_assets()
    install_dependencies()
    audio_results = run_audio_pipeline()
    write_config(audio_results, moved_assets)
    print("🕉️ Setup complete. Your scroll is ready to unfold.")

if __name__ == "__main__":
    main()