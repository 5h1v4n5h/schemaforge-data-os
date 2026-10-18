import numpy as np
import soundfile as sf
import subprocess
import os
import imageio_ffmpeg

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

# Convert test_gtts.mp3 to wav
subprocess.run([ffmpeg_exe, "-y", "-i", "scripts/test_gtts.mp3", "-ar", "16000", "-ac", "1", "scripts/test_gtts.wav"], capture_output=True)

# Analyze user's recording
user_audio, sr_user = sf.read("scripts/recording_9.wav")
gtts_audio, sr_gtts = sf.read("scripts/test_gtts.wav")

def estimate_pitch_autocorr(signal, sr):
    # simple autocorrelation pitch detector on active frames
    energy = signal ** 2
    threshold = np.mean(energy) * 0.5
    active = signal[energy > threshold]
    if len(active) < 1600:
        return 0
    # take 2-second slice
    slice_data = active[1600:1600+8000]
    corr = np.correlate(slice_data, slice_data, mode='full')
    corr = corr[len(corr)//2:]
    # search between 80Hz and 300Hz
    min_lag = int(sr / 300)
    max_lag = int(sr / 80)
    peak_lag = min_lag + np.argmax(corr[min_lag:max_lag])
    return sr / peak_lag

user_f0 = estimate_pitch_autocorr(user_audio, sr_user)
gtts_f0 = estimate_pitch_autocorr(gtts_audio, sr_gtts)

print(f"User Shivansh F0 (pitch): ~{user_f0:.1f} Hz")
print(f"gTTS raw F0 (pitch): ~{gtts_f0:.1f} Hz")
