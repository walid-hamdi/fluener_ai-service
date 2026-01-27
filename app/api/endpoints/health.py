"""Health check endpoint"""
from fastapi import APIRouter
from app.models.schemas import HealthResponse
from app.core.models import models
from app.services.ollama_service import OllamaService

router = APIRouter()

@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Check service health and model status"""
    return HealthResponse(
        status="healthy",
        models={
            "whisper": "loaded" if models.whisper else "not_loaded",
            "mistral": await OllamaService.check_health(),
            "tts": "loaded" if models.styletts2 else "not_loaded"
        }
    )