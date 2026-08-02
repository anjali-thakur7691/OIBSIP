"""
===========================================
        System Commands Module
===========================================
Author      : Anjali Thakur
Project     : AI Voice Assistant
Internship  : OASIS INFOBYTE
===========================================
"""

import os
import webbrowser


# ==========================
# Notepad
# ==========================
def open_notepad():
    try:
        os.system("notepad")
        return "Opening Notepad"
    except Exception as e:
        return f"Error opening Notepad: {e}"


# ==========================
# Calculator
# ==========================
def open_calculator():
    try:
        os.system("calc")
        return "Opening Calculator"
    except Exception as e:
        return f"Error opening Calculator: {e}"


# ==========================
# Camera
# ==========================

def open_camera():

    return "Camera feature works only on local desktop application."

# ==========================
# Google
# ==========================
def open_google():

    webbrowser.open("https://www.google.com")

    return "Opening Google."


# ==========================
# YouTube
# ==========================
def open_youtube():

    webbrowser.open("https://www.youtube.com")

    return "Opening YouTube."


# ==========================
# Gmail
# ==========================
def open_gmail():

    webbrowser.open("https://mail.google.com")

    return "Opening Gmail."


# ==========================
# WhatsApp
# ==========================
def open_whatsapp():

    webbrowser.open("https://web.whatsapp.com")

    return "Opening WhatsApp."


# ==========================
# Google Maps
# ==========================
def open_maps():

    webbrowser.open("https://maps.google.com")

    return "Opening Google Maps."


# ==========================
# ChatGPT
# ==========================
def open_chatgpt():

    webbrowser.open("https://chat.openai.com")

    return "Opening ChatGPT."