"""Global model initialization"""
import whisper
from styletts2 import tts
from typing import Optional

class ModelManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        print("Initializing models...")
        
        # Load Whisper
        print("Loading Whisper model...")
        self.whisper_model = whisper.load_model("base")
        print("✓ Whisper base model loaded (74M parameters)")
        
        # Load StyleTTS2
        print("Loading StyleTTS2 model...")
        self.styletts2_model: Optional[tts.StyleTTS2] = None
        try:
            self.styletts2_model = tts.StyleTTS2()
            print("✓ StyleTTS2 model loaded successfully")
        except Exception as e:
            print(f"✗ StyleTTS2 failed to load: {e}")
        
        self._initialized = True
    
    @property
    def whisper(self):
        return self.whisper_model
    
    @property
    def styletts2(self):
        return self.styletts2_model

# Global instance
models = ModelManager()