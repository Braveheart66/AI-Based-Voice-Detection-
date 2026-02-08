import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
from pathlib import Path

# ----------------------------
# Paths
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "deepfake_cnn.pth"

# ----------------------------
# Device
# ----------------------------
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ----------------------------
# Model Architecture
# ----------------------------
def get_deepfake_model():
    model = models.efficientnet_b0(weights=None)
    model.classifier[1] = nn.Linear(
        model.classifier[1].in_features, 2
    )
    return model


# ----------------------------
# Lazy-loaded Singleton Model
# ----------------------------
_model = None

def get_model():
    """
    Load the deepfake model once and reuse it.
    """
    global _model

    if _model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Deepfake model not found at: {MODEL_PATH}"
            )

        model = get_deepfake_model().to(DEVICE)

        state_dict = torch.load(MODEL_PATH, map_location=DEVICE)
        model.load_state_dict(state_dict)

        model.eval()
        _model = model

        print("✅ Deepfake image model loaded successfully")

    return _model


# ----------------------------
# Image Preprocessing
# ----------------------------
_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


# ----------------------------
# Image Prediction
# ----------------------------
def predict_image(model, image_path: str) -> float:
    image = Image.open(image_path).convert("RGB")

    tensor = _transform(image).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        outputs = model(tensor)
        probs = torch.softmax(outputs, dim=1)

    # 🔍 Debug (keep during testing)
    print("LOGITS:", outputs.cpu().tolist())
    print("PROBS:", probs.cpu().tolist())

    # Deepfake probability = class index 1
    confidence = float(probs[0][0])

    # 🛡️ Safety clamp (never expose 1.0)
    confidence = min(confidence, 0.99)

    return confidence
