"""Constants and declarative configuration for the Scroll of Dharma app."""

from __future__ import annotations

# Prologue configuration ----------------------------------------------------

PROLOGUE_TEXT = """
<p><strong>The scroll wakes.</strong> Glyphs flare. The page is waiting.</p>
<p>Move with purpose:</p>
<ul>
    <li>Pick a chapter to snap the visuals, fonts, and texture into a new mood.</li>
    <li>Open a story to get the glyph, the conflict, and the resolution in one view.</li>
    <li>Start the ambience when you want the soundscape to carry the scene.</li>
</ul>
<p>Lock in your focus. Choose a chapter. Begin.</p>
"""

PROLOGUE_GLYPH = {
    "svg": "lotus.svg",
    "anim_class": "lotus-animated",
    "alt": "Lotus glyph introducing the scroll",
}

# Relative path components for the prologue ambience audio
PROLOGUE_AUDIO_ASSET = ("audio/raw", "ambient_loop.mp3")

# Typography ---------------------------------------------------------------

FONT_SPECS = [
    ("Cormorant Garamond", "CormorantGaramond-400.woff2", 400, "normal"),
    ("Cormorant Garamond", "CormorantGaramond-700.woff2", 700, "normal"),
    ("Cormorant Garamond", "CormorantGaramond-Italic-400.woff2", 400, "italic"),
    ("EB Garamond", "EBGaramond-400.woff2", 400, "normal"),
    ("EB Garamond", "EBGaramond-700.woff2", 700, "normal"),
    ("EB Garamond", "EBGaramond-Italic-400.woff2", 400, "italic"),
    ("Cinzel", "Cinzel-400.woff2", 400, "normal"),
    ("Cinzel", "Cinzel-700.woff2", 700, "normal"),
    ("Spectral", "Spectral-400.woff2", 400, "normal"),
    ("Spectral", "Spectral-700.woff2", 700, "normal"),
    ("Spectral", "Spectral-Italic-400.woff2", 400, "italic"),
    ("Cormorant Unicase", "CormorantUnicase-400.woff2", 400, "normal"),
    ("Cormorant Unicase", "CormorantUnicase-700.woff2", 700, "normal"),
    ("Alegreya", "Alegreya-400.woff2", 400, "normal"),
    ("Alegreya", "Alegreya-700.woff2", 700, "normal"),
    ("Alegreya", "Alegreya-Italic-400.woff2", 400, "italic"),
    ("Noto Serif Devanagari", "NotoSerifDevanagari-400.woff2", 400, "normal"),
    ("Noto Serif Devanagari", "NotoSerifDevanagari-700.woff2", 700, "normal"),
    ("Tiro Devanagari Sanskrit", "TiroDevanagariSanskrit-400.woff2", 400, "normal"),
]

PARCHMENT_GRADIENT_LAYERS = ", ".join(
    [
        "radial-gradient(circle at 20% 20%, rgba(255, 255, 255, 0.55), rgba(234, 216, 181, 0.65))",
        "radial-gradient(circle at 80% 0%, rgba(255, 255, 255, 0.4), rgba(229, 208, 170, 0.55))",
        "linear-gradient(135deg, rgba(245, 230, 201, 0.92), rgba(233, 211, 174, 0.95))",
    ]
)

# Scene + chapter metadata -------------------------------------------------

SCENE_ASSETS = {
    # Gita Scroll
    "lotus_of_doubt": {
        "svg": "lotus.svg",
        "anim_class": "lotus-animated",
        "alt": "Lotus flower icon representing doubt",
    },
    "chakra_of_dharma": {
        "svg": "dharma_wheel.svg",
        "anim_class": "chakra-animated",
        "alt": "Dharma wheel icon representing counsel",
    },
    "spiral_of_vision": {
        "svg": "lotus_outline.svg",
        "anim_class": "lotus-outline-animated",
        "alt": "Lotus outline icon representing vision",
    },
    "sword_of_resolve": {
        "svg": "trident.svg",
        "anim_class": "trident-animated",
        "alt": "Trident icon representing resolve",
    },
    # Fall of Dharma
    "game_of_fate": {
        "svg": "dice.svg",
        "anim_class": "dice-animated",
        "alt": "Dice icon representing the game of fate",
    },
    "silence_of_protest": {
        "svg": "dharma_collapse.svg",
        "anim_class": "collapse-animated",
        "alt": "Collapsed dharma icon representing silent protest",
    },
    "divine_intervention": {
        "svg": "restore_flower.svg",
        "anim_class": "restore-animated",
        "alt": "Restored flower icon representing grace",
    },
    # Weapon Quest
    "forest_of_austerity": {
        "svg": "forest.svg",
        "anim_class": "forest-animated",
        "alt": "Forest icon representing austerity",
    },
    "shiva_and_the_hunter": {
        "svg": "bow_and_arrow.svg",
        "anim_class": "bow-animated",
        "alt": "Bow and arrow icon representing the hunter",
    },
    "celestial_audience": {
        "svg": "galaxy.svg",
        "anim_class": "galaxy-animated",
        "alt": "Galaxy icon representing celestial audience",
    },
    "trial_of_heaven": {
        "svg": "bell.svg",
        "anim_class": "bell-animated",
        "alt": "Bell icon representing the trial of heaven",
    },
    # Birth of Dharma
    "cosmic_egg": {
        "svg": "cosmic_egg.svg",
        "anim_class": "cosmic-egg-animated",
        "alt": "Cosmic egg icon representing the first breath",
    },
    "wheel_turns": {
        "svg": "wheel_turns.svg",
        "anim_class": "wheel-turns-animated",
        "alt": "Turning wheel icon representing the golden parchment",
    },
    "river_oath": {
        "svg": "river_oath.svg",
        "anim_class": "river-oath-animated",
        "alt": "River oath icon representing flowing wisdom",
    },
    "balance_restored": {
        "svg": "balance_restored.svg",
        "anim_class": "balance-restored-animated",
        "alt": "Balance restored icon representing sacred glyphs",
    },
    "first_flame": {
        "svg": "sacred_flame.svg",
        "anim_class": "first-flame-animated",
        "alt": "Sacred flame icon representing the awakening scroll",
    },
    # Trials of Karna
    "suns_gift": {
        "svg": "suns_gift.svg",
        "anim_class": "suns-gift-animated",
        "alt": "Sun's gift icon representing Surya's boon",
    },
    "brahmin_curse": {
        "svg": "brahmins_curse.svg",
        "anim_class": "brahmin-curse-animated",
        "alt": "Brahmin's curse icon representing fated forgetfulness",
    },
    "friends_vow": {
        "svg": "friends_vow.svg",
        "anim_class": "friends-vow-animated",
        "alt": "Friend's vow icon representing loyalty",
    },
    "birth_revealed": {
        "svg": "birth_revealed.svg",
        "anim_class": "birth-revealed-animated",
        "alt": "Birth revealed icon representing hidden lineage",
    },
    "final_arrow": {
        "svg": "final_arrow.svg",
        "anim_class": "final-arrow-animated",
        "alt": "Final arrow icon representing Karna's fate",
    },
}

CHAPTER_TITLES = {
    "gita_scroll": "Gita Scroll",
    "fall_of_dharma": "Fall of Dharma",
    "weapon_quest": "Weapon Quest",
    "birth_of_dharma": "Birth of Dharma",
    "trials_of_karna": "Trials of Karna",
}

CHAPTER_BACKGROUNDS = {
    "gita_scroll": "gita_scroll.webp",
    "fall_of_dharma": "fall_of_dharma.webp",
    "weapon_quest": "weapon_quest.webp",
    "birth_of_dharma": "birth_of_dharma.webp",
    "trials_of_karna": "trials_of_karna.webp",
}

SOUNDSCAPE_ARTWORK = {
    "gita_scroll": {
        "default": {"subfolder": "textures", "filename": "gita_scroll.webp"},
        "lotus_of_doubt": {
            "subfolder": "artworks",
            "filename": "lotus_of_doubt.jpeg",
        },
        "chakra_of_dharma": {
            "subfolder": "artworks",
            "filename": "chakra_of_dharma.jpeg",
        },
    },
    "fall_of_dharma": {
        "default": {"subfolder": "textures", "filename": "fall_of_dharma.webp"},
        "game_of_fate": {
            "subfolder": "artworks",
            "filename": "Game of Fate.jpeg",
        },
        "silence_of_protest": {
            "subfolder": "artworks",
            "filename": "Silence of Protest.jpeg",
        },
    },
    "weapon_quest": {
        "default": {"subfolder": "textures", "filename": "weapon_quest.webp"},
        "forest_of_austerity": {
            "subfolder": "textures",
            "filename": "weapon_quest.webp",
        },
        "shiva_and_the_hunter": {
            "subfolder": "textures",
            "filename": "weapon_quest.webp",
        },
    },
    "birth_of_dharma": {
        "default": {"subfolder": "textures", "filename": "birth_of_dharma.webp"},
        "cosmic_egg": {
            "subfolder": "textures",
            "filename": "birth_of_dharma.webp",
        },
        "wheel_turns": {
            "subfolder": "textures",
            "filename": "birth_of_dharma.webp",
        },
    },
    "trials_of_karna": {
        "default": {"subfolder": "textures", "filename": "trials_of_karna.webp"},
        "suns_gift": {
            "subfolder": "textures",
            "filename": "trials_of_karna.webp",
        },
        "brahmin_curse": {
            "subfolder": "textures",
            "filename": "trials_of_karna.webp",
        },
    },
}

SOUNDSCAPE_DESCRIPTIONS = {
    "gita_scroll": "Crimson dusk settles over Kurukshetra while Krishna's counsel shimmers between the strings and tambura drones.",
    "fall_of_dharma": "Echoes of judgement halls and solemn vows weave with temple bells to honor the gravity of the court.",
    "weapon_quest": "Forest breezes rustle beside the seeker—flutes, drums, and distant thunder accompany each trial.",
    "birth_of_dharma": "Cosmic breaths, cradle songs, and gentle chimes cradle the origin spark of righteousness.",
    "trials_of_karna": "Sunlit brass and low murmurings follow Karna's vow, balancing valor with the ache of destiny.",
}

STORY_DISPLAY_TITLES = {
    "sword_of_resolve": "Trident of Resolve",
}

CHANT_LINES = {
    "gita_scroll": {
        "lotus_of_doubt": [
            "Om Shanti Shanti Shanti",
            "Om Shanti Shanti Shanti",
            "Om Shanti Shanti Shanti",
            "Om Shanti Shanti Shanti",
        ],
        "chakra_of_dharma": [
            "Om Namo Bhagavate Vasudevaya",
            "Om Namo Bhagavate Vasudevaya",
            "Om Namo Bhagavate Vasudevaya",
            "Om Namo Bhagavate Vasudevaya",
        ],
        "spiral_of_vision": [
            "Om Namo Narayanaya",
            "Om Namo Narayanaya",
            "Om Namo Narayanaya",
            "Om Namo Narayanaya",
        ],
        "sword_of_resolve": [
            "Om Tat Sat",
            "Om Tat Sat",
            "Om Tat Sat",
            "Om Tat Sat",
        ],
    },
    "fall_of_dharma": {
        "game_of_fate": [
            "Asato maa sadgamaya",
            "Tamaso maa jyotirgamaya",
            "Mrityor maa amritam gamaya",
            "Om Shanti Shanti Shanti",
        ],
        "silence_of_protest": [
            "Om Shanti Shanti Shanti",
            "Om Shanti Shanti Shanti",
            "Om Shanti Shanti Shanti",
            "Om Shanti Shanti Shanti",
        ],
        "divine_intervention": [
            "Hare Krishna Hare Krishna",
            "Krishna Krishna Hare Hare",
            "Hare Rama Hare Rama",
            "Rama Rama Hare Hare",
        ],
    },
    "weapon_quest": {
        "forest_of_austerity": [
            "Om Bhur Bhuvah Swaha",
            "Tat Savitur Varenyam",
            "Bhargo Devasya Dhimahi",
            "Dhiyo Yo Nah Prachodayat",
        ],
        "shiva_and_the_hunter": [
            "Om Namah Shivaya",
            "Om Namah Shivaya",
            "Om Namah Shivaya",
            "Om Namah Shivaya",
        ],
        "celestial_audience": [
            "Om Indraya Namah",
            "Om Indraya Namah",
            "Om Indraya Namah",
            "Om Indraya Namah",
        ],
        "trial_of_heaven": [
            "Tryambakam yajamahe",
            "Sugandhim Pushtivardhanam",
            "Urvarkam iva bandhanan",
            "Mrityor mukshiya mamritat",
        ],
    },
    "birth_of_dharma": {
        "cosmic_breath": [
            "Om Pranaya Namah",
            "Om Pranaya Namah",
            "Om Pranaya Namah",
            "Om Pranaya Namah",
        ],
        "golden_parchment": [
            "Om Saraswatyai Namah",
            "Om Saraswatyai Namah",
            "Om Saraswatyai Namah",
            "Om Saraswatyai Namah",
        ],
        "flowing_wisdom": [
            "Om Namo Narayanaya",
            "Om Namo Narayanaya",
            "Om Namo Narayanaya",
            "Om Namo Narayanaya",
        ],
        "glyphs_of_dharma": [
            "Om Gam Ganapataye Namah",
            "Om Gam Ganapataye Namah",
            "Om Gam Ganapataye Namah",
            "Om Gam Ganapataye Namah",
        ],
        "awakening_scroll": [
            "Om Sri Gurubhyo Namah",
            "Om Sri Gurubhyo Namah",
            "Om Sri Gurubhyo Namah",
            "Om Sri Gurubhyo Namah",
        ],
        # narrative-key aliases
        "cosmic_egg": [
            "Om Pranaya Namah",
            "Om Pranaya Namah",
            "Om Pranaya Namah",
            "Om Pranaya Namah",
        ],
        "wheel_turns": [
            "Om Saraswatyai Namah",
            "Om Saraswatyai Namah",
            "Om Saraswatyai Namah",
            "Om Saraswatyai Namah",
        ],
        "river_oath": [
            "Om Namo Narayanaya",
            "Om Namo Narayanaya",
            "Om Namo Narayanaya",
            "Om Namo Narayanaya",
        ],
        "balance_restored": [
            "Om Gam Ganapataye Namah",
            "Om Gam Ganapataye Namah",
            "Om Gam Ganapataye Namah",
            "Om Gam Ganapataye Namah",
        ],
        "first_flame": [
            "Om Sri Gurubhyo Namah",
            "Om Sri Gurubhyo Namah",
            "Om Sri Gurubhyo Namah",
            "Om Sri Gurubhyo Namah",
        ],
    },
    "trials_of_karna": {
        "suns_gift": [
            "Om Suryaya Namah",
            "Om Suryaya Namah",
            "Om Suryaya Namah",
            "Om Suryaya Namah",
        ],
        "brahmin_curse": [
            "Asato maa sadgamaya",
            "Tamaso maa jyotirgamaya",
            "Mrityor maa amritam gamaya",
            "Om Shanti Shanti Shanti",
        ],
        "friends_vow": [
            "Om Mitraya Namah",
            "Om Mitraya Namah",
            "Om Mitraya Namah",
            "Om Mitraya Namah",
        ],
        "birth_revealed": [
            "Om Kuntidevyai Namah",
            "Om Kuntidevyai Namah",
            "Om Kuntidevyai Namah",
            "Om Kuntidevyai Namah",
        ],
        "final_arrow": [
            "Tryambakam yajamahe",
            "Sugandhim Pushtivardhanam",
            "Urvarkam iva bandhanan",
            "Mrityor mukshiya mamritat",
        ],
    },
}

BIRTH_STORY_AUDIO_MAP = {
    "cosmic_egg": "cosmic_breath",
    "wheel_turns": "awakening_scroll",
    "river_oath": "flowing_wisdom",
    "balance_restored": "glyphs_of_dharma",
    "first_flame": "golden_parchment",
}

BACKGROUND_OVERLAYS = {
    "default": {
        "background": (
            "radial-gradient(circle at 20% 15%, rgba(250, 230, 180, 0.22), rgba(250, 230, 180, 0) 55%), "
            "radial-gradient(circle at 80% 30%, rgba(255, 196, 140, 0.16), rgba(255, 196, 140, 0) 60%), "
            "linear-gradient(140deg, rgba(60, 38, 15, 0.25), rgba(32, 18, 8, 0.38)), "
            "radial-gradient(circle at 50% 50%, rgba(0, 0, 0, 0) 62%, rgba(0, 0, 0, 0.42) 100%)"
        ),
        "size": "160% 160%, 180% 180%, 100% 100%, 100% 100%",
        "position": "10% 10%, 90% 20%, center, center",
        "blend_layers": "screen, screen, soft-light, multiply",
        "mix": "soft-light",
        "animation": "none",
        "opacity": "0.85",
    },
    "gita_scroll": {
        "background": (
            "radial-gradient(circle at 15% 18%, rgba(102, 197, 255, 0.32), rgba(102, 197, 255, 0) 55%), "
            "radial-gradient(circle at 85% 25%, rgba(255, 255, 255, 0.24), rgba(255, 255, 255, 0) 60%), "
            "linear-gradient(115deg, rgba(15, 52, 96, 0.35), rgba(71, 113, 158, 0.25) 55%, rgba(200, 224, 255, 0.35)), "
            "radial-gradient(circle at 50% 55%, rgba(255, 255, 255, 0.05) 0%, rgba(0, 5, 15, 0.52) 100%)"
        ),
        "size": "200% 200%, 220% 220%, 100% 100%, 100% 100%",
        "position": "0% 15%, 80% 5%, center, center",
        "blend_layers": "screen, screen, soft-light, multiply",
        "mix": "soft-light",
        "animation": "waterShimmer 42s ease-in-out infinite",
        "opacity": "0.9",
    },
    "fall_of_dharma": {
        "background": (
            "radial-gradient(circle at 18% 22%, rgba(255, 163, 102, 0.32), rgba(255, 163, 102, 0) 58%), "
            "radial-gradient(circle at 78% 18%, rgba(255, 89, 48, 0.26), rgba(255, 89, 48, 0) 55%), "
            "linear-gradient(135deg, rgba(73, 22, 7, 0.45), rgba(25, 8, 3, 0.55)), "
            "radial-gradient(circle at 50% 52%, rgba(40, 5, 0, 0.05) 0%, rgba(7, 0, 0, 0.55) 100%)"
        ),
        "size": "190% 190%, 210% 210%, 100% 100%, 100% 100%",
        "position": "0% 0%, 100% 0%, center, center",
        "blend_layers": "screen, screen, soft-light, multiply",
        "mix": "soft-light",
        "animation": "emberDrift 34s linear infinite",
        "opacity": "0.92",
    },
    "weapon_quest": {
        "background": (
            "radial-gradient(circle at 16% 24%, rgba(126, 217, 87, 0.28), rgba(126, 217, 87, 0) 55%), "
            "radial-gradient(circle at 82% 28%, rgba(255, 241, 176, 0.22), rgba(255, 241, 176, 0) 60%), "
            "linear-gradient(130deg, rgba(25, 78, 32, 0.42), rgba(10, 36, 18, 0.45)), "
            "radial-gradient(circle at 50% 50%, rgba(10, 18, 7, 0.08) 0%, rgba(4, 9, 2, 0.5) 100%)"
        ),
        "size": "200% 200%, 220% 220%, 100% 100%, 100% 100%",
        "position": "5% 0%, 95% 10%, center, center",
        "blend_layers": "screen, screen, soft-light, multiply",
        "mix": "soft-light",
        "animation": "forestMotes 38s ease-in-out infinite",
        "opacity": "0.88",
    },
    "birth_of_dharma": {
        "background": (
            "radial-gradient(circle at 22% 24%, rgba(255, 214, 153, 0.32), rgba(255, 214, 153, 0) 58%), "
            "radial-gradient(circle at 78% 26%, rgba(255, 177, 194, 0.22), rgba(255, 177, 194, 0) 55%), "
            "linear-gradient(125deg, rgba(214, 127, 61, 0.38), rgba(133, 76, 19, 0.4)), "
            "radial-gradient(circle at 50% 52%, rgba(255, 255, 255, 0.02) 0%, rgba(41, 14, 0, 0.48) 100%)"
        ),
        "size": "190% 190%, 210% 210%, 100% 100%, 100% 100%",
        "position": "0% 5%, 90% 5%, center, center",
        "blend_layers": "screen, screen, soft-light, multiply",
        "mix": "soft-light",
        "animation": "dawnBloom 46s ease-in-out infinite",
        "opacity": "0.9",
    },
    "trials_of_karna": {
        "background": (
            "radial-gradient(circle at 20% 20%, rgba(255, 206, 102, 0.32), rgba(255, 206, 102, 0) 55%), "
            "radial-gradient(circle at 80% 22%, rgba(255, 112, 67, 0.26), rgba(255, 112, 67, 0) 60%), "
            "linear-gradient(140deg, rgba(108, 43, 10, 0.48), rgba(45, 12, 0, 0.48)), "
            "radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.04) 0%, rgba(18, 0, 0, 0.55) 100%)"
        ),
        "size": "200% 200%, 220% 220%, 100% 100%, 100% 100%",
        "position": "0% 10%, 90% 0%, center, center",
        "blend_layers": "screen, screen, soft-light, multiply",
        "mix": "soft-light",
        "animation": "solarPulse 36s ease-in-out infinite",
        "opacity": "0.93",
    },
}

