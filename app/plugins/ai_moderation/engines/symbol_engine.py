import re

# ===============================
# Symbol normalization map
# ===============================

SYMBOL_MAP = {
    "@": "a",
    "$": "s",
    "0": "o",
    "1": "i",
    "!": "i",
    "3": "e",
    "4": "a",
    "5": "s",
    "7": "t",
    "*": "",
}

# Common masked abuse patterns
MASKED_PATTERNS = [
    r"f[\W_]*u[\W_]*c[\W_]*k",
    r"b[\W_]*i[\W_]*t[\W_]*c[\W_]*h",
    r"i[\W_]*d[\W_]*i[\W_]*o[\W_]*t",
]


def normalize_symbols(text: str) -> str:
    """Convert leetspeak to normal text"""
    text = text.lower()

    # Replace mapped symbols
    for sym, char in SYMBOL_MAP.items():
        text = text.replace(sym, char)

    # Remove repeated special chars
    text = re.sub(r"[^\w\s]", "", text)

    return text


def detect_masked_abuse(text: str) -> float:
    """Detect heavily masked abuse patterns"""
    lowered = text.lower()

    for pattern in MASKED_PATTERNS:
        if re.search(pattern, lowered):
            return 0.7  # strong suspicion

    return 0.0


# ===============================
# Main engine function
# ===============================

def analyze_symbols(text: str) -> float:
    if not text.strip():
        return 0.0

    normalized = normalize_symbols(text)
    masked_score = detect_masked_abuse(text)

    # Mild boost if normalization changes text a lot
    distortion = 0.0
    if normalized != text.lower():
        distortion = 0.2

    return min(masked_score + distortion, 0.8)
