import os

class AIConfig:
    ENABLED = os.getenv("AI_ENABLED", "false").lower() == "true"

    # Engine toggles
    ENABLE_TEXT = True
    ENABLE_SYMBOL = True
    ENABLE_EMOJI = True
    ENABLE_IMAGE = True

    # Thresholds
    WARN_THRESHOLD = 0.5
    BLOCK_THRESHOLD = 0.75


ai_config = AIConfig()
