"""
===========================================
        Speak Module
===========================================
Author      : Anjali Thakur
Project     : AI Voice Assistant
Internship  : OASIS INFOBYTE
===========================================
"""

import pyttsx3

from config import VOICE_RATE, VOICE_INDEX

# Initialize engine only once
engine = pyttsx3.init()

engine.setProperty("rate", VOICE_RATE)

voices = engine.getProperty("voices")

if len(voices) > VOICE_INDEX:
    engine.setProperty("voice", voices[VOICE_INDEX].id)


def speak(text):
    """
    Convert text to speech.
    """

    print(f"Jarvis : {text}")

    engine.say(text)

    engine.runAndWait()