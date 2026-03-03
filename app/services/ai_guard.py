# app/services/ai_guard.py

from app.plugins.ai_moderation.plugin import ai_plugin


def moderate_text(text: str):
    """
    Shared AI moderation wrapper.
    Uses same AI engine as DM chat.
    """

    ai_result = ai_plugin.process(content=text)
    score = ai_result.get("score", 0)
    reasons = ai_result.get("reasons", [])

    if score > 0.75:
        level = "block"
    elif score > 0.5:
        level = "warn"
    else:
        level = "ok"

    return {
        "level": level,
        "score": score,
        "reasons": reasons,
    }