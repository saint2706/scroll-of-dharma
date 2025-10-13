# ✅ Quick Start Checklist: Begin Migration Today

This checklist helps you start the migration from Streamlit to Next.js immediately. Follow these steps in order.

---

## 🎯 Phase 0: Decision & Planning (1-2 days)

### Day 1: Understand the Strategy
- [ ] Read [Executive Summary](./EXECUTIVE_SUMMARY.md) (10 minutes)
- [ ] Review [Deployment Comparison](./DEPLOYMENT_COMPARISON.md) (15 minutes)
- [ ] Skim [Deployment Roadmap](../DEPLOYMENT_ROADMAP.md) (20 minutes)
- [ ] Check [Visual Timeline](./VISUAL_TIMELINE.md) for overview
- [ ] Make decision: Proceed with migration? YES/NO

### Day 2: Assess Resources
- [ ] Determine if DIY or hiring contractor
- [ ] Identify available time/budget
- [ ] Set up project tracking (GitHub Projects/Trello)
- [ ] Create timeline spreadsheet
- [ ] Assign responsibilities (if team)

**Decision Point**: If YES to migration, continue below ↓

---

## 📚 Week 1: Learning Prerequisites (if needed)

### If New to JavaScript/TypeScript
- [ ] Complete [JavaScript.info](https://javascript.info/) basics (10-15 hours)
  - Variables, functions, arrays, objects
  - Promises and async/await
  - ES6+ features (arrow functions, destructuring, spread)
- [ ] Watch [TypeScript for Beginners](https://www.youtube.com/watch?v=BwuLxPH8IDs) (1 hour)
- [ ] Practice: Convert 1-2 Python functions to TypeScript

### If New to React
- [ ] Complete [React Tutorial](https://react.dev/learn/tutorial-tic-tac-toe) (2-3 hours)
- [ ] Study React Hooks: [useState](https://react.dev/reference/react/useState) & [useEffect](https://react.dev/reference/react/useEffect) (1 hour)
- [ ] Build simple counter app for practice (1 hour)

### If New to Next.js
- [ ] Watch [Next.js 14 Tutorial](https://www.youtube.com/results?search_query=nextjs+14+tutorial) (2 hours)
- [ ] Read [Next.js App Router docs](https://nextjs.org/docs/app) (2 hours)
- [ ] Create a "Hello World" Next.js app (1 hour)

**Total Learning Time**: 20-30 hours over 1-2 weeks (if starting from scratch)

**Skip this section if already familiar with React/Next.js**

---

## 🛠️ Week 2: Environment Setup (1-2 days)

### Install Required Software
- [ ] Install Node.js 18+ ([download](https://nodejs.org/))
  ```bash
  node --version  # Should be 18.x or higher
  npm --version   # Should be 9.x or higher
  ```
- [ ] Install Git ([download](https://git-scm.com/))
  ```bash
  git --version
  ```
- [ ] Install VS Code ([download](https://code.visualstudio.com/))
- [ ] Install VS Code extensions:
  - [ ] ESLint
  - [ ] Prettier
  - [ ] TypeScript and JavaScript Language Features
  - [ ] Tailwind CSS IntelliSense
  - [ ] ES7+ React/Redux/React-Native snippets

### Set Up Project Repository
- [ ] Create new directory: `scroll-of-dharma-next`
- [ ] Initialize Git repository
  ```bash
  mkdir scroll-of-dharma-next
  cd scroll-of-dharma-next
  git init
  ```
- [ ] Create GitHub repository (public or private)
- [ ] Connect local to GitHub
  ```bash
  git remote add origin YOUR_GITHUB_URL
  ```

### Create Next.js Project
- [ ] Run create-next-app
  ```bash
  npx create-next-app@latest . --typescript --tailwind --app --eslint
  ```
- [ ] Answer prompts:
  - TypeScript: **Yes**
  - ESLint: **Yes**
  - Tailwind CSS: **Yes**
  - src/ directory: **No**
  - App Router: **Yes**
  - Import alias: **No** (or @/*)
- [ ] Verify installation
  ```bash
  npm run dev
  ```
- [ ] Open http://localhost:3000 - should see Next.js welcome page
- [ ] Stop the dev server (Ctrl+C)

### Install Additional Dependencies
```bash
# Animation
npm install framer-motion

# Audio
npm install howler
npm install --save-dev @types/howler

# State management
npm install zustand

# UI components
npm install @radix-ui/react-icons
npm install @radix-ui/react-dropdown-menu
npm install @radix-ui/react-dialog

# Utilities
npm install clsx tailwind-merge

# Dev tools
npm install --save-dev prettier eslint-config-prettier
npm install --save-dev husky lint-staged
```

- [ ] Verify package.json has all dependencies
- [ ] Run `npm install` to ensure everything installed
- [ ] Initial git commit
  ```bash
  git add .
  git commit -m "Initial Next.js setup with dependencies"
  git push -u origin main
  ```

---

## 📁 Week 3: Project Structure (1 day)

### Create Directory Structure
```bash
# Main directories
mkdir -p app/\(main\)/\[chapter\]/\[story\]
mkdir -p components/ui
mkdir -p lib
mkdir -p types
mkdir -p public/assets/{audio,svg,textures,fonts}
mkdir -p __tests__

# Verify structure
tree -L 3 -d  # or use ls -R if tree not available
```

### Copy Assets from Original Project
```bash
# Assuming original project is at ../scroll-of-dharma
cp -r ../scroll-of-dharma/assets/svg/* public/assets/svg/
cp -r ../scroll-of-dharma/assets/textures/* public/assets/textures/
cp -r ../scroll-of-dharma/assets/fonts/* public/assets/fonts/
cp -r ../scroll-of-dharma/assets/audio/gita/* public/assets/audio/gita/

# Verify files copied
ls -lh public/assets/svg/
ls -lh public/assets/textures/
```

### Set Up Configuration Files

**Create `.prettierrc.json`:**
```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2
}
```

**Update `.eslintrc.json`:**
```json
{
  "extends": ["next/core-web-vitals", "prettier"],
  "rules": {
    "react/no-unescaped-entities": "off"
  }
}
```

**Create `.gitignore` additions:**
```
# Next.js
.next/
out/
.vercel

# Testing
coverage/

# Local
.DS_Store
*.local
```

- [ ] Commit configuration
  ```bash
  git add .
  git commit -m "Add project structure and configuration"
  git push
  ```

---

## 💻 Week 4: First Component (2-3 days)

### Create Type Definitions
**Create `types/index.ts`:**
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
  stories: Story[];
}
```

### Migrate One Story Data
**Create `lib/narratives.ts`:**
```typescript
import { Chapter } from '@/types';

export const chapters: Chapter[] = [
  {
    id: 'gita_scroll',
    title: 'Gita Scroll',
    description: 'Arjuna halts a war, interrogates duty, and chooses how to fight.',
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
      // Add more stories here as you migrate
    ],
  },
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

### Create First Component
**Create `components/NarrativeDisplay.tsx`:**
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

### Create Simple Page
**Update `app/page.tsx`:**
```tsx
import Link from 'next/link';
import { chapters } from '@/lib/narratives';

export default function HomePage() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-amber-50 to-orange-50 p-8">
      <div className="container mx-auto max-w-4xl">
        <h1 className="text-5xl font-bold text-center mb-8 text-amber-900">
          🕉️ The Scroll of Dharma
        </h1>
        <p className="text-center text-xl mb-12 italic text-amber-700">
          "Dharma is not a rule. It is a rhythm."
        </p>
        
        <div className="grid gap-6">
          {chapters.map((chapter) => (
            <Link
              key={chapter.id}
              href={`/${chapter.id}/${chapter.stories[0]?.id}`}
              className="block p-6 bg-white rounded-lg shadow-md hover:shadow-xl transition-shadow"
            >
              <h2 className="text-2xl font-bold mb-2 text-amber-900">
                {chapter.title}
              </h2>
              <p className="text-gray-700">{chapter.description}</p>
            </Link>
          ))}
        </div>
      </div>
    </main>
  );
}
```

- [ ] Test in browser
  ```bash
  npm run dev
  ```
- [ ] Verify home page displays
- [ ] Click chapter link (will 404 - that's OK for now)
- [ ] Commit progress
  ```bash
  git add .
  git commit -m "Add types, narratives, and first component"
  git push
  ```

---

## 🎨 Week 5-6: Core Features (1-2 weeks)

Follow the detailed guide in [Migration Guide Phase 1](./MIGRATION_GUIDE_PHASE1.md) sections:
- Week 5-6: Chapter Navigation & Layout
- Week 7-8: Story Display & Audio Player

### Key Tasks:
- [ ] Create story page with dynamic routing
- [ ] Implement narrative display
- [ ] Add audio player component
- [ ] Add SVG animation component
- [ ] Style with Tailwind CSS
- [ ] Test on mobile

---

## 🚀 Week 7-8: Deploy & Optimize (1 week)

### Testing
- [ ] Write basic tests
  ```bash
  npm install --save-dev @testing-library/react @testing-library/jest-dom jest
  npm test
  ```
- [ ] Test on different browsers (Chrome, Firefox, Safari)
- [ ] Test on mobile devices
- [ ] Check for console errors

### Performance Optimization
- [ ] Run Lighthouse audit
  ```bash
  npm run build
  npm start
  # Then run Lighthouse in Chrome DevTools
  ```
- [ ] Optimize images (Next.js does this automatically)
- [ ] Check bundle size
- [ ] Target: Lighthouse score > 90

### Deploy to Vercel
- [ ] Install Vercel CLI
  ```bash
  npm i -g vercel
  ```
- [ ] Login to Vercel
  ```bash
  vercel login
  ```
- [ ] Deploy
  ```bash
  vercel
  ```
- [ ] Test production URL
- [ ] Production deploy
  ```bash
  vercel --prod
  ```

### Share & Gather Feedback
- [ ] Share link with 5-10 people
- [ ] Collect feedback
- [ ] Create GitHub issues for improvements
- [ ] Measure metrics (Lighthouse, load time, user feedback)

---

## ✅ Phase 1 Complete Checklist

### Functionality
- [ ] Home page displays chapter
- [ ] Can navigate to story page
- [ ] Narrative displays with formatting
- [ ] SVG loads and displays
- [ ] Audio player works (play/pause)
- [ ] Mobile responsive

### Performance
- [ ] Lighthouse Performance > 90
- [ ] Lighthouse Accessibility > 90
- [ ] Lighthouse Best Practices > 90
- [ ] Lighthouse SEO > 90
- [ ] First Contentful Paint < 2s
- [ ] Time to Interactive < 3s

### Code Quality
- [ ] No TypeScript errors (`npm run build`)
- [ ] No ESLint warnings (`npm run lint`)
- [ ] Code formatted (`npx prettier --check .`)
- [ ] Basic tests passing (`npm test`)

### Deployment
- [ ] Deployed to Vercel
- [ ] Production URL works
- [ ] Assets loading correctly
- [ ] No 404 errors
- [ ] Works on mobile

---

## 🎉 Success! What's Next?

### Immediate (Week 9-10)
- [ ] Document lessons learned
- [ ] Update roadmap based on experience
- [ ] Decide: Continue to Phase 2?

### If Continuing to Phase 2
- [ ] Review [Deployment Roadmap](../DEPLOYMENT_ROADMAP.md) Phase 2
- [ ] Migrate remaining 4 chapters
- [ ] Implement PWA features
- [ ] Add analytics
- [ ] Optimize all assets

### If Pausing
- [ ] Keep POC deployed as demo
- [ ] Maintain Streamlit version
- [ ] Schedule review in 1-3 months

---

## 📞 Need Help?

### Resources
- **Next.js Docs**: https://nextjs.org/docs
- **React Docs**: https://react.dev
- **TypeScript Docs**: https://www.typescriptlang.org/docs
- **Tailwind Docs**: https://tailwindcss.com/docs

### Community
- **Next.js Discord**: https://nextjs.org/discord
- **Stack Overflow**: Tag [next.js] or [reactjs]
- **GitHub Discussions**: For this project

### Common Issues
- **"Module not found"**: Run `npm install`
- **Port 3000 in use**: Stop other processes or use `npm run dev -- -p 3001`
- **TypeScript errors**: Check [Migration Guide](./MIGRATION_GUIDE_PHASE1.md) troubleshooting
- **Slow build**: Normal for first build; subsequent builds are faster

---

## 📊 Track Your Progress

### Time Tracking Template
```
Week 1:  Learning         [_____] Hours: ____ / Target: 20-30
Week 2:  Setup            [_____] Hours: ____ / Target: 8-16
Week 3:  Structure        [_____] Hours: ____ / Target: 8-12
Week 4:  First Component  [_____] Hours: ____ / Target: 16-24
Week 5-6: Core Features   [_____] Hours: ____ / Target: 40-60
Week 7-8: Deploy          [_____] Hours: ____ / Target: 16-24
                          ─────────────────────────────────
Total:                              ____ / Target: 120-160
```

### Milestone Tracker
```
✅ Environment setup complete      Date: __________
✅ First page renders              Date: __________
✅ Navigation working              Date: __________
✅ Audio playing                   Date: __________
✅ Lighthouse > 90                 Date: __________
✅ Deployed to Vercel              Date: __________
✅ Positive user feedback          Date: __________
🎯 PHASE 1 COMPLETE!               Date: __________
```

---

**Last Updated**: January 2025  
**Status**: Ready to use  
**Estimated Time**: 8-12 weeks (including learning)  
**Difficulty**: Moderate (beginner-friendly with guides)

🚀 **Start today! Your journey awaits.**
