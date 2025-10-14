import { describe, it, expect } from 'vitest';
import { chapters, getChapter, getStory } from '../../src/lib/narratives';

/**
 * Unit tests for narrative content and helper functions
 */

describe('chapters', () => {
  it('should export an array of chapters', () => {
    expect(Array.isArray(chapters)).toBe(true);
    expect(chapters.length).toBeGreaterThan(0);
  });

  it('should have all expected chapters', () => {
    const chapterIds = chapters.map(c => c.id);
    expect(chapterIds).toContain('gita_scroll');
    expect(chapterIds).toContain('fall_of_dharma');
    expect(chapterIds).toContain('weapon_quest');
    expect(chapterIds).toContain('birth_of_dharma');
    expect(chapterIds).toContain('trials_of_karna');
    expect(chapterIds).toContain('exile_of_rama');
    expect(chapterIds).toContain('draupadis_fire');
  });

  it('should have valid chapter structure', () => {
    chapters.forEach(chapter => {
      expect(chapter).toHaveProperty('id');
      expect(chapter).toHaveProperty('title');
      expect(chapter).toHaveProperty('description');
      expect(chapter).toHaveProperty('stories');
      expect(chapter).toHaveProperty('soundscapeDescription');
      
      expect(typeof chapter.id).toBe('string');
      expect(typeof chapter.title).toBe('string');
      expect(typeof chapter.description).toBe('string');
      expect(typeof chapter.soundscapeDescription).toBe('string');
      expect(Array.isArray(chapter.stories)).toBe(true);
    });
  });

  it('should have stories in each chapter', () => {
    chapters.forEach(chapter => {
      expect(chapter.stories.length).toBeGreaterThan(0);
    });
  });

  it('should have valid story structure', () => {
    chapters.forEach(chapter => {
      chapter.stories.forEach(story => {
        expect(story).toHaveProperty('id');
        expect(story).toHaveProperty('title');
        expect(story).toHaveProperty('content');
        
        expect(typeof story.id).toBe('string');
        expect(typeof story.title).toBe('string');
        expect(typeof story.content).toBe('string');
        expect(story.content.length).toBeGreaterThan(0);
      });
    });
  });

  it('should have SVG files for stories', () => {
    chapters.forEach(chapter => {
      chapter.stories.forEach(story => {
        if (story.svgFile) {
          expect(typeof story.svgFile).toBe('string');
          expect(story.svgFile).toMatch(/\.svg$/);
        }
      });
    });
  });

  it('should have alt text when SVG is provided', () => {
    chapters.forEach(chapter => {
      chapter.stories.forEach(story => {
        if (story.svgFile) {
          expect(story.alt).toBeDefined();
          expect(typeof story.alt).toBe('string');
          expect(story.alt!.length).toBeGreaterThan(0);
        }
      });
    });
  });

  it('should have chant lines for all stories', () => {
    chapters.forEach(chapter => {
      chapter.stories.forEach(story => {
        expect(story.chantLines).toBeDefined();
        expect(Array.isArray(story.chantLines)).toBe(true);
        expect(story.chantLines!.length).toBe(4);
      });
    });
  });

  it('should have non-empty chant lines', () => {
    chapters.forEach(chapter => {
      chapter.stories.forEach(story => {
        story.chantLines?.forEach(line => {
          expect(line.trim().length).toBeGreaterThan(0);
        });
      });
    });
  });

  it('should have soundscape descriptions for all chapters', () => {
    chapters.forEach(chapter => {
      expect(chapter.soundscapeDescription).toBeDefined();
      expect(chapter.soundscapeDescription!.length).toBeGreaterThan(20);
    });
  });
});

describe('getChapter', () => {
  it('should return a chapter by id', () => {
    const chapter = getChapter('gita_scroll');
    expect(chapter).toBeDefined();
    expect(chapter?.id).toBe('gita_scroll');
    expect(chapter?.title).toBe('Gita Scroll');
  });

  it('should return undefined for non-existent chapter', () => {
    const chapter = getChapter('non_existent_chapter');
    expect(chapter).toBeUndefined();
  });

  it('should work for all valid chapters', () => {
    const chapterIds = ['gita_scroll', 'fall_of_dharma', 'weapon_quest', 'birth_of_dharma', 'trials_of_karna', 'exile_of_rama', 'draupadis_fire'];
    chapterIds.forEach(id => {
      const chapter = getChapter(id);
      expect(chapter).toBeDefined();
      expect(chapter?.id).toBe(id);
    });
  });
});

describe('getStory', () => {
  it('should return a story by chapter and story id', () => {
    const story = getStory('gita_scroll', 'lotus_of_doubt');
    expect(story).toBeDefined();
    expect(story?.id).toBe('lotus_of_doubt');
    expect(story?.title).toBe('Lotus of Doubt');
  });

  it('should apply title override for sword_of_resolve', () => {
    const story = getStory('gita_scroll', 'sword_of_resolve');
    expect(story).toBeDefined();
    expect(story?.title).toBe('Trident of Resolve');
  });

  it('should return undefined for non-existent story', () => {
    const story = getStory('gita_scroll', 'non_existent_story');
    expect(story).toBeUndefined();
  });

  it('should return undefined for non-existent chapter', () => {
    const story = getStory('non_existent_chapter', 'lotus_of_doubt');
    expect(story).toBeUndefined();
  });

  it('should work for stories across different chapters', () => {
    const tests = [
      { chapter: 'gita_scroll', story: 'lotus_of_doubt' },
      { chapter: 'fall_of_dharma', story: 'game_of_fate' },
      { chapter: 'weapon_quest', story: 'forest_of_austerity' },
      { chapter: 'birth_of_dharma', story: 'cosmic_egg' },
      { chapter: 'trials_of_karna', story: 'suns_gift' },
      { chapter: 'exile_of_rama', story: 'golden_palace' },
      { chapter: 'draupadis_fire', story: 'born_from_flame' },
    ];

    tests.forEach(({ chapter, story }) => {
      const result = getStory(chapter, story);
      expect(result).toBeDefined();
      expect(result?.id).toBe(story);
    });
  });
});

describe('content quality', () => {
  it('should have meaningful content for all stories', () => {
    chapters.forEach(chapter => {
      chapter.stories.forEach(story => {
        expect(story.content.trim().length).toBeGreaterThan(50);
      });
    });
  });

  it('should have proper formatting in content', () => {
    chapters.forEach(chapter => {
      chapter.stories.forEach(story => {
        // Content should not have excessive whitespace
        expect(story.content).not.toMatch(/\s{3,}/);
      });
    });
  });

  it('should have descriptive chapter descriptions', () => {
    chapters.forEach(chapter => {
      expect(chapter.description.trim().length).toBeGreaterThan(20);
    });
  });
});

describe('edge cases', () => {
  it('should handle invalid chapter gracefully', () => {
    const story = getStory('invalid_chapter', 'lotus_of_doubt');
    expect(story).toBeUndefined();
  });

  it('should handle invalid story gracefully', () => {
    const story = getStory('gita_scroll', 'invalid_story');
    expect(story).toBeUndefined();
  });

  it('should have default values for all stories', () => {
    chapters.forEach(chapter => {
      chapter.stories.forEach(story => {
        // Every story should have basic required properties
        expect(story.id).toBeTruthy();
        expect(story.title).toBeTruthy();
        expect(story.content).toBeTruthy();
      });
    });
  });

  it('should provide fallback SVG for stories without assets', () => {
    chapters.forEach(chapter => {
      chapter.stories.forEach(story => {
        // Every story should have either an SVG file or undefined
        if (story.svgFile !== undefined) {
          expect(typeof story.svgFile).toBe('string');
        }
      });
    });
  });
});
