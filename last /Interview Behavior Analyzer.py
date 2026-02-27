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
def analyze_filler_words(text):
    count = 0
    for word in FILLER_WORDS:
        count += text.lower().count(word)
    return count

def speaking_speed(word_count, duration):
    if duration == 0:
        return 0
    return word_count / (duration / 60)

def sentiment_score(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

def confidence_score(speed, filler_count):
    score = 100
    if speed < 80:
        score -= 20
    if speed > 160:
        score -= 15
    score -= filler_count * 5
    return max(score, 0)

def relevance_score(text, question):
    text_words = set(text.lower().split())
    question_words = set(question.lower().split())
    match = text_words.intersection(question_words)
    return len(match) / len(question_words) * 100
