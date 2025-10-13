# Scroll of Dharma - Content Directory

This directory contains all narrative content converted to Markdown format with frontmatter metadata.

## Structure

```
content/
├── gita-scroll/        # Chapter 1: Gita Scroll (4 stories)
├── fall-of-dharma/     # Chapter 2: Fall of Dharma (3 stories)
├── weapon-quest/       # Chapter 3: Weapon Quest (4 stories)
├── birth-of-dharma/    # Chapter 4: Birth of Dharma (5 stories)
└── trials-of-karna/    # Chapter 5: Trials of Karna (5 stories)
```

## Story Format

Each story is a Markdown file with YAML frontmatter:

```markdown
---
title: "The Lotus of Doubt"
chapter: "Gita Scroll"
audio: "/audio/gita_scroll/lotus_of_doubt_mix.mp3"
svg: "/svg/lotus.svg"
---

The conch shells fell silent...
```

## Frontmatter Fields

- **title**: Human-readable story title
- **chapter**: Parent chapter name
- **audio**: Path to the story's audio file (relative to `/public`)
- **svg**: Path to the story's SVG glyph (relative to `/public`)

## Usage with Static Site Generators

### Astro

```typescript
import { getCollection } from 'astro:content';

// Get all stories
const stories = await getCollection('stories');

// Filter by chapter
const gitaStories = stories.filter(s => 
  s.data.chapter === 'Gita Scroll'
);
```

### Next.js

```typescript
import fs from 'fs';
import matter from 'gray-matter';

const story = matter(
  fs.readFileSync('content/gita-scroll/lotus_of_doubt.md')
);
```

## Migration Note

This content was automatically extracted from `narrative.py` as part of the Week 1 migration plan documented in `docs/FREE_HOSTING_OPTIONS.md`.
