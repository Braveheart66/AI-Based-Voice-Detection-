import torch
from app.services.vision.preprocess_faces_unseen import preprocess_image

MODEL_PATH = "app/services/vision/deepfake_cnn.pth"

# Load model
model = torch.load(MODEL_PATH, map_location="cpu")
model.eval()

# Load test image
image_path = "test.jpg"   # put any face image here
image_tensor = preprocess_image(image_path)

# Run inference
with torch.no_grad():
    output = model(image_tensor)
    confidence = float(output.item())

print("Deepfake confidence:", confidence)
print("Prediction:", "DEEPFAKE" if confidence > 0.5 else "REAL")
