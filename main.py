import speech_recognition as sr
from gtts import gTTS
import os
import pygame
import tempfile
import time

def speak(text):
    tts = gTTS(text=text, lang='en', slow=True)  # Slower and smoother
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        pygame.mixer.init()
        pygame.mixer.music.load(fp.name)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        pygame.mixer.quit()
        os.remove(fp.name)


r = sr.Recognizer()

try:
    mic = sr.Microphone(device_index=4)
except Exception as e:
    print("Could not initialize microphone:", e)
    exit()

with mic as source:
    print("Calibrating mic... please stay silent.")
    r.adjust_for_ambient_noise(source, duration=1)
    print("Mic calibrated with ambient noise level:", r.energy_threshold)
    print("Listening now...")
    try:
        audio = r.listen(source, timeout=5, phrase_time_limit=5)
        print("Processing...")
        text = r.recognize_google(audio)
        print("You said:", text)
        speak("You said " + text)
    except sr.WaitTimeoutError:
        print("Timeout: No speech detected.")
    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google: {e}")
