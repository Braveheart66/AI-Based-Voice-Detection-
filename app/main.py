from fastapi import FastAPI
from app.api.routes import fraud, deepfake

app = FastAPI(
    title="AI-Based Fraud & Deepfake Detection",
    version="1.0"
)

app.include_router(fraud.router, prefix="/api/fraud", tags=["Fraud"])
app.include_router(deepfake.router, prefix="/api/deepfake", tags=["Deepfake"])
