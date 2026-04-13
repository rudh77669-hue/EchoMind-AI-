# from gtts import gTTS
# import pygame as pg
# import os
# import time
# import speech_recognition as sr

# def speak(text):
#     print("speaking")
#     try:
#         voice_path="voice_output.mp3"
#         tts=gTTS(text=text,lang='en')
#         tts.save(voice_path)
    
#         pg.mixer.init()
#         pg.mixer.music.load(voice_path)
#         pg.mixer.music.play()
        
#         while pg.mixer.music.get_busy():
#             time.sleep(0.1)
#         pg.mixer.quit()
#         os.remove(voice_path)
#     except Exception as e:
#         return f"Error : {e}"

    
# def listen_commnad():
#     print("comojnhg")
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         try:
#             r.adjust_for_ambient_noise(source, duration=1)
#             audio = r.listen(source)

#             # Try Google Speech Recognition
#             content = r.recognize_google(audio, language='en-in')
#             print("You said:", content)
#             return content.lower()

#         except sr.UnknownValueError:
#             # Speech was not understood
#             print("I didn't understand. Please say again.")
#             speak("I didn't understand. Please say again.")
#             return ""

#         except sr.RequestError:
#             # API is unreachable (no internet or Google service issue)
#             print("Could not reach the speech service. Check your internet connection.")
#             speak("Could not reach the speech service. Please check your internet connection.")
#             return ""

#         except Exception as e:
#             # Any other unexpected errors
#             print(f"[Error] {e}")
#             speak("Sorry, something went wrong.")
#             return ""

import threading
import time
import os
from gtts import gTTS
import pygame as pg
import speech_recognition as sr

# ---------- Optimized TTS (Non-blocking) ----------
def speak(text):
    """Convert text to speech and play it without blocking the main program."""
    def _speak():
        try:
            voice_path = "voice_output.mp3"
            tts = gTTS(text=text, lang='en')
            tts.save(voice_path)
            
            pg.mixer.init()
            pg.mixer.music.load(voice_path)
            pg.mixer.music.play()
            
            while pg.mixer.music.get_busy():
                time.sleep(0.1)
            pg.mixer.quit()
            os.remove(voice_path)
        except Exception as e:
            print(f"[TTS Error] {e}")

    # Run TTS in a separate thread to avoid blocking
    threading.Thread(target=_speak, daemon=True).start()


# ---------- Optimized Speech Recognition ----------
def listen_command():
    """Listen to user voice input and return text. Minimal lag."""
    r = sr.Recognizer()
    r.energy_threshold = 300             # Adjust mic sensitivity
    r.dynamic_energy_threshold = True
    r.pause_threshold = 0.5              # Shorter pause before stopping
    r.operation_timeout = 5              # Optional: max listen time

    with sr.Microphone() as source:
        print("Listening...")
        try:
            # Shorter ambient noise calibration (reduces startup delay)
            r.adjust_for_ambient_noise(source, duration=0.3)
            audio = r.listen(source, timeout=5, phrase_time_limit=7)

            # Use Google STT in the same thread (or you can move to another thread)
            content = r.recognize_google(audio, language='en-in')
            print("You said:", content)
            return content.lower()

        except sr.UnknownValueError:
            print("I didn't understand. Please say again.")
            speak("I didn't understand. Please say again.")
            return ""

        except sr.RequestError:
            print("Could not reach the speech service. Check your internet connection.")
            speak("Could not reach the speech service. Please check your internet connection.")
            return ""

        except Exception as e:
            print(f"[Error] {e}")
            speak("Sorry, something went wrong.")
            return ""


# ---------- Optional Async Version ----------
def listen_command_async(callback):
    """Listen in a separate thread and return result via callback."""
    def _listen():
        result = listen_command()
        callback(result)
    threading.Thread(target=_listen, daemon=True).start()
