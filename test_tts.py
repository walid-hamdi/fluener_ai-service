import requests
import base64

response = requests.post(
    "http://localhost:8000/api/tts",
    json={"text": "Hello world! StyleTTS2 is working perfectly.", "language": "en"}
)

print("Status Code:", response.status_code)
print("Response:", response.json())

data = response.json()

# Check if there's an error
if "detail" in data:
    print(f"❌ Error: {data['detail']}")
else:
    # Success - decode audio
    audio_bytes = base64.b64decode(data["audio_base64"])
    
    with open("output.wav", "wb") as f:
        f.write(audio_bytes)
    
    print(f"✅ Audio saved to output.wav (took {data['processing_time']:.2f}s)")
    print("▶️  Play it now!")