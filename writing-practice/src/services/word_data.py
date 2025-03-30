"""
Service for managing kanji word data and generation.
"""

KANJI_WORDS = [
    {
        "kanji": "水",
        "reading": "みず",
        "meaning": "water",
        "level": "N5"
    },
    {
        "kanji": "火",
        "reading": "ひ",
        "meaning": "fire",
        "level": "N5"
    },
    {
        "kanji": "山",
        "reading": "やま",
        "meaning": "mountain",
        "level": "N5"
    },
    {
        "kanji": "川",
        "reading": "かわ",
        "meaning": "river",
        "level": "N5"
    },
    {
        "kanji": "木",
        "reading": "き",
        "meaning": "tree",
        "level": "N5"
    }
]

def get_random_word():
    """Get a random kanji word from the collection."""
    import random
    return random.choice(KANJI_WORDS)

def get_word_by_level(level):
    """Get a random kanji word of a specific JLPT level."""
    import random
    level_words = [word for word in KANJI_WORDS if word["level"] == level]
    return random.choice(level_words) if level_words else None 