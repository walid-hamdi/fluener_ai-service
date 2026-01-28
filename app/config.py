# app/config.py
from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    """Application settings - reads from .env or environment variables"""
    
    # App info
    APP_NAME: str = "AI Models Service"
    VERSION: str = "1.0.0"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Environment
    ENVIRONMENT: str = "development"
    
    # CORS Origins (comma-separated string)
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:4000"
    
    # AI Services
    OLLAMA_URL: str = "http://localhost:11434"
    
    # Security
    API_SECRET_KEY: Optional[str] = None
    
    # Cloudflare Tunnel
    TUNNEL_TOKEN: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "allow"  # Allow extra fields from .env
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert comma-separated CORS origins to list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
    
    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT.lower() in ["development", "dev", "local"]
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() in ["production", "prod"]
 
settings = Settings()