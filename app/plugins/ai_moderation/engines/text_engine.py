from transformers import pipeline
import threading

_model = None
_lock = threading.Lock()

def load_model():
    global _model
    with _lock:
        if _model is None:
            print("[AI] Loading toxicity model...")
            _model = pipeline(
                "text-classification",
                model="unitary/toxic-bert"
            )
            print("[AI] Model ready.")
    return _model


def analyze_text(text: str) -> float:
    if not text.strip():
        return 0.0

    try:
        model = load_model()
        output = model(text)

        score = float(output[0]["score"])
        return score

    except Exception as e:
        print("[AI ERROR]", e)
        return 0.0
