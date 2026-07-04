from fastapi import APIRouter
from .. import inference
from ..schemas import ToxicRequest, ToxicResponse

router = APIRouter()

@router.post("/predict", response_model=ToxicResponse)
def predict_toxic(data: ToxicRequest):
    return inference.predict_toxic_text(data.text)
