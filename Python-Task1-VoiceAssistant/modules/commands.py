"""
===========================================
        AI Voice Assistant
        Commands Module
===========================================
Author : Anjali Thakur
Project : AI Voice Assistant
Internship : OASIS INFOBYTE
===========================================
"""

import datetime
# import pywhatkit
import webbrowser
import wikipedia
import pyjokes

from modules.weather import get_weather
# from modules.email_sender import send_email
from modules.reminder import set_reminder
from modules.system_info import get_system_info
from modules.history import save_history, get_history

from modules.music import (
    play_music,
    stop_music,
    pause_music,
    resume_music
)

from modules.system_commands import (
    open_google,
    open_youtube,
    open_gmail,
    open_whatsapp,
    open_notepad,
    open_calculator,
    open_camera
)


def execute_command(command):

    command = command.lower().strip()

    # -------------------------
    # Greeting
    # -------------------------

    if "hello" in command or "hi" in command:

        response = "Hello Anjali. How can I help you today?"

    # -------------------------
    # Time
    # -------------------------

    elif "time" in command:

        current_time = datetime.datetime.now().strftime("%I:%M %p")

        response = f"The current time is {current_time}"

    # -------------------------
    # Date
    # -------------------------

    elif "date" in command:

        current_date = datetime.datetime.now().strftime("%d %B %Y")

        response = f"Today is {current_date}"

    # -------------------------
    # Weather
    # -------------------------

    elif "weather" in command:

        response = get_weather()

    # -------------------------
    # Google
    # -------------------------

    elif "open google" in command:

        response = open_google()

    # -------------------------
    # YouTube
    # -------------------------

    elif "open youtube" in command:

        response = open_youtube()

    # -------------------------
    # Gmail
    # -------------------------

    elif "open gmail" in command:

        response = open_gmail()

    # -------------------------
    # WhatsApp
    # -------------------------

    elif "open whatsapp" in command:

        response = open_whatsapp()

    # -------------------------
    # Notepad
    # -------------------------

    elif "open notepad" in command:

        response = open_notepad()

    # -------------------------
    # Calculator
    # -------------------------

    elif "open calculator" in command:

        response = open_calculator()

    # -------------------------
    # Camera
    # -------------------------

    elif "open camera" in command:

        response = open_camera()

    # -------------------------
    # Play Music
    # -------------------------

    elif "play music" in command:

        response = play_music()

    # -------------------------
    # Stop Music
    # -------------------------

    elif "stop music" in command:

        response = stop_music()

    # -------------------------
    # Pause Music
    # -------------------------

    elif "pause music" in command:

        response = pause_music()

    # -------------------------
    # Resume Music
    # -------------------------

    elif "resume music" in command:

        response = resume_music()

    # -------------------------
    # Next Song
    # -------------------------

    elif "next song" in command:

        response = "Next song feature will be added soon."

    # -------------------------
    # Google Search
    # -------------------------

    elif command.startswith("search"):

        search_query = command.replace("search", "").strip()

        if search_query:

            webbrowser.open(f"https://www.google.com/search?q={search_query}")

            response = f"Searching {search_query} on Google."

        else:

            response = "Please tell me what you want to search."

    # -------------------------
    # Wikipedia (Who is / What is / Tell me about)
    # -------------------------

    elif command.startswith("who is") or command.startswith("what is") or command.startswith("tell me about"):

        person = command.replace("who is", "").replace("what is", "").replace("tell me about", "").strip()

        try:

            response = wikipedia.summary(
                person,
                sentences=2
            )

        except Exception:

            response = "Sorry, I couldn't find any information."

    # -------------------------
    # Joke
    # -------------------------

    elif "joke" in command:

        response = pyjokes.get_joke()

    # -------------------------
    # System Information
    # -------------------------

    elif "system information" in command \
            or "computer information" in command \
            or "pc information" in command:

        response = get_system_info()

    # -------------------------
    # Reminder
    # -------------------------

    elif "set reminder" in command or "remind me" in command:

        response = set_reminder(
            10,
            "Please drink water."
        )

    # -------------------------
    # Email
    # -------------------------

    elif "send email" in command:

        response = "Email feature is ready. Browser form connection will be added soon."

    # -------------------------
    # Show History
    # -------------------------

    elif "show history" in command:

        response = "Here is your recent command history."

    # -------------------------
    # Privacy
    # -------------------------

    elif "privacy" in command:

        response = "Voice recognition happens in your browser and text commands are handled securely."

    # -------------------------
    # Exit
    # -------------------------

    elif "exit" in command \
            or "bye" in command \
            or "goodbye" in command:

        response = "Good Bye Anjali. Have a nice day."

    # -------------------------
    # Unknown Command
    # -------------------------

    else:

        response = "Sorry, I don't understand this command."

    # -------------------------
    # Save History
    # -------------------------

    save_history(
        command,
        response
    )

    return response