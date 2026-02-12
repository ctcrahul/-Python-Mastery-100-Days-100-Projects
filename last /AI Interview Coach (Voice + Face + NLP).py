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

# Facial emotion capture
cap = cv2.VideoCapture(0)
emotion_count = []

for _ in range(30):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.3,5)

    for (x,y,w,h) in faces:
        roi = gray[y:y+h,x:x+w]
        roi = cv2.resize(roi,(48,48))/255.0
        roi = roi.reshape(1,48,48,1)
        pred = emotion_model.predict(roi)[0]
        emotion_count.append(emotions[np.argmax(pred)])

cap.release()

# Feedback
confidence = emotion_count.count("Happy") + emotion_count.count("Neutral")

print("\n--- Feedback ---")
print("Detected emotions:", set(emotion_count))
print("Confidence Score:", confidence)
print("Answer Length:", len(answer_text.split()))
