import { describe, it, expect } from 'vitest';
import { CHAPTER_TITLES, STORY_TITLES } from '../../src/lib/types';

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
});
