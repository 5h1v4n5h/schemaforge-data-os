import numpy as np
import soundfile as sf

sample_rate = 44100
duration_sec = 680.0  # ~11.3 minutes to cover all 7 scenes
total_samples = int(sample_rate * duration_sec)
t = np.linspace(0, duration_sec, total_samples, endpoint=False)

# Rich ambient chord frequencies: C2 (65.41), G2 (97.99), Eb3 (155.56), Bb3 (233.08), D4 (293.66), G4 (392.00)
freqs = [65.41, 97.99, 155.56, 196.00, 233.08, 293.66, 392.00]
chords = np.zeros(total_samples)

print("Synthesizing 11-minute ambient background music bed...")

for i, f in enumerate(freqs):
    lfo_rate = 0.08 + i * 0.02
    detune = 1.0 + 0.0025 * np.sin(2 * np.pi * lfo_rate * t)
    amp_lfo = 0.5 + 0.5 * np.sin(2 * np.pi * (0.03 + i * 0.015) * t)
    tone = np.sin(2 * np.pi * f * detune * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t)
    chords += tone * amp_lfo * (0.7 / (i + 1))

# Normalize and scale to soft background level (-26 dB)
chords = chords / np.max(np.abs(chords))
chords = chords * 0.045  # subtle, non-intrusive volume

# Soft attack fade-in and fade-out
fade_len = int(sample_rate * 4.0)
fade_in = np.linspace(0, 1, fade_len)
fade_out = np.linspace(1, 0, fade_len)
chords[:fade_len] *= fade_in
chords[-fade_len:] *= fade_out

# Stereo widening
left = chords
right = np.roll(chords, int(sample_rate * 0.025))  # 25ms delay for stereo width
stereo = np.column_stack([left, right])

sf.write("scripts/long_ambient_bed.wav", stereo, sample_rate)
print("Saved 11-minute ambient bed: scripts/long_ambient_bed.wav")
