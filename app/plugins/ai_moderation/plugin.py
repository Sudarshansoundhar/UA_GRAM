from .engines.text_engine import analyze_text
from .engines.symbol_engine import analyze_symbols
from .engines.emoji_engine import analyze_emojis

class AIModerationPlugin:
    def __init__(self):
        self.enabled = True

    def process(self, content: str):
        if not self.enabled or not content:
            return {"allowed": True, "score": 0.0, "reasons": []}

        text_score = analyze_text(content)
        symbol_score = analyze_symbols(content)
        emoji_score = analyze_emojis(content)

        # Weighted fusion
        final_score = min(
            text_score + symbol_score * 0.5 + emoji_score * 0.7,
            1.0
        )

        reasons = []

        if text_score > 0.6:
            reasons.append("Toxic language detected")

        if symbol_score > 0.3:
            reasons.append("Masked or distorted abusive text")

        if emoji_score > 0.4:
            reasons.append("Offensive emoji usage")

        allowed = final_score < 0.75

        return {
            "allowed": allowed,
            "score": float(final_score),
            "reasons": reasons,
            "breakdown": {
                "text": text_score,
                "symbol": symbol_score,
                "emoji": emoji_score
            }
        }


ai_plugin = AIModerationPlugin()
