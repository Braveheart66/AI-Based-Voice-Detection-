from call_fraud_detection import predict_fraud
from hindi_to_hinglish import hindi_to_hinglish

# 🔐 High-risk fraud keywords (industry-style rules)
FRAUD_PATTERNS = [
    "otp",
    "one time password",
    "verification code",
    "share otp",
    "bank otp",
    "account blocked",
    "account suspended",
    "kyc",
    "urgent action",
    "press 1",
    "press one",
    "immediately",
    "customer care",
    "bank account",
    "debit card",
    "credit card"
]


def rule_based_fraud(text: str) -> bool:
    print("🔴 RULE CHECK TEXT >>>", text.lower())
    return True



def detect_fraud(text: str, language: str = "en"):
    if "otp" in text.lower():
        return {
            "fraud": True,
            "confidence": 1.0,
            "source": "forced-test"
        }

    if not text or not text.strip():
        return {
            "fraud": False,
            "confidence": 0.0,
            "reason": "empty input"
        }

    # 🌐 Language normalization
    if language.lower() != "en":
        text = hindi_to_hinglish(text)

    # 🚨 RULE-BASED OVERRIDE (HIGHEST PRIORITY)
    if rule_based_fraud(text):
        return {
            "fraud": True,
            "confidence": 0.99,
            "reason": "OTP / banking scam pattern detected",
            "source": "rule-based"
        }

    # 🤖 ML MODEL PREDICTION
    prediction, confidence = predict_fraud(text)

    result = "genuine"
    if confidence >= 0.25:
        result = "fraud"
    elif confidence >= 0.4:
        result = "suspicious"

    return {
        "fraud": result != "genuine",
        "confidence": round(float(confidence), 4),
        "result": result,
        "source": "ml"
    }
