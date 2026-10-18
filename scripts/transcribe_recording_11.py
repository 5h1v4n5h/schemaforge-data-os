import os
import subprocess
import imageio_ffmpeg
import soundfile as sf
from transformers import pipeline

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

rec_path = r"C:\Users\shiva\OneDrive\Documents\Sound recordings\Recording (11).m4a"
wav_path = "scripts/recording_11.wav"

print("Converting Recording (11).m4a to 16kHz WAV...")
subprocess.run([
    ffmpeg_exe, "-y",
    "-i", rec_path,
    "-ar", "16000",
    "-ac", "1",
    wav_path
], check=True, capture_output=True)

print("Loading audio array...")
audio_data, sample_rate = sf.read(wav_path)
print(f"Audio duration: {len(audio_data)/sample_rate:.2f} seconds")

print("Transcribing with Whisper...")
pipe = pipeline("automatic-speech-recognition", model="openai/whisper-tiny", device="cpu")
result = pipe({"raw": audio_data, "sampling_rate": sample_rate}, return_timestamps=True)

print("\n=== TRANSCRIPTION RESULT (RECORDING 11) ===")
print(result["text"])
print("===========================================\n")

# Save transcription to file
with open("scripts/transcription_recording_11.txt", "w", encoding="utf-8") as f:
    f.write(result["text"])
    if "chunks" in result:
        f.write("\n\n--- CHUNKS ---\n")
        for ch in result["chunks"]:
            f.write(f"[{ch['timestamp'][0]} - {ch['timestamp'][1]}] {ch['text']}\n")

print("Saved transcription to scripts/transcription_recording_11.txt")
