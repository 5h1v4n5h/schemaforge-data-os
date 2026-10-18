import os
import imageio_ffmpeg
import soundfile as sf
from transformers import pipeline

# Add ffmpeg to PATH
ffmpeg_dir = os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())
os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

print("Loading soundfile audio...")
audio_data, sample_rate = sf.read("scripts/recording_9.wav")
print(f"Loaded audio: shape={audio_data.shape}, sample_rate={sample_rate}")

print("Loading whisper pipeline...")
pipe = pipeline("automatic-speech-recognition", model="openai/whisper-tiny", device="cpu")

print("Transcribing audio array...")
result = pipe({"raw": audio_data, "sampling_rate": sample_rate}, return_timestamps=True)

print("\n=== TRANSCRIPTION RESULT ===")
print(result["text"])
print("============================\n")
