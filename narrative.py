"""
Contains all the narrative content for the Scroll of Dharma application.

The `NARRATIVES` dictionary is the central repository for the text displayed
in the application. It is structured as a nested dictionary where:
- The top-level keys are identifiers for each "chapter" (e.g., 'gita_scroll').
- The second-level keys are identifiers for each "story" or "scroll" within a chapter
  (e.g., 'lotus_of_doubt').
- The values are the narrative strings associated with each story.

This structure allows the main application (`app.py`) to easily look up
the appropriate text based on the user's chapter and story selections.
"""

NARRATIVES = {
    "gita_scroll": {
        "lotus_of_doubt": (
            "“My limbs fail me, my mouth is parched, my body trembles...”\n"
            "The lotus trembles. Dharma fades.\n"
            "Arjuna stands at the edge of battle, torn between duty and despair. The bow slips from his hand, not from weakness, but from the weight of compassion.\n"
            "In the hush before the storm, the lotus whispers: Doubt is not defeat, but the fertile soil of wisdom.\n"
            "He gazes at the faces before him-kin and teacher, friend and foe-each a reflection of his own heart.\n"
            "The wind stirs the parchment, and petals fall. In this moment, the seeker is born."
        ),
        "chakra_of_dharma": (
            "“You grieve for those who should not be grieved for...”\n"
            "The chakra awakens. Dharma stirs.\n"
            "Krishna’s voice is a river, gentle yet unyielding, carving a path through Arjuna’s confusion.\n"
            "Action without attachment, he teaches, is the way of the wise.\n"
            "The wheel turns, and with each revolution, the fog lifts. Duty becomes devotion, and the battlefield transforms into a temple of learning.\n"
            "The seeker finds clarity in the counsel of the divine."
        ),
        "spiral_of_vision": (
            "“Behold my cosmic form...”\n"
            "Time devours all. Dharma transcends fear.\n"
            "Krishna reveals his Vishvarupa, the infinite form. Galaxies swirl in his eyes, creation and destruction dance in his breath.\n"
            "Arjuna beholds the spiral of existence-past, present, and future entwined.\n"
            "Awe and terror mingle in his soul, and surrender becomes the only prayer.\n"
            "The seeker bows, humbled by the vastness of dharma."
        ),
        "sword_of_resolve": (
            "“Slay with equanimity...”\n"
            "The scroll seals. The warrior rises.\n"
            "Arjuna lifts his bow, not with anger, but with serene resolve.\n"
            "He understands: to act is not to destroy, but to uphold the balance of the world.\n"
            "The sword gleams, a beacon of purpose. The final chapter is written in the fire of courage and the ink of compassion.\n"
            "The seeker becomes the hero, and dharma is restored."
        ),
    },
    "fall_of_dharma": {
        "game_of_fate": (
            "“The court is gilded, but the air is heavy.”\n"
            "Shakuni lifts the dice-bones of betrayal, carved from vengeance.\n"
            "They do not roll. They choose.\n"
            "Yudhishthira wagers not gold, but virtue. Pride blinds the wise. Ego deafens the just.\n"
            "With each throw, dharma frays. The wheel does not turn-it cracks.\n"
            "And Draupadi, untouched by the game, becomes its cruelest stake."
        ),
        "silence_of_protest": (
            "“The dice have fallen. The wager is made.”\n"
            "Bhishma, the grand pillar, stands unmoved. His vow, once noble, now binds him in chains.\n"
            "Vidura, the voice of wisdom, speaks not. His words are drowned in royal pride.\n"
            "Silence spreads like smoke. Not from fire-but from fear.\n"
            "Dharma does not die in battle. It dies when the righteous choose quiet."
        ),
        "divine_intervention": (
            "“She stands in the court of kings-alone, yet unshaken.”\n"
            "Her voice trembles, but her spirit does not.\n"
            "Hands raised, eyes closed, she calls not for vengeance, but for grace.\n"
            "A whisper-‘Govinda’-pierces the veil. And the fabric flows, endless as compassion.\n"
            "She is not stripped. She is sanctified."
        ),
    },
    "weapon_quest": {
        "forest_of_austerity": (
            "“Withdraw from the world, and the world shall reveal its secrets.”\n"
            "Arjuna steps into the forest, not as a warrior, but as a seeker. The clang of battle fades. In its place: rustling leaves, distant chants, and the breath of the earth.\n"
            "His bow rests beside him. His armor gathers dust. He wears only resolve.\n"
            "Days stretch into weeks. Hunger gnaws. The body weakens, but the spirit sharpens. Each breath is a mantra. Each moment, a mirror.\n"
            "The forest watches. It does not speak, but it teaches:\n"
            "- The stillness of the lake reflects the chaos within.\n"
            "- The roots of ancient trees whisper of forgotten truths.\n"
            "- The fireflies dance like astras waiting to be earned.\n"
            "Arjuna’s mind wanders-to Draupadi’s laughter, to Krishna’s gaze, to the faces he must one day face. But he returns, again and again, to the silence.\n"
            "One night, beneath a moon veiled in mist, he sees a figure in meditation-a sage carved from starlight. The sage does not open his eyes, but Arjuna hears:\n"
            "“To wield the divine, you must first dissolve the self.”\n"
            "Arjuna bows. Not to the sage, but to the path.\n"
            "The forest does not test him. It transforms him.\n"
            "The seeker becomes the vessel."
        ),
        "shiva_and_the_hunter": (
            "“Strike not in anger, but in truth.”\n"
            "A wild boar charges. Arjuna’s arrow flies. But another pierces first.\n"
            "A hunter stands before him-rugged, radiant, unknowable.\n"
            "They clash, not in hatred, but in revelation. Each blow is a question. Each parry, a prayer.\n"
            "When the dust settles, the hunter smiles. The illusion fades.\n"
            "Shiva stands revealed. The seeker is blessed with the Pashupatastra-the weapon of dissolution and grace."
        ),
        "celestial_audience": (
            "“Come forth, son of Indra.”\n"
            "Arjuna ascends to Amaravati, the city of gods. Music flows like rivers. Stars bow in rhythm.\n"
            "Indra embraces his son, and the heavens open their vaults.\n"
            "He learns the dance of astras-the thunderbolt, the wind blade, the fire wheel.\n"
            "Urged by sages, trained by celestials, Arjuna becomes more than mortal.\n"
            "The seeker becomes the wielder, and the cosmos lends him its fury."
        ),
        "trial_of_heaven": (
            "“Power without humility is ruin.”\n"
            "Arjuna is tested-not by enemies, but by temptation.\n"
            "The apsaras beckon. The halls shimmer. Pride stirs.\n"
            "But he bows to wisdom, not indulgence. He chooses restraint over revelry.\n"
            "The gods nod. The astras glow.\n"
            "The seeker passes the trial-not by conquest, but by character."
        ),
    },
    "birth_of_dharma": {
        "cosmic_egg": (
            "“From silence, the seed of creation cracked.”\n"
            "The Brahmanda floats in the void-golden, whole, waiting.\n"
            "No gods yet speak. No winds yet stir. But within the egg, time coils like a serpent.\n"
            "A crack forms-not of violence, but of yearning.\n"
            "From this fracture, breath emerges. Space unfolds. The first vibration hums.\n"
            "The spiral glyph pulses. The cosmos inhales.\n"
            "The seeker glimpses the origin-not as myth, but as memory."
        ),
        "first_flame": (
            "“Agni rises-not to burn, but to illuminate.”\n"
            "From the ash of silence, the flame dances.\n"
            "It does not consume. It reveals.\n"
            "Agni bears the spark of sacrifice, the warmth of devotion, the fire of transformation.\n"
            "He flickers between realms, a messenger of intent.\n"
            "The flame glyph glows. The scroll warms.\n"
            "The seeker learns: to offer is to awaken."
        ),
        "river_oath": (
            "“Flow not to conquer, but to cleanse.”\n"
            "Saraswati emerges, veiled in mist, her currents braided with wisdom.\n"
            "She does not rush. She remembers.\n"
            "Her waters carry restraint, clarity, and the promise of truth.\n"
            "The river glyph ripples. The parchment softens.\n"
            "The seeker listens-not to words, but to whispers."
        ),
        "wheel_turns": (
            "“Dharma is not a rule. It is a rhythm.”\n"
            "From flame and flow, the wheel awakens.\n"
            "It does not command. It turns.\n"
            "Each spoke a path. Each revolution a lesson.\n"
            "The chakra spins-not to dominate, but to balance.\n"
            "The wheel glyph pulses. The scroll hums.\n"
            "The seeker stands at the center-not above, but within."
        ),
        "balance_restored": (
            "“Thus was Dharma born-not imposed, but invoked.”\n"
            "The egg cracked. The flame rose. The river flowed. The wheel turned.\n"
            "Creation did not begin with command. It began with harmony.\n"
            "The scroll closes, but the rhythm continues.\n"
            "The seeker walks forward-not with answers, but with alignment."
        ),
    },
    "trials_of_karna": {
        "suns_gift": (
            "“Born of the Sun, yet cast to the shadows.”\n"
            "Karna awakens with divine armor and earrings-gifts of Surya, radiant and silent.\n"
            "The world does not know him, but the cosmos already sings his name.\n"
            "He walks among mortals with celestial grace, yet bears the ache of abandonment.\n"
            "The seeker is marked-not by lineage, but by light."
        ),
        "brahmin_curse": (
            "“Compassion is a blade that cuts both ways.”\n"
            "Karna, moved by mercy, kills a cow by mistake. The Brahmin curses him:\n"
            "‘In your moment of need, memory shall fail.’\n"
            "The curse coils around his fate, quiet but fatal.\n"
            "The seeker learns: even kindness must carry consequence."
        ),
        "friends_vow": (
            "“Loyalty is a crown-and a chain.”\n"
            "Duryodhana offers Karna a throne. Karna accepts-not for power, but for gratitude.\n"
            "He stands beside the one who saw his worth, even as dharma trembles.\n"
            "In friendship, he finds purpose. In purpose, he finds chains.\n"
            "The seeker chooses loyalty over lineage."
        ),
        "birth_revealed": (
            "“Truth arrives-but not always in time.”\n"
            "Kunti speaks. Karna is her son-sun-born, Pandava by blood.\n"
            "But the war is near, and Karna chooses silence over reunion.\n"
            "Identity flickers, but loyalty holds firm.\n"
            "The seeker carries truth-not to claim, but to protect."
        ),
        "final_arrow": (
            "“The wheel sinks. The memory fades. The arrow flies.”\n"
            "On the field of Kurukshetra, Karna’s chariot falters. His mind blanks. Fate strikes.\n"
            "He dies with dignity, not victory. Dharma watches.\n"
            "The sun sets-not in defeat, but in grace.\n"
            "The seeker falls-not forgotten, but fulfilled."
        ),
    },
}
