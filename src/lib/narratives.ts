import type { Chapter, Story } from './types';
import { CHAPTER_TITLES, STORY_TITLES, CHAPTER_BACKGROUNDS, STORY_ARTWORK, CHANT_LINES, SOUNDSCAPE_DESCRIPTIONS } from './types';

const narrativeContent = {
  gita_scroll: {
    lotus_of_doubt: `"My limbs fail me, my mouth is parched, my body trembles..."
Arjuna freezes on the battle line while family and mentors wait for his bow.
Fight and he kills kin; retreat and duty collapses.
He forces the pause, demanding a path before the first arrow flies.`,
    chakra_of_dharma: `"You grieve for those who should not be grieved for..."
Krishna answers the stalemate with ruthless clarity.
Act without clinging, he commands, or watch dharma die.
The wheel turns; confusion thins; the next move becomes inevitable.`,
    spiral_of_vision: `"Behold my cosmic form..."
Krishna shows the war's true scale—worlds burning, worlds reborn.
Arjuna sees every life he might spare already consumed by time.
Terror flips to surrender; he accepts the role the cosmos demands.`,
    sword_of_resolve: `"Slay with equanimity..."
Arjuna picks up the bow, steady now.
He fights to defend order, not to feed anger.
Resolve replaces panic; the campaign finally begins.`,
  },
  fall_of_dharma: {
    game_of_fate: `"The court is gilded, but the air is heavy."
Loaded dice decide the empire while Yudhishthira gambles reputation for pride.
Each throw strips another safeguard.
By the time Draupadi is wagered, the kingdom is already lost.`,
    silence_of_protest: `"The dice have fallen. The wager is made."
Bhishma's oath shackles him, Vidura's warnings die in his throat.
No elder moves, so the outrage hardens into law.
Dharma falls not from defeat but from complicity.`,
    divine_intervention: `"She stands in the court of kings-alone, yet unshaken."
Draupadi calls Krishna before the assembly can finish the assault.
The cloth keeps coming; the conspirators freeze.
The court witnesses mercy as judgment—and the revolt seeds itself.`,
  },
  weapon_quest: {
    forest_of_austerity: `"Withdraw from the world, and the world shall reveal its secrets."
Arjuna abandons steel for stillness and lets hunger and doubt grind him down.
If he breaks, the quest ends; if he endures, the gods take notice.
He holds the vigil, and the forest answers with the next guide.`,
    shiva_and_the_hunter: `"Strike not in anger, but in truth."
A boar falls to two arrows; Arjuna demands the prize.
The hunter matches him strike for strike until arrogance cracks.
Shiva reveals himself and gifts the Pashupatastra to the disciplined challenger.`,
    celestial_audience: `"Come forth, son of Indra."
Heaven summons Arjuna to trade mortal instincts for celestial drills.
Every lesson ties a weapon to a moral boundary.
He leaves with power measured by discipline, ready for the war ahead.`,
    trial_of_heaven: `"Power without humility is ruin."
Heaven offers Arjuna indulgence to see if the new arsenal controls him.
He turns away, keeping his vow sharper than any blade.
The gods endorse him; the mission stays on course.`,
  },
  birth_of_dharma: {
    cosmic_egg: `"From silence, the seed of creation cracked."
The cosmic egg holds every possibility and every collapse.
One fracture decides whether the universe ignites or stays void.
It splits—the first breath commits reality to motion.`,
    first_flame: `"Agni rises-not to burn, but to illuminate."
Fire tests every offering; refuse to feed it and creation stalls.
The flame accepts the vow and turns devotion into power.
Sacrifice becomes the currency of progress.`,
    river_oath: `"Flow not to conquer, but to cleanse."
Saraswati's current offers a choice: drown in noise or ride toward clarity.
Those who enter with deceit are swept aside.
The oath to speak truth keeps the waters calm.`,
    wheel_turns: `"Dharma is not a rule. It is a rhythm."
The wheel locks the elements into order; ignore its timing and harmony shatters.
Each spoke demands a choice between imbalance and alignment.
When it turns smoothly, creation stays upright.`,
    balance_restored: `"Thus was Dharma born-not imposed, but invoked."
Creation holds only because each force keeps its promise.
Break one vow and the cycle collapses.
Keep them, and balance stays restored.`,
  },
  trials_of_karna: {
    suns_gift: `"Born of the Sun, yet cast to the shadows."
Karna arrives armed with celestial armor but no pedigree.
Keep the secret and survive as an outcast; reveal it and risk rejection.
He chooses anonymity, sharpening resolve in isolation.`,
    brahmin_curse: `"Compassion is a blade that cuts both ways."
A single misfired arrow earns Karna a curse: forget every skill when it matters most.
He accepts the judgment to honor the grieving Brahmin.
Mercy now guarantees a fatal gap later.`,
    friends_vow: `"Loyalty is a crown-and a chain."
Duryodhana elevates Karna, demanding allegiance in return.
Honor the bond and fight against dharma, or betray the one ally who believed in him.
Karna locks the vow, knowing it fixes his fate.`,
    birth_revealed: `"Truth arrives-but not always in time."
Kunti finally names him her son; the Pandavas become his brothers.
Switch sides and live, or keep the oath and march toward certain loss.
He shields the secret to protect her honor and his promise.`,
    final_arrow: `"The wheel sinks. The memory fades. The arrow flies."
Karna's chariot stalls, the curse erases his mantras, and Arjuna closes in.
He begs for time; the battlefield denies it.
He falls, keeping the vow that cost him everything.`,
  },
};

const svgAssets: Record<string, { svg: string; anim: string; alt: string }> = {
  lotus_of_doubt: { svg: 'lotus.svg', anim: 'lotus-animated', alt: 'Lotus flower representing doubt and contemplation' },
  chakra_of_dharma: { svg: 'dharma_wheel.svg', anim: 'chakra-animated', alt: 'Spinning wheel of dharma' },
  spiral_of_vision: { svg: 'galaxy.svg', anim: 'galaxy-animated', alt: 'Cosmic spiral representing universal vision' },
  sword_of_resolve: { svg: 'bow_and_arrow.svg', anim: 'bow-animated', alt: 'Bow representing resolve and duty' },
  game_of_fate: { svg: 'dice.svg', anim: 'dice-animated', alt: 'Dice representing fate and chance' },
  silence_of_protest: { svg: 'dharma_collapse.svg', anim: 'collapse-animated', alt: 'Collapsing structure representing moral failure' },
  divine_intervention: { svg: 'restore_flower.svg', anim: 'restore-animated', alt: 'Divine restoration and protection' },
  forest_of_austerity: { svg: 'forest.svg', anim: 'forest-animated', alt: 'Sacred forest of meditation' },
  shiva_and_the_hunter: { svg: 'trident.svg', anim: 'trident-animated', alt: 'Shiva\'s trident' },
  celestial_audience: { svg: 'bell.svg', anim: 'bell-animated', alt: 'Celestial bell summoning divine audience' },
  trial_of_heaven: { svg: 'bow_and_arrow.svg', anim: 'bow-animated', alt: 'Divine test of character' },
  cosmic_egg: { svg: 'cosmic_egg.svg', anim: 'cosmic-egg-animated', alt: 'Primordial cosmic egg' },
  first_flame: { svg: 'sacred_flame.svg', anim: 'first-flame-animated', alt: 'First sacred flame' },
  river_oath: { svg: 'river_oath.svg', anim: 'river-oath-animated', alt: 'Sacred river of truth' },
  wheel_turns: { svg: 'wheel_turns.svg', anim: 'wheel-turns-animated', alt: 'Eternal wheel of dharma' },
  balance_restored: { svg: 'balance_restored.svg', anim: 'balance-restored-animated', alt: 'Universal balance restored' },
  suns_gift: { svg: 'suns_gift.svg', anim: 'suns-gift-animated', alt: 'Sun\'s divine armor' },
  brahmin_curse: { svg: 'brahmin_curse.svg', anim: 'brahmin-curse-animated', alt: 'Curse of forgotten knowledge' },
  friends_vow: { svg: 'friends_vow.svg', anim: 'friends-vow-animated', alt: 'Sacred vow of friendship' },
  birth_revealed: { svg: 'birth_revealed.svg', anim: 'birth-revealed-animated', alt: 'Truth revealed' },
  final_arrow: { svg: 'final_arrow.svg', anim: 'final-arrow-animated', alt: 'Final arrow of destiny' },
};

const audioAssets: Record<string, { narrative?: string; ambient?: string }> = {
  // Gita Scroll
  lotus_of_doubt: { narrative: 'fadein/lotus_of_doubt_fadein.mp3', ambient: 'ambient/lotus_of_doubt_ambient_loop.mp3' },
  chakra_of_dharma: { narrative: 'fadein/chakra_of_dharma_fadein.mp3', ambient: 'ambient/chakra_of_dharma_ambient_loop.mp3' },
  spiral_of_vision: { narrative: 'fadein/spiral_of_vision_fadein.mp3', ambient: 'ambient/spiral_of_vision_ambient_loop.mp3' },
  sword_of_resolve: { narrative: 'fadein/sword_of_resolve_fadein.mp3', ambient: 'ambient/sword_of_resolve_ambient_loop.mp3' },
  // Fall of Dharma
  game_of_fate: { narrative: 'composite/game_of_fate_composite.mp3' },
  silence_of_protest: { narrative: 'composite/silence_of_protest_composite.mp3' },
  divine_intervention: { narrative: 'composite/divine_intervention_composite.mp3' },
  // Weapon Quest
  forest_of_austerity: { narrative: 'forest/forest_of_austerity/forest_of_austerity_mix.mp3', ambient: 'forest/forest_of_austerity/ambient.mp3' },
  shiva_and_the_hunter: { narrative: 'forest/shiva_and_the_hunter/shiva_and_the_hunter_mix.mp3', ambient: 'forest/shiva_and_the_hunter/ambient.mp3' },
  celestial_audience: { narrative: 'forest/celestial_audience/celestial_audience_mix.mp3', ambient: 'forest/celestial_audience/ambient.mp3' },
  trial_of_heaven: { narrative: 'forest/trial_of_heaven/trial_of_heaven_mix.mp3', ambient: 'forest/trial_of_heaven/ambient.mp3' },
  // Birth of Dharma
  cosmic_egg: { narrative: 'birth/cosmic_breath/cosmic_breath_mix.mp3' },
  first_flame: { narrative: 'birth/awakening_scroll/awakening_scroll_mix.mp3' },
  river_oath: { narrative: 'birth/flowing_wisdom/flowing_wisdom_mix.mp3' },
  wheel_turns: { narrative: 'birth/glyphs_of_dharma/glyphs_of_dharma_mix.mp3' },
  balance_restored: { narrative: 'birth/golden_parchment/golden_parchment_mix.mp3' },
  // Trials of Karna
  suns_gift: { narrative: 'karna/suns_gift/suns_gift_mix.mp3' },
  brahmin_curse: { narrative: 'karna/brahmin_curse/brahmin_curse_mix.mp3' },
  friends_vow: { narrative: 'karna/friends_vow/friends_vow_mix.mp3' },
  birth_revealed: { narrative: 'karna/birth_revealed/birth_revealed_mix.mp3' },
  final_arrow: { narrative: 'karna/final_arrow/final_arrow_mix.mp3' },
};

function createStory(chapterId: string, storyId: string): Story {
  const chapterContent = narrativeContent[chapterId as keyof typeof narrativeContent];
  const content = chapterContent ? (chapterContent as any)[storyId] || '' : '';
  const asset = svgAssets[storyId] || { svg: 'lotus.svg', anim: '', alt: 'Story illustration' };
  const audio = audioAssets[storyId];
  
  return {
    id: storyId,
    title: STORY_TITLES[storyId] || storyId.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
    content,
    svgFile: asset.svg,
    animationClass: asset.anim,
    alt: asset.alt,
    audio,
    artworkFile: STORY_ARTWORK[storyId],
    chantLines: CHANT_LINES[storyId],
  };
}

export const chapters: Chapter[] = [
  {
    id: 'gita_scroll',
    title: CHAPTER_TITLES.gita_scroll,
    description: 'Arjuna halts a war, interrogates duty, and chooses how to fight.',
    stories: ['lotus_of_doubt', 'chakra_of_dharma', 'spiral_of_vision', 'sword_of_resolve'].map(id => createStory('gita_scroll', id)),
    backgroundImage: CHAPTER_BACKGROUNDS.gita_scroll,
    soundscapeDescription: SOUNDSCAPE_DESCRIPTIONS.gita_scroll,
  },
  {
    id: 'fall_of_dharma',
    title: CHAPTER_TITLES.fall_of_dharma,
    description: 'A fixed dice game topples a kingdom while a court watches in silence.',
    stories: ['game_of_fate', 'silence_of_protest', 'divine_intervention'].map(id => createStory('fall_of_dharma', id)),
    backgroundImage: CHAPTER_BACKGROUNDS.fall_of_dharma,
    soundscapeDescription: SOUNDSCAPE_DESCRIPTIONS.fall_of_dharma,
  },
  {
    id: 'weapon_quest',
    title: CHAPTER_TITLES.weapon_quest,
    description: 'Training, divine trials, and discipline decide who earns celestial weapons.',
    stories: ['forest_of_austerity', 'shiva_and_the_hunter', 'celestial_audience', 'trial_of_heaven'].map(id => createStory('weapon_quest', id)),
    backgroundImage: CHAPTER_BACKGROUNDS.weapon_quest,
    soundscapeDescription: SOUNDSCAPE_DESCRIPTIONS.weapon_quest,
  },
  {
    id: 'birth_of_dharma',
    title: CHAPTER_TITLES.birth_of_dharma,
    description: 'Creation itself balances promises between fire, water, and motion.',
    stories: ['cosmic_egg', 'first_flame', 'river_oath', 'wheel_turns', 'balance_restored'].map(id => createStory('birth_of_dharma', id)),
    backgroundImage: CHAPTER_BACKGROUNDS.birth_of_dharma,
    soundscapeDescription: SOUNDSCAPE_DESCRIPTIONS.birth_of_dharma,
  },
  {
    id: 'trials_of_karna',
    title: CHAPTER_TITLES.trials_of_karna,
    description: 'Loyalty, secrecy, and a fatal curse lock a hero into his final stand.',
    stories: ['suns_gift', 'brahmin_curse', 'friends_vow', 'birth_revealed', 'final_arrow'].map(id => createStory('trials_of_karna', id)),
    backgroundImage: CHAPTER_BACKGROUNDS.trials_of_karna,
    soundscapeDescription: SOUNDSCAPE_DESCRIPTIONS.trials_of_karna,
  },
];

export function getChapter(chapterId: string): Chapter | undefined {
  return chapters.find(c => c.id === chapterId);
}

export function getStory(chapterId: string, storyId: string): Story | undefined {
  const chapter = getChapter(chapterId);
  return chapter?.stories.find(s => s.id === storyId);
}
