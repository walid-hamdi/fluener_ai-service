"""Whisper STT service"""
import tempfile
import os
from app.core.models import models
from app.core.constants import LANG_MAP

class WhisperService:
    @staticmethod
    async def transcribe(audio_content: bytes, language: str, filename: str = "audio.wav") -> str:
        """Transcribe audio to text"""
        tmp_path = None
        
        try:
            # Detect file extension
            file_extension = filename.split('.')[-1] if filename else 'wav'
            
            # Save uploaded audio
            with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_extension}') as tmp_file:
                tmp_file.write(audio_content)
                tmp_path = tmp_file.name
            
            # Map language code
            whisper_lang = LANG_MAP.get(language, 'en')
            
            # Transcribe
            result = models.whisper.transcribe(
                tmp_path,
                language=whisper_lang,
                fp16=False,
                verbose=False
            )
            
            text = result["text"].strip()
            
            # Cleanup
            os.unlink(tmp_path)
            
            return text if text else "[No speech detected]"
            
        except Exception as e:
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.unlink(tmp_path)
                except:
                    pass
            raise e