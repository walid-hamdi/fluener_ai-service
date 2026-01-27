"""Text-to-Speech endpoint"""
from fastapi import APIRouter, HTTPException, Depends, Request
from app.models.schemas import TTSRequest, TTSResponse
from app.services.styletts_service import StyleTTSService
from app.core.security import verify_api_key
from slowapi import Limiter
from slowapi.util import get_remote_address
import time

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.post("/tts", response_model=TTSResponse, tags=["Text-to-Speech"])
@limiter.limit("20/minute")
async def text_to_speech(
    request: Request,
    tts_request: TTSRequest,
    api_key: str = Depends(verify_api_key)
):
    """Convert text to speech using StyleTTS2"""
    start_time = time.time()
    
    try:
        audio_base64 = StyleTTSService.synthesize(tts_request.text, tts_request.speed)
        
        return TTSResponse(
            audio_base64=audio_base64,
            processing_time=time.time() - start_time
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS error: {str(e)}")