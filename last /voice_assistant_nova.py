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
