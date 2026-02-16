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
