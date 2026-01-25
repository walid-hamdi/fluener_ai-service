# AI Models Microservice

FastAPI service providing AI models for language learning platform.

## Features

- 🎤 Speech-to-Text (Whisper)
- 🤖 AI Responses (Mixtral)
- 🔊 Text-to-Speech (StyleTTS)

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload
```

## API Endpoints

- `POST /api/stt` - Speech to text
- `POST /api/llm` - Generate AI response
- `POST /api/tts` - Text to speech
- `GET /api/health` - Health check

## Documentation

Visit http://localhost:8000/docs for interactive API documentation.


![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

