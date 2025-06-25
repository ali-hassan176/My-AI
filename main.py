import speech_recognition as sr
from gtts import gTTS
import os
import pygame
import tempfile
import time
import webbrowser
import musiclibrary  # This should be your local file with song name -> URL mapping
from datetime import datetime
# Initialize the speech recognizer
recognizer = sr.Recognizer()
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8
recognizer.phrase_threshold = 0.3

# Speak a message using Google Text-to-Speech and pygame
def speak(text):
    try:
        tts = gTTS(text=text, lang='en', slow=False)  # Use fast female voice
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            pygame.mixer.init()
            pygame.mixer.music.load(fp.name)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            pygame.mixer.quit()
            os.unlink(fp.name)
    except Exception as e:
        print(f"Speak error: {e}")

# Listen from microphone and return recognized text
def listen(source, timeout=3, phrase_time_limit=5):
    try:
        audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        text = recognizer.recognize_google(audio, language="en-US").lower()
        return text
    except sr.WaitTimeoutError:
        return None
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print(f"Speech recognition error: {e}")
        return None


# Process spoken command
def process_command(command):
    if not command:
        return

    command = command.lower()
    
    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "open instagram" in command:
        speak("Opening Instagram")
        webbrowser.open("https://www.instagram.com")

    elif "open whatsapp" in command:
        speak("Opening WhatsApp")
        webbrowser.open("https://web.whatsapp.com")

    elif "open github" in command:
        speak("Opening GitHub")
        webbrowser.open("https://github.com")

    elif "open linkedin" in command:
        speak("Opening LinkedIn")
        webbrowser.open("https://www.linkedin.com")

    elif "open deepseek" in command:
        speak("Opening DeepSeek")
        webbrowser.open("https://chat.deepseek.com")

    elif "open chatgpt" in command:
        speak("Opening ChatGPT")
        webbrowser.open("https://chatgpt.com")

    elif command.startswith("play"):
        song = command.split("play")[-1].strip()
        if song in musiclibrary.music:
            speak(f"Playing {song}")
            webbrowser.open(musiclibrary.music[song])
        else:
            speak("Song not found in library.")

    elif "time" in command:
        now = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {now}")
    elif "date" in command or "day" in command:
        today = datetime.now().strftime("%A, %B %d")
        speak(f"Today is {today}")
    elif "exit" in command or "shutdown" in command or "stop" in command:
        speak("Goodbye, sir. Shutting down.")
        exit()
    else:
        speak("I did not understand the command.")
# ... same imports ...

def is_wake_word(text):
    if not text:
        return False
    text = text.lower()
    # Flexible check (you can expand this list)
    wake_words = ["friday", "hey friday", "hi friday", "fridy", "fry day", "freddy"]
    return any(word in text for word in wake_words)

# ... rest of the same code ...

if __name__ == "__main__":
    try:
        mic = sr.Microphone(device_index=4)
    except Exception as e:
        print("Could not initialize microphone:", e)
        exit()

    with mic as source:
        print("Calibrating mic... stay silent.")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Calibration complete.")
        speak("Hi sir. Say 'Friday' to activate me.")

        while True:
            print("Waiting for wake word...")
            heard = listen(source, timeout=4, phrase_time_limit=3)

            if heard:
                print(f"Wake word check: Heard '{heard}'")
            else:
                print("No speech detected for wake word.")

            if is_wake_word(heard):
                speak("Yes sir, I am listening.")

                last_command_time = time.time()
                while time.time() - last_command_time < 15:
                    print("Listening for command...")
                    command = listen(source, timeout=4, phrase_time_limit=5)

                    if command:
                        print("Command heard:", command)
                        process_command(command)
                        last_command_time = time.time()
                    else:
                        print("No command detected.")

                speak("Going back to sleep.")

