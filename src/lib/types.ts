export interface Story {
  id: string;
  title: string;
  content: string;
  svgFile?: string;
  animationClass?: string;
  alt?: string;
  audio?: {
    narrative?: string;
    ambient?: string;
  };
  artworkFile?: string;
}

export interface Chapter {
  id: string;
  title: string;
  description: string;
  stories: Story[];
  backgroundImage?: string;
}

export const CHAPTER_TITLES: Record<string, string> = {
  gita_scroll: "Gita Scroll",
  fall_of_dharma: "Fall of Dharma",
  weapon_quest: "Weapon Quest",
  birth_of_dharma: "Birth of Dharma",
  trials_of_karna: "Trials of Karna",
};

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

// Maps each chapter to its background texture file
export const CHAPTER_BACKGROUNDS: Record<string, string> = {
  gita_scroll: "gita_scroll.webp",
  fall_of_dharma: "fall_of_dharma.webp",
  weapon_quest: "weapon_quest.webp",
  birth_of_dharma: "birth_of_dharma.webp",
  trials_of_karna: "trials_of_karna.webp",
};

// Maps stories to their artwork files (when available)
export const STORY_ARTWORK: Record<string, string> = {
  // Gita Scroll
  lotus_of_doubt: "lotus_of_doubt.jpeg",
  chakra_of_dharma: "chakra_of_dharma.jpeg",
  spiral_of_vision: "spiral_of_vision.jpeg",
  sword_of_resolve: "trident_of_resolve.jpeg",
  // Fall of Dharma
  game_of_fate: "Game of Fate.jpeg",
  silence_of_protest: "Silence of Protest.jpeg",
  divine_intervention: "Divine Intervention.jpeg",
};
