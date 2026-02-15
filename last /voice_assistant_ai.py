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


# -------- FEATURES --------

def tell_time():
    time_now = datetime.datetime.now().strftime('%I:%M %p')
    speak("Current time is " + time_now)

def open_youtube():
    webbrowser.open("https://youtube.com")

def play_song(song):
    speak("Playing " + song)
    pywhatkit.playonyt(song)

def take_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    speak("Screenshot taken")

def save_note():
    speak("What should I remember?")
    note = take_command()
    with open("memory.txt", "a") as f:
        f.write(note + "\n")
    speak("Saved successfully")

def read_notes():
    try:
        with open("memory.txt", "r") as f:
            data = f.read()
            speak("You told me to remember")
            speak(data)
    except:
        speak("No memory found")

def open_app(command):
    apps = {
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "notepad": "notepad.exe",
        "calculator": "calc.exe"
    }

    for app in apps:
        if app in command:
            speak(f"Opening {app}")
            os.startfile(apps[app])
            return

    speak("App not found")

def shutdown_system():
    speak("Shutting down system")
    os.system("shutdown /s /t 5")


# -------- MAIN LOOP --------

def run_assistant():
    speak("AI Voice Assistant Activated")

    while True:
        command = take_command()

        if command == "none":
            continue

        intent = predict_intent(command)

        if intent == "time":
            tell_time()

        elif intent == "youtube":
            open_youtube()

        elif intent == "screenshot":
            take_screenshot()

        elif intent == "save_note":
            save_note()

        elif intent == "read_note":
            read_notes()

        elif intent == "shutdown":
            shutdown_system()

        elif intent == "play":
            play_song(command)

        elif intent == "open_app":
            open_app(command)

run_assistant()
