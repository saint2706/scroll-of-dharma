# 🕉️ The Scroll of Dharma

*"Dharma is not a rule. It is a rhythm."*

<p align="center">
    <a href="LICENSE"><img alt="License" src="https://img.shields.io/github/license/saint2706/scroll-of-dharma"></a>
    <a href="https://astro.build/"><img alt="Built with Astro" src="https://img.shields.io/badge/Astro-5.x-FF5D01?logo=astro"></a>
    <a href="https://saint2706.github.io/scroll-of-dharma"><img alt="Live Demo" src="https://img.shields.io/badge/demo-live-success"></a>
    <a href="https://github.com/saint2706/scroll-of-dharma/commits">
        <img alt="Last commit" src="https://img.shields.io/github/last-commit/saint2706/scroll-of-dharma">
    </a>
</p>

An interactive story experience bringing pivotal moments from ancient Hindu epics to life. Built with Astro for lightning-fast performance, featuring animated illustrations and elegant storytelling.

**🌐 Live Site:** [https://saint2706.github.io/scroll-of-dharma](https://saint2706.github.io/scroll-of-dharma)

## ✨ Features

*   **⚡ Lightning Fast:** Pre-rendered pages load in under 1 second
*   **📱 Mobile-First:** Responsive design that works beautifully on all devices
*   **🎨 Visual Excellence:** Animated SVG illustrations for each story
*   **♿ Accessible:** Semantic HTML and WCAG 2.1 AA compliant
*   **🆓 Free Hosting:** Deployed on GitHub Pages with zero cost

## 📜 The Chapters

Five chapters cover the critical pivots of the epic. Each one surfaces a decision that tilts the world.

*   **Gita Scroll:** Arjuna halts a war, interrogates duty, and chooses how to fight.
*   **Fall of Dharma:** A fixed dice game topples a kingdom while a court watches in silence.
*   **Weapon Quest:** Training, divine trials, and discipline decide who earns celestial weapons.
*   **Birth of Dharma:** Creation itself balances promises between fire, water, and motion.
*   **Trials of Karna:** Loyalty, secrecy, and a fatal curse lock a hero into his final stand.

*"To wield the divine, you must first dissolve the self."*

## 🚀 Quick Start

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

## 🧪 Testing

We maintain high quality through comprehensive automated testing:

```bash
# Run unit tests
npm test

# Run unit tests with coverage
npm run test:coverage

# Run accessibility tests (Playwright)
npm run test:a11y

# Run Pa11y accessibility audit
npm run test:pa11y
```

**Test Coverage:**
- ✅ **Unit Tests:** 32 tests covering TypeScript utilities and data structures
- ✅ **Accessibility Tests:** 16 E2E tests validating WCAG 2.1 AA compliance
- ✅ **Code Coverage:** 80%+ on business logic with Vitest
- ✅ **CI/CD:** Automated testing on every pull request

See [ACCESSIBILITY_TESTING.md](ACCESSIBILITY_TESTING.md) for complete testing guide.

## 🤝 Contributing

Contributions welcome! Please see our **[Contributing Guide](CONTRIBUTING.md)** for detailed instructions on:

- Development workflow and setup
- Code style and conventions
- **Accessibility standards (WCAG 2.1 AA compliance)**
- Adding new stories and chapters
- Testing and building
- Pull request process

Quick start for adding a new story:

1. Edit `src/lib/narratives.ts` to add your narrative
2. Add SVG illustration to `public/assets/svg/`
3. Update the SVG assets mapping in `narratives.ts`
4. Run tests: `npm test && npm run test:a11y`
5. Submit a pull request

Please ensure your changes:
- Follow the existing code style
- Include descriptive commit messages
- Pass all tests (unit and accessibility)
- Maintain accessibility standards (WCAG 2.1 AA)
All contributions must maintain accessibility standards and pass the build without errors.

## 📁 Project Structure

```
src/
├── pages/              # Route pages
│   ├── index.astro     # Home page
│   └── chapters/       # Dynamic chapter/story pages
├── layouts/            # Page layouts
├── components/         # Reusable Astro components
├── lib/                # TypeScript utilities and data
│   ├── narratives.ts   # Story content
│   └── types.ts        # Type definitions
└── styles/             # Global styles

public/
├── assets/
│   └── svg/           # SVG illustrations
└── favicon.svg        # Site favicon
```

## 🛠️ Technology Stack

- **Framework:** [Astro](https://astro.build/) - Static site generator
- **Styling:** [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS
- **Language:** TypeScript for type safety
- **Deployment:** GitHub Pages with GitHub Actions
- **Fonts:** Google Fonts (Cinzel Decorative, EB Garamond, Cormorant Garamond, Spectral)

## 🔄 Migration Summary

The project has been migrated from Streamlit to Astro, delivering significant improvements:

- **Performance:** 10x faster page loads (5-8s → 0.5-1s)
- **Bundle Size:** 40x smaller (2MB → 50KB)
- **Hosting:** Free GitHub Pages with unlimited bandwidth
- **SEO:** Improved discoverability and search engine optimization
- **Mobile:** Responsive design optimized for all devices

See [MIGRATION_TO_ASTRO.md](MIGRATION_TO_ASTRO.md) for complete migration details.

## 📚 Documentation

- **[ACCESSIBILITY_TESTING.md](ACCESSIBILITY_TESTING.md)** - Comprehensive testing guide
- **[MIGRATION_TO_ASTRO.md](MIGRATION_TO_ASTRO.md)** - Complete migration documentation
- **[ACCESSIBILITY_AUDIT.md](ACCESSIBILITY_AUDIT.md)** - Accessibility audit and improvements
- **[AUDIO_TRANSCRIPTS.md](docs/AUDIO_TRANSCRIPTS.md)** - Audio transcripts for accessibility
- **[ROADMAP_2025-2027.md](ROADMAP_2025-2027.md)** - Strategic roadmap
- **[docs/STREAMLIT_SETUP.md](docs/STREAMLIT_SETUP.md)** - Legacy Streamlit version setup

## 📊 Performance

- **Lighthouse Score:** 95+
- **First Contentful Paint:** <1s
- **Time to Interactive:** <1s
- **Bundle Size:** ~50KB (gzipped)

## 📝 License

This project is open source and available under the [ISC License](LICENSE).

---

*Crafted with reverence • Powered by Astro*
