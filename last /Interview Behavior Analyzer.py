"""
AI Interview Behavior Analyzer

This program:
1. Listens to your spoken answer
2. Converts speech to text
3. Evaluates your communication quality
"""

import speech_recognition as sr
from textblob import TextBlob
import time

# ---------- CONFIG ---------- #

FILLER_WORDS = [
    "um", "uh", "like", "you know",
    "actually", "basically", "so",
    "hmm", "right", "okay"
]

INTERVIEW_QUESTION = "Tell me about your strengths"

# ---------- RECORD SPEECH ---------- #

def record_answer():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("\nSpeak your answer now...")
        recognizer.adjust_for_ambient_noise(source)

        start = time.time()
        audio = recognizer.listen(source)
        end = time.time()

    duration = end - start

    try:
        text = recognizer.recognize_google(audio)
        return text, duration
    except:
        return None, duration

# ---------- ANALYSIS FUNCTIONS ---------- #

def count_filler_words(text):
    count = 0
    for word in FILLER_WORDS:
        count += text.lower().count(word)
    return count

def speaking_speed(word_count, duration):
    if duration == 0:
        return 0
    return word_count / (duration / 60)

def sentiment_analysis(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

def confidence_score(speed, filler_count):
    score = 100

    # Too slow
    if speed < 90:
        score -= 20

    # Too fast
    if speed > 170:
        score -= 15

    # Filler penalty
    score -= filler_count * 4

    return max(score, 0)

def relevance_score(answer, question):
    answer_words = set(answer.lower().split())
    question_words = set(question.lower().split())

    match = answer_words.intersection(question_words)

    if len(question_words) == 0:
        return 0

    return (len(match) / len(question_words)) * 100

# ---------- MAIN ANALYSIS ---------- #

def analyze(answer, duration):

    words = answer.split()
    word_count = len(words)

    fillers = count_filler_words(answer)
    speed = speaking_speed(word_count, duration)
    sentiment = sentiment_analysis(answer)
    confidence = confidence_score(speed, fillers)
    relevance = relevance_score(answer, INTERVIEW_QUESTION)

    print("\n========== AI FEEDBACK ==========")
    print("Your Answer:", answer)
    print("\nFiller Words Used:", fillers)
    print("Speaking Speed (WPM):", round(speed, 2))
    print("Sentiment Score:", round(sentiment, 2))
    print("Confidence Score:", confidence)
    print("Answer Relevance:", round(relevance, 2), "%")
    print("=================================\n")

# ---------- RUN ---------- #

print("Interview Question:", INTERVIEW_QUESTION)

answer, duration = record_answer()

if answer:
    analyze(answer, duration)
else:
    print("Speech not recognized. Try again.")
