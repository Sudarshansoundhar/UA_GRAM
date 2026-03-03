# app/services/bullying_detector.py

BULLYING_KEYWORDS = {
    "idiot": 0.6,
    "stupid": 0.6,
    "loser": 0.7,
    "ugly": 0.8,
    "hate you": 0.9,
    "kill yourself": 1.0
}


def analyze_text(text: str):
    text = text.lower()

    score = 0.0
    matched_words = []

    for word, weight in BULLYING_KEYWORDS.items():
        if word in text:
            score = max(score, weight)
            matched_words.append(word)

    return {
        "is_bullying": score >= 0.6,
        "score": score,
        "matched_words": matched_words
    }
