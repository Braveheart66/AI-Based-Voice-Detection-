from fastapi import APIRouter, UploadFile, File
import tempfile, os
from app.services.audio_service import detect_fraud_from_audio

router = APIRouter()

@router.post("/audio")
async def fraud_audio(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename)[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    result = detect_fraud_from_audio(tmp_path)
    os.remove(tmp_path)
    return result
