"""Speech-to-Text endpoint"""
from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from app.models.schemas import STTResponse
from app.services.whisper_service import WhisperService
import time

router = APIRouter()

@router.post("/stt", response_model=STTResponse, tags=["Speech-to-Text"])
async def speech_to_text(
    audio: UploadFile = File(...),
    language: str = Form(...)
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