import cv2
import os
import uuid
from PIL import Image
from app.services.vision.model import predict_image
from app.services.vision.model import get_model


def detect_video_deepfake(video_path: str):
    model = get_model()

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError("Could not open video file")

    confidences = []
    frame_count = 0

    while frame_count < 5:  # sample only first 5 frames
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        # Generate SAFE temp filename
        img_path = f"{uuid.uuid4().hex}.jpg"

        # Save frame
        cv2.imwrite(img_path, frame)

        try:
            confidence = predict_image(model, img_path)
            confidences.append(confidence)
        finally:
            # Ensure file is fully released before delete
            if os.path.exists(img_path):
                os.remove(img_path)

    cap.release()

    if not confidences:
        raise RuntimeError("No frames processed from video")

    avg_confidence = sum(confidences) / len(confidences)

    return {
        "deepfake": avg_confidence > 0.5,
        "confidence": round(float(avg_confidence), 4)
    }
