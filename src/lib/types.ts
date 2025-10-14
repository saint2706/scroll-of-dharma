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
  chantLines?: string[];
}

export interface Chapter {
  id: string;
  title: string;
  description: string;
  stories: Story[];
  backgroundImage?: string;
  soundscapeDescription?: string;
}

export const CHAPTER_TITLES: Record<string, string> = {
  gita_scroll: "Gita Scroll",
  fall_of_dharma: "Fall of Dharma",
  weapon_quest: "Weapon Quest",
  birth_of_dharma: "Birth of Dharma",
  trials_of_karna: "Trials of Karna",
  exile_of_rama: "Exile of Rama",
  draupadis_fire: "Draupadi's Fire",
};

export const STORY_TITLES: Record<string, string> = {
  // Gita Scroll
  lotus_of_doubt: "Lotus of Doubt",
  chakra_of_dharma: "Chakra of Dharma",
  spiral_of_vision: "Spiral of Vision",
  sword_of_resolve: "Trident of Resolve", // Override from ui_constants.py STORY_DISPLAY_TITLES
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
  // Exile of Rama
  golden_palace: "Golden Palace",
  forest_exile: "Forest Exile",
  golden_deer: "Golden Deer",
  stolen_beloved: "Stolen Beloved",
  // Draupadi's Fire
  born_from_flame: "Born from Flame",
  swayamvara_choice: "Swayamvara Choice",
  five_husbands: "Five Husbands",
  fire_of_defiance: "Fire of Defiance",
};

// Maps each chapter to its background texture file
export const CHAPTER_BACKGROUNDS: Record<string, string> = {
  gita_scroll: "gita_scroll.webp",
  fall_of_dharma: "fall_of_dharma.webp",
  weapon_quest: "weapon_quest.webp",
  birth_of_dharma: "birth_of_dharma.webp",
  trials_of_karna: "trials_of_karna.webp",
  exile_of_rama: "exile_of_rama.webp",
  draupadis_fire: "draupadis_fire.webp",
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

// Soundscape descriptions for each chapter (from ui_constants.py SOUNDSCAPE_DESCRIPTIONS)
export const SOUNDSCAPE_DESCRIPTIONS: Record<string, string> = {
  gita_scroll: "Crimson dusk settles over Kurukshetra while Krishna's counsel shimmers between the strings and tambura drones.",
  fall_of_dharma: "Echoes of judgement halls and solemn vows weave with temple bells to honor the gravity of the court.",
  weapon_quest: "Forest breezes rustle beside the seeker—flutes, drums, and distant thunder accompany each trial.",
  birth_of_dharma: "Cosmic breaths, cradle songs, and gentle chimes cradle the origin spark of righteousness.",
  trials_of_karna: "Sunlit brass and low murmurings follow Karna's vow, balancing valor with the ache of destiny.",
  exile_of_rama: "Bamboo flutes drift through ancient forests where duty calls and kingdoms fade into distant memory.",
  draupadis_fire: "Temple flames crackle with intensity as the unconquerable spirit rises from the sacrificial altar.",
};

// Sanskrit chant lines for each story (from ui_constants.py CHANT_LINES)
export const CHANT_LINES: Record<string, string[]> = {
  // Gita Scroll
  lotus_of_doubt: ["Om Shanti Shanti Shanti", "Om Shanti Shanti Shanti", "Om Shanti Shanti Shanti", "Om Shanti Shanti Shanti"],
  chakra_of_dharma: ["Om Namo Bhagavate Vasudevaya", "Om Namo Bhagavate Vasudevaya", "Om Namo Bhagavate Vasudevaya", "Om Namo Bhagavate Vasudevaya"],
  spiral_of_vision: ["Om Namo Narayanaya", "Om Namo Narayanaya", "Om Namo Narayanaya", "Om Namo Narayanaya"],
  sword_of_resolve: ["Om Tat Sat", "Om Tat Sat", "Om Tat Sat", "Om Tat Sat"],
  // Fall of Dharma
  game_of_fate: ["Asato maa sadgamaya", "Tamaso maa jyotirgamaya", "Mrityor maa amritam gamaya", "Om Shanti Shanti Shanti"],
  silence_of_protest: ["Om Shanti Shanti Shanti", "Om Shanti Shanti Shanti", "Om Shanti Shanti Shanti", "Om Shanti Shanti Shanti"],
  divine_intervention: ["Hare Krishna Hare Krishna", "Krishna Krishna Hare Hare", "Hare Rama Hare Rama", "Rama Rama Hare Hare"],
  // Weapon Quest
  forest_of_austerity: ["Om Bhur Bhuvah Swaha", "Tat Savitur Varenyam", "Bhargo Devasya Dhimahi", "Dhiyo Yo Nah Prachodayat"],
  shiva_and_the_hunter: ["Om Namah Shivaya", "Om Namah Shivaya", "Om Namah Shivaya", "Om Namah Shivaya"],
  celestial_audience: ["Om Indraya Namah", "Om Indraya Namah", "Om Indraya Namah", "Om Indraya Namah"],
  trial_of_heaven: ["Tryambakam yajamahe", "Sugandhim Pushtivardhanam", "Urvarkam iva bandhanan", "Mrityor mukshiya mamritat"],
  // Birth of Dharma
  cosmic_egg: ["Om Pranaya Namah", "Om Pranaya Namah", "Om Pranaya Namah", "Om Pranaya Namah"],
  first_flame: ["Om Sri Gurubhyo Namah", "Om Sri Gurubhyo Namah", "Om Sri Gurubhyo Namah", "Om Sri Gurubhyo Namah"],
  river_oath: ["Om Namo Narayanaya", "Om Namo Narayanaya", "Om Namo Narayanaya", "Om Namo Narayanaya"],
  wheel_turns: ["Om Saraswatyai Namah", "Om Saraswatyai Namah", "Om Saraswatyai Namah", "Om Saraswatyai Namah"],
  balance_restored: ["Om Gam Ganapataye Namah", "Om Gam Ganapataye Namah", "Om Gam Ganapataye Namah", "Om Gam Ganapataye Namah"],
  // Trials of Karna
  suns_gift: ["Om Suryaya Namah", "Om Suryaya Namah", "Om Suryaya Namah", "Om Suryaya Namah"],
  brahmin_curse: ["Asato maa sadgamaya", "Tamaso maa jyotirgamaya", "Mrityor maa amritam gamaya", "Om Shanti Shanti Shanti"],
  friends_vow: ["Om Mitraya Namah", "Om Mitraya Namah", "Om Mitraya Namah", "Om Mitraya Namah"],
  birth_revealed: ["Om Kuntidevyai Namah", "Om Kuntidevyai Namah", "Om Kuntidevyai Namah", "Om Kuntidevyai Namah"],
  final_arrow: ["Tryambakam yajamahe", "Sugandhim Pushtivardhanam", "Urvarkam iva bandhanan", "Mrityor mukshiya mamritat"],
  // Exile of Rama
  golden_palace: ["Om Sri Ramaya Namah", "Om Sri Ramaya Namah", "Om Sri Ramaya Namah", "Om Sri Ramaya Namah"],
  forest_exile: ["Raghupati Raghava Raja Ram", "Patita Pavana Sita Ram", "Sita Ram Sita Ram", "Bhaja Pyare Tu Sita Ram"],
  golden_deer: ["Om Namo Narayanaya", "Om Namo Narayanaya", "Om Namo Narayanaya", "Om Namo Narayanaya"],
  stolen_beloved: ["Om Hanumate Namah", "Om Hanumate Namah", "Om Hanumate Namah", "Om Hanumate Namah"],
  // Draupadi's Fire
  born_from_flame: ["Om Agnidevaya Namah", "Om Agnidevaya Namah", "Om Agnidevaya Namah", "Om Agnidevaya Namah"],
  swayamvara_choice: ["Om Arjunaya Namah", "Om Arjunaya Namah", "Om Arjunaya Namah", "Om Arjunaya Namah"],
  five_husbands: ["Om Kuntidevyai Namah", "Om Kuntidevyai Namah", "Om Kuntidevyai Namah", "Om Kuntidevyai Namah"],
  fire_of_defiance: ["Om Shaktyai Namah", "Om Shaktyai Namah", "Om Shaktyai Namah", "Om Shaktyai Namah"],
};
