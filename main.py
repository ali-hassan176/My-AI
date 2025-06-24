import speech_recognition as sr
from gtts import gTTS
import os
import pygame
import tempfile
import time
import webbrowser
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
def processcommand(c):
    if "open google" in c.lower():
        speak("opening google")
        webbrowser.open("https://brave.com")
    elif "open youtube" in c.lower():
        speak("opening youtube")
        webbrowser.open("https://youtube.com")
    elif "open instagram" in c.lower():
        speak("opening instagram")
        webbrowser.open("https://instagram.com")
    elif "open whatsapp" in c.lower():
        speak("opening whatsapp")
        webbrowser.open("https://web.whatsapp.com")
    elif "open github" in c.lower():
        speak("opening github")
        webbrowser.open("https://github.com")
    
    
    
if __name__=="__main__":
    speak("Hi sir...")
    while True:
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
                audio = r.listen(source, timeout=2, phrase_time_limit=5)
                print("Processing...")
                word = r.recognize_google(audio)
                if (word.lower()=="friday"):
                    speak("yes sir...")
        
                    print("Friday is Active...")
                    audio = r.listen(source)
                    print("Processing...")
                    command = r.recognize_google(audio)
                    processcommand(command)
            except sr.WaitTimeoutError:
                print("Timeout: No speech detected.")
            except sr.UnknownValueError:
                print("Speech Recognition could not understand audio.")
            except sr.RequestError as e:
                print(f"Could not request results from Google: {e}")
