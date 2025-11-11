"""
Voice Assistant (single-file)
Dependencies:
  pip install SpeechRecognition pyttsx3 wikipedia requests
On Windows you may also need: pip install PyAudio (or install from binaries)
This script uses:
 - speech_recognition for microphone -> text
 - pyttsx3 for offline TTS
 - wikipedia for quick facts
 - webbrowser for opening URLs
 - requests for simple web queries (optional)
Run: python voice_assistant.py
"""

import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import subprocess
import sys
import os
import threading
import time
import wikipedia
import requests
from queue import Queue, Empty


# ---------------------------
# Configuration
# ---------------------------
WAKE_WORDS = ("hey assistant", "ok assistant", "assistant", "hey jarvis")  # words to wake assistant
RATE = 150            # TTS speech rate
VOICE_GENDER = "female"  # "male" or "female" preference, engine will select closest match
LISTEN_TIMEOUT = 5    # seconds to wait for phrase
LISTEN_PHRASE_TIME_LIMIT = 8  # max seconds to record a phrase

# ---------------------------
# Utilities: TTS, Recognition
# ---------------------------
class VoiceAssistant:
    def __init__(self):
        # speech recognizer
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        # tts engine
        self.engine = pyttsx3.init()
        self._configure_tts()
        # command queue for worker thread
        self.command_q = Queue()
        self.running = True
        # small history
        self.history = []


    def _configure_tts(self):
        # set rate
        self.engine.setProperty("rate", RATE)
        # choose voice based on gender preference if available
        voices = self.engine.getProperty("voices")
        chosen = None
        if VOICE_GENDER.lower() == "female":
            for v in voices:
                if "female" in v.name.lower() or "female" in getattr(v, "gender", "").lower():
                    chosen = v.id
                    break
        elif VOICE_GENDER.lower() == "male":
            for v in voices:
                if "male" in v.name.lower() or "male" in getattr(v, "gender", "").lower():
                    chosen = v.id
                    break
        if not chosen and voices:
            chosen = voices[0].id
        if chosen:
            try:
                self.engine.setProperty("voice", chosen)
            except Exception:
                pass

    def speak(self, text, block=False):
        """Speak text. If block False, run in backgr""""
                def _say():
                  
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception:
                # fallback print
                print("[TTS failed] " + text)
        if block:
            _say()
        else:
            t = threading.Thread(target=_say, daemon=True)
            t.start()

   def listen(self, timeout=LISTEN_TIMEOUT, phrase_time_limit=LISTEN_PHRASE_TIME_LIMIT):
        """Listens from microphone and returns recognized lowercase text or None."""
        with self.microphone as source:
            try:
                # dynamic energy threshold for noisy environments
                self.recognizer.adjust_for_ambient_noise(source, duration=0.7)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            except sr.WaitTimeoutError:
                return None
        try:
            text = self.recognizer.recognize_google(audio)
            return text.lower()
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            # network issue with Google API - return None
            return None
          


    # ---------------------------
    # Command handling
    # ---------------------------
    def handle_command_text(self, text):
        """Main command parser. Receives a phrase already stripped of wake word."""
        if not text:
            return
        text = text.strip()
        self.history.append((datetime.datetime.utcnow().isoformat(), text))
        print("COMMAND:", text)

        # Basic conversational replies
        if any(kw in text for kw in ("hello", "hi", "hey")):
            self.speak("Hello. How can I help you?")
            return

    # Time and date
        if "time" in text:
            now = datetime.datetime.now()
            resp = now.strftime("It's %I:%M %p")
            self.speak(resp)
            return
        if "date" in text:
            now = datetime.datetime.now()
            resp = now.strftime("Today is %A, %B %d, %Y")
            self.speak(resp)
            return

        # Open website / search
        if text.startswith("search for "):
            query = text.replace("search for ", "", 1).strip()
            if query:
                url = f"https://www.google.com/search?q={requests.utils.quote(query)}"
                webbrowser.open(url)
                self.speak(f"Searching Google for {query}")
                return



        if text.startswith("open "):
            target = text.replace("open ", "", 1).strip()
            # simple mapping
            sites = {
                "youtube": "https://www.youtube.com",
                "google": "https://www.google.com",
                "github": "https://github.com",
                "stackoverflow": "https://stackoverflow.com",
                "gmail": "https://mail.google.com"
            }
            if target in sites:
                webbrowser.open(sites[target])
                self.speak(f"Opening {target}")
                return
            # allow opening URLs directly
            if "." in target:
                url = target if target.startswith("http") else "https://" + target
                webbrowser.open(url)
                self.speak(f"Opening {target}")
                return
            # else try as app name
            self.open_application(target)
            return

      # wikipedia quick facts
        if text.startswith("wikipedia ") or text.startswith("who is ") or text.startswith("what is "):
            query = text.replace("wikipedia ", "", 1) if text.startswith("wikipedia ") else text
            query = query.replace("who is ", "").replace("what is ", "").strip()
            if not query:
                self.speak("What would you like to look up on Wikipedia?")
                return
            try:
                summary = wikipedia.summary(query, sentences=2, auto_suggest=True, redirect=True)
                self.speak(summary)
            except Exception as e:
                self.speak("I couldn't fetch that


                           


