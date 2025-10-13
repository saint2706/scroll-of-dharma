# 🕉️ The Scroll of Dharma (Astro Version)

*"Dharma is not a rule. It is a rhythm."*

A fast, modern static site showcasing pivotal moments from ancient epics. Built with Astro for optimal performance and deployed on GitHub Pages.

## ✨ Features

- **⚡ Lightning Fast:** Static site generation for instant page loads
- **📱 Mobile-First:** Responsive design optimized for all devices
- **♿ Accessible:** WCAG 2.1 AA compliant with semantic HTML
- **🎨 Beautiful:** Animated SVG illustrations and elegant typography
- **🆓 Free Hosting:** Deployed on GitHub Pages with unlimited bandwidth

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

# Preview production build
npm run preview
```

Visit `http://localhost:4321` to view the site locally.

## 📖 The Chapters

### 1. Gita Scroll
Arjuna halts a war, interrogates duty, and chooses how to fight.

### 2. Fall of Dharma
A fixed dice game topples a kingdom while a court watches in silence.

### 3. Weapon Quest
Training, divine trials, and discipline decide who earns celestial weapons.

### 4. Birth of Dharma
Creation itself balances promises between fire, water, and motion.

### 5. Trials of Karna
Loyalty, secrecy, and a fatal curse lock a hero into his final stand.

## 🛠️ Technology Stack

- **Framework:** [Astro](https://astro.build/) - Static site generator
- **Styling:** [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS
- **Language:** TypeScript for type safety
- **Deployment:** GitHub Pages with GitHub Actions
- **Fonts:** Google Fonts (Cinzel Decorative, EB Garamond, Cormorant Garamond, Spectral)

## 📁 Project Structure

```
src/
├── pages/              # Route pages
│   ├── index.astro     # Home page
│   └── chapters/       # Dynamic chapter/story pages
├── layouts/            # Page layouts
├── components/         # Reusable Astro components
├── lib/                # TypeScript utilities and data
└── styles/             # Global styles

public/
├── assets/
│   └── svg/           # SVG illustrations
└── favicon.svg        # Site favicon

.github/
└── workflows/
    └── deploy.yml     # GitHub Pages deployment
```

## 🎨 Customization

### Adding a New Story

1. Edit `src/lib/narratives.ts` to add your story data
2. Add the SVG illustration to `public/assets/svg/`
3. Update the `svgAssets` mapping with the new SVG file
4. The pages will be automatically generated

### Styling

Global styles are in `src/styles/global.css`. The site uses:
- Tailwind CSS utilities for layout
- Custom CSS classes for components
- CSS animations for SVG illustrations

## 🚢 Deployment

The site automatically deploys to GitHub Pages when changes are pushed to the main branch.

**Live Site:** https://saint2706.github.io/scroll-of-dharma

### Manual Deployment

```bash
# Build the site
npm run build

# The output will be in the dist/ directory
# Deploy the dist/ directory to any static hosting service
```

## 📊 Performance

- **Lighthouse Score:** 95+
- **First Contentful Paint:** <1s
- **Time to Interactive:** <1s
- **Bundle Size:** ~50KB (gzipped)

## 🤝 Contributing

Contributions are welcome! To add a new narrative:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-story`)
3. Add your story to `src/lib/narratives.ts`
4. Add any required assets to `public/assets/`
5. Test locally with `npm run dev`
6. Submit a pull request

Please ensure your changes:
- Follow the existing code style
- Include descriptive commit messages
- Pass all builds without errors
- Maintain accessibility standards

## 📝 License

This project is open source and available under the [ISC License](LICENSE).

## 🙏 Acknowledgments

- Ancient epics: Mahabharata and Bhagavad Gita
- Modern web technologies that make this experience possible
- The open-source community for excellent tools and documentation

---

*Crafted with reverence • Powered by Astro*
