import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import pywhatkit
import os
import requests

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

def tell_time():
    time = datetime.datetime.now().strftime('%I:%M %p')
    speak("Current time is " + time)

def search_wiki(query):
    speak("Searching Wikipedia")
    result = wikipedia.summary(query, sentences=2)
    speak(result)

def open_youtube():
    webbrowser.open("https://youtube.com")

def open_google():
    webbrowser.open("https://google.com")

def play_song(song):
    speak("Playing " + song)
    pywhatkit.playonyt(song)
def weather(city):
    api_key = "your_api_key_here"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    data = requests.get(url).json()

    if data["cod"] != "404":
        temp = int(data["main"]["temp"] - 273.15)
        speak(f"Temperature in {city} is {temp} degree Celsius")
    else:
        speak("City not found")

def run_assistant():
    speak("Voice assistant activated")

    while True:
        command = take_command()

        if "time" in command:
            tell_time()

        elif "wikipedia" in command:
            query = command.replace("wikipedia", "")
            search_wiki(query)

        elif "open youtube" in command:
            open_youtube()

        elif "open google" in command:
            open_google()
