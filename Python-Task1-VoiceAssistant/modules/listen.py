"""
===========================================
        Listen Module
===========================================
Author      : Anjali Thakur
Project     : AI Voice Assistant
Internship  : OASIS INFOBYTE
===========================================
"""

import speech_recognition as sr
from config import LANGUAGE


def listen():
    recognizer = sr.Recognizer()

    recognizer.pause_threshold = 0.8
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True

    try:
        with sr.Microphone() as source:

            print("🎤 Listening...")

            # Reduce delay
            recognizer.adjust_for_ambient_noise(source, duration=0.2)

            audio = recognizer.listen(
    source,
    timeout=5,
    phrase_time_limit=6
)

        print("🔍 Recognizing...")

        command = recognizer.recognize_google(
            audio,
            language=LANGUAGE
        )

        command = command.lower().strip()

        print("User :", command)

        return command

    except sr.WaitTimeoutError:
        print("❌ No speech detected.")
        return ""

    except sr.UnknownValueError:
        print("❌ Could not understand.")
        return ""

    except sr.RequestError:
        print("❌ Internet connection error.")
        return ""

    except OSError:
        print("❌ Microphone not found.")
        return ""

    except Exception as e:
        print("Listen Error :", e)
        return ""