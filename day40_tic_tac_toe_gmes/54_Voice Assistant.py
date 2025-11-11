"""                                                                    Day = 54

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
        """Speak text. If block False, run in background thread so assistant stays responsive."""
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
                self.speak("I couldn't fetch that. Try a different query.")
            return

        # system commands
        if text in ("shutdown", "shut down", "turn off computer"):
            self.speak("Shutting down the computer. Goodbye.", block=True)
            if sys.platform.startswith("win"):
                subprocess.Popen(["shutdown", "/s", "/t", "5"])
            else:
                subprocess.Popen(["shutdown", "now"])
            return

        if "restart" in text and "computer" in text:
            self.speak("Restarting the computer.", block=True)
            if sys.platform.startswith("win"):
                subprocess.Popen(["shutdown", "/r", "/t", "5"])
            else:
                subprocess.Popen(["reboot"])
            return

        if any(word in text for word in ("play music", "play song", "play audio")):
            # default behavior: open music folder or ask for file path
            music_folder = os.path.join(os.path.expanduser("~"), "Music")
            if os.path.isdir(music_folder):
                self.speak("Opening your music folder.")
                self.open_folder(music_folder)
            else:
                self.speak("I couldn't find a music folder. Tell me the file path to play.")
            return

        if "open folder" in text:
            # open home dir
            self.open_folder(os.path.expanduser("~"))
            self.speak("Opening your home folder.")
            return

        # calculator: simple math
        if text.startswith("calculate ") or text.startswith("what is "):
            expr = text.replace("calculate ", "", 1) if text.startswith("calculate ") else text.replace("what is ", "", 1)
            expr = expr.strip()
            # safe evaluation: allow digits and operators only
            safe_chars = set("0123456789+-*/(). %")
            if all(c in safe_chars or c.isalpha() for c in expr):
                try:
                    # replace words like 'times' or 'plus'
                    expr = expr.replace("times", "*").replace("plus", "+").replace("minus", "-").replace("divided by", "/")
                    result = eval(expr, {"__builtins__": {}})
                    self.speak(f"The result is {result}")
                except Exception:
                    self.speak("I couldn't calculate that.")
            else:
                self.speak("That expression may be unsafe to evaluate.")
            return

        # fallback: ask to perform a web search
        self.speak("I didn't quite get that. Would you like me to search the web for this?")
        # optionally wait for yes/no and then search - we do a non-blocking prompt
        # For simplicity, do not block here.

    # ---------------------------
    # Helpers
    # ---------------------------
    def open_application(self, name):
        """Try to open an application by name. Works best on common apps/paths."""
        name = name.lower()
        # Windows common apps
        if sys.platform.startswith("win"):
            cmd_map = {
                "notepad": ["notepad"],
                "calculator": ["calc"],
                "paint": ["mspaint"],
                "word": ["start", "winword"],
                "excel": ["start", "excel"],
                "chrome": ["start", "chrome"],
            }
            if name in cmd_map:
                try:
                    subprocess.Popen(cmd_map[name], shell=True)
                    self.speak(f"Opening {name}")
                    return True
                except Exception:
                    pass
        # macOS common apps
        if sys.platform == "darwin":
            try_map = {
                "safari": ["open", "-a", "Safari"],
                "chrome": ["open", "-a", "Google Chrome"],
                "calculator": ["open", "-a", "Calculator"],
                "notes": ["open", "-a", "Notes"]
            }
            if name in try_map:
                subprocess.Popen(try_map[name])
                self.speak(f"Opening {name}")
                return True
        # Linux - try opening command directly
        try:
            subprocess.Popen([name])
            self.speak(f"Opening {name}")
            return True
        except Exception:
            self.speak(f"Unable to open {name}.")
            return False

    def open_folder(self, path):
        try:
            if sys.platform.startswith("win"):
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])
        except Exception:
            self.speak("Failed to open folder.")

    # ---------------------------
    # Main loop: listening for wake word and commands
    # ---------------------------
    def run(self):
        self.speak("Assistant is ready. Say the wake word to start.")
        listener_thread = threading.Thread(target=self._background_listener_loop, daemon=True)
        worker_thread = threading.Thread(target=self._command_worker, daemon=True)
        listener_thread.start()
        worker_thread.start()
        try:
            while self.running:
                time.sleep(0.3)
        except KeyboardInterrupt:
            self.running = False
            self.speak("Shutting down. Goodbye.", block=True)

    def _background_listener_loop(self):
        """Continuously listen for the wake word. When detected, listen for a command."""
        while self.running:
            try:
                phrase = self.listen(timeout=None, phrase_time_limit=4)  # blocking until something heard
            except Exception:
                phrase = None
            if not phrase:
                continue
            print("Heard:", phrase)
            # check for wake words
            if any(phrase.startswith(w) or (" " + w + " ") in (" " + phrase + " ") for w in WAKE_WORDS):
                # strip wake word
                stripped = phrase
                for w in WAKE_WORDS:
                    if stripped.startswith(w):
                        stripped = stripped[len(w):].strip()
                        break
                if stripped:
                    # user spoke command immediately after wake word
                    self.command_q.put(stripped)
                else:
                    # prompt for command
                    self.speak("Yes? Listening for your command.")
                    cmd = self.listen(timeout=6, phrase_time_limit=LISTEN_PHRASE_TIME_LIMIT)
                    if cmd:
                        self.command_q.put(cmd)
                    else:
                        self.speak("I didn't hear a command.")
            else:
                # optional: support direct command without wake if short and addressed to assistant name
                # else ignore
                continue

    def _command_worker(self):
        """Process commands sequentially from the queue."""
        while self.running:
            try:
                cmd = self.command_q.get(timeout=0.5)
            except Empty:
                continue
            try:
                self.handle_command_text(cmd)
            except Exception as e:
                print("Error handling command:", e)
                self.speak("An error occurred while handling the command.")
            finally:
                self.command_q.task_done()

# ---------------------------
# Entry point
# ---------------------------
if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()

#===========================================================================================================================================================================
                                                    Thanks for visiting and keep supporting....
#===========================================================================================================================================================================
