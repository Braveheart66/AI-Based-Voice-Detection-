from fastapi import APIRouter
from pydantic import BaseModel
from app.services.fraud_service import detect_fraud

router = APIRouter()

class FraudRequest(BaseModel):
    text: str
    language: str = "en"

@router.post("/text")
def detect_fraud_text(req: FraudRequest):
    return detect_fraud(req.text, req.language)
