import os
from pathlib import Path
import yt_dlp
from pydub import AudioSegment
from pydub.effects import normalize

# Directory setup
BASE_DIR = Path("assets/audio")
RAW_DIR = BASE_DIR / "raw"
FADEIN_DIR = BASE_DIR / "fadein"
AMBIENT_DIR = BASE_DIR / "ambient"

# Directory creation is handled by setup.py's ensure_structure()

# Hardcoded chant sources
CHANTS = {
    "lotus_of_doubt": {
        "youtube_url": "https://www.youtube.com/watch?v=g27HV8NvRSg",
        "title": "Lotus of Doubt – Shanti Mantra"
    },
    "chakra_of_dharma": {
        "youtube_url": "https://www.youtube.com/watch?v=UaI3G5eaE28",
        "title": "Chakra of Dharma – Karmanye Vadhikaraste"
    },
    "spiral_of_vision": {
        "youtube_url": "https://www.youtube.com/watch?v=UySFFSDKsg0",
        "title": "Spiral of Vision – Om Tat Sat"
    },
    "sword_of_resolve": {
        "youtube_url": "https://www.youtube.com/watch?v=hiBxKwtn08Q",
        "title": "Sword of Resolve – Ya Devi Sarva Bhuteshu"
    }
}

def download_audio(youtube_url: str, name: str):
    """Download audio from YouTube and save as MP3, if it doesn't exist."""
    output_path = RAW_DIR / f"{name}.mp3"
    
    if output_path.exists():
        print(f"✅ Audio '{name}.mp3' already exists. Skipping download.")
        return output_path

    print(f"🔽 Downloading '{name}.mp3'...")
    # yt-dlp adds the extension, so we provide the path without it.
    output_template = RAW_DIR / name
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': str(output_template),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        print(f"✅ Download complete: {output_path}")
        return output_path
    except Exception as e:
        print(f"❌ Error downloading {name} from {youtube_url}: {e}")
        return None

def create_fadein_version(input_path: Path, name: str, duration_ms=5000):
    """Create fade-in version of chant"""
    if not input_path:
        return None
    audio = AudioSegment.from_mp3(input_path)
    faded = normalize(audio.fade_in(duration_ms))
    output_path = FADEIN_DIR / f"{name}_fadein.mp3"
    faded.export(output_path, format="mp3")
    return output_path

def create_ambient_loop(input_path: Path, name: str, loop_duration_ms=60000):
    """Create ambient loop from chant"""
    if not input_path:
        return None
    audio = AudioSegment.from_mp3(input_path)
    loop = normalize(audio.low_pass_filter(400).fade_in(3000).fade_out(3000))
    loop = loop[:loop_duration_ms] * 2  # Repeat to extend
    output_path = AMBIENT_DIR / f"{name}_ambient_loop.mp3"
    loop.export(output_path, format="mp3")
    return output_path

def process_all_chants():
    """Run full pipeline for all hardcoded chants"""
    results = {}
    for key, chant in CHANTS.items():
        print(f"🎧 Processing: {chant['title']}")
        raw_path = download_audio(chant["youtube_url"], key)
        
        if not raw_path:
            print(f"⚠️ Skipping audio processing for '{key}' due to download failure.")
            continue

        fadein_path = create_fadein_version(raw_path, key)
        ambient_path = create_ambient_loop(raw_path, key)
        
        results[key] = {
            "fadein": str(fadein_path) if fadein_path else "N/A",
            "ambient": str(ambient_path) if ambient_path else "N/A"
        }
    return results
