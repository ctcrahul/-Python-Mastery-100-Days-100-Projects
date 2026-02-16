import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import pywhatkit
import os
import pyautogui
import time
import queue
import sounddevice as sd
import json

from vosk import Model, KaldiRecognizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

# -------- WAKE WORD --------

q = queue.Queue()

model = Model("vosk-model-small-en-us-0.15")
rec = KaldiRecognizer(model, 16000)

def callback(indata, frames, time, status):
    q.put(bytes(indata))

def listen_for_wake_word():
    with sd.RawInputStream(samplerate=16000, blocksize=8000,
                           dtype='int16', channels=1,
                           callback=callback):

        print("Waiting for wake word...")

        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")

                if "hey nova" in text:
                    speak("Yes?")
                    return
# -------- COMMAND LISTENER --------

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        print("You:", command)
    except:
        return "none"

    return command

# -------- AI INTENT --------

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
