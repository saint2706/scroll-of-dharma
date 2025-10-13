# Copilot Instructions for Scroll of Dharma

## Project Overview

The Scroll of Dharma is an interactive storytelling experience that brings pivotal moments from ancient Hindu epics (Mahabharata and Bhagavad Gita) to life through elegant web design. The project has been migrated from Streamlit to Astro for optimal performance and hosting on GitHub Pages.

**Live Site:** https://saint2706.github.io/scroll-of-dharma

## Technology Stack

### Primary Technologies
- **Framework:** Astro 5.x (Static Site Generator)
- **Language:** TypeScript (strict mode)
- **Styling:** Tailwind CSS 3.x
- **Build Tool:** Astro's built-in compiler
- **Deployment:** GitHub Pages via GitHub Actions

### Key Dependencies
- `@astrojs/mdx` - MDX support for content
- `@astrojs/tailwind` - Tailwind integration
- `@astrojs/check` - TypeScript checking

### Legacy Code
The repository contains legacy Python/Streamlit files (`app.py`, `narrative.py`, `audio_builder.py`, etc.) that are preserved for reference only. **Do not modify or remove these files** unless explicitly requested.

## Project Structure

```
src/
├── pages/              # Astro route pages
│   ├── index.astro     # Home page
│   └── chapters/       # Dynamic chapter/story pages
├── layouts/            # Page layout components
├── components/         # Reusable Astro components
├── lib/                # TypeScript utilities and data
│   ├── narratives.ts   # Story content (primary data source)
│   └── types.ts        # Type definitions
└── styles/             # Global styles

public/
├── assets/
│   └── svg/           # SVG illustrations for stories
└── favicon.svg        # Site favicon
```

## Code Style & Conventions

### TypeScript
- Use strict TypeScript configuration (`extends: "astro/tsconfigs/strict"`)
- Define types in `src/lib/types.ts`
- Prefer type inference where possible
- Use descriptive variable and function names

### Component Structure
- Use `.astro` files for components and pages
- Keep components focused and reusable
- Use Astro's component syntax and frontmatter
- Avoid unnecessary client-side JavaScript (leverage Astro's static generation)

### Styling
- Use Tailwind CSS utility classes
- Custom theme extends defined in `tailwind.config.mjs`:
  - Font families: `heading` (Cinzel Decorative), `body` (EB Garamond), `cormorant`, `spectral`
  - Custom colors: `parchment` palette (50-500)
- Follow mobile-first responsive design
- Maintain existing visual theming (parchment/dharma aesthetic)

### Narrative Content
- Story content lives in `src/lib/narratives.ts`
- Each narrative is organized by chapter → story structure
- Maintain poetic, meditative tone in narrative text
- SVG assets for stories are in `public/assets/svg/`

## Development Workflow

### Setup
```bash
npm install        # Install dependencies
npm run dev        # Start dev server (localhost:4321)
npm run build      # Build for production
npm run preview    # Preview production build
```

### Before Committing
1. Run `npm run build` to ensure TypeScript checks pass
2. Verify no build errors or warnings
3. Test locally with `npm run dev`
4. Follow existing code formatting and style

### Adding New Stories
1. Add narrative text to `src/lib/narratives.ts`
2. Create/add SVG illustration to `public/assets/svg/`
3. Update type definitions in `src/lib/types.ts` if needed
4. Test rendering in development mode
5. Verify accessibility (semantic HTML, alt text, etc.)

## Build & Deployment

- **Build Command:** `npm run build`
- **Build Output:** `./dist/` directory
- **Deploy Target:** GitHub Pages
- **CI/CD:** `.github/workflows/deploy.yml` (deploys from `main` branch)
- The build process includes:
  - TypeScript type checking (`astro check`)
  - Static page generation
  - Asset optimization

## Accessibility Requirements

This project maintains **WCAG 2.1 AA compliance**. When making changes:

- Use semantic HTML elements
- Provide meaningful alt text for images and SVGs
- Maintain sufficient color contrast (see `ACCESSIBILITY_AUDIT.md`)
- Ensure keyboard navigation works
- Test with screen readers when possible
- Keep focus indicators visible
- Support reduced motion preferences

Reference `ACCESSIBILITY_AUDIT.md` for detailed audit findings and recommendations.

## Performance Standards

Maintain these performance targets:
- **Lighthouse Score:** 95+
- **First Contentful Paint:** <1s
- **Time to Interactive:** <1s
- **Bundle Size:** ~50KB (gzipped)

Use Astro's static generation capabilities to avoid unnecessary JavaScript bundles.

## Documentation

Key documentation files:
- `README.md` - Main project documentation
- `MIGRATION_TO_ASTRO.md` - Migration details from Streamlit
- `ACCESSIBILITY_AUDIT.md` - Accessibility improvements and audit
- `ROADMAP_2025-2027.md` - Strategic roadmap
- `CLEANUP_SUMMARY.md` - Recent repository cleanup details

Keep documentation updated when making significant changes.

## Contributing Guidelines

When suggesting or making changes:

1. **Respect the theme:** Maintain the reverent, meditative aesthetic
2. **Minimal changes:** Make surgical, focused modifications
3. **Test thoroughly:** Verify builds pass and functionality works
4. **Follow conventions:** Match existing code style and structure
5. **Accessibility first:** Ensure changes don't break accessibility
6. **No breaking changes:** Don't modify working functionality unnecessarily
7. **Preserve legacy:** Don't touch Python/Streamlit files unless explicitly requested

## Common Tasks

### Modifying Story Content
- Edit `src/lib/narratives.ts`
- Maintain consistent narrative structure and tone
- Keep narratives concise and impactful

### Updating Styles
- Modify Tailwind classes in `.astro` components
- Update `tailwind.config.mjs` for theme changes
- Test responsive behavior across screen sizes

### Adding New Pages
- Create `.astro` files in `src/pages/`
- Use existing layouts from `src/layouts/`
- Follow naming conventions and route structure

### Fixing TypeScript Errors
- Check type definitions in `src/lib/types.ts`
- Run `npm run build` to see all type errors
- Use strict TypeScript patterns

## Testing

- **Current Test Command:** `npm test` (currently returns success with no tests)
- No automated test suite is currently implemented
- Manual testing is performed through:
  - `npm run dev` - Development server testing
  - `npm run build` - Build-time validation
  - Visual inspection of changes

## Important Notes

1. **Legacy Code:** The repository contains Python/Streamlit code that should be preserved but not actively maintained
2. **Performance:** Prioritize static generation over client-side JavaScript
3. **Content:** Narrative content is the core value - maintain quality and consistency
4. **Design:** The aesthetic is intentional - parchment theme, serif fonts, meditative tone
5. **Deployment:** Only the `main` branch triggers deployments to GitHub Pages

## Questions?

Refer to:
- README.md for quick start and overview
- MIGRATION_TO_ASTRO.md for technical migration details
- ACCESSIBILITY_AUDIT.md for accessibility standards
- Existing code for patterns and conventions
