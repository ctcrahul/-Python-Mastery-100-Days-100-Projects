import speech_recognition as sr
import re

# Common filler words list
FILLER_WORDS = [
    "um", "uh", "er", "ah",
    "like", "you know",
    "basically", "actually",
    "literally", "so", "well"
]

def detect_fillers(text):
    text = text.lower()
    words = re.findall(r"\b\w+\b", text)

    filler_count = 0
    filler_hits = {}

    for filler in FILLER_WORDS:
        count = len(re.findall(r"\b" + re.escape(filler) + r"\b", text))
        if count > 0:
            filler_hits[filler] = count
            filler_count += count

    total_words = len(words)
    filler_ratio = round((filler_count / total_words) * 100, 2) if total_words > 0 else 0

    return total_words, filler_count, filler_ratio, filler_hits


# Speech to text
recognizer = sr.Recognizer()

print("Speak your answer (press Ctrl+C to stop)...")

with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

try:
    text = recognizer.recognize_google(audio)
    print("\nTranscribed Text:")
    print(text)

    total, fillers, ratio, details = detect_fillers(text)

    print("\n--- Filler Word Analysis ---")
    print("Total words:", total)
    print("Filler words used:", fillers)
    print("Filler density:", ratio, "%")
    print("Details:", details)

    if ratio > 8:
        print("⚠ Too many filler words. You sound unprepared.")
    elif ratio > 4:
        print("⚠ Moderate filler usage. Needs improvement.")
    else:
        print("✅ Good clarity. Minimal filler usage.")

except sr.UnknownValueError:
    print("Could not understand speech")
except sr.RequestError:
    print("Speech recognition service error")
