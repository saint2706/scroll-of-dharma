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
            "Arjuna freezes on the battle line while family and mentors "
            "wait for his bow.\n"
            "Fight and he kills kin; retreat and duty collapses.\n"
            "He forces the pause, demanding a path before the first arrow flies."
        ),
        "chakra_of_dharma": (
            "“You grieve for those who should not be grieved for...”\n"
            "Krishna answers the stalemate with ruthless clarity.\n"
            "Act without clinging, he commands, or watch dharma die.\n"
            "The wheel turns; confusion thins; the next move becomes inevitable."
        ),
        "spiral_of_vision": (
            "“Behold my cosmic form...”\n"
            "Krishna shows the war's true scale—worlds burning, worlds reborn.\n"
            "Arjuna sees every life he might spare already consumed by time.\n"
            "Terror flips to surrender; he accepts the role the cosmos demands."
        ),
        "sword_of_resolve": (
            "“Slay with equanimity...”\n"
            "Arjuna picks up the bow, steady now.\n"
            "He fights to defend order, not to feed anger.\n"
            "Resolve replaces panic; the campaign finally begins."
        ),
    },
    "fall_of_dharma": {
        "game_of_fate": (
            "“The court is gilded, but the air is heavy.”\n"
            "Loaded dice decide the empire while "
            "Yudhishthira gambles reputation for pride.\n"
            "Each throw strips another safeguard.\n"
            "By the time Draupadi is wagered, the kingdom is already lost."
        ),
        "silence_of_protest": (
            "“The dice have fallen. The wager is made.”\n"
            "Bhishma's oath shackles him, Vidura's warnings die in his throat.\n"
            "No elder moves, so the outrage hardens into law.\n"
            "Dharma falls not from defeat but from complicity."
        ),
        "divine_intervention": (
            "“She stands in the court of kings-alone, yet unshaken.”\n"
            "Draupadi calls Krishna before the assembly can finish the assault.\n"
            "The cloth keeps coming; the conspirators freeze.\n"
            "The court witnesses mercy as judgment—and the revolt seeds itself."
        ),
    },
    "weapon_quest": {
        "forest_of_austerity": (
            "“Withdraw from the world, and the world shall reveal its secrets.”\n"
            "Arjuna abandons steel for stillness and lets hunger and doubt "
            "grind him down.\n"
            "If he breaks, the quest ends; if he endures, the gods take notice.\n"
            "He holds the vigil, and the forest answers with the next guide."
        ),
        "shiva_and_the_hunter": (
            "“Strike not in anger, but in truth.”\n"
            "A boar falls to two arrows; Arjuna demands the prize.\n"
            "The hunter matches him strike for strike until arrogance cracks.\n"
            "Shiva reveals himself and gifts the Pashupatastra "
            "to the disciplined challenger."
        ),
        "celestial_audience": (
            "“Come forth, son of Indra.”\n"
            "Heaven summons Arjuna to trade mortal instincts for celestial drills.\n"
            "Every lesson ties a weapon to a moral boundary.\n"
            "He leaves with power measured by discipline, ready for the war ahead."
        ),
        "trial_of_heaven": (
            "“Power without humility is ruin.”\n"
            "Heaven offers Arjuna indulgence to see if the new arsenal controls him.\n"
            "He turns away, keeping his vow sharper than any blade.\n"
            "The gods endorse him; the mission stays on course."
        ),
    },
    "birth_of_dharma": {
        "cosmic_egg": (
            "“From silence, the seed of creation cracked.”\n"
            "The cosmic egg holds every possibility and every collapse.\n"
            "One fracture decides whether the universe ignites or stays void.\n"
            "It splits—the first breath commits reality to motion."
        ),
        "first_flame": (
            "“Agni rises-not to burn, but to illuminate.”\n"
            "Fire tests every offering; refuse to feed it and creation stalls.\n"
            "The flame accepts the vow and turns devotion into power.\n"
            "Sacrifice becomes the currency of progress."
        ),
        "river_oath": (
            "“Flow not to conquer, but to cleanse.”\n"
            "Saraswati's current offers a choice: drown in noise or "
            "ride toward clarity.\n"
            "Those who enter with deceit are swept aside.\n"
            "The oath to speak truth keeps the waters calm."
        ),
        "wheel_turns": (
            "“Dharma is not a rule. It is a rhythm.”\n"
            "The wheel locks the elements into order; ignore its timing and harmony "
            "shatters.\n"
            "Each spoke demands a choice between imbalance and alignment.\n"
            "When it turns smoothly, creation stays upright."
        ),
        "balance_restored": (
            "“Thus was Dharma born-not imposed, but invoked.”\n"
            "Creation holds only because each force keeps its promise.\n"
            "Break one vow and the cycle collapses.\n"
            "Keep them, and balance stays restored."
        ),
    },
    "trials_of_karna": {
        "suns_gift": (
            "“Born of the Sun, yet cast to the shadows.”\n"
            "Karna arrives armed with celestial armor but no pedigree.\n"
            "Keep the secret and survive as an outcast; reveal it and risk rejection.\n"
            "He chooses anonymity, sharpening resolve in isolation."
        ),
        "brahmin_curse": (
            "“Compassion is a blade that cuts both ways.”\n"
            "A single misfired arrow earns Karna a curse: "
            "forget every skill when it matters most.\n"
            "He accepts the judgment to honor the grieving Brahmin.\n"
            "Mercy now guarantees a fatal gap later."
        ),
        "friends_vow": (
            "“Loyalty is a crown-and a chain.”\n"
            "Duryodhana elevates Karna, demanding allegiance in return.\n"
            "Honor the bond and fight against dharma, or betray the one ally who "
            "believed in him.\n"
            "Karna locks the vow, knowing it fixes his fate."
        ),
        "birth_revealed": (
            "“Truth arrives-but not always in time.”\n"
            "Kunti finally names him her son; the Pandavas become his brothers.\n"
            "Switch sides and live, or keep the oath and march toward certain loss.\n"
            "He shields the secret to protect her honor and his promise."
        ),
        "final_arrow": (
            "“The wheel sinks. The memory fades. The arrow flies.”\n"
            "Karna's chariot stalls, the curse erases his mantras, "
            "and Arjuna closes in.\n"
            "He begs for time; the battlefield denies it.\n"
            "He falls, keeping the vow that cost him everything."
        ),
    },
}
