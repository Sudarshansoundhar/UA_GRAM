# Emoji cyberbullying intelligence

TOXIC_EMOJI_MAP = {
    "🤡": 0.6,  # mocking
    "💀": 0.5,  # humiliation
    "🐍": 0.7,  # betrayal / snake insult
    "🐷": 0.7,  # body shaming
    "🖕": 0.9,  # explicit insult
    "🤮": 0.6,  # disgust bullying
    "🤢": 0.6,
    "💩": 0.7,
    "👎": 0.4,
}

# Combo bullying patterns
TOXIC_COMBOS = [
    ("🤡", "💀"),  # mock + humiliation
    ("🐍", "🤡"),  # betrayal mock
    ("💩", "🤡"),
]


def analyze_emojis(text: str) -> float:
    if not text:
        return 0.0

    score = 0.0

    # Single emoji scoring
    for emoji, val in TOXIC_EMOJI_MAP.items():
        if emoji in text:
            score = max(score, val)

    # Combo detection
    for e1, e2 in TOXIC_COMBOS:
        if e1 in text and e2 in text:
            score = max(score, 0.85)

    return score
