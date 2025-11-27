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
