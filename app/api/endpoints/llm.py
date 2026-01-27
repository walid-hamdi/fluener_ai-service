"""Language Model endpoint"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import LLMRequest, LLMResponse
from app.services.ollama_service import OllamaService
import httpx
import time

router = APIRouter()

@router.post("/llm", response_model=LLMResponse, tags=["Language Model"])
async def generate_response(request: LLMRequest):
    """Generate AI response using Mistral"""
    start_time = time.time()
    
    try:
        messages = [
            {"role": msg.role, "content": msg.content}
            for msg in request.messages
        ]
        
        content = await OllamaService.generate(
            messages,
            request.temperature,
            request.max_tokens
        )
        
        return LLMResponse(
            content=content,
            processing_time=time.time() - start_time
        )
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="Mistral service not available. Is Ollama running?"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error: {str(e)}")