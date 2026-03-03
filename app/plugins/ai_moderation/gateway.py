from .config import ai_config
from .engines.text_engine import analyze_text
from .engines.symbol_engine import analyze_symbols
from .engines.emoji_engine import analyze_emojis
from .engines.image_engine import analyze_image

class AIGateway:
    def analyze(self, content=None, image=None):
        scores = []

        if content:
            if ai_config.ENABLE_SYMBOL:
                scores.append(analyze_symbols(content))

            if ai_config.ENABLE_EMOJI:
                scores.append(analyze_emojis(content))

            if ai_config.ENABLE_TEXT:
                scores.append(analyze_text(content))

        if image and ai_config.ENABLE_IMAGE:
            scores.append(analyze_image(image))

        if not scores:
            return {"allowed": True}

        final_score = max(scores)

        if final_score >= ai_config.BLOCK_THRESHOLD:
            return {"allowed": False, "action": "block", "score": final_score}

        if final_score >= ai_config.WARN_THRESHOLD:
            return {"allowed": True, "action": "warn", "score": final_score}

        return {"allowed": True, "action": "allow", "score": final_score}
