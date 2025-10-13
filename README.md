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

The Scroll of Dharma is an interactive story lab built with Streamlit. Animated glyphs, reactive themes, and scored soundscapes bring epic turning points into a focused reading flow. Pick a chapter, inspect the pressure on every hero, and track the consequences of each choice.

## ✨ The Experience

A modern, static site optimized for speed and accessibility.

*   **⚡ Lightning Fast:** Pre-rendered pages load in under 1 second
*   **📱 Mobile-First:** Responsive design that works beautifully on all devices
*   **🎨 Visual Excellence:** Animated SVG glyphs for each story
*   **♿ Accessible:** Semantic HTML and WCAG 2.1 AA compliant
*   **🆓 Free Hosting:** Deployed on GitHub Pages with zero cost

## 📜 The Chapters

Five chapters cover the critical pivots of the epic. Each one surfaces a decision that tilts the world.

*   **Gita Scroll:** Arjuna halts a war, interrogates duty, and chooses how to fight.
*   **Fall of Dharma:** A fixed dice game topples a kingdom while a court watches in silence.
*   **Weapon Quest:** Training, divine trials, and discipline decide who earns celestial weapons.
*   **Birth of Dharma:** Creation itself balances promises between fire, water, and motion.
*   **Trials of Karna:** Loyalty, secrecy, and a fatal curse lock a hero into his final stand.

*“To wield the divine, you must first dissolve the self.”*

## 🚀 Quick Start

Get started with the modern Astro version:

```bash
# Clone the repository
git clone https://github.com/saint2706/scroll-of-dharma.git
cd scroll-of-dharma

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

Visit `http://localhost:4321` to view the site locally.

### Legacy Streamlit Version

The original Streamlit version is still available. See [STREAMLIT_SETUP.md](docs/STREAMLIT_SETUP.md) for setup instructions (Python 3.11+, ffmpeg required).

## 🔄 Migration Summary

The project has been migrated from Streamlit to Astro, delivering significant improvements:

- **Performance:** 10x faster page loads (5-8s → 0.5-1s)
- **Bundle Size:** 40x smaller (2MB → 50KB)
- **Hosting:** Free GitHub Pages with unlimited bandwidth
- **SEO:** Improved discoverability and search engine optimization
- **Mobile:** Responsive design optimized for all devices

See [MIGRATION_TO_ASTRO.md](MIGRATION_TO_ASTRO.md) for complete migration details.

## 🤝 Contributing

Contributions welcome! To add a new story (Astro version):

1. Edit `src/lib/narratives.ts` to add your narrative
2. Add SVG illustration to `public/assets/svg/`
3. Update the SVG assets mapping
4. Test with `npm run dev`
5. Submit a pull request

For Streamlit contributions, see [docs/STREAMLIT_SETUP.md](docs/STREAMLIT_SETUP.md).

## ✍️ The Scribe's Tools (Legacy Streamlit - For Reference)

Should you feel the call to contribute a new story to the Scroll, your path is clear. The process is a meditation in three parts: composing the narrative, forging the soundscape, and weaving the elements together.

> **Keep your scroll aligned.** Before pushing your changes, rebase your branch onto the latest `main` so that the automated merge check in CI can complete without conflict.

Let us say you wish to add a new story called `"The River's Wisdom"` to the `"Birth of Dharma"` chapter.

### 1. Compose the Narrative

The heart of the scroll lies in `narrative.py`. Open this file and add your new story's text. Give it a unique key, like `the_rivers_wisdom`.

```python
# In narrative.py, within the "birth_of_dharma" chapter...
"the_rivers_wisdom": (
    "“The river does not carve the stone with force, but with persistence...”\n"
    "Your narrative continues here, a gentle stream of wisdom..."
),
```

### 2. Forge the Soundscape

The soul of the scroll echoes in `audio_builder.py`. Here, you must provide the sources for your new soundscape.

1.  **Add the Source:** Find the configuration dictionary for your chapter (e.g., `BIRTH_CHAPTERS`). Add a new entry for `the_rivers_wisdom` with URLs to your chosen audio from YouTube or Pixabay.

    ```python
    # In audio_builder.py, within BIRTH_CHAPTERS...
    "the_rivers_wisdom": [
        { "type": "pixabay", "url": "https://.../ambient_water.mp3" },
        { "type": "youtube", "url": "https://www.youtube.com/watch?v=..." },
    ],
    ```

2.  **Run the Forge:** After saving your changes, invoke the setup scribe again to create the audio asset.

    ```powershell
    python setup.py
    ```

    This will download, process, and mix your audio, placing the final file in `assets/audio/birth/the_rivers_wisdom/`.

### 3. Weave the Elements

The final thread is woven in `app.py`, the loom of the experience. Here, you will connect your new narrative to its visual glyph.

1.  **Add the Glyph:** Place your new SVG icon (e.g., `river.svg`) into the `assets/svg/` directory.

2.  **Bind the Assets:** In `app.py`, find the `scene_assets` dictionary. Add a new entry for `the_rivers_wisdom`, linking it to your SVG. If it has an animation, define its class.

    ```python
    # In app.py, within scene_assets...
    "the_rivers_wisdom": {
        "svg": "river.svg",
        "anim_class": "", # Add an animation class if you created one in the CSS
        "alt": "An icon of a flowing river representing wisdom",
    },
    ```
3. **Map the Audio (If Needed)**: Some chapters, like 'Birth of Dharma', require an extra step to map the narrative key to the audio key if they differ. In `app.py`, find the `BIRTH_STORY_AUDIO_MAP` and add your mapping if necessary. If your keys are identical, you can skip this.

That is all. Unfurl the scroll (`streamlit run app.py`) and behold your contribution. The river of Dharma flows on, enriched by your devotion.

### Development workflow and quality gates

The scroll now follows a shared rhythm for code style and quality checks, codified in `pyproject.toml`. Before opening a pull request, invoke the following guardians:

```bash
black --check .
ruff check .
mypy app.py narrative.py audio_builder.py setup.py
pytest
pip-audit --strict
```

These same commands run automatically on GitHub Actions for both Linux and Windows environments, so keeping them green locally will help your contribution sail smoothly through the review current.

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

## 🚀 Future: Deployment Options

The Scroll of Dharma is currently powered by Streamlit Community Cloud, which is excellent for prototyping. Depending on your needs, there are different paths forward:

### 🆓 For Personal Projects (Free Hosting Only)
**Current**: Streamlit Community Cloud (free)  
**Alternatives**: GitHub Pages, Netlify, Cloudflare Pages (all free)

👉 **[Free Hosting Options Guide](./docs/FREE_HOSTING_OPTIONS.md)** - For personal projects with <1K users and $0 budget

**Key Improvements with Free Static Hosting:**
- **5-10x faster** load times (5-8s → 0.5-1.5s)
- **Better mobile** experience
- **Improved SEO** for discoverability
- **$0 cost** forever (GitHub Pages, Netlify free tier)
- **Simple** maintenance

**Realistic assessment**: For personal projects with 500 users, keeping Streamlit Community Cloud is also a valid choice. Migration takes 40+ hours. See the guide for honest recommendations.

### 🏢 For Production/Commercial Projects (Growth Expected)
**If planning for 10K+ users**, consider enterprise solutions:

- **[Executive Summary](./docs/EXECUTIVE_SUMMARY.md)** - Production deployment strategy (5 min read)
- **[Deployment Comparison](./docs/DEPLOYMENT_COMPARISON.md)** - Detailed analysis of options (15 min read)
- **[Deployment Roadmap](./DEPLOYMENT_ROADMAP.md)** - Complete 3-year strategy (30 min read)
- **[Migration Guide Phase 1](./docs/MIGRATION_GUIDE_PHASE1.md)** - Step-by-step implementation guide

**Recommendation**: Next.js + Vercel for optimal performance, SEO, and scalability to millions of users.

### 📚 Complete Documentation
See [docs/README.md](./docs/README.md) for complete documentation index organized by project scale.

## ❓ Clearing the Path (Troubleshooting)

*   **`ffmpeg` not found:** You must install it from [ffmpeg.org](https://ffmpeg.org) and ensure it is in your system's PATH.
*   **Audio fails to download:** Some sources may be protected. A `cookies.txt` file from your browser, placed in the project root, may appease the guardians of the content.
*   **Autoplay is silent:** Some browsers require an interaction before they will play audio. A simple click or selection will awaken the soundscape.

---

*Crafted with reverence • Powered by Streamlit*
