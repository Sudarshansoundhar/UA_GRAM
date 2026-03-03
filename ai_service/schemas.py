from pydantic import BaseModel
from typing import List

class UserHistory(BaseModel):
    previous_flags: int = 0

class AnalyzeRequest(BaseModel):
    text: str
    source: str
    language_hint: str = "en"
    user_history: UserHistory

class AnalyzeResponse(BaseModel):
    is_bullying: bool
    severity: str
    score: float
    categories: List[str]
    recommended_action: str
    explanation: str
