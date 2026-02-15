import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import pywhatkit
import os
import requests
import pyautogui
import yagmail
import time

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        print("You:", command)
    except:
        return "none"

    return command
# -------- AI INTENT TRAINING --------

training_sentences = [
    "open chrome", "launch browser", "start chrome",
    "open youtube", "go to youtube", "launch youtube",
    "what time is it", "tell me the time",
    "take screenshot", "capture screen",
    "remember this", "save this note",
    "what do you remember", "show memory",
    "shutdown system", "turn off computer",
    "play music", "play song"
]

training_labels = [
    "open_app", "open_app", "open_app",
    "youtube", "youtube", "youtube",
    "time", "time",
    "screenshot", "screenshot",
    "save_note", "save_note",
    "read_note", "read_note",
    "shutdown", "shutdown",
    "play", "play"
]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(training_sentences)

model = LogisticRegression()
model.fit(X, training_labels)

def predict_intent(command):
    X_test = vectorizer.transform([command])
    return model.predict(X_test)[0]
