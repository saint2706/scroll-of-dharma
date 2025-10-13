# Contributing to The Scroll of Dharma

Thank you for your interest in contributing to The Scroll of Dharma! This guide will help you get started with contributing to this project while maintaining our high standards for accessibility, code quality, and narrative excellence.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Accessibility Standards](#accessibility-standards)
- [Code Style and Conventions](#code-style-and-conventions)
- [Adding New Content](#adding-new-content)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Community and Support](#community-and-support)

---

## Code of Conduct

This project is committed to providing a welcoming and inclusive environment for all contributors. By participating, you agree to:

- Be respectful and considerate in all interactions
- Focus on constructive feedback and collaboration
- Honor the spiritual and cultural significance of the source material
- Maintain the dignity and reverence appropriate to ancient Hindu epics

---

## Getting Started

### Prerequisites

- **Node.js** 18+ and npm
- **Git** for version control
- A text editor or IDE (VS Code recommended)
- Basic knowledge of TypeScript and Astro (or willingness to learn)

### Initial Setup

1. **Fork the repository** on GitHub

2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/scroll-of-dharma.git
   cd scroll-of-dharma
   ```

3. **Install dependencies**:
   ```bash
   npm install
   ```

4. **Start the development server**:
   ```bash
   npm run dev
   ```

5. **Visit** `http://localhost:4321` to see the site

---

## Development Workflow

### Branch Strategy

1. Create a new branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Use descriptive branch names:
   - `feature/add-ramayana-chapter` - New features
   - `fix/audio-player-bug` - Bug fixes
   - `docs/update-api-guide` - Documentation
   - `a11y/improve-keyboard-nav` - Accessibility improvements

### Making Changes

1. **Make small, focused commits**:
   ```bash
   git add .
   git commit -m "Add: New story for Birth of Dharma chapter"
   ```

2. **Write clear commit messages**:
   - Use imperative mood ("Add" not "Added")
   - Be specific and descriptive
   - Reference issues when applicable

3. **Keep your branch updated**:
   ```bash
   git fetch origin
   git rebase origin/main
   ```

### Building and Testing

Before submitting a PR:

1. **Check TypeScript types**:
   ```bash
   npm run build
   ```

2. **Test locally**:
   ```bash
   npm run dev
   ```

3. **Preview production build**:
   ```bash
   npm run build
   npm run preview
   ```

---

## Accessibility Standards

**This project is committed to WCAG 2.1 Level AA compliance.** All contributions must maintain or improve accessibility.

### Core Accessibility Requirements

#### 1. Semantic HTML
- Use appropriate HTML elements (`<nav>`, `<article>`, `<section>`, etc.)
- Maintain proper heading hierarchy (h1 → h2 → h3)
- Use `<button>` for interactive elements, not `<div>` or `<span>`

**Example:**
```astro
<!-- Good -->
<nav aria-label="Chapter navigation">
  <h2>Navigate Chapters</h2>
  <ul>
    <li><a href="/chapter1">Chapter 1</a></li>
  </ul>
</nav>

<!-- Bad -->
<div class="navigation">
  <div class="title">Navigate Chapters</div>
  <div onclick="navigate()">Chapter 1</div>
</div>
```

#### 2. Keyboard Navigation
- All interactive elements must be keyboard accessible
- Provide visible focus indicators
- Support standard keyboard shortcuts (Tab, Enter, Space, Escape)
- Ensure logical tab order

**Testing:** Navigate the entire site using only your keyboard.

#### 3. Color Contrast
- Maintain minimum contrast ratios:
  - **Normal text:** 4.5:1
  - **Large text (18pt+):** 3:1
  - **UI components:** 3:1

**Tool:** Use [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)

#### 4. Alternative Text
- Provide descriptive alt text for all images and SVGs
- Be specific and meaningful
- Don't start with "Image of..." or "Picture of..."

**Example:**
```typescript
{
  lotus_of_doubt: {
    svg: 'lotus.svg',
    anim: 'lotus-animated',
    alt: 'Lotus flower representing doubt and contemplation'  // Good
    // alt: 'Image of a lotus'  // Bad - not descriptive
  }
}
```

#### 5. Audio Accessibility
- **All audio content MUST have text transcripts**
- Use native HTML5 audio controls
- Provide captions or transcripts for narrative audio
- Include descriptive labels

**Example:**
```astro
<audio controls aria-label="Narrative audio for Lotus of Doubt">
  <source src={narrativeUrl} type="audio/mpeg" />
  Your browser does not support audio playback.
</audio>
<!-- Transcript must be available via link or on same page -->
```

#### 6. ARIA Labels
- Use ARIA attributes when semantic HTML is insufficient
- Common attributes:
  - `aria-label`: Provides accessible name
  - `aria-labelledby`: References another element's ID
  - `aria-describedby`: Provides additional description
  - `aria-current`: Indicates current item in navigation

**Example:**
```astro
<button aria-label="Close modal" aria-pressed="false">
  ✕
</button>
```

#### 7. Motion and Animation
- Respect `prefers-reduced-motion` media query
- Provide alternative static content
- Avoid auto-playing animations

**Example:**
```css
@media (prefers-reduced-motion: reduce) {
  .lotus-animated {
    animation: none;
  }
}
```

### Accessibility Checklist

Before submitting a PR with UI changes, verify:

- [ ] All interactive elements are keyboard accessible
- [ ] Focus indicators are visible on all interactive elements
- [ ] Color contrast meets WCAG AA standards (4.5:1 minimum)
- [ ] Images and SVGs have descriptive alt text
- [ ] Heading hierarchy is logical (no skipped levels)
- [ ] ARIA labels are used appropriately
- [ ] Audio/video content has text alternatives
- [ ] Animations respect `prefers-reduced-motion`
- [ ] Forms have proper labels and error messages
- [ ] Page titles are descriptive and unique

---

## Code Style and Conventions

### TypeScript

1. **Use strict TypeScript configuration**
   - Project uses `"extends": "astro/tsconfigs/strict"`
   - Define types explicitly when type inference isn't clear

2. **Naming Conventions**
   - **Interfaces/Types**: PascalCase (`Story`, `Chapter`)
   - **Variables/Functions**: camelCase (`getStory`, `chapterId`)
   - **Constants**: SCREAMING_SNAKE_CASE (`CHAPTER_TITLES`)
   - **Files**: snake_case for IDs, PascalCase for components

3. **Type Definitions**
   - Define all types in `src/lib/types.ts`
   - Export shared interfaces
   - Avoid `any` type unless absolutely necessary

**Example:**
```typescript
// Good
export interface Story {
  id: string;
  title: string;
  content: string;
}

function getStory(chapterId: string, storyId: string): Story | undefined {
  // implementation
}

// Bad
function getStory(chapterId, storyId): any {
  // implementation
}
```

### Astro Components

1. **Component Structure**
   ```astro
   ---
   // Frontmatter: imports and logic
   import type { Story } from '../lib/types';
   
   interface Props {
     story: Story;
   }
   
   const { story } = Astro.props;
   ---
   
   <!-- Template: HTML markup -->
   <article>
     <h2>{story.title}</h2>
   </article>
   
   <style>
     /* Scoped styles */
     article {
       padding: 1rem;
     }
   </style>
   ```

2. **Props Interface**
   - Always define a `Props` interface
   - Document complex props with comments
   - Use optional chaining for optional props

3. **Keep Components Focused**
   - Single responsibility principle
   - Extract reusable logic to separate functions
   - Prefer composition over large monolithic components

### CSS and Styling

1. **Use Tailwind CSS Utilities**
   - Prefer utility classes over custom CSS
   - Use custom classes only when necessary

2. **Custom Theme**
   - Use defined theme colors (parchment-50 through parchment-500)
   - Use theme fonts: `font-heading`, `font-body`, `font-cormorant`, `font-spectral`

3. **Responsive Design**
   - Mobile-first approach
   - Use Tailwind breakpoints: `sm:`, `md:`, `lg:`, `xl:`

**Example:**
```astro
<div class="p-4 md:p-6 bg-parchment-100 font-body text-amber-900">
  <!-- Mobile: p-4, Desktop: p-6 -->
</div>
```

### Narrative Content Style

1. **Tone and Voice**
   - Poetic, meditative, contemplative
   - Present tense for immediacy
   - Short, impactful sentences
   - Open with a quoted line when possible

2. **Structure**
   - 3-5 sentences per story
   - Each sentence builds on the last
   - End with consequence or reflection

**Example:**
```typescript
const narrativeContent = {
  example_story: `"The opening sets the scene..."
The second line reveals the conflict.
Stakes rise; choices narrow.
Resolution arrives with moral weight.`
};
```

3. **Content Guidelines**
   - Stay true to source material
   - Respect cultural and spiritual significance
   - Avoid sensationalism or modern slang
   - Maintain scholarly accuracy

---

## Adding New Content

### Adding a New Story

1. **Add narrative text** in `src/lib/narratives.ts`:
   ```typescript
   const narrativeContent = {
     your_chapter: {
       new_story: `"Opening quote..."
   Narrative content following the style guide.
   Maintain poetic, meditative tone.
   End with meaningful reflection.`,
     },
   };
   ```

2. **Create SVG illustration**:
   - Design or source an appropriate SVG
   - Save to `public/assets/svg/new_story.svg`
   - Optimize SVG (remove unnecessary elements)
   - Ensure SVG is accessible

3. **Add SVG mapping**:
   ```typescript
   const svgAssets: Record<string, { svg: string; anim: string; alt: string }> = {
     new_story: {
       svg: 'new_story.svg',
       anim: 'new-story-animated',
       alt: 'Descriptive alternative text for accessibility'
     },
   };
   ```

4. **Add audio** (if available):
   ```typescript
   const audioAssets: Record<string, { narrative?: string; ambient?: string }> = {
     new_story: {
       narrative: 'path/to/narrative.mp3',
       ambient: 'path/to/ambient.mp3'
     },
   };
   ```

5. **Update story titles** in `src/lib/types.ts`:
   ```typescript
   export const STORY_TITLES: Record<string, string> = {
     // ... existing stories
     new_story: "New Story Display Title",
   };
   ```

6. **Update chapter's story array**:
   ```typescript
   stories: [
     'existing_story',
     'new_story'  // Add here
   ].map(id => createStory('your_chapter', id))
   ```

7. **Create audio transcript** in `docs/AUDIO_TRANSCRIPTS.md`

### Adding a New Chapter

1. **Add chapter ID to `CHAPTER_TITLES`** in `src/lib/types.ts`
2. **Add narrative content** for all stories in the chapter
3. **Create SVG assets** for all stories
4. **Add chapter to `chapters` array** in `src/lib/narratives.ts`
5. **Create audio transcripts** for all stories
6. **Update README.md** with chapter description
7. **Test all routes** work correctly

---

## Testing Guidelines

### Manual Testing Checklist

Before submitting a PR:

- [ ] Test in multiple browsers (Chrome, Firefox, Safari)
- [ ] Test on mobile devices or browser dev tools
- [ ] Verify keyboard navigation works
- [ ] Check with screen reader if possible (NVDA/JAWS/VoiceOver)
- [ ] Verify color contrast with tools
- [ ] Test with reduced motion enabled
- [ ] Check all links and routes work
- [ ] Verify images load correctly
- [ ] Test audio playback (if applicable)

### Automated Testing

Currently, the project uses:
- **TypeScript checking**: `npm run build` runs `astro check`
- **Build validation**: Ensures all pages compile without errors

Future: We plan to add:
- Unit tests with Vitest
- E2E tests with Playwright
- Accessibility tests with axe-core

---

## Pull Request Process

### Before Submitting

1. **Ensure your code builds**:
   ```bash
   npm run build
   ```

2. **Test locally**:
   ```bash
   npm run dev
   ```

3. **Update documentation** if needed (README, API docs, etc.)

4. **Commit your changes** with clear messages

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

### Creating the Pull Request

1. **Go to GitHub** and create a Pull Request from your fork

2. **Write a clear PR description**:
   - What does this PR do?
   - Why is this change needed?
   - How has it been tested?
   - Screenshots for UI changes
   - Reference related issues

3. **PR Title Format**:
   - `Add: New story for Weapon Quest chapter`
   - `Fix: Audio player keyboard navigation`
   - `Docs: Update API documentation for Story interface`
   - `A11y: Improve color contrast on buttons`

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] New feature (story, chapter, component)
- [ ] Bug fix
- [ ] Documentation update
- [ ] Accessibility improvement
- [ ] Performance optimization

## Testing Completed
- [ ] Builds successfully
- [ ] Tested in multiple browsers
- [ ] Keyboard navigation verified
- [ ] Accessibility checked
- [ ] Mobile responsive verified

## Screenshots (if applicable)
[Add screenshots for UI changes]

## Related Issues
Closes #123
```

### Review Process

1. **Maintainers will review** your PR within 3-5 business days
2. **Address feedback** by pushing additional commits
3. **Once approved**, a maintainer will merge your PR
4. **Celebrate!** 🎉 You've contributed to The Scroll of Dharma

---

## Community and Support

### Getting Help

- **Documentation**: Start with [README.md](README.md) and [API.md](docs/API.md)
- **Issues**: Check [GitHub Issues](https://github.com/saint2706/scroll-of-dharma/issues) for existing questions
- **Discussions**: Use [GitHub Discussions](https://github.com/saint2706/scroll-of-dharma/discussions) for questions

### Reporting Issues

When reporting bugs:
1. **Search existing issues** first
2. **Use issue templates** if available
3. **Include**:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Browser and OS information
   - Screenshots if relevant

### Suggesting Features

We welcome feature suggestions! When proposing new features:
1. **Check the [roadmap](ROADMAP_2025-2027.md)** first
2. **Open a Discussion** to gather feedback
3. **Describe**:
   - The problem or need
   - Your proposed solution
   - Alternative solutions considered
   - How it aligns with project goals

---

## Additional Resources

### Project Documentation
- **[API.md](docs/API.md)** - Complete API reference
- **[ACCESSIBILITY_AUDIT.md](ACCESSIBILITY_AUDIT.md)** - Accessibility audit and standards
- **[ROADMAP_2025-2027.md](ROADMAP_2025-2027.md)** - Strategic roadmap

### External Resources
- **[Astro Documentation](https://docs.astro.build/)** - Astro framework guide
- **[Tailwind CSS Docs](https://tailwindcss.com/docs)** - Utility-first CSS framework
- **[WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)** - Accessibility standards
- **[WebAIM](https://webaim.org/)** - Web accessibility resources
- **[TypeScript Handbook](https://www.typescriptlang.org/docs/)** - TypeScript guide

---

## Recognition

Contributors are recognized in:
- **GitHub Contributors** page
- **Project README** (for significant contributions)
- **Release notes** for version contributions

---

## Questions?

If you have questions not covered in this guide:
1. Check existing documentation
2. Search GitHub Issues and Discussions
3. Open a new Discussion with the "question" tag

---

**Thank you for contributing to The Scroll of Dharma!** 

*"Dharma is not a rule. It is a rhythm."*

Together, we preserve and share these timeless teachings with the world.
