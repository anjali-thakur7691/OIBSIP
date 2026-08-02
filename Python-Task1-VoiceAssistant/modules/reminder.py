"""
===========================================
        Reminder Module
===========================================
Author : Anjali Thakur
Project : AI Voice Assistant
Internship : OASIS INFOBYTE
===========================================
"""

import threading
import time

from modules.speak import speak


def reminder(seconds, message):
    """
    Background reminder
    """

    time.sleep(seconds)

    speak(f"Reminder! {message}")

    print(f"\n⏰ Reminder: {message}")


def set_reminder(seconds, message):
    """
    Start reminder thread
    """

    try:

        thread = threading.Thread(
            target=reminder,
            args=(seconds, message),
            daemon=True
        )

        thread.start()

        return f"Reminder has been set for {seconds} seconds."

    except Exception as e:
        return f"Reminder Error: {e}"