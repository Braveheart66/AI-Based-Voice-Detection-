from fastapi import APIRouter, UploadFile, File
from app.services.deepfake_service import detect_image_deepfake

router = APIRouter()

@router.post("/image")
async def deepfake_image(file: UploadFile = File(...)):
    return detect_image_deepfake(file)
