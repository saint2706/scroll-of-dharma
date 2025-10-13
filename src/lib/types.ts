export interface Story {
  id: string;
  title: string;
  content: string;
  svgFile?: string;
  animationClass?: string;
  alt?: string;
}

export interface Chapter {
  id: string;
  title: string;
  description: string;
  stories: Story[];
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
