"""Constants and mappings"""
import os

LANG_MAP = {
    'tn': 'ar',  # Tunisia → Arabic
    'cn': 'zh',  # China → Chinese
    'gb': 'en',  # Great Britain → English
    'fr': 'fr',
    'de': 'de',
    'it': 'it',
    'jp': 'ja',  # Japan → Japanese
    'pt': 'pt',
    'ru': 'ru',
    'es': 'es',
}

# Read from environment variable (from .env file or Docker environment)
# Defaults to localhost for local development, or "ollama" in Docker
OLLAMA_BASE_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MISTRAL_MODEL = "mistral:7b-instruct"