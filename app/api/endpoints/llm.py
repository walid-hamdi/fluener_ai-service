"""Language Model endpoint"""
from fastapi import APIRouter, HTTPException, Depends, Request
from app.models.schemas import LLMRequest, LLMResponse
from app.services.ollama_service import OllamaService
from app.core.security import verify_api_key
from slowapi import Limiter
from slowapi.util import get_remote_address
import httpx
import time

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.post("/llm", response_model=LLMResponse, tags=["Language Model"])
@limiter.limit("20/minute")
async def generate_response(
    request: Request,
    llm_request: LLMRequest,
    api_key: str = Depends(verify_api_key)
):
    """Generate AI response using Mistral"""
    start_time = time.time()
    
    try:
        messages = [
            {"role": msg.role, "content": msg.content}
            for msg in llm_request.messages
        ]
        
        content = await OllamaService.generate(
            messages,
            llm_request.temperature,
            llm_request.max_tokens
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