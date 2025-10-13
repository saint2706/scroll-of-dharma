# Scroll of Dharma - Public Assets Directory

This directory contains all static assets organized for web deployment.

## Structure

```
public/
├── audio/          # Audio files for narratives and soundscapes
│   ├── ambient/    # Ambient loop tracks
│   ├── birth/      # Birth of Dharma chapter audio
│   ├── composite/  # Composite audio mixes
│   ├── fadein/     # Fade-in versions
│   ├── forest/     # Weapon Quest (forest) audio
│   ├── karna/      # Trials of Karna chapter audio
│   └── raw/        # Raw audio files
├── svg/            # SVG glyphs and icons (22 files)
└── textures/       # Background textures for chapters (6 files)
```

## Audio Organization

Audio files are organized by chapter and story:

- `audio/birth/cosmic_breath/cosmic_breath_mix.mp3`
- `audio/karna/final_arrow/final_arrow_mix.mp3`
- `audio/forest/forest_of_austerity/forest_of_austerity_mix.mp3`

Ambient loops follow the pattern:
- `audio/ambient/{story_key}_ambient_loop.mp3`

## SVG Glyphs

All SVG files represent symbolic glyphs for stories:

- `lotus.svg` - Gita Scroll: Lotus of Doubt
- `dharma_wheel.svg` - Gita Scroll: Chakra of Dharma
- `cosmic_egg.svg` - Birth of Dharma: Cosmic Egg
- And 19 more...

## Chapter Textures

Background textures for each chapter:

- `gita_scroll.webp`
- `fall_of_dharma.webp`
- `weapon_quest.webp`
- `birth_of_dharma.webp`
- `trials_of_karna.webp`
- `parchment_bg.webp` (base texture)

## Usage in Web Apps

### Static Site Generators (Astro, Next.js, etc.)

Files in the `public/` directory are served from the root path:

```html
<!-- Audio -->
<audio src="/audio/gita_scroll/lotus_of_doubt_mix.mp3"></audio>

<!-- SVG -->
<img src="/svg/lotus.svg" alt="Lotus glyph" />

<!-- Texture -->
<div style="background-image: url('/textures/gita_scroll.webp')"></div>
```

### File Sizes

- Audio files: ~1-5 MB each (MP3 format)
- SVG files: ~5-50 KB each
- Texture files: ~100-500 KB each (WebP format)

## Migration Note

These assets were copied from the `assets/` directory as part of the Week 1 migration plan documented in `docs/FREE_HOSTING_OPTIONS.md`.

All audio files were generated using the `audio_builder.py` script, which processes and mixes raw audio sources with ambient soundscapes.
