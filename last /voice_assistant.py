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

# -------- BASIC FEATURES --------

def tell_time():
    time_now = datetime.datetime.now().strftime('%I:%M %p')
    speak("Current time is " + time_now)

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

# -------- WEATHER --------

def weather(city):
    api_key = "YOUR_API_KEY"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    data = requests.get(url).json()

    if data["cod"] != "404":
        temp = int(data["main"]["temp"] - 273.15)
        speak(f"Temperature in {city} is {temp} degree Celsius")
    else:
        speak("City not found")

# -------- APP CONTROL --------

def open_app(app_name):
    apps = {
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"
    }

    if app_name in apps:
        speak(f"Opening {app_name}")
        os.startfile(apps[app_name])
    else:
        speak("App not found")

# -------- SCREENSHOT --------

def take_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    speak("Screenshot taken")

# -------- MEMORY --------

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

# -------- EMAIL --------

def send_email():
    speak("What should I say?")
    content = take_command()

    yag = yagmail.SMTP('your_email@gmail.com', 'your_app_password')
    yag.send('receiver@gmail.com', 'Voice Assistant Message', content)

    speak("Email sent")

# -------- REMINDER --------

def set_reminder():
    speak("What should I remind you?")
    task = take_command()

    speak("After how many seconds?")
    delay = take_command()

    try:
        delay = int(delay)
        speak("Reminder set")
        time.sleep(delay)
        speak("Reminder: " + task)
    except:
        speak("Invalid time")

# -------- MAIN LOOP --------

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

        elif "play" in command:
            song = command.replace("play", "")
            play_song(song)

        elif "weather" in command:
            speak("Tell city name")
            city = take_command()
            weather(city)

        elif "open" in command:
            app = command.replace("open", "").strip()
            open_app(app)

        elif "screenshot" in command:
            take_screenshot()

        elif "remember this" in command:
            save_note()

        elif "what do you remember" in command:
            read_notes()

        elif "send email" in command:
            send_email()

        elif "remind me" in command:
            set_reminder()

        elif "shutdown" in command:
            speak("Shutting down system")
            os.system("shutdown /s /t 5")

        elif "stop" in command:
            speak("Goodbye")
            break

run_assistant()
