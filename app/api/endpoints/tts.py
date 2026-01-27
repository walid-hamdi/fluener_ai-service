"""Text-to-Speech endpoint"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import TTSRequest, TTSResponse
from app.services.styletts_service import StyleTTSService
import time

router = APIRouter()

@router.post("/tts", response_model=TTSResponse, tags=["Text-to-Speech"])
async def text_to_speech(request: TTSRequest):
    """Convert text to speech using StyleTTS2"""
    start_time = time.time()
    
    try:
        audio_base64 = StyleTTSService.synthesize(request.text, request.speed)
        
        return TTSResponse(
            audio_base64=audio_base64,
            processing_time=time.time() - start_time
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS error: {str(e)}")