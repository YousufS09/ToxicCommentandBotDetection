from fastapi import APIRouter
from .. import inference
from ..schemas import BotRequest, BotResponse

router = APIRouter()

# --------------------------------------------------
# Prediction endpoint
# --------------------------------------------------
@router.post("/predict", response_model=BotResponse)
def predict_bot(user: BotRequest):
    return inference.predict_bot_user(user)
