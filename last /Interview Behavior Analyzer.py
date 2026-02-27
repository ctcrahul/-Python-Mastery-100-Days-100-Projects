"""
AI Interview Behavior Analyzer
This program listens to a spoken answer and evaluates:
- Confidence
- Filler words
- Sentiment
- Speaking speed
- Answer relevance

Useful for mock interview preparation.
"""

import speech_recognition as sr
from textblob import TextBlob
import time

# Common filler words list
FILLER_WORDS = ["um", "uh", "like", "you know", "actually", "basically", "so"]

def record_answer():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nSpeak your interview answer now...")
        start_time = time.time()
        audio = r.listen(source)
        end_time = time.time()

    try:
        text = r.recognize_google(audio)
        duration = end_time - start_time
        return text, duration
    except:
        return None, 0
