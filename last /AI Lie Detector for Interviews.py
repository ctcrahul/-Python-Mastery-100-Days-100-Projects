import streamlit as st
import speech_recognition as sr
import librosa
import numpy as np
import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt')

st.title("🎤 AI Interview Lie Detector")

filler_words = ["um", "uh", "like", "basically", "actually", "you know", "so"]

def analyze_filler(text):
    words = word_tokenize(text.lower())
    filler_count = sum(1 for w in words if w in filler_words)
    return filler_count

def analyze_confidence(audio_file):
    y, sr = librosa.load(audio_file)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    energy = np.mean(librosa.feature.rms(y=y))
    return tempo, energy
