import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

rec_path = Path(r"C:\Users\shiva\OneDrive\Documents\Sound recordings\Recording (9).m4a")
print("Recording exists:", rec_path.exists())
if rec_path.exists():
    print("File size:", rec_path.stat().st_size)

api_key = os.getenv("GEMINI_API_KEY")
print("GEMINI_API_KEY present:", bool(api_key))

# Transcribe recording (9) using Gemini multimodal audio
if api_key and rec_path.exists():
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        audio_file = client.files.upload(file=rec_path)
        print("Uploaded audio file to Gemini Files API:", audio_file.name)
        
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[
                audio_file,
                "Please transcribe this audio exactly word-for-word, and describe the speaker's tone, accent, pacing, and what they are talking about."
            ]
        )
        print("\n--- TRANSCRIPTION & ANALYSIS ---")
        print(response.text)
        print("--------------------------------\n")
    except Exception as e:
        print("Gemini transcription error:", e)
