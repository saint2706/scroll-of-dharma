import { describe, it, expect } from 'vitest';
import { CHAPTER_TITLES, STORY_TITLES, CHANT_LINES, SOUNDSCAPE_DESCRIPTIONS } from '../../src/lib/types';

/**
 * Unit tests for type definitions and constants
 */

describe('CHAPTER_TITLES', () => {
  it('should have all expected chapters', () => {
    const expectedChapters = [
      'gita_scroll',
      'fall_of_dharma',
      'weapon_quest',
      'birth_of_dharma',
      'trials_of_karna',
    ];

    expectedChapters.forEach(chapter => {
      expect(CHAPTER_TITLES).toHaveProperty(chapter);
      expect(typeof CHAPTER_TITLES[chapter]).toBe('string');
      expect(CHAPTER_TITLES[chapter].length).toBeGreaterThan(0);
    });
  });

  it('should have human-readable titles', () => {
    expect(CHAPTER_TITLES.gita_scroll).toBe('Gita Scroll');
    expect(CHAPTER_TITLES.fall_of_dharma).toBe('Fall of Dharma');
    expect(CHAPTER_TITLES.weapon_quest).toBe('Weapon Quest');
    expect(CHAPTER_TITLES.birth_of_dharma).toBe('Birth of Dharma');
    expect(CHAPTER_TITLES.trials_of_karna).toBe('Trials of Karna');
  });

  it('should not have empty titles', () => {
    Object.values(CHAPTER_TITLES).forEach(title => {
      expect(title.trim()).not.toBe('');
    });
  });
});

describe('STORY_TITLES', () => {
  it('should have all Gita Scroll stories', () => {
    const gitaStories = ['lotus_of_doubt', 'chakra_of_dharma', 'spiral_of_vision', 'sword_of_resolve'];
    gitaStories.forEach(story => {
      expect(STORY_TITLES).toHaveProperty(story);
      expect(typeof STORY_TITLES[story]).toBe('string');
    });
  });

  it('should have all Fall of Dharma stories', () => {
    const fallStories = ['game_of_fate', 'silence_of_protest', 'divine_intervention'];
    fallStories.forEach(story => {
      expect(STORY_TITLES).toHaveProperty(story);
    });
  });

  it('should have all Weapon Quest stories', () => {
    const weaponStories = [
      'forest_of_austerity',
      'shiva_and_the_hunter',
      'celestial_audience',
      'trial_of_heaven'
    ];
    weaponStories.forEach(story => {
      expect(STORY_TITLES).toHaveProperty(story);
    });
  });

  it('should have all Birth of Dharma stories', () => {
    const birthStories = [
      'cosmic_egg',
      'first_flame',
      'river_oath',
      'wheel_turns',
      'balance_restored'
    ];
    birthStories.forEach(story => {
      expect(STORY_TITLES).toHaveProperty(story);
    });
  });

  it('should have all Trials of Karna stories', () => {
    const karnaStories = [
      'suns_gift',
      'brahmin_curse',
      'friends_vow',
      'birth_revealed',
      'final_arrow'
    ];
    karnaStories.forEach(story => {
      expect(STORY_TITLES).toHaveProperty(story);
    });
  });

  it('should have formatted titles with proper capitalization', () => {
    expect(STORY_TITLES.lotus_of_doubt).toBe('Lotus of Doubt');
    expect(STORY_TITLES.suns_gift).toBe("Sun's Gift");
    expect(STORY_TITLES.brahmin_curse).toBe("Brahmin's Curse");
  });

  it('should not have empty story titles', () => {
    Object.values(STORY_TITLES).forEach(title => {
      expect(title.trim()).not.toBe('');
    });
  });

  it('should have at least 21 stories total', () => {
    const totalStories = Object.keys(STORY_TITLES).length;
    expect(totalStories).toBeGreaterThanOrEqual(21);
  });

  it('should have title override for sword_of_resolve', () => {
    // From ui_constants.py STORY_DISPLAY_TITLES
    expect(STORY_TITLES.sword_of_resolve).toBe('Trident of Resolve');
  });
});

describe('CHANT_LINES', () => {
  it('should have chant lines for all stories', () => {
    const allStoryIds = Object.keys(STORY_TITLES);
    allStoryIds.forEach(storyId => {
      expect(CHANT_LINES).toHaveProperty(storyId);
      expect(Array.isArray(CHANT_LINES[storyId])).toBe(true);
      expect(CHANT_LINES[storyId].length).toBeGreaterThan(0);
    });
  });

  it('should have exactly 4 chant lines per story', () => {
    Object.values(CHANT_LINES).forEach(lines => {
      expect(lines.length).toBe(4);
    });
  });

  it('should have non-empty chant lines', () => {
    Object.values(CHANT_LINES).forEach(lines => {
      lines.forEach(line => {
        expect(line.trim()).not.toBe('');
      });
    });
  });

  it('should have correct chants for specific stories', () => {
    expect(CHANT_LINES.lotus_of_doubt[0]).toBe('Om Shanti Shanti Shanti');
    expect(CHANT_LINES.chakra_of_dharma[0]).toBe('Om Namo Bhagavate Vasudevaya');
    expect(CHANT_LINES.shiva_and_the_hunter[0]).toBe('Om Namah Shivaya');
    expect(CHANT_LINES.suns_gift[0]).toBe('Om Suryaya Namah');
  });
});

describe('SOUNDSCAPE_DESCRIPTIONS', () => {
  it('should have descriptions for all chapters', () => {
    const allChapters = Object.keys(CHAPTER_TITLES);
    allChapters.forEach(chapterId => {
      expect(SOUNDSCAPE_DESCRIPTIONS).toHaveProperty(chapterId);
      expect(typeof SOUNDSCAPE_DESCRIPTIONS[chapterId]).toBe('string');
      expect(SOUNDSCAPE_DESCRIPTIONS[chapterId].length).toBeGreaterThan(0);
    });
  });

  it('should have poetic descriptions', () => {
    // Check that descriptions contain evocative words
    expect(SOUNDSCAPE_DESCRIPTIONS.gita_scroll).toContain('Krishna');
    expect(SOUNDSCAPE_DESCRIPTIONS.weapon_quest).toContain('Forest');
    expect(SOUNDSCAPE_DESCRIPTIONS.trials_of_karna).toContain('Karna');
  });

  it('should have non-empty descriptions', () => {
    Object.values(SOUNDSCAPE_DESCRIPTIONS).forEach(description => {
      expect(description.trim()).not.toBe('');
      expect(description.length).toBeGreaterThan(20);
    });
  });
});
