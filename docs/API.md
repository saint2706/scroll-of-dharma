# API Documentation

**Version:** 1.0.0  
**Last Updated:** December 2025

This document provides comprehensive API documentation for The Scroll of Dharma project, including TypeScript interfaces, exported functions, and component APIs.

---

## Table of Contents

- [Core Data Types](#core-data-types)
- [Library Functions](#library-functions)
- [Component APIs](#component-apis)
- [Constants and Mappings](#constants-and-mappings)
- [Usage Examples](#usage-examples)

---

## Core Data Types

### Story Interface

Represents a single narrative story within a chapter.

```typescript
interface Story {
  id: string;                    // Unique identifier (e.g., 'lotus_of_doubt')
  title: string;                 // Human-readable title
  content: string;               // Narrative text/meditation content
  svgFile?: string;              // SVG filename in public/assets/svg/
  animationClass?: string;       // CSS class for animation
  alt?: string;                  // Accessible alt text for SVG
  audio?: {                      // Optional audio assets
    narrative?: string;          // Path to narrative audio file
    ambient?: string;            // Path to ambient audio file
  };
}
```

**Fields:**
- `id` (required): Unique string identifier using snake_case convention
- `title` (required): Display title for the story
- `content` (required): The narrative meditation text
- `svgFile` (optional): Filename of the SVG illustration (defaults to 'lotus.svg')
- `animationClass` (optional): CSS class name for SVG animation effects
- `alt` (optional): Alternative text for screen readers
- `audio` (optional): Object containing audio file paths
  - `narrative`: Path relative to `/assets/audio/` for narrative voiceover
  - `ambient`: Path relative to `/assets/audio/` for background soundscape

---

### Chapter Interface

Represents a collection of related stories forming a chapter.

```typescript
interface Chapter {
  id: string;                    // Unique identifier (e.g., 'gita_scroll')
  title: string;                 // Display title
  description: string;           // Brief chapter summary
  stories: Story[];              // Array of Story objects
}
```

**Fields:**
- `id` (required): Unique string identifier using snake_case convention
- `title` (required): Display title for the chapter
- `description` (required): One-sentence summary describing the chapter theme
- `stories` (required): Array of Story objects contained in this chapter

---

## Library Functions

### Exported from `src/lib/narratives.ts`

#### `getChapter(chapterId: string): Chapter | undefined`

Retrieves a chapter by its ID.

**Parameters:**
- `chapterId` (string): The unique identifier of the chapter

**Returns:**
- `Chapter | undefined`: The chapter object if found, otherwise `undefined`

**Example:**
```typescript
import { getChapter } from '@/lib/narratives';

const chapter = getChapter('gita_scroll');
if (chapter) {
  console.log(chapter.title); // "Gita Scroll"
  console.log(chapter.stories.length); // 4
}
```

---

#### `getStory(chapterId: string, storyId: string): Story | undefined`

Retrieves a specific story from a chapter.

**Parameters:**
- `chapterId` (string): The chapter's unique identifier
- `storyId` (string): The story's unique identifier

**Returns:**
- `Story | undefined`: The story object if found, otherwise `undefined`

**Example:**
```typescript
import { getStory } from '@/lib/narratives';

const story = getStory('gita_scroll', 'lotus_of_doubt');
if (story) {
  console.log(story.title); // "Lotus of Doubt"
  console.log(story.content); // Full narrative text
}
```

---

#### `chapters: Chapter[]`

An exported array containing all chapters in order.

**Type:** `Chapter[]`

**Example:**
```typescript
import { chapters } from '@/lib/narratives';

// Iterate over all chapters
chapters.forEach(chapter => {
  console.log(`${chapter.title}: ${chapter.stories.length} stories`);
});

// Total story count
const totalStories = chapters.reduce((sum, ch) => sum + ch.stories.length, 0);
```

---

## Component APIs

### AudioPlayer

**File:** `src/components/AudioPlayer.astro`

Renders audio controls for narrative voiceover and ambient soundscapes.

#### Props

```typescript
interface Props {
  narrative?: string;  // Path to narrative audio file
  ambient?: string;    // Path to ambient audio file
}
```

**Props:**
- `narrative` (optional): Relative path to narrative audio (e.g., `'fadein/lotus_of_doubt_fadein.mp3'`)
- `ambient` (optional): Relative path to ambient audio (e.g., `'ambient/lotus_of_doubt_ambient_loop.mp3'`)

**Usage:**
```astro
---
import AudioPlayer from '@/components/AudioPlayer.astro';
---

<AudioPlayer 
  narrative="fadein/lotus_of_doubt_fadein.mp3"
  ambient="ambient/lotus_of_doubt_ambient_loop.mp3"
/>
```

**Accessibility:**
- Uses native HTML5 `<audio>` elements with accessible controls
- Includes descriptive labels for each audio track
- Falls back to informative message if no audio available

---

### NarrativeDisplay

**File:** `src/components/NarrativeDisplay.astro`

Displays a story's illustration, narrative content, and audio player.

#### Props

```typescript
interface Props {
  story: Story;  // Complete Story object
}
```

**Props:**
- `story` (required): A Story object containing all story data

**Usage:**
```astro
---
import NarrativeDisplay from '@/components/NarrativeDisplay.astro';
import { getStory } from '@/lib/narratives';

const story = getStory('gita_scroll', 'lotus_of_doubt');
---

{story && <NarrativeDisplay story={story} />}
```

**Features:**
- Responsive grid layout (1 column mobile, 2 columns desktop)
- SVG illustration with animations
- Meditation text blockquote
- Integrated AudioPlayer component

---

### StoryCard

**File:** `src/components/StoryCard.astro`

Renders a card for story navigation with a link to the story page.

#### Props

```typescript
interface Props {
  story: Story;
  chapterId: string;
  active?: boolean;  // Whether this is the current story
}
```

**Props:**
- `story` (required): The Story object to display
- `chapterId` (required): Parent chapter ID for link generation
- `active` (optional, default: `false`): Highlights card if current story

**Usage:**
```astro
---
import StoryCard from '@/components/StoryCard.astro';
---

<StoryCard 
  story={story}
  chapterId="gita_scroll"
  active={currentStoryId === story.id}
/>
```

---

### ChapterCard

**File:** `src/components/ChapterCard.astro`

Renders a card for chapter navigation with a link to the first story.

#### Props

```typescript
interface Props {
  chapter: Chapter;
}
```

**Props:**
- `chapter` (required): The Chapter object to display

**Usage:**
```astro
---
import ChapterCard from '@/components/ChapterCard.astro';
import { chapters } from '@/lib/narratives';
---

{chapters.map(chapter => (
  <ChapterCard chapter={chapter} />
))}
```

**Features:**
- Displays chapter title and description
- Shows story count
- Links to first story in the chapter

---

### BaseLayout

**File:** `src/layouts/BaseLayout.astro`

Main page layout providing site structure, header, and footer.

#### Props

```typescript
interface Props {
  title?: string;        // Page title (default: "The Scroll of Dharma")
  description?: string;  // Meta description
}
```

**Props:**
- `title` (optional): HTML page title and meta title
- `description` (optional): Meta description for SEO

**Usage:**
```astro
---
import BaseLayout from '@/layouts/BaseLayout.astro';
---

<BaseLayout 
  title="Lotus of Doubt - Gita Scroll | The Scroll of Dharma"
  description="Arjuna freezes on the battle line..."
>
  <slot />
</BaseLayout>
```

**Features:**
- Responsive header with site title
- Parchment background texture
- Google Fonts integration (Cinzel Decorative, EB Garamond, etc.)
- Footer with attribution

---

## Constants and Mappings

### CHAPTER_TITLES

Maps chapter IDs to display titles.

**File:** `src/lib/types.ts`

```typescript
export const CHAPTER_TITLES: Record<string, string> = {
  gita_scroll: "Gita Scroll",
  fall_of_dharma: "Fall of Dharma",
  weapon_quest: "Weapon Quest",
  birth_of_dharma: "Birth of Dharma",
  trials_of_karna: "Trials of Karna",
};
```

---

### STORY_TITLES

Maps story IDs to display titles.

**File:** `src/lib/types.ts`

```typescript
export const STORY_TITLES: Record<string, string> = {
  // Gita Scroll
  lotus_of_doubt: "Lotus of Doubt",
  chakra_of_dharma: "Chakra of Dharma",
  spiral_of_vision: "Spiral of Vision",
  sword_of_resolve: "Sword of Resolve",
  
  // Fall of Dharma
  game_of_fate: "Game of Fate",
  silence_of_protest: "Silence of Protest",
  divine_intervention: "Divine Intervention",
  
  // Weapon Quest
  forest_of_austerity: "Forest of Austerity",
  shiva_and_the_hunter: "Shiva and the Hunter",
  celestial_audience: "Celestial Audience",
  trial_of_heaven: "Trial of Heaven",
  
  // Birth of Dharma
  cosmic_egg: "Cosmic Egg",
  first_flame: "First Flame",
  river_oath: "River Oath",
  wheel_turns: "Wheel Turns",
  balance_restored: "Balance Restored",
  
  // Trials of Karna
  suns_gift: "Sun's Gift",
  brahmin_curse: "Brahmin's Curse",
  friends_vow: "Friend's Vow",
  birth_revealed: "Birth Revealed",
  final_arrow: "Final Arrow",
};
```

---

## Usage Examples

### Creating a New Story

To add a new story to the application:

1. **Add narrative content** in `src/lib/narratives.ts`:

```typescript
const narrativeContent = {
  your_chapter: {
    new_story: `"Your opening quote..."
Full narrative meditation text here.
Multiple paragraphs supported.
Poetic, contemplative tone recommended.`,
  },
};
```

2. **Add SVG asset mapping**:

```typescript
const svgAssets: Record<string, { svg: string; anim: string; alt: string }> = {
  new_story: { 
    svg: 'new_story.svg', 
    anim: 'new-story-animated', 
    alt: 'Descriptive alt text' 
  },
};
```

3. **Add audio assets** (optional):

```typescript
const audioAssets: Record<string, { narrative?: string; ambient?: string }> = {
  new_story: { 
    narrative: 'path/to/narrative.mp3',
    ambient: 'path/to/ambient.mp3'
  },
};
```

4. **Add story title** in `src/lib/types.ts`:

```typescript
export const STORY_TITLES: Record<string, string> = {
  // ... existing stories
  new_story: "New Story Title",
};
```

5. **Update chapter stories array**:

```typescript
export const chapters: Chapter[] = [
  {
    id: 'your_chapter',
    title: CHAPTER_TITLES.your_chapter,
    description: 'Chapter description',
    stories: [
      'existing_story',
      'new_story'  // Add here
    ].map(id => createStory('your_chapter', id)),
  },
];
```

---

### Querying Data in Pages

Example from a dynamic route:

```astro
---
import { getChapter, getStory } from '@/lib/narratives';

const { chapter: chapterId, story: storyId } = Astro.params;

const chapter = getChapter(chapterId);
const story = getStory(chapterId, storyId);

if (!chapter || !story) {
  return Astro.redirect('/404');
}
---

<h1>{chapter.title}</h1>
<h2>{story.title}</h2>
<p>{story.content}</p>
```

---

### Building Navigation

Example of chapter navigation:

```astro
---
import { chapters } from '@/lib/narratives';
import ChapterCard from '@/components/ChapterCard.astro';
---

<div class="grid md:grid-cols-2 gap-6">
  {chapters.map(chapter => (
    <ChapterCard chapter={chapter} />
  ))}
</div>
```

---

## Best Practices

1. **Type Safety**: Always use TypeScript interfaces for type checking
2. **Accessibility**: Include meaningful `alt` text for all SVG assets
3. **Narrative Style**: Maintain poetic, meditative tone in story content
4. **File Naming**: Use snake_case for IDs, descriptive names for files
5. **Audio Paths**: Store audio in `/public/assets/audio/` directory
6. **SVG Assets**: Store illustrations in `/public/assets/svg/` directory

---

## Related Documentation

- **[CONTRIBUTING.md](../CONTRIBUTING.md)** - Contribution guidelines
- **[ACCESSIBILITY_AUDIT.md](../ACCESSIBILITY_AUDIT.md)** - Accessibility standards
- **[ROADMAP_2025-2027.md](../ROADMAP_2025-2027.md)** - Project roadmap
- **[README.md](../README.md)** - Project overview

---

*For questions or contributions, please see our [Contributing Guide](../CONTRIBUTING.md).*
