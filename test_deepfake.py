import torch
from app.services.vision.model import get_deepfake_model
from app.services.vision.preprocess_faces_unseen import preprocess_image
import app.services.vision.model as m
print("MODEL FILE USED:", m.__file__)


MODEL_PATH = "app/services/vision/deepfake_cnn.pth"

model = get_deepfake_model()
state_dict = torch.load(MODEL_PATH, map_location="cpu")
model.load_state_dict(state_dict)
model.eval()

image_tensor = preprocess_image("test.png")

with torch.no_grad():
    logits = model(image_tensor)
    probs = torch.softmax(logits, dim=1)
    deepfake_prob = probs[0, 1].item()  # class 1 = deepfake

print("Deepfake confidence:", round(deepfake_prob, 4))
print("Prediction:", "DEEPFAKE" if deepfake_prob >= 0.5 else "REAL")
