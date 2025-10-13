# 🚀 Phase 1 Migration Guide: From Streamlit to Next.js

## Overview

This guide provides step-by-step instructions for implementing Phase 1 of the migration roadmap: creating a proof-of-concept Next.js application with one complete chapter from the Scroll of Dharma.

**Timeline**: 3 months (Q1-Q2 2025)  
**Effort**: 120-160 hours  
**Goal**: Working prototype with Gita Scroll chapter

---

## Prerequisites

### Required Knowledge
- Basic JavaScript/TypeScript (can learn as you go)
- React fundamentals (components, props, state)
- Git version control
- Command line basics

### Software Requirements
- Node.js 18+ ([download](https://nodejs.org/))
- npm or yarn (comes with Node.js)
- Git ([download](https://git-scm.com/))
- VS Code or your preferred editor
- Optional: GitHub CLI for easier workflows

### Learning Resources (Before You Start)
1. **JavaScript/TypeScript**:
   - [JavaScript.info](https://javascript.info/) (1-2 weeks)
   - [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html) (3-5 days)

2. **React Basics**:
   - [React Tutorial](https://react.dev/learn) (1 week)
   - Focus on: Components, Props, State, Hooks (useState, useEffect)

3. **Next.js**:
   - [Next.js Tutorial](https://nextjs.org/learn) (3-5 days)
   - Focus on: App Router, Routing, Server Components

---

## Month 1: Project Setup & Architecture

### Week 1: Initialize Next.js Project

#### Step 1: Create Next.js Application
```bash
# Navigate to your workspace
cd ~/projects

# Create new Next.js app
npx create-next-app@latest scroll-of-dharma-next

# Follow prompts:
# ✓ Would you like to use TypeScript? Yes
# ✓ Would you like to use ESLint? Yes
# ✓ Would you like to use Tailwind CSS? Yes
# ✓ Would you like to use `src/` directory? No
# ✓ Would you like to use App Router? Yes
# ✓ Would you like to customize the default import alias? No

cd scroll-of-dharma-next
```

#### Step 2: Install Additional Dependencies
```bash
# Animation library
npm install framer-motion

# Audio library
npm install howler
npm install --save-dev @types/howler

# State management (lightweight)
npm install zustand

# UI components
npm install @radix-ui/react-icons
npm install @radix-ui/react-dropdown-menu
npm install @radix-ui/react-dialog

# Utilities
npm install clsx tailwind-merge

# Development tools
npm install --save-dev prettier eslint-config-prettier
npm install --save-dev husky lint-staged
```

#### Step 3: Project Structure
```bash
# Create directory structure
mkdir -p app/\(main\)/\[chapter\]/\[story\]
mkdir -p components/ui
mkdir -p lib
mkdir -p types
mkdir -p public/assets/{audio,svg,textures,fonts}
```

Final structure:
```
scroll-of-dharma-next/
├── app/
│   ├── (main)/
│   │   ├── page.tsx              # Home page
│   │   └── [chapter]/
│   │       └── [story]/
│   │           └── page.tsx      # Story page
│   ├── layout.tsx                # Root layout
│   └── globals.css
├── components/
│   ├── ui/
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   └── Select.tsx
│   ├── NarrativeDisplay.tsx
│   ├── AudioPlayer.tsx
│   ├── SVGAnimation.tsx
│   ├── ChapterSelector.tsx
│   └── ThemeProvider.tsx
├── lib/
│   ├── narratives.ts             # Converted from narrative.py
│   ├── audio.ts                  # Audio utilities
│   ├── themes.ts                 # Theme configuration
│   └── utils.ts                  # Helper functions
├── types/
│   └── index.ts                  # TypeScript types
├── public/
│   └── assets/
│       ├── audio/
│       ├── svg/
│       ├── textures/
│       └── fonts/
└── package.json
```

### Week 2: Configure Development Environment

#### Step 1: Set Up Prettier
Create `.prettierrc.json`:
```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2
}
```

#### Step 2: Configure ESLint
Update `.eslintrc.json`:
```json
{
  "extends": [
    "next/core-web-vitals",
    "prettier"
  ],
  "rules": {
    "react/no-unescaped-entities": "off",
    "@next/next/no-img-element": "off"
  }
}
```

#### Step 3: Set Up Husky (Git Hooks)
```bash
# Initialize husky
npx husky init

# Create pre-commit hook
echo "npx lint-staged" > .husky/pre-commit
```

Create `.lintstagedrc.json`:
```json
{
  "*.{js,jsx,ts,tsx}": [
    "eslint --fix",
    "prettier --write"
  ],
  "*.{json,md}": [
    "prettier --write"
  ]
}
```

#### Step 4: Configure Tailwind
Update `tailwind.config.ts`:
```typescript
import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        cinzel: ['var(--font-cinzel)', 'serif'],
        eb: ['var(--font-eb-garamond)', 'serif'],
      },
      colors: {
        parchment: {
          50: '#fdfcfb',
          100: '#f8f5f0',
          200: '#f0ebe0',
          300: '#e8dfd0',
        },
      },
    },
  },
  plugins: [],
};
export default config;
```

### Week 3: Type Definitions & Data Migration

#### Step 1: Define TypeScript Types
Create `types/index.ts`:
```typescript
export interface Story {
  id: string;
  title: string;
  displayTitle: string;
  content: string;
  audio?: {
    narrative?: string;
    ambient?: string;
  };
  visual: {
    svgFile: string;
    animationClass?: string;
    altText: string;
  };
  metadata: {
    chapter: string;
    order: number;
  };
}

export interface Chapter {
  id: string;
  title: string;
  description: string;
  theme: Theme;
  stories: Story[];
}

export interface Theme {
  name: string;
  fonts: {
    heading: string;
    body: string;
  };
  colors: {
    primary: string;
    secondary: string;
    accent: string;
  };
  background: {
    texture: string;
    overlay?: string;
  };
}

export interface AudioControls {
  volume: number;
  narrativeEnabled: boolean;
  ambientEnabled: boolean;
  isPlaying: boolean;
}
```

#### Step 2: Convert Narrative Data
Create `lib/narratives.ts`:
```typescript
import { Chapter } from '@/types';

export const chapters: Chapter[] = [
  {
    id: 'gita_scroll',
    title: 'Gita Scroll',
    description: 'Arjuna halts a war, interrogates duty, and chooses how to fight.',
    theme: {
      name: 'ancient',
      fonts: {
        heading: 'Cinzel Decorative',
        body: 'EB Garamond',
      },
      colors: {
        primary: '#4A3728',
        secondary: '#8B7355',
        accent: '#D4A574',
      },
      background: {
        texture: 'ancient_parchment.jpg',
        overlay: 'subtle_grain.png',
      },
    },
    stories: [
      {
        id: 'lotus_of_doubt',
        title: 'The Lotus of Doubt',
        displayTitle: '🪷 The Lotus of Doubt',
        content: `The conch shells fell silent. Across the field of Kurukshetra, two armies stood ready—yet one chariot remained still.

Arjuna lowered his bow.

"Drive forward, Krishna," he said. "I must see those I am meant to kill."

Krishna urged the white horses between the lines. Relatives stood on both sides. Teachers who had shaped Arjuna's hands now waited to fight him. Friends he had trained beside were ready to die by his hand.

Arjuna's fingers went slack. The Gandiva bow fell from his grip.

"What victory can be sweet when bought with their blood?" he whispered. "I will not fight."

Krishna said nothing. He waited. The armies waited. The choice belonged to Arjuna alone.`,
        audio: {
          narrative: '/assets/audio/gita/lotus_of_doubt_mix.mp3',
          ambient: '/assets/audio/gita/ambient.mp3',
        },
        visual: {
          svgFile: 'lotus.svg',
          animationClass: 'lotus-float',
          altText: 'A lotus flower symbolizing doubt and contemplation',
        },
        metadata: {
          chapter: 'gita_scroll',
          order: 1,
        },
      },
      // Add more stories here...
    ],
  },
  // Add more chapters as you migrate them
];

export function getChapterById(id: string): Chapter | undefined {
  return chapters.find((chapter) => chapter.id === id);
}

export function getStoryById(
  chapterId: string,
  storyId: string
): Story | undefined {
  const chapter = getChapterById(chapterId);
  return chapter?.stories.find((story) => story.id === storyId);
}
```

### Week 4: Design System Implementation

#### Step 1: Create Utility Functions
Create `lib/utils.ts`:
```typescript
import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatTitle(title: string): string {
  return title
    .split('_')
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}
```

#### Step 2: Create Base UI Components
Create `components/ui/Button.tsx`:
```tsx
import { ButtonHTMLAttributes, forwardRef } from 'react';
import { cn } from '@/lib/utils';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'default', size = 'md', ...props }, ref) => {
    return (
      <button
        className={cn(
          'inline-flex items-center justify-center rounded-md font-medium transition-colors',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2',
          'disabled:pointer-events-none disabled:opacity-50',
          {
            'bg-primary text-white hover:bg-primary/90': variant === 'default',
            'border border-primary bg-transparent hover:bg-primary/10':
              variant === 'outline',
            'hover:bg-primary/10': variant === 'ghost',
            'h-8 px-3 text-sm': size === 'sm',
            'h-10 px-4': size === 'md',
            'h-12 px-6 text-lg': size === 'lg',
          },
          className
        )}
        ref={ref}
        {...props}
      />
    );
  }
);

Button.displayName = 'Button';

export { Button };
```

---

## Month 2: Core Features Development

### Week 5-6: Chapter Navigation & Layout

#### Step 1: Root Layout
Create `app/layout.tsx`:
```tsx
import type { Metadata } from 'next';
import { Cinzel_Decorative, EB_Garamond } from 'next/font/google';
import './globals.css';

const cinzel = Cinzel_Decorative({
  weight: ['400', '700'],
  subsets: ['latin'],
  variable: '--font-cinzel',
});

const ebGaramond = EB_Garamond({
  weight: ['400', '500', '700'],
  subsets: ['latin'],
  variable: '--font-eb-garamond',
});

export const metadata: Metadata = {
  title: 'The Scroll of Dharma',
  description:
    'An interactive exploration of pivotal moments from ancient epics',
  icons: {
    icon: '/favicon.ico',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${cinzel.variable} ${ebGaramond.variable}`}>
      <body className="font-eb antialiased">{children}</body>
    </html>
  );
}
```

#### Step 2: Home Page
Create `app/(main)/page.tsx`:
```tsx
import Link from 'next/link';
import { chapters } from '@/lib/narratives';
import { Button } from '@/components/ui/Button';

export default function HomePage() {
  return (
    <main className="min-h-screen bg-parchment-100">
      <div className="container mx-auto px-4 py-16">
        <header className="text-center mb-16">
          <h1 className="font-cinzel text-5xl md:text-7xl font-bold mb-4 text-primary">
            🕉️ The Scroll of Dharma
          </h1>
          <p className="text-xl text-secondary italic">
            "Dharma is not a rule. It is a rhythm."
          </p>
        </header>

        <section className="max-w-4xl mx-auto">
          <h2 className="font-cinzel text-3xl font-bold mb-8 text-center">
            Choose Your Chapter
          </h2>
          
          <div className="grid gap-6 md:grid-cols-2">
            {chapters.map((chapter) => (
              <Link
                key={chapter.id}
                href={`/${chapter.id}/${chapter.stories[0]?.id || ''}`}
                className="block"
              >
                <div className="p-6 bg-white rounded-lg shadow-md hover:shadow-xl transition-shadow border border-primary/20">
                  <h3 className="font-cinzel text-2xl font-bold mb-2 text-primary">
                    {chapter.title}
                  </h3>
                  <p className="text-secondary">{chapter.description}</p>
                  <div className="mt-4 text-accent font-medium">
                    {chapter.stories.length} Stories →
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}
```

### Week 7-8: Story Display & Audio Player

#### Step 1: Story Page
Create `app/(main)/[chapter]/[story]/page.tsx`:
```tsx
import { notFound } from 'next/navigation';
import { getChapterById, getStoryById } from '@/lib/narratives';
import NarrativeDisplay from '@/components/NarrativeDisplay';
import AudioPlayer from '@/components/AudioPlayer';
import SVGAnimation from '@/components/SVGAnimation';

interface StoryPageProps {
  params: {
    chapter: string;
    story: string;
  };
}

export default function StoryPage({ params }: StoryPageProps) {
  const chapter = getChapterById(params.chapter);
  const story = getStoryById(params.chapter, params.story);

  if (!chapter || !story) {
    notFound();
  }

  return (
    <main
      className="min-h-screen"
      style={{
        backgroundImage: `url(/assets/textures/${chapter.theme.background.texture})`,
        backgroundSize: 'cover',
        backgroundAttachment: 'fixed',
      }}
    >
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-8">
          <h1 className="font-cinzel text-4xl font-bold text-primary">
            {chapter.title}
          </h1>
          <h2 className="text-2xl mt-2 text-secondary">{story.displayTitle}</h2>
        </header>

        <div className="grid lg:grid-cols-2 gap-8 max-w-6xl mx-auto">
          <div className="order-2 lg:order-1">
            <NarrativeDisplay story={story} />
          </div>

          <div className="order-1 lg:order-2">
            <SVGAnimation
              svgFile={story.visual.svgFile}
              animationClass={story.visual.animationClass}
              altText={story.visual.altText}
            />
          </div>
        </div>

        {story.audio && (
          <div className="mt-8 max-w-2xl mx-auto">
            <AudioPlayer audio={story.audio} />
          </div>
        )}
      </div>
    </main>
  );
}
```

#### Step 2: Narrative Display Component
Create `components/NarrativeDisplay.tsx`:
```tsx
'use client';

import { motion } from 'framer-motion';
import { Story } from '@/types';

interface NarrativeDisplayProps {
  story: Story;
}

export default function NarrativeDisplay({ story }: NarrativeDisplayProps) {
  const paragraphs = story.content.split('\n\n');

  return (
    <motion.article
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="bg-white/90 backdrop-blur-sm p-8 rounded-lg shadow-xl"
    >
      <div className="prose prose-lg max-w-none">
        {paragraphs.map((paragraph, index) => (
          <motion.p
            key={index}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: index * 0.1 }}
            className="mb-4 text-gray-800 leading-relaxed"
          >
            {paragraph}
          </motion.p>
        ))}
      </div>
    </motion.article>
  );
}
```

#### Step 3: Audio Player Component
Create `components/AudioPlayer.tsx`:
```tsx
'use client';

import { useState, useEffect, useRef } from 'react';
import { Howl } from 'howler';

interface AudioPlayerProps {
  audio: {
    narrative?: string;
    ambient?: string;
  };
}

export default function AudioPlayer({ audio }: AudioPlayerProps) {
  const [narrativePlaying, setNarrativePlaying] = useState(false);
  const [ambientPlaying, setAmbientPlaying] = useState(false);
  const narrativeRef = useRef<Howl | null>(null);
  const ambientRef = useRef<Howl | null>(null);

  useEffect(() => {
    if (audio.narrative) {
      narrativeRef.current = new Howl({
        src: [audio.narrative],
        html5: true,
      });
    }

    if (audio.ambient) {
      ambientRef.current = new Howl({
        src: [audio.ambient],
        html5: true,
        loop: true,
        volume: 0.5,
      });
    }

    return () => {
      narrativeRef.current?.unload();
      ambientRef.current?.unload();
    };
  }, [audio]);

  const toggleNarrative = () => {
    if (!narrativeRef.current) return;

    if (narrativePlaying) {
      narrativeRef.current.pause();
    } else {
      narrativeRef.current.play();
    }
    setNarrativePlaying(!narrativePlaying);
  };

  const toggleAmbient = () => {
    if (!ambientRef.current) return;

    if (ambientPlaying) {
      ambientRef.current.pause();
    } else {
      ambientRef.current.play();
    }
    setAmbientPlaying(!ambientPlaying);
  };

  return (
    <div className="bg-white/90 backdrop-blur-sm p-6 rounded-lg shadow-xl">
      <h3 className="font-cinzel text-xl font-bold mb-4 text-primary">
        Sacred Soundscape
      </h3>
      
      <div className="flex gap-4">
        {audio.narrative && (
          <button
            onClick={toggleNarrative}
            className="flex-1 px-4 py-2 bg-primary text-white rounded-md hover:bg-primary/90 transition-colors"
          >
            {narrativePlaying ? '⏸ Pause' : '▶ Play'} Narrative
          </button>
        )}
        
        {audio.ambient && (
          <button
            onClick={toggleAmbient}
            className="flex-1 px-4 py-2 bg-secondary text-white rounded-md hover:bg-secondary/90 transition-colors"
          >
            {ambientPlaying ? '🔇 Mute' : '🔊 Play'} Ambient
          </button>
        )}
      </div>
    </div>
  );
}
```

---

## Month 3: POC Completion & Deployment

### Week 9: SVG Animations

Create `components/SVGAnimation.tsx`:
```tsx
'use client';

import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';

interface SVGAnimationProps {
  svgFile: string;
  animationClass?: string;
  altText: string;
}

export default function SVGAnimation({
  svgFile,
  animationClass,
  altText,
}: SVGAnimationProps) {
  const [svgContent, setSvgContent] = useState<string>('');

  useEffect(() => {
    fetch(`/assets/svg/${svgFile}`)
      .then((res) => res.text())
      .then(setSvgContent);
  }, [svgFile]);

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.8 }}
      className={`flex items-center justify-center p-8 ${animationClass || ''}`}
    >
      <div
        className="w-full max-w-md"
        dangerouslySetInnerHTML={{ __html: svgContent }}
        aria-label={altText}
      />
    </motion.div>
  );
}
```

### Week 10: Testing & Optimization

#### Step 1: Install Testing Tools
```bash
npm install --save-dev @testing-library/react @testing-library/jest-dom jest jest-environment-jsdom
npm install --save-dev @playwright/test
```

#### Step 2: Write Basic Tests
Create `__tests__/narratives.test.ts`:
```typescript
import { getChapterById, getStoryById } from '@/lib/narratives';

describe('Narratives', () => {
  it('should get chapter by id', () => {
    const chapter = getChapterById('gita_scroll');
    expect(chapter).toBeDefined();
    expect(chapter?.title).toBe('Gita Scroll');
  });

  it('should get story by id', () => {
    const story = getStoryById('gita_scroll', 'lotus_of_doubt');
    expect(story).toBeDefined();
    expect(story?.title).toBe('The Lotus of Doubt');
  });
});
```

### Week 11-12: Deployment

#### Step 1: Copy Assets
```bash
# Copy assets from original project
cp -r ../scroll-of-dharma/assets/* public/assets/
```

#### Step 2: Optimize Images
```bash
# Install sharp for image optimization
npm install sharp

# Next.js will automatically optimize images at build time
```

#### Step 3: Deploy to Vercel
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# Production deployment
vercel --prod
```

---

## Success Checklist

### Functionality
- [ ] Home page displays all chapters
- [ ] Can navigate to story pages
- [ ] Narratives display correctly with formatting
- [ ] SVG animations load and display
- [ ] Audio players work (play/pause)
- [ ] Theme applies correctly per chapter
- [ ] Mobile responsive design

### Performance
- [ ] Lighthouse score > 90 (Performance)
- [ ] First Contentful Paint < 2s
- [ ] Time to Interactive < 3s
- [ ] No console errors

### Code Quality
- [ ] No TypeScript errors
- [ ] No ESLint warnings
- [ ] Code formatted with Prettier
- [ ] Basic tests passing

### Deployment
- [ ] Successfully deployed to Vercel
- [ ] Assets loading correctly
- [ ] No 404 errors
- [ ] Works on mobile devices

---

## Common Issues & Solutions

### Issue: SVG Not Loading
**Solution**: Check file path and ensure SVG is in `public/assets/svg/`

### Issue: Audio Not Playing
**Solution**: Verify audio format (MP3) and check browser console for errors

### Issue: Slow Build Times
**Solution**: Optimize images, check bundle size with `next build --profile`

### Issue: TypeScript Errors
**Solution**: Run `npm run type-check` and fix type issues incrementally

---

## Next Steps

After completing Phase 1:
1. Gather user feedback on POC
2. Measure performance metrics
3. Plan Phase 2: Full migration
4. Document lessons learned
5. Update roadmap based on learnings

---

**Document Version**: 1.0  
**Last Updated**: January 2025  
**Status**: Ready for Implementation
