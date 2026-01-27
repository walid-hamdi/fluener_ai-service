"""Speech-to-Text endpoint"""
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends, Request
from app.models.schemas import STTResponse
from app.services.whisper_service import WhisperService
from app.core.security import verify_api_key
from slowapi import Limiter
from slowapi.util import get_remote_address
import time

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.post("/stt", response_model=STTResponse, tags=["Speech-to-Text"])
@limiter.limit("20/minute")
async def speech_to_text(
    request: Request,
    audio: UploadFile = File(...),
    language: str = Form(...),
    api_key: str = Depends(verify_api_key)
):
    """Convert speech to text using OpenAI Whisper"""
    start_time = time.time()
    
    try:
        content = await audio.read()
        text = await WhisperService.transcribe(
            content,
            language,
            audio.filename or "audio.wav"
        )
        
        return STTResponse(
            text=text,
            language=language,
            processing_time=time.time() - start_time
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"STT error: {str(e)}")