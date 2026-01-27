from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from app.models.schemas import (
    STTResponse, LLMRequest, LLMResponse,
    TTSRequest, TTSResponse, HealthResponse
)
import time
import asyncio
import httpx
import tempfile
import os
import base64
import whisper

router = APIRouter()

# Load Whisper model globally (once at startup)
print("Loading Whisper model...")
whisper_model = whisper.load_model("base")
print("Whisper base model loaded (74M parameters)")

# Load StyleTTS2 model globally (once at startup)
print("Loading StyleTTS2 model...")
styletts2_model = None
try:
    from styletts2 import tts
    styletts2_model = tts.StyleTTS2()
    print("StyleTTS2 model loaded successfully")
except Exception as e:
    print(f"Warning: StyleTTS2 failed to load: {e}")
    styletts2_model = None

# Language code mapping
LANG_MAP = {
    'tn': 'ar',  # Tunisia → Arabic
    'cn': 'zh',  # China → Chinese
    'gb': 'en',  # Great Britain → English
    'fr': 'fr',  # French
    'de': 'de',  # German
    'it': 'it',  # Italian
    'jp': 'ja',  # Japan → Japanese
    'pt': 'pt',  # Portuguese
    'ru': 'ru',  # Russian
    'es': 'es',  # Spanish
}

# ==========================================
# Endpoint 1: Speech to Text (REAL WHISPER!)
# ==========================================
@router.post("/stt", response_model=STTResponse)
async def speech_to_text(
    audio: UploadFile = File(...),
    language: str = Form(...)
):
    """Convert speech to text using OpenAI Whisper"""
    start_time = time.time()
    tmp_path = None
    
    try:
        # Detect file extension
        file_extension = audio.filename.split('.')[-1] if audio.filename else 'wav'
        
        # Save uploaded audio with correct extension
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_extension}') as tmp_file:
            content = await audio.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        # Map language code
        whisper_lang = LANG_MAP.get(language, 'en')
        
        # Transcribe with Whisper (automatically handles format conversion)
        result = whisper_model.transcribe(
            tmp_path,
            language=whisper_lang,
            fp16=False,
            verbose=False
        )
        
        # Get text from result dict
        text = result["text"].strip()
        
        # Cleanup
        os.unlink(tmp_path)
        
        if not text:
            text = "[No speech detected]"
        
        return STTResponse(
            text=text,
            language=language,
            processing_time=time.time() - start_time
        )
        
    except Exception as e:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except:
                pass
        raise HTTPException(status_code=500, detail=f"STT error: {str(e)}")

# ==========================================
# Endpoint 2: Language Model (No Changes)
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
                        "num_predict": min(request.max_tokens, 100),
                        "num_ctx": 2048,
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
# Endpoint 3: Text to Speech
# ==========================================
@router.post("/tts", response_model=TTSResponse)
async def text_to_speech(request: TTSRequest):
    """Convert text to speech using StyleTTS2"""
    start_time = time.time()
    
    try:
        if styletts2_model is None:
            raise HTTPException(
                status_code=503,
                detail="StyleTTS2 model not loaded"
            )
        
        # Generate audio with StyleTTS2
        audio = styletts2_model.inference(
            request.text,
            target_voice_path=None,  # Use default voice
            diffusion_steps=10,      # Balance between quality and speed
            embedding_scale=1.0
        )
        
        # Convert audio array to bytes
        import io
        import scipy.io.wavfile as wavfile
        
        audio_buffer = io.BytesIO()
        # StyleTTS2 outputs at 24kHz
        wavfile.write(audio_buffer, 24000, audio)
        audio_bytes = audio_buffer.getvalue()
        
        # Encode to base64
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        
        return TTSResponse(
            audio_base64=audio_base64,
            processing_time=time.time() - start_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS error: {str(e)}")

# ==========================================
# Health Check
# ==========================================
@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Check service health and model status"""
    
    # Check Whisper
    whisper_status = "loaded" if whisper_model else "not_loaded"
    
    # Check StyleTTS2
    tts_status = "loaded" if styletts2_model else "not_loaded"
    
    # Check Mistral
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
            "whisper": whisper_status,
            "mistral": mistral_status,
            "tts": tts_status
        }
    )