"""API Security - API Key Authentication"""
from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
import os

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """Verify API key from request header"""
    correct_api_key = os.getenv("API_SECRET_KEY")
    
    # Allow requests without auth in development mode
    if os.getenv("ENVIRONMENT") == "development" and not correct_api_key:
        return "dev-bypass"
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Missing API Key. Include 'X-API-Key' header."
        )
    
    if api_key != correct_api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )
    
    return api_key