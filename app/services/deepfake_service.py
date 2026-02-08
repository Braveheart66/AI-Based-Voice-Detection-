import torch
from preprocess_faces_unseen import preprocess_image

MODEL_PATH = "deepfake_cnn.pth"
model = torch.load(MODEL_PATH, map_location="cpu")
model.eval()

def detect_image_deepfake(file):
    image = preprocess_image(file.file)
    output = model(image)

    confidence = float(output.item())

    return {
        "deepfake": confidence > 0.5,
        "confidence": confidence
    }
