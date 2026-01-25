from pydantic import BaseModel, Field
from typing import List, Dict

# Response for STT (Speech to Text)
class STTResponse(BaseModel):
    text: str
    language: str
    processing_time: float

# Request for LLM (Language Model)
class Message(BaseModel):
    role: str
    content: str

class LLMRequest(BaseModel):
    messages: List[Message]
    temperature: float = 0.7
    max_tokens: int = 200

# Response for LLM
class LLMResponse(BaseModel):
    content: str
    processing_time: float

# Request for TTS (Text to Speech)
class TTSRequest(BaseModel):
    text: str
    language: str
    speed: float = 0.85

# Response for TTS
class TTSResponse(BaseModel):
    audio_base64: str
    processing_time: float

# Health check
class HealthResponse(BaseModel):
    status: str
    models: Dict[str, str]