import os
import requests
import yt_dlp
from pydub import AudioSegment
from pydub.effects import normalize, compress_dynamic_range

# --- CONFIGS ---
# From audio_utils.py
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

# From audio_maker_trilogy.py
trilogy_sources = {
    "game_of_fate": {
        "tracks": {
            "base_drone": "https://www.youtube.com/watch?v=47ED-zK3t7U",
            "dice_fx": "https://www.youtube.com/watch?v=WFon1xbVGN8",
            "whispers": "https://www.youtube.com/watch?v=yI85C7V88Sc",
            "climax_bells": "https://www.youtube.com/watch?v=CvCD8ZEoIes",
            "ambient_loop": "https://www.youtube.com/watch?v=5rC0AYRDF3M"
        }
    },
    "silence_of_protest": {
        "tracks": {
            "base_drone": "https://www.youtube.com/watch?v=47ED-zK3t7U",
            "whispers": "https://www.youtube.com/watch?v=yI85C7V88Sc",
            "bhishma_vow": "https://www.youtube.com/watch?v=2zFSZge17lo",
            "bell_toll": "https://www.youtube.com/watch?v=CvCD8ZEoIes",
            "ambient_loop": "https://www.youtube.com/watch?v=5rC0AYRDF3M"
        }
    },
    "divine_intervention": {
        "tracks": {
            "base_drone": "https://www.youtube.com/watch?v=47ED-zK3t7U",
            "govinda_whisper": "https://www.youtube.com/watch?v=6qrI2l1K1ks",
            "flute_soft": "https://www.youtube.com/watch?v=tF4z5kntXAA",
            "temple_bells": "https://www.youtube.com/watch?v=CvCD8ZEoIes",
            "ambient_loop": "https://www.youtube.com/watch?v=5rC0AYRDF3M"
        }
    }
}

# From audio_maker_forest_story.py
CHAPTERS = {
    "forest_of_austerity": {
        "ambient_url": "https://cdn.pixabay.com/download/audio/2021/10/07/audio_52143d4cea.mp3?filename=relax-in-the-forest-background-music-for-video-9145.mp3",
        "instrument_url": "https://cdn.pixabay.com/download/audio/2025/06/28/audio_01460b9e9e.mp3?filename=drone-of-the-divine-tanpura-367354.mp3",
        "chant_yt": "https://www.youtube.com/watch?v=Jy5o66NXgVs"
    },
    "shiva_and_the_hunter": {
        "ambient_url": "https://cdn.pixabay.com/download/audio/2024/07/10/audio_97b54301f0.mp3?filename=mortal-combat-in-japan-223567.mp3",
        "instrument_url": "https://cdn.pixabay.com/download/audio/2025/01/24/audio_1cda33d74c.mp3?filename=tabla-110-292145.mp3",
        "chant_yt": "https://www.youtube.com/watch?v=cIBHw7lVeY8",
        "flute_yt": "https://www.youtube.com/watch?v=EsbTBaPA_7w"
    },
    "celestial_audience": {
        "ambient_url": "https://cdn.pixabay.com/download/audio/2025/06/24/audio_179d267020.mp3?filename=wind-from-the-mountain-raga-pahad-364841.mp3",
        "instrument_url": "https://cdn.pixabay.com/download/audio/2024/12/19/audio_bad4789377.mp3?filename=indian-music-loop-sitar-story-275666.mp3",
        "chant_yt": "https://www.youtube.com/watch?v=TyHTJyWcVH4",
        "harp_yt": "https://www.youtube.com/watch?v=kZIEQUdSqLQ"
    },
    "trial_of_heaven": {
        "ambient_url": "https://cdn.pixabay.com/download/audio/2025/06/24/audio_b2612d0f66.mp3?filename=cosmic-serenity-celestial-soundscapes-365183.mp3",
        "instrument_url": "https://cdn.pixabay.com/download/audio/2025/01/26/audio_3f5c09b7be.mp3?filename=relaxing-krishna-flute-music-deep-sleep-relaxing-music-292793.mp3",
        "chant_yt": "https://www.youtube.com/watch?v=6IKwiV4dioQ",
        "tanpura_yt": "https://www.youtube.com/watch?v=8Osnnmp09SA"
    }
}

# --- Downloaders ---
def _ensure_dirs_for(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def condense_to_key_moments(audio: AudioSegment,
                            target_ms: int = 10 * 60 * 1000,
                            window_ms: int = 2000,
                            segment_ms: int = 60000,
                            min_gap_ms: int = 30000,
                            crossfade_ms: int = 800) -> AudioSegment:
    """If audio > target_ms, select high-energy moments and splice to <= target_ms.
    Heuristic: pick non-overlapping windows with highest RMS and assemble.
    """
    try:
        total = len(audio)
        if total <= target_ms:
            return audio

        # Compute RMS over sliding windows
        rms_list = []  # (start_ms, rms)
        for start in range(0, total, window_ms):
            chunk = audio[start:start + window_ms]
            if len(chunk) == 0:
                continue
            rms_list.append((start, chunk.rms))

        # Sort by RMS descending and select with non-max suppression by time distance
        rms_list.sort(key=lambda x: x[1], reverse=True)
        selected_centers = []
        for start, _ in rms_list:
            if all(abs(start - c) >= min_gap_ms for c in selected_centers):
                selected_centers.append(start)
            if len(selected_centers) >= max(1, target_ms // segment_ms + 2):
                break

        # Build segments around centers
        segments = []
        half = segment_ms // 2
        for c in selected_centers:
            s = max(0, c - half)
            e = min(total, s + segment_ms)
            # Adjust start if near end
            s = max(0, e - segment_ms)
            seg = audio[s:e]
            if len(seg) > 0:
                segments.append((s, seg))

        # Order by time and concatenate with crossfades until target duration reached
        segments.sort(key=lambda x: x[0])
        if not segments:
            return audio[:target_ms]

        composite = segments[0][1]
        for _, seg in segments[1:]:
            if len(composite) >= target_ms:
                break
            remaining = target_ms - len(composite)
            seg = seg[:max(0, remaining)]
            composite = composite.append(seg, crossfade=crossfade_ms)

        if len(composite) > target_ms:
            composite = composite[:target_ms]

        # Smooth edges
        edge = min(1000, len(composite) // 10)
        return composite.fade_in(edge).fade_out(edge)
    except Exception:
        # Fallback to simple trim on any error
        return audio[:target_ms]

def download_youtube_audio(url, dest):
    print(f"→ Downloading YouTube audio: {url}")
    # Normalize destination: yt-dlp adds .mp3
    if dest.endswith('.mp3'):
        base = dest[:-4]
    else:
        base = dest
    mp3_path = base + '.mp3'
    _ensure_dirs_for(mp3_path)
    if os.path.exists(mp3_path):
        print(f"✅ File already exists: {mp3_path}. Skipping download.")
        return True

    # Optional cookies support
    cookie_candidates = [
        os.path.join(os.getcwd(), 'cookies.txt'),
        os.path.join(os.getcwd(), 'assets', 'cookies.txt')
    ]
    cookiefile = next((p for p in cookie_candidates if os.path.exists(p)), None)

    def try_download(opts):
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
            return os.path.exists(mp3_path)
        except Exception as e:
            print(f"  ↪︎ attempt failed: {e}")
            return False

    common_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'outtmpl': base,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'geo_bypass': True,
        'noplaylist': True,
        'concurrent_fragment_downloads': 1,
        'retries': 3,
        'fragment_retries': 3,
        'skip_unavailable_fragments': True,
        'extractor_args': {
            'youtube': {
                # Avoid TV client (DRM experiments). We'll try web/mweb/android/ios order.
            }
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
        },
        'youtube_include_dash_manifest': False,
    }
    if cookiefile:
        common_opts['cookiefile'] = cookiefile

    # Fallback chain of player clients
    clients = ['web', 'mweb', 'android', 'ios']
    for client in clients:
        opts = dict(common_opts)
        opts['extractor_args'] = {'youtube': {'player_client': [client]}}
        print(f"  • trying client: {client}")
        if try_download(opts):
            break

    if not os.path.exists(mp3_path):
        print(f"❌ Error downloading {url}: yt-dlp did not create output file.")
        print("⚠️ Tips: update yt-dlp, provide cookies.txt (logged-in browser export), or download manually to:")
        print(f"   {mp3_path}")
        return False
    return True

def download_direct_mp3(url, dest):
    print(f"→ Downloading direct MP3: {url}")
    if os.path.exists(dest):
        print(f"✅ File already exists: {dest}. Skipping download.")
        return True
    r = requests.get(url)
    with open(dest, "wb") as f:
        f.write(r.content)
    return True

# --- Audio Mixing ---
def mix_audio(layers, output_path, fade_in=3000, fade_out=4000):
    print(f"→ Mixing audio layers into: {output_path}")
    base_duration = min(len(layer) for layer in layers)
    layers = [layer[:base_duration] for layer in layers]
    mix = layers[0]
    for layer in layers[1:]:
        mix = mix.overlay(layer)
    mix = mix.fade_in(fade_in).fade_out(fade_out)
    # Final polish: mild compression and peak normalization to -1 dBFS
    try:
        mix = compress_dynamic_range(mix, threshold=-6.0, ratio=3.0, attack=5, release=50)
    except Exception:
        pass
    mix = normalize(mix).apply_gain(-1.0)
    mix.export(output_path, format="mp3")

# --- Loudness helpers ---
def set_target_dbfs(audio: AudioSegment, target_dbfs: float, soft_clip: bool = True) -> AudioSegment:
    """Adjust audio to target dBFS with optional soft compression to prevent clipping."""
    try:
        if audio.dBFS == float('-inf'):
            return audio
        gain = target_dbfs - audio.dBFS
        out = audio.apply_gain(gain)
        if soft_clip:
            try:
                out = compress_dynamic_range(out, threshold=-3.0, ratio=4.0, attack=5, release=80)
            except Exception:
                return out
        return out
    except Exception:
        return audio

def trilogy_target_dbfs(track_name: str) -> float:
    # Background ambience very low, SFX mid, voice/music elements moderate
    if track_name in ("ambient_loop", "base_drone"):
        return -24.0
    if track_name in ("dice_fx", "whispers"):
        return -20.0
    if track_name in ("climax_bells", "bell_toll", "flute_soft", "temple_bells", "govinda_whisper"):
        return -19.0
    return -21.0

# --- Story Audio Builders ---
def build_chant_and_ambient():
    """Process all hardcoded chants from CHANTS."""
    for key, chant in CHANTS.items():
        print(f"🎧 Processing: {chant['title']}")
        raw_path = f"assets/audio/raw/{key}.mp3"
        success = download_youtube_audio(chant["youtube_url"], raw_path)
        if not success or not os.path.exists(raw_path):
            print(f"⚠️ Skipping {key}: raw chant not available. Please download manually if needed.")
            continue
        # Fadein
    audio = AudioSegment.from_mp3(raw_path)
    # Condense if longer than 10 minutes
    audio = condense_to_key_moments(audio)
    faded = normalize(audio.fade_in(5000))
    fadeout_path = f"assets/audio/fadein/{key}_fadein.mp3"
    _ensure_dirs_for(fadeout_path)
    faded.export(fadeout_path, format="mp3")
    # Ambient
    loop = normalize(audio.low_pass_filter(400).fade_in(3000).fade_out(3000))
    loop = loop[:60000] * 2
    ambient_out = f"assets/audio/ambient/{key}_ambient_loop.mp3"
    _ensure_dirs_for(ambient_out)
    loop.export(ambient_out, format="mp3")

# Trilogy builder

def build_trilogy():
    def loop_to_duration(seg: AudioSegment, duration_ms: int) -> AudioSegment:
        if len(seg) == 0:
            return AudioSegment.silent(duration=duration_ms)
        out = AudioSegment.silent(duration=0)
        while len(out) < duration_ms:
            out += seg
        return out[:duration_ms]

    for chap_key, chap_data in trilogy_sources.items():
        title = chap_key
        tracks = chap_data["tracks"]
        print(f"\n🎬 Building audio for {title}...")

        processed = {}
        for name, url in tracks.items():
            path = f"assets/audio/raw/{name}.mp3"
            _ensure_dirs_for(path)
            success = download_youtube_audio(url, path)
            if not success or not os.path.exists(path):
                print(f"⚠️ Skipping {name}: audio not available. Please download manually if needed.")
                continue
            seg = AudioSegment.from_mp3(path)
            seg = condense_to_key_moments(seg)
            seg = set_target_dbfs(seg, trilogy_target_dbfs(name))
            processed[name] = seg

        # Build base bed
        bed_duration = 60_000  # 60 seconds composite
        composite = AudioSegment.silent(duration=bed_duration)
        if "ambient_loop" in processed:
            composite = composite.overlay(loop_to_duration(processed["ambient_loop"], bed_duration).apply_gain(-1.0))
        if "base_drone" in processed:
            composite = composite.overlay(loop_to_duration(processed["base_drone"], bed_duration))

        # Overlay SFX/music during the bed, staggered
        sfx_names = [n for n in processed.keys() if n not in ("ambient_loop", "base_drone")]
        n = len(sfx_names)
        if n > 0:
            step = bed_duration // (n + 1)
            for i, name in enumerate(sfx_names, start=1):
                seg = processed[name]
                pos = max(0, min(bed_duration - min(len(seg), 5000), i * step))
                composite = composite.overlay(seg.fade_in(300).fade_out(700), position=pos)

        # Final polish and export
        composite = normalize(composite).fade_in(1500).fade_out(2000)
        output_path = f"assets/audio/composite/{title}_composite.mp3"
        os.makedirs("assets/audio/composite", exist_ok=True)
        composite.export(output_path, format="mp3")
        print(f"🎧 Exported: {output_path}")

# Forest story builder

def build_forest_stories():
    for chapter, config in CHAPTERS.items():
        print(f"\n=== Processing: {chapter} ===")
        chapter_dir = f"assets/audio/forest/{chapter}"
        os.makedirs(chapter_dir, exist_ok=True)
        # Download ambient and instrument
        ambient_path = os.path.join(chapter_dir, "ambient.mp3")
        instrument_path = os.path.join(chapter_dir, "instrument.mp3")
        download_direct_mp3(config["ambient_url"], ambient_path)
        download_direct_mp3(config["instrument_url"], instrument_path)
        # Load base layers
        ambient = set_target_dbfs(condense_to_key_moments(AudioSegment.from_mp3(ambient_path)), -24.0)
        instrument = set_target_dbfs(condense_to_key_moments(AudioSegment.from_mp3(instrument_path)), -21.0)
        # Download and load chant
        chant_path = os.path.join(chapter_dir, "chant.mp3")
        success = download_youtube_audio(config["chant_yt"], chant_path)
        if not success or not os.path.exists(chant_path):
            print(f"⚠️ Skipping {chapter}: chant not available. Please download manually if needed.")
            continue
        chant = set_target_dbfs(condense_to_key_moments(AudioSegment.from_mp3(chant_path)), -18.0)
        # Optional layers
        extra_layers = []
        for key in ["flute_yt", "harp_yt", "tanpura_yt"]:
            if key in config:
                extra_path = os.path.join(chapter_dir, f"{key}.mp3")
                success = download_youtube_audio(config[key], extra_path)
                if not success or not os.path.exists(extra_path):
                    print(f"⚠️ Skipping {key} for {chapter}: extra layer not available. Please download manually if needed.")
                    continue
                extra_layers.append(set_target_dbfs(condense_to_key_moments(AudioSegment.from_mp3(extra_path)), -19.0))
        # Mix all layers
        all_layers = [ambient, instrument, chant] + extra_layers
        output_path = os.path.join(chapter_dir, f"{chapter}_mix.mp3")
        mix_audio(all_layers, output_path)

if __name__ == "__main__":
    build_chant_and_ambient()
    build_trilogy()
    build_forest_stories()
