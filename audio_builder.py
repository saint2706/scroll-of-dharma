"""
Audio processing pipeline for the Scroll of Dharma application.

This script is responsible for creating all the audio assets required by the
main application. It is designed to be run from the command line via `setup.py`.

The pipeline performs the following steps for each audio soundscape:
1.  **Downloads** source audio files from YouTube and Pixabay using URLs
    defined in the configuration dictionaries. It uses `yt-dlp` for robust
    YouTube downloading and `requests` for direct MP3s.
2.  **Processes** the raw audio. This includes:
    - Condensing long audio tracks into shorter, more impactful segments by
      selecting high-energy moments (`condense_to_key_moments`).
    - Normalizing loudness levels to create a balanced mix (`set_target_dbfs`).
3.  **Mixes** multiple audio layers together to create the final soundscapes.
    This involves overlaying tracks, adding fades, and applying light
    compression for a polished result.
4.  **Exports** the final audio files to the appropriate subdirectories within
    `assets/audio/`, ready to be used by `app.py`.

The script is idempotent; it checks for the existence of final output files
and skips processing if the asset has already been built, saving time on
subsequent runs.
"""
import os
import requests
import yt_dlp
from pydub import AudioSegment
from pydub.effects import normalize, compress_dynamic_range

# --- CONFIGURATIONS: Audio Sources ---

# Defines the audio sources for the "Gita Scroll" chapter.
# Each key corresponds to a story, and the value contains the YouTube URL.
CHANTS = {
    "lotus_of_doubt": {
        "youtube_url": "https://www.youtube.com/watch?v=g27HV8NvRSg",
        "title": "Lotus of Doubt – Shanti Mantra",
    },
    "chakra_of_dharma": {
        "youtube_url": "https://www.youtube.com/watch?v=UaI3G5eaE28",
        "title": "Chakra of Dharma – Karmanye Vadhikaraste",
    },
    "spiral_of_vision": {
        "youtube_url": "https://www.youtube.com/watch?v=UySFFSDKsg0",
        "title": "Spiral of Vision – Om Tat Sat",
    },
    "sword_of_resolve": {
        "youtube_url": "https://www.youtube.com/watch?v=hiBxKwtn08Q",
        "title": "Sword of Resolve – Ya Devi Sarva Bhuteshu",
    },
}

# Defines the audio sources for the "Fall of Dharma" chapter stories.
# Each story is a composite mix of several YouTube tracks.
trilogy_sources = {
    "game_of_fate": {
        "tracks": {
            "base_drone": "https://www.youtube.com/watch?v=47ED-zK3t7U",
            "dice_fx": "https://www.youtube.com/watch?v=WFon1xbVGN8",
            "whispers": "https://www.youtube.com/watch?v=yI85C7V88Sc",
            "climax_bells": "https://www.youtube.com/watch?v=CvCD8ZEoIes",
            "ambient_loop": "https://www.youtube.com/watch?v=5rC0AYRDF3M",
        }
    },
    "silence_of_protest": {
        "tracks": {
            "base_drone": "https://www.youtube.com/watch?v=47ED-zK3t7U",
            "whispers": "https://www.youtube.com/watch?v=yI85C7V88Sc",
            "bhishma_vow": "https://www.youtube.com/watch?v=2zFSZge17lo",
            "bell_toll": "https://www.youtube.com/watch?v=CvCD8ZEoIes",
            "ambient_loop": "https://www.youtube.com/watch?v=5rC0AYRDF3M",
        }
    },
    "divine_intervention": {
        "tracks": {
            "base_drone": "https://www.youtube.com/watch?v=47ED-zK3t7U",
            "govinda_whisper": "https://www.youtube.com/watch?v=6qrI2l1K1ks",
            "flute_soft": "https://www.youtube.com/watch?v=tF4z5kntXAA",
            "temple_bells": "https://www.youtube.com/watch?v=CvCD8ZEoIes",
            "ambient_loop": "https://www.youtube.com/watch?v=5rC0AYRDF3M",
        }
    },
}

# Defines audio sources for the "Weapon Quest" chapter stories.
# Mixes direct downloads from Pixabay with YouTube sources.
CHAPTERS = {
    "forest_of_austerity": {
        "ambient_url": "https://cdn.pixabay.com/download/audio/2021/10/07/audio_52143d4cea.mp3?filename=relax-in-the-forest-background-music-for-video-9145.mp3",
        "instrument_url": "https://cdn.pixabay.com/download/audio/2025/06/28/audio_01460b9e9e.mp3?filename=drone-of-the-divine-tanpura-367354.mp3",
        "chant_yt": "https://www.youtube.com/watch?v=Jy5o66NXgVs",
    },
    "shiva_and_the_hunter": {
        "ambient_url": "https://cdn.pixabay.com/download/audio/2024/07/10/audio_97b54301f0.mp3?filename=mortal-combat-in-japan-223567.mp3",
        "instrument_url": "https://cdn.pixabay.com/download/audio/2025/01/24/audio_1cda33d74c.mp3?filename=tabla-110-292145.mp3",
        "chant_yt": "https://www.youtube.com/watch?v=cIBHw7lVeY8",
        "flute_yt": "https://www.youtube.com/watch?v=EsbTBaPA_7w",
    },
    "celestial_audience": {
        "ambient_url": "https://cdn.pixabay.com/download/audio/2025/06/24/audio_179d267020.mp3?filename=wind-from-the-mountain-raga-pahad-364841.mp3",
        "instrument_url": "https://cdn.pixabay.com/download/audio/2024/12/19/audio_bad4789377.mp3?filename=indian-music-loop-sitar-story-275666.mp3",
        "chant_yt": "https://www.youtube.com/watch?v=TyHTJyWcVH4",
        "harp_yt": "https://www.youtube.com/watch?v=kZIEQUdSqLQ",
    },
    "trial_of_heaven": {
        "ambient_url": "https://cdn.pixabay.com/download/audio/2025/06/24/audio_b2612d0f66.mp3?filename=cosmic-serenity-celestial-soundscapes-365183.mp3",
        "instrument_url": "https://cdn.pixabay.com/download/audio/2025/01/26/audio_3f5c09b7be.mp3?filename=relaxing-krishna-flute-music-deep-sleep-relaxing-music-292793.mp3",
        "chant_yt": "https://www.youtube.com/watch?v=6IKwiV4dioQ",
        "tanpura_yt": "https://www.youtube.com/watch?v=8Osnnmp09SA",
    },
}

# Defines audio sources for the "Birth of Dharma" chapter stories.
# Each story is a mix of several layers from Pixabay and YouTube.
BIRTH_CHAPTERS = {
    "cosmic_breath": [
        {
            "type": "pixabay",
            "url": "https://cdn.pixabay.com/download/audio/2025/06/04/audio_ac1eb8617c.mp3?filename=meditation-ambient-music-354473.mp3",
        },
        {"type": "youtube", "url": "https://www.youtube.com/watch?v=Kf2aNUEW1kM"},
        {"type": "youtube", "url": "https://www.youtube.com/watch?v=JVuFPVlTaJw"},
    ],
    "golden_parchment": [
        {
            "type": "pixabay",
            "url": "https://cdn.pixabay.com/download/audio/2025/06/28/audio_8a3d48bb58.mp3?filename=mystic-voice-ethereal-vocal-soundscape-with-ambient-layers-367428.mp3",
        },
        {"type": "youtube", "url": "https://www.youtube.com/watch?v=NNSzEnm_IxY"},
        {"type": "youtube", "url": "https://www.youtube.com/watch?v=cTXPLlfAvpE"},
    ],
    "flowing_wisdom": [
        {
            "type": "pixabay",
            "url": "https://cdn.pixabay.com/download/audio/2025/05/29/audio_5a0c0f1a13.mp3?filename=pure-theta-4-7hz-gentle-water-flow-351397.mp3",
        },
        {"type": "youtube", "url": "https://www.youtube.com/watch?v=Qo6eO50oxHc"},
        {"type": "youtube", "url": "https://www.youtube.com/watch?v=_gJzooUKm2E"},
    ],
    "glyphs_of_dharma": [
        {
            "type": "pixabay",
            "url": "https://cdn.pixabay.com/download/audio/2025/06/04/audio_d821f3c614.mp3?filename=ritual-in-the-jungle-tribal-world-cinematic-no-pads-354226.mp3",
        },
        {"type": "youtube", "url": "https://www.youtube.com/watch?v=0n8ui6df2CU"},
        {"type": "youtube", "url": "https://www.youtube.com/watch?v=ABy95341Dto"},
    ],
    "awakening_scroll": [
        {
            "type": "pixabay",
            "url": "https://cdn.pixabay.com/download/audio/2025/06/04/audio_ac1eb8617c.mp3?filename=meditation-ambient-music-354473.mp3",
        },
        {"type": "youtube", "url": "https://www.youtube.com/watch?v=yr9jvP8mf9k"},
        {"type": "youtube", "url": "https://www.youtube.com/watch?v=cTXPLlfAvpE"},
    ],
}


# --- File and Directory Utilities ---
def _exists(path: str) -> bool:
    """
    Checks if a file exists and has a non-zero size.

    Args:
        path: The path to the file.

    Returns:
        True if the file exists and is not empty, False otherwise.
    """
    try:
        return os.path.exists(path) and os.path.getsize(path) > 0
    except OSError:
        return os.path.exists(path)


def _ensure_dirs_for(path: str):
    """
    Ensures that the directory for a given file path exists.

    Args:
        path: The file path for which to create the parent directory.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)


# --- Audio Processing and Downloading ---
def condense_to_key_moments(
    audio: AudioSegment,
    target_ms: int = 10 * 60 * 1000,
    window_ms: int = 2000,
    segment_ms: int = 60000,
    min_gap_ms: int = 30000,
    crossfade_ms: int = 800,
) -> AudioSegment:
    """
    Condenses a long audio segment into a shorter one by selecting "key moments".

    This function is a heuristic to extract the most interesting parts of a long
    audio track (e.g., a 1-hour chant) to create a shorter, representative sample.
    It works by finding segments with the highest energy (RMS) and splicing them
    together with crossfades.

    Args:
        audio: The input Pydub AudioSegment.
        target_ms: The desired final length of the audio in milliseconds.
        window_ms: The size of the sliding window for RMS calculation.
        segment_ms: The length of each extracted audio chunk.
        min_gap_ms: The minimum time gap between selected high-energy moments.
        crossfade_ms: The duration of the crossfade between spliced segments.

    Returns:
        A new, condensed AudioSegment. If the original audio is already shorter
        than `target_ms`, it is returned unmodified.
    """
    try:
        total = len(audio)
        if total <= target_ms:
            return audio

        # Compute RMS over sliding windows to find high-energy parts
        rms_list = []  # (start_ms, rms)
        for start in range(0, total, window_ms):
            chunk = audio[start : start + window_ms]
            if len(chunk) == 0:
                continue
            rms_list.append((start, chunk.rms))

        # Sort by energy and select distinct moments
        rms_list.sort(key=lambda x: x[1], reverse=True)
        selected_centers = []
        for start, _ in rms_list:
            if all(abs(start - c) >= min_gap_ms for c in selected_centers):
                selected_centers.append(start)
            if len(selected_centers) >= max(1, target_ms // segment_ms + 2):
                break

        # Build audio segments around the selected center points
        segments = []
        half = segment_ms // 2
        for c in selected_centers:
            s = max(0, c - half)
            e = min(total, s + segment_ms)
            s = max(0, e - segment_ms)  # Adjust start if near end
            seg = audio[s:e]
            if len(seg) > 0:
                segments.append((s, seg))

        # Sort segments by their original timestamp and concatenate with crossfades
        segments.sort(key=lambda x: x[0])
        if not segments:
            return audio[:target_ms]

        composite = segments[0][1]
        for _, seg in segments[1:]:
            if len(composite) >= target_ms:
                break
            remaining = target_ms - len(composite)
            seg = seg[: max(0, remaining)]
            composite = composite.append(seg, crossfade=crossfade_ms)

        if len(composite) > target_ms:
            composite = composite[:target_ms]

        # Smooth edges with a fade-in and fade-out
        edge = min(1000, len(composite) // 10)
        return composite.fade_in(edge).fade_out(edge)
    except Exception:
        # Fallback to a simple trim on any processing error
        return audio[:target_ms]


def download_youtube_audio(url: str, dest: str) -> bool:
    """
    Downloads audio from a YouTube URL using yt-dlp.

    Handles existing files, optional cookies for restricted content, and a
    fallback chain of user agents to maximize success rate.

    Args:
        url: The YouTube URL to download from.
        dest: The destination path for the output MP3 file.

    Returns:
        True if the download was successful or the file already existed,
        False otherwise.
    """
    print(f"→ Downloading YouTube audio: {url}")
    # Normalize destination path since yt-dlp adds its own extension
    if dest.endswith(".mp3"):
        base = dest[:-4]
    else:
        base = dest
    mp3_path = base + ".mp3"
    _ensure_dirs_for(mp3_path)
    if os.path.exists(mp3_path):
        print(f"✅ File already exists: {mp3_path}. Skipping download.")
        return True

    # Check for an optional cookies.txt file to help with age-restricted content
    cookie_candidates = [
        os.path.join(os.getcwd(), "cookies.txt"),
        os.path.join(os.getcwd(), "assets", "cookies.txt"),
    ]
    cookiefile = next((p for p in cookie_candidates if os.path.exists(p)), None)

    def try_download(opts: dict) -> bool:
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
            return os.path.exists(mp3_path)
        except Exception as e:
            print(f"  ↪︎ attempt failed: {e}")
            return False

    common_opts = {
        "format": "bestaudio[ext=m4a]/bestaudio/best",
        "outtmpl": base,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
        "geo_bypass": True,
        "noplaylist": True,
        "concurrent_fragment_downloads": 1,
        "retries": 3,
        "fragment_retries": 3,
        "skip_unavailable_fragments": True,
        "extractor_args": {"youtube": {}},
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
        },
        "youtube_include_dash_manifest": False,
    }
    if cookiefile:
        common_opts["cookiefile"] = cookiefile

    # Fallback chain of player clients to try different user agents
    clients = ["web", "mweb", "android", "ios"]
    for client in clients:
        opts = dict(common_opts)
        opts["extractor_args"] = {"youtube": {"player_client": [client]}}
        print(f"  • trying client: {client}")
        if try_download(opts):
            break

    if not os.path.exists(mp3_path):
        print(f"❌ Error downloading {url}: yt-dlp did not create output file.")
        print(
            "⚠️ Tips: update yt-dlp, provide cookies.txt (logged-in browser export), or download manually to:"
        )
        print(f"   {mp3_path}")
        return False
    return True


def download_direct_mp3(url: str, dest: str) -> bool:
    """
    Downloads an MP3 file from a direct URL.

    Args:
        url: The direct URL to the MP3 file.
        dest: The destination path to save the file.

    Returns:
        True on success or if the file already exists.
    """
    print(f"→ Downloading direct MP3: {url}")
    if os.path.exists(dest):
        print(f"✅ File already exists: {dest}. Skipping download.")
        return True
    r = requests.get(url)
    with open(dest, "wb") as f:
        f.write(r.content)
    return True


def mix_audio(layers: list, output_path: str, fade_in: int = 3000, fade_out: int = 4000):
    """
    Mixes multiple Pydub AudioSegments into a single file.

    The layers are overlaid, faded in and out, and then normalized and
    compressed for a balanced, polished sound. The final mix is truncated
    to the length of the shortest layer.

    Args:
        layers: A list of AudioSegment objects to mix.
        output_path: The path to save the final mixed MP3 file.
        fade_in: The fade-in duration in milliseconds.
        fade_out: The fade-out duration in milliseconds.
    """
    print(f"→ Mixing audio layers into: {output_path}")
    base_duration = min(len(layer) for layer in layers)
    layers = [layer[:base_duration] for layer in layers]
    mix = layers[0]
    for layer in layers[1:]:
        mix = mix.overlay(layer)
    mix = mix.fade_in(fade_in).fade_out(fade_out)
    # Final polish: mild compression and peak normalization to -1 dBFS
    try:
        mix = compress_dynamic_range(
            mix, threshold=-6.0, ratio=3.0, attack=5, release=50
        )
    except Exception:
        pass
    mix = normalize(mix).apply_gain(-1.0)
    mix.export(output_path, format="mp3")


def set_target_dbfs(
    audio: AudioSegment, target_dbfs: float, soft_clip: bool = True
) -> AudioSegment:
    """
    Adjusts the loudness of an audio segment to a target level.

    Normalizes the audio to a target dBFS (decibels relative to full scale).
    Optionally applies a soft compressor to prevent clipping if the gain
    adjustment is large.

    Args:
        audio: The input AudioSegment.
        target_dbfs: The target loudness in dBFS (e.g., -18.0).
        soft_clip: Whether to apply a light compressor to avoid clipping.

    Returns:
        The loudness-adjusted AudioSegment.
    """
    try:
        if audio.dBFS == float("-inf"):  # Avoid division by zero on silent audio
            return audio
        gain = target_dbfs - audio.dBFS
        out = audio.apply_gain(gain)
        if soft_clip:
            try:
                # Apply a light touch of compression to prevent harsh clipping
                out = compress_dynamic_range(
                    out, threshold=-3.0, ratio=4.0, attack=5, release=80
                )
            except Exception:
                return out  # Return gain-adjusted audio if compression fails
        return out
    except Exception:
        return audio  # Return original audio on any error


def trilogy_target_dbfs(track_name: str) -> float:
    """
    Provides a target loudness level for tracks in the "Fall of Dharma" chapter.

    This ensures a consistent mix, with background elements being quieter
    than foreground sound effects or musical motifs.

    Args:
        track_name: The name of the audio track (e.g., 'base_drone', 'dice_fx').

    Returns:
        The target dBFS value for that track.
    """
    # Background ambience very low, SFX mid, voice/music elements moderate
    if track_name in ("ambient_loop", "base_drone"):
        return -24.0
    if track_name in ("dice_fx", "whispers"):
        return -20.0
    if track_name in (
        "climax_bells",
        "bell_toll",
        "flute_soft",
        "temple_bells",
        "govinda_whisper",
    ):
        return -19.0
    return -21.0  # Default for other elements


# --- Chapter-Specific Audio Builders ---
def build_chant_and_ambient():
    """
    Builds the audio assets for the "Gita Scroll" chapter.

    For each story in this chapter, it downloads a source chant and creates two
    derivatives:
    1. A primary version with a long fade-in (`_fadein.mp3`).
    2. A quiet, looping ambient version (`_ambient_loop.mp3`).
    """
    for key, chant in CHANTS.items():
        print(f"🎧 Processing: {chant['title']}")
        fadeout_path = f"assets/audio/fadein/{key}_fadein.mp3"
        ambient_out = f"assets/audio/ambient/{key}_ambient_loop.mp3"
        if _exists(fadeout_path) and _exists(ambient_out):
            print(f"⏭️  Skipping {key}: outputs already exist.")
            continue

        raw_path = f"assets/audio/raw/{key}.mp3"
        success = download_youtube_audio(chant["youtube_url"], raw_path)
        if not success or not os.path.exists(raw_path):
            print(f"⚠️ Skipping {key}: raw chant not available.")
            continue

        audio = AudioSegment.from_mp3(raw_path)
        audio = condense_to_key_moments(audio)

        # Create the primary version with a fade-in
        if not _exists(fadeout_path):
            faded = normalize(audio.fade_in(5000))
            _ensure_dirs_for(fadeout_path)
            faded.export(fadeout_path, format="mp3")

        # Create the ambient loop version (low-pass filtered and quieter)
        if not _exists(ambient_out):
            loop = normalize(audio.low_pass_filter(400).fade_in(3000).fade_out(3000))
            loop = loop[:60000] * 2  # Ensure it's long enough and loop
            _ensure_dirs_for(ambient_out)
            loop.export(ambient_out, format="mp3")


def build_trilogy():
    """
    Builds the composite audio assets for the "Fall of Dharma" chapter.

    Each story in this chapter is a complex mix of multiple layers (drones,
    sound effects, whispers). This function downloads all sources, adjusts their
    loudness individually, and then overlays them at staggered intervals to
    create a 60-second composite soundscape.
    """
    def loop_to_duration(seg: AudioSegment, duration_ms: int) -> AudioSegment:
        """Helper to loop or truncate an audio segment to a specific duration."""
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

        output_path = f"assets/audio/composite/{title}_composite.mp3"
        if _exists(output_path):
            print(f"⏭️  Skipping {title}: composite already exists -> {output_path}")
            continue

        # Download and process each track layer individually
        processed = {}
        for name, url in tracks.items():
            path = f"assets/audio/raw/{name}.mp3"
            _ensure_dirs_for(path)
            success = download_youtube_audio(url, path)
            if not success or not os.path.exists(path):
                print(f"⚠️ Skipping {name}: audio not available.")
                continue
            seg = AudioSegment.from_mp3(path)
            seg = condense_to_key_moments(seg)
            seg = set_target_dbfs(seg, trilogy_target_dbfs(name))
            processed[name] = seg

        # Build the base audio bed (60 seconds) from ambient and drone layers
        bed_duration = 60_000
        composite = AudioSegment.silent(duration=bed_duration)
        if "ambient_loop" in processed:
            composite = composite.overlay(
                loop_to_duration(processed["ambient_loop"], bed_duration).apply_gain(-1.0)
            )
        if "base_drone" in processed:
            composite = composite.overlay(
                loop_to_duration(processed["base_drone"], bed_duration)
            )

        # Overlay the sound effects and musical elements at staggered positions
        sfx_names = [n for n in processed.keys() if n not in ("ambient_loop", "base_drone")]
        n = len(sfx_names)
        if n > 0:
            step = bed_duration // (n + 1)
            for i, name in enumerate(sfx_names, start=1):
                seg = processed[name]
                pos = max(0, min(bed_duration - min(len(seg), 5000), i * step))
                composite = composite.overlay(
                    seg.fade_in(300).fade_out(700), position=pos
                )

        # Final polish and export
        composite = normalize(composite).fade_in(1500).fade_out(2000)
        os.makedirs("assets/audio/composite", exist_ok=True)
        composite.export(output_path, format="mp3")
        print(f"🎧 Exported: {output_path}")


def build_forest_stories():
    """
    Builds the audio assets for the "Weapon Quest" chapter.

    Each story in this chapter consists of an ambient track, an instrumental
    track, a chant, and optional extra layers. This function downloads all
    sources, normalizes their loudness, and mixes them into a primary
    soundscape (`_mix.mp3`) and also saves the raw ambient track separately.
    """
    for chapter, config in CHAPTERS.items():
        print(f"\n=== Processing: {chapter} ===")
        chapter_dir = f"assets/audio/forest/{chapter}"
        os.makedirs(chapter_dir, exist_ok=True)
        output_path = os.path.join(chapter_dir, f"{chapter}_mix.mp3")
        if _exists(output_path):
            print(f"⏭️  Skipping {chapter}: forest mix already exists -> {output_path}")
            continue

        # Download and load base layers (ambient and instrument)
        ambient_path = os.path.join(chapter_dir, "ambient.mp3")
        instrument_path = os.path.join(chapter_dir, "instrument.mp3")
        download_direct_mp3(config["ambient_url"], ambient_path)
        download_direct_mp3(config["instrument_url"], instrument_path)

        ambient = set_target_dbfs(AudioSegment.from_mp3(ambient_path), -24.0)
        instrument = set_target_dbfs(AudioSegment.from_mp3(instrument_path), -21.0)

        # Download and load main chant
        chant_path = os.path.join(chapter_dir, "chant.mp3")
        if not download_youtube_audio(config["chant_yt"], chant_path):
            print(f"⚠️ Skipping {chapter}: main chant not available.")
            continue
        chant = set_target_dbfs(AudioSegment.from_mp3(chant_path), -18.0)

        # Download and load optional extra layers
        extra_layers = []
        for key in ["flute_yt", "harp_yt", "tanpura_yt"]:
            if key in config:
                extra_path = os.path.join(chapter_dir, f"{key}.mp3")
                if not download_youtube_audio(config[key], extra_path):
                    print(f"⚠️ Skipping optional layer {key} for {chapter}.")
                    continue
                extra_layers.append(
                    set_target_dbfs(AudioSegment.from_mp3(extra_path), -19.0)
                )

        # Mix all available layers
        all_layers = [ambient, instrument, chant] + extra_layers
        all_layers = [condense_to_key_moments(layer) for layer in all_layers]
        mix_audio(all_layers, output_path)


def build_birth_of_dharma():
    """
    Builds the audio assets for the "Birth of Dharma" chapter.

    Each story is created by mixing several source files (from Pixabay and
    YouTube). The first source is treated as a quieter background bed, while
    the others are more prominent foreground layers.
    """
    def safe_load(path: str) -> AudioSegment | None:
        """Safely load an MP3, returning None on failure."""
        try:
            return AudioSegment.from_mp3(path)
        except Exception:
            return None

    for story, sources in BIRTH_CHAPTERS.items():
        print(f"\n🌅 Building Birth of Dharma story: {story}")
        story_dir = os.path.join("assets", "audio", "birth", story)
        os.makedirs(story_dir, exist_ok=True)
        out_path = os.path.join(story_dir, f"{story}_mix.mp3")
        if _exists(out_path):
            print(f"⏭️  Skipping {story}: birth mix already exists -> {out_path}")
            continue

        # Download all source files for the story
        downloaded_paths = []
        for idx, src in enumerate(sources):
            t, url = src.get("type"), src.get("url")
            if not url: continue
            if t == "pixabay":
                dest = os.path.join(story_dir, f"pixabay_{idx}.mp3")
                if download_direct_mp3(url, dest): downloaded_paths.append(dest)
            elif t == "youtube":
                dest = os.path.join(story_dir, f"youtube_{idx}.mp3")
                if download_youtube_audio(url, dest): downloaded_paths.append(dest)

        if not downloaded_paths:
            print(f"⚠️ No audio layers available for {story}; skipping.")
            continue

        # Load and prepare layers; first is the bed (quieter), others are supporting
        layers: list[AudioSegment] = []
        for i, p in enumerate(downloaded_paths):
            seg = safe_load(p)
            if not seg: continue
            seg = condense_to_key_moments(seg)
            target = -24.0 if i == 0 else -19.0  # Make the first layer quieter
            layers.append(set_target_dbfs(seg, target))

        if not layers:
            print(f"⚠️ Could not decode any layers for {story}; skipping.")
            continue

        mix_audio(layers, out_path)
        print(f"🎧 Exported: {out_path}")


if __name__ == "__main__":
    print("🎶 Starting audio pipeline... 🎶")
    build_chant_and_ambient()
    build_trilogy()
    build_forest_stories()
    build_birth_of_dharma()
    print("✅ Audio pipeline complete.")
