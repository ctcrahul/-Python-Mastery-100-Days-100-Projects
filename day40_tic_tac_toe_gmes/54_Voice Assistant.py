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
