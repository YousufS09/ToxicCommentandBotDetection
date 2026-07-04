from pydantic import BaseModel
from typing import Optional

class ToxicRequest(BaseModel):
    text: str

class ToxicResponse(BaseModel):
    label: str
    confidence: float
    interpretation: str


class BotRequest(BaseModel):
    description: Optional[str] = ""
    followers_count: int = 0
    following_count: int = 0
    tweet_count: int = 0
    created_at: Optional[str] = None
    account_age_days: Optional[int] = None

class BotResponse(BaseModel):
    prediction: str
    confidence: float
    interpretation: str
    account_age_days: int


class CombinedAnalysisRequest(BaseModel):
    comment: str
    description: Optional[str] = ""
    followers_count: int = 0
    following_count: int = 0
    tweet_count: int = 0
    created_at: Optional[str] = None
    account_age_days: Optional[int] = None


class CombinedAnalysisResponse(BaseModel):
    toxic: ToxicResponse
    bot: BotResponse
    toxicity_risk: float
    bot_risk: float
    risk_score: float
    risk_level: str
    summary: str
    recommendation: str
