import numpy as np
import simpleaudio as sa
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

SAMPLE_RATE = 44100

# -------------------------------
# Sound Generators
# -------------------------------

def generate_kick(duration=0.15, freq=80):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    envelope = np.exp(-10 * t)
    wave = np.sin(2 * np.pi * freq * t) * envelope
    return wave

def generate_snare(duration=0.12):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    noise = np.random.randn(len(t))
    envelope = np.exp(-15 * t)
    wave = noise * envelope
    return wave

def generate_hihat(duration=0.05):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    noise = np.random.randn(len(t))
    high_pass = noise - np.mean(noise)
    envelope = np.exp(-25 * t)
    return high_pass * envelope

 -------------------------------
# Beat Generator
# -------------------------------

def generate_pattern(steps=16, complexity=3):
    """
    Returns a list of steps with [kick, snare, hihat]
    """
    pattern = []

    for i in range(steps):
        kick = 1 if i % 4 == 0 else np.random.rand() < complexity * 0.05
        snare = 1 if i % 8 == 4 else np.random.rand() < complexity * 0.04
        hihat = 1 if i % 2 == 0 else np.random.rand() < complexity * 0.08

        pattern.append([kick, snare, hihat])

    return pattern

# -------------------------------
# Sequence Builder
# -------------------------------

def build_beat(pattern, bpm):
    beat_time = 60 / bpm
    step_duration = beat_time / 4

    final_wave = np.zeros(int(SAMPLE_RATE * step_duration * len(pattern)))

    for i, step in enumerate(pattern):
        start_idx = int(i * step_duration * SAMPLE_RATE)

        if step[0]:
            final_wave[start_idx:start_idx+len(kick_sound)] += kick_sound
        if step[1]:
            final_wave[start_idx:start_idx+len(snare_sound)] += snare_sound
        if step[2]:
            final_wave[start_idx:start_idx+len(hihat_sound)] += hihat_sound

    max_val = np.max(np.abs(final_wave))
    if max_val > 0:
        final_wave /= max_val

    return final_wave


# -------------------------------
# Audio Play
# -------------------------------

def play_sound(wave):
    audio = (wave * 32767).astype(np.int16)
    sa.play_buffer(audio, 1, 2, SAMPLE_RATE).wait_done()

# -------------------------------
# GUI App
# -------------------------------

class DrumBeatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Drum Beat Generator")
        self.root.geometry("500x400")

        self.bpm = tk.IntVar(value=120)
        self.complexity = tk.IntVar(value=3)

        ttk.Label(root, text="AI Drum Beat Generator", font=("Arial", 14, "bold")).pack(pady=10)

        ttk.Label(root, text="Tempo (BPM)").pack()
        ttk.Scale(root, from_=60, to=200, variable=self.bpm).pack(fill="x", padx=20)

        ttk.Label(root, text="Pattern Complexity").pack()
        ttk.Scale(root, from_=1, to=10, variable=self.complexity).pack(fill="x", padx=20)

        ttk.Button(root, text="Generate & Play", command=self.generate_and_play).pack(pady=20)
        ttk.Button(root, text="Export as WAV", command=self.export_wav).pack(pady=5)

        self.status = ttk.Label(root, text="", foreground="green")
        self.status.pack()

        self.last_wave = None




