import cv2
import numpy as np
import speech_recognition as sr
from tensorflow.keras.models import load_model

# Load emotion model
emotion_model = load_model("emotion_model.hdf5")
emotions = ["Angry","Disgust","Fear","Happy","Sad","Surprise","Neutral"]

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

question = "Tell me about yourself"
print("Interview Question:", question)

# Voice input
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Speak your answer...")
    audio = r.listen(source)

try:
    answer_text = r.recognize_google(audio)
    print("Your Answer:", answer_text)
except:
    answer_text = ""
    print("Could not recognize speech")
