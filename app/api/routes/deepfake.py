from fastapi import APIRouter, UploadFile, File, HTTPException
import tempfile
import os

from app.services.deepfake_service import detect_image_deepfake
from app.services.video_service import detect_video_deepfake

router = APIRouter()


# -------------------------------
# Image Deepfake Detection
# -------------------------------
@router.post("/image")
async def deepfake_image(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload an image (.jpg, .jpeg, .png)."
        )

    suffix = os.path.splitext(file.filename)[-1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        result = detect_image_deepfake(tmp_path)
        return result
    finally:
        os.remove(tmp_path)


# -------------------------------
# Video Deepfake Detection
# -------------------------------
@router.post("/video")
async def deepfake_video(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".mp4"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload a video (.mp4)."
        )

    suffix = os.path.splitext(file.filename)[-1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        result = detect_video_deepfake(tmp_path)
        return result
    finally:
        os.remove(tmp_path)
