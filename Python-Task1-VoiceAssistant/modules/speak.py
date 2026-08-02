"""
===========================================
        Speak Module
===========================================
Author      : Anjali Thakur
Project     : AI Voice Assistant
Internship  : OASIS INFOBYTE
===========================================
"""

try:
    import pyttsx3
    from config import VOICE_RATE, VOICE_INDEX

    engine = pyttsx3.init()
    engine.setProperty("rate", VOICE_RATE)

    voices = engine.getProperty("voices")

    if len(voices) > VOICE_INDEX:
        engine.setProperty("voice", voices[VOICE_INDEX].id)

    TTS_AVAILABLE = True

except Exception:
    TTS_AVAILABLE = False


def speak(text):
    """
    Convert text to speech (Render Safe)
    """
    print(f"Jarvis : {text}")

    if TTS_AVAILABLE:
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception:
            pass