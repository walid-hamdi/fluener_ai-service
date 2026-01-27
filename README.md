<!-- # AI Models Microservice

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

Visit http://localhost:8000/docs for interactive API documentation. -->

---

title: AI Tutor Service
emoji: 🎓
colorFrom: blue
colorTo: green
sdk: docker
app_port: 8000
pinned: false

---

# 🎓 AI Tutor Service

High-performance FastAPI service providing AI-powered language learning capabilities.

## 🚀 Features

- 🎤 **Speech-to-Text**: Convert speech to text using OpenAI Whisper
- 🤖 **Language Model**: Generate responses using Mistral 7B
- 🔊 **Text-to-Speech**: Natural speech synthesis using StyleTTS2

## 🔐 Security

This API requires authentication via API Key. Include the `X-API-Key` header in all requests.

## 📚 API Documentation

Visit `/docs` for interactive API documentation (Swagger UI).

## 🛠️ Tech Stack

- **FastAPI** - Modern Python web framework
- **Whisper** - Speech recognition (OpenAI)
- **Mistral 7B** - Large language model
- **StyleTTS2** - Text-to-speech synthesis
- **Docker** - Containerization

## 📊 Rate Limits

- 100 requests/hour per IP (global)
- 20 requests/minute per endpoint

## 🔗 Endpoints

### Health Check

```bash
GET /health
```

### Speech to Text

```bash
POST /api/stt
Content-Type: multipart/form-data

Parameters:
- audio: audio file
- language: language code (en, fr, es, etc.)
```

### Language Model

```bash
POST /api/llm
Content-Type: application/json
X-API-Key: your-api-key

{
  "messages": [{"role": "user", "content": "Hello"}],
  "temperature": 0.7,
  "max_tokens": 200
}
```

### Text to Speech

```bash
POST /api/tts
Content-Type: application/json
X-API-Key: your-api-key

{
  "text": "Hello world",
  "language": "en",
  "speed": 0.85
}
```

## 📝 License

MIT License - Feel free to use for your projects!

## 🤝 Contributing

Issues and pull requests welcome!
