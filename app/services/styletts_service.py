"""StyleTTS2 TTS service"""
import io
import base64
import scipy.io.wavfile as wavfile
from app.core.models import models

class StyleTTSService:
    @staticmethod
    def synthesize(text: str, speed: float = 0.85) -> str:
        """Generate speech from text, return base64 audio"""
        if models.styletts2 is None:
            raise RuntimeError("StyleTTS2 model not loaded")
        
        # Generate audio
        audio = models.styletts2.inference(
            text,
            target_voice_path=None,
            diffusion_steps=10,
            embedding_scale=1.0
        )
        
        # Convert to WAV bytes
        audio_buffer = io.BytesIO()
        wavfile.write(audio_buffer, 24000, audio)
        audio_bytes = audio_buffer.getvalue()
        
        # Encode to base64
        return base64.b64encode(audio_bytes).decode('utf-8')