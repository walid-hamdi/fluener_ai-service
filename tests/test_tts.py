import requests
import base64
import time

def generate_speech(text, filename="output.wav", language="en", speed=0.85):
    """Generate speech and save to file"""
    print(f"\n🎤 Generating speech for: '{text[:50]}...'")
    
    response = requests.post(
        "http://localhost:8000/api/tts",
        json={
            "text": text,
            "language": language,
            "speed": speed
        }
    )
    
    print(f"Status Code: {response.status_code}")
    
    data = response.json()
    
    if "detail" in data:
        print(f"❌ Error: {data['detail']}")
        return False
    
    # Success - decode audio
    audio_bytes = base64.b64decode(data["audio_base64"])
    
    with open(filename, "wb") as f:
        f.write(audio_bytes)
    
    print(f"✅ Audio saved to {filename}")
    print(f"⏱️  Processing time: {data['processing_time']:.2f}s")
    print(f"📊 Audio size: {len(audio_bytes) / 1024:.1f} KB")
    return True


# Test samples - from simple to complex
samples = {
    "simple": "Hello world! This is a test of StyleTTS2.",
    
    "expressive": "Wow! This voice synthesis technology is absolutely incredible. Can you believe how natural it sounds?",
    
    "story": """Once upon a time, in a small village nestled between rolling hills, there lived a curious young girl named Sarah. 
    Every morning, she would wake up before dawn to watch the sunrise paint the sky in brilliant shades of orange and pink. 
    Her grandmother often told her that each sunrise was unique, a gift that could never be repeated.""",
    
    "technical": """Artificial intelligence and machine learning have revolutionized the field of text-to-speech synthesis. 
    Modern neural networks can now capture the nuances of human speech, including emotion, emphasis, and natural prosody. 
    StyleTTS2 represents a significant advancement in zero-shot voice cloning and high-quality speech generation.""",
    
    "poem": """The road not taken by Robert Frost. Two roads diverged in a yellow wood, 
    And sorry I could not travel both. And be one traveler, long I stood, 
    And looked down one as far as I could, to where it bent in the undergrowth.""",
    
    "conversation": """Hey, how are you doing today? I hope you're having a wonderful day! 
    You know, I was just thinking about how amazing technology has become. 
    It's incredible that we can now synthesize human speech with such clarity and emotion!"""
}

# Generate all samples
print("=" * 60)
print("🎵 StyleTTS2 Voice Quality Test")
print("=" * 60)

for name, text in samples.items():
    success = generate_speech(
        text, 
        filename=f"output_{name}.wav",
        language="en",
        speed=0.85
    )
    if success:
        print(f"▶️  Play: output_{name}.wav\n")
    time.sleep(1)  # Small delay between requests

print("\n" + "=" * 60)
print("✨ All samples generated!")
print("=" * 60)
print("\n🎧 Listen to the files to compare quality:")
for name in samples.keys():
    print(f"   • output_{name}.wav")