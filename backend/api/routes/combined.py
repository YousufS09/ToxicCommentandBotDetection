from fastapi import APIRouter

from .. import inference
from ..schemas import CombinedAnalysisRequest, CombinedAnalysisResponse


router = APIRouter()


@router.post("/combined", response_model=CombinedAnalysisResponse)
def analyze_combined(payload: CombinedAnalysisRequest):
    return inference.analyze_combined_payload(payload)
