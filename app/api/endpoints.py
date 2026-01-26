from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from app.models.schemas import (
    STTResponse, LLMRequest, LLMResponse,
    TTSRequest, TTSResponse, HealthResponse
)
import time
import asyncio
import httpx

router = APIRouter()

# ==========================================
# Endpoint 1: Speech to Text (Mock)
# ==========================================
@router.post("/stt", response_model=STTResponse)
async def speech_to_text(
    audio: UploadFile = File(...),
    language: str = Form(...)
):
    """Convert speech to text using Whisper"""
    start_time = time.time()
    
    try:
        audio_bytes = await audio.read()
        await asyncio.sleep(0.5)
        
        return STTResponse(
            text=f"Mock transcription in {language}",
            language=language,
            processing_time=time.time() - start_time
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"STT error: {str(e)}")

# ==========================================
# Endpoint 2: Language Model (REAL MISTRAL!)
# ==========================================
@router.post("/llm", response_model=LLMResponse)
async def generate_response(request: LLMRequest):
    """Generate AI response using Mistral"""
    start_time = time.time()
    
    try:
        messages = [
            {"role": msg.role, "content": msg.content}
            for msg in request.messages
        ]
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": "mistral:7b-instruct",
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": request.temperature,
                        "num_predict": request.max_tokens
                    }
                }
            )
            
            if response.status_code != 200:
                raise HTTPException(500, f"Mistral error: {response.text}")
            
            data = response.json()
            
            return LLMResponse(
                content=data["message"]["content"],
                processing_time=time.time() - start_time
            )
        
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="Mistral service not available. Is Ollama running?"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error: {str(e)}")

# ==========================================
# Endpoint 3: Text to Speech (Mock)
# ==========================================
@router.post("/tts", response_model=TTSResponse)
async def text_to_speech(request: TTSRequest):
    """Convert text to speech using StyleTTS"""
    start_time = time.time()
    
    try:
        await asyncio.sleep(0.5)
        
        return TTSResponse(
            audio_base64="dGVzdCBhdWRpbw==",
            processing_time=time.time() - start_time
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS error: {str(e)}")

# ==========================================
# Health Check
# ==========================================
@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Check service health"""
    
    # Check if Mistral is available
    mistral_status = "not_loaded"
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:11434/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                if any("mistral" in model.get("name", "") for model in models):
                    mistral_status = "loaded"
    except:
        mistral_status = "not_loaded"
    
    return HealthResponse(
        status="healthy",
        models={
            "whisper": "not_loaded",
            "mistral": mistral_status,
            "styletts": "not_loaded"
        }
    )