"""
AI Interview Confidence Analyzer

Purpose:
Evaluate interview responses using speech patterns and language usage
to estimate confidence level.

Method:
1. Convert speech to text
2. Detect filler words (hesitation markers)
3. Measure speech tempo and vocal energy
4. Combine signals into confidence score

Why this matters:
Confident candidates tend to speak with fewer fillers,
stable energy, and consistent pacing.

Limitations:
- Not a true lie detector
- Does not account for cultural speaking styles
- Works best with clear audio input

Future Improvements:
- Emotion detection
- Contextual answer relevance scoring
- Transformer-based hesitation analysis
"""


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

def score_response(filler_count, tempo, energy):
    score = 100

    score -= filler_count * 5

    if tempo < 90:
        score -= 10

    if energy < 0.02:
        score -= 10

    return max(score, 0)

uploaded_audio = st.file_uploader("Upload your interview answer (wav)", type=["wav"])

if uploaded_audio:

    r = sr.Recognizer()
    with sr.AudioFile(uploaded_audio) as source:
        audio = r.record(source)

    try:
        text = r.recognize_google(audio)
        st.write("📝 Transcribed Text:", text)

        filler_count = analyze_filler(text)
        tempo, energy = analyze_confidence(uploaded_audio)

        score = score_response(filler_count, tempo, energy)

        st.subheader("📊 AI Confidence Score")
        st.write(score)

        if score > 80:
            st.success("Strong and confident answer")
        elif score > 50:
            st.warning("Moderate confidence")
        else:
            st.error("Low confidence / nervous response")

    except:
        st.error("Could not understand audio")
