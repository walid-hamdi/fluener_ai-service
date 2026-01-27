"""Ollama/Mistral LLM service"""
import httpx
from typing import List, Dict
from app.core.constants import OLLAMA_BASE_URL, MISTRAL_MODEL

class OllamaService:
    @staticmethod
    async def generate(
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 200
    ) -> str:
        """Generate response using Mistral"""
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{OLLAMA_BASE_URL}/api/chat",
                json={
                    "model": MISTRAL_MODEL,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": min(max_tokens, 100),
                        "num_ctx": 2048,
                    }
                }
            )
            
            if response.status_code != 200:
                raise RuntimeError(f"Mistral error: {response.text}")
            
            data = response.json()
            return data["message"]["content"]
    
    @staticmethod
    async def check_health() -> str:
        """Check if Ollama is available and has Mistral"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
                if response.status_code == 200:
                    models = response.json().get("models", [])
                    if any("mistral" in model.get("name", "") for model in models):
                        return "loaded"
        except:
            pass
        return "not_loaded"