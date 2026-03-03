from fastapi import FastAPI
from schemas import AnalyzeRequest, AnalyzeResponse
from core.normalizer import normalize_text
from core.rules import rule_based_detection
from core.scorer import calculate_score
from core.decision import decide_action

app = FastAPI(title="Cyberbullying AI Service")

@app.post("/ai/analyze", response_model=AnalyzeResponse)
def analyze_content(data: AnalyzeRequest):
    clean_text = normalize_text(data.text)

    rule_result = rule_based_detection(clean_text)
    score, categories = calculate_score(
        clean_text,
        rule_result,
        data.user_history.previous_flags
    )

    decision = decide_action(score)

    return {
        "is_bullying": score > 0.3,
        "severity": decision["severity"],
        "score": score,
        "categories": categories,
        "recommended_action": decision["action"],
        "explanation": decision["reason"]
    }
