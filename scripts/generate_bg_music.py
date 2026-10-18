import numpy as np
import soundfile as sf

sample_rate = 44100
duration_sec = 100.0  # 100 seconds to cover all scenes
total_samples = int(sample_rate * duration_sec)
t = np.linspace(0, duration_sec, total_samples, endpoint=False)

# Ambient chord frequencies: C2 (65.4), G2 (98.0), Eb3 (155.6), Bb3 (233.1), D4 (293.7), G4 (392.0)
freqs = [65.41, 97.99, 155.56, 196.00, 233.08, 293.66, 392.00]
chords = np.zeros(total_samples)

for i, f in enumerate(freqs):
    # Slow LFO detune and amplitude flutter
    lfo_rate = 0.1 + i * 0.03
    detune = 1.0 + 0.003 * np.sin(2 * np.pi * lfo_rate * t)
    amp_lfo = 0.5 + 0.5 * np.sin(2 * np.pi * (0.05 + i * 0.02) * t)
    # Harmonics
    tone = np.sin(2 * np.pi * f * detune * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t)
    chords += tone * amp_lfo * (0.8 / (i + 1))

# Normalize and scale to soft background level (-24 dB)
chords = chords / np.max(np.abs(chords))
chords = chords * 0.05  # subtle, non-intrusive volume

# Soft attack fade-in and fade-out
fade_len = int(sample_rate * 3.0)
fade_in = np.linspace(0, 1, fade_len)
fade_out = np.linspace(1, 0, fade_len)
chords[:fade_len] *= fade_in
chords[-fade_len:] *= fade_out

# Stereo widening
left = chords
right = np.roll(chords, int(sample_rate * 0.02))  # 20ms delay for stereo width
stereo = np.column_stack([left, right])

sf.write("scripts/ambient_bed.wav", stereo, sample_rate)
print("Synthesized ambient corporate background music bed: scripts/ambient_bed.wav")
