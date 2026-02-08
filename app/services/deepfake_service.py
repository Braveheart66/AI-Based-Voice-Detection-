from unittest import result
import torch
from pathlib import Path
from app.services.vision.model import get_deepfake_model, predict_image

BASE_DIR = Path(__file__).resolve().parent / "vision"
MODEL_PATH = BASE_DIR / "deepfake_cnn.pth"

_model = None

def _load_model():
    global _model
    if _model is None:
        model = get_deepfake_model()
        state_dict = torch.load(MODEL_PATH, map_location="cpu")
        model.load_state_dict(state_dict)
        model.eval()
        _model = model
    return _model


def detect_image_deepfake(image_path: str):
    model = _load_model()
    confidence = predict_image(model, image_path)

    if confidence >= 0.85:
        result = "deepfake"
    elif confidence >= 0.6:
        result = "suspicious"
    else:
        result = "real"

    return {
        "deepfake": confidence > 0.5,
        "confidence": round(confidence, 4),
        "result": result
    }
