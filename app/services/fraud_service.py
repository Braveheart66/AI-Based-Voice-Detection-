from call_fraud_detection import predict_fraud
from hindi_to_hinglish import hindi_to_hinglish

def detect_fraud(text: str, language: str):
    if language.lower() != "en":
        text = hindi_to_hinglish(text)

    prediction, confidence = predict_fraud(text)

    return {
        "fraud": bool(prediction),
        "confidence": confidence
    }
