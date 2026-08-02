"""
===========================================
        Command History Module
===========================================
Author      : Anjali Thakur
Project     : AI Voice Assistant
Internship  : OASIS INFOBYTE
===========================================
"""

import json
import os
from datetime import datetime

HISTORY_FILE = "data/history.json"


def save_history(command, response):
    """
    Save every command and response in history.json
    """

    try:

        if not os.path.exists("data"):
            os.makedirs("data")

        if not os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "w") as file:
                json.dump([], file)

        with open(HISTORY_FILE, "r") as file:
            try:
                history = json.load(file)
            except json.JSONDecodeError:
                history = []

        history.append({
            "time": datetime.now().strftime("%d-%m-%Y %I:%M:%S %p"),
            "command": command,
            "response": response
        })

        with open(HISTORY_FILE, "w") as file:
            json.dump(history, file, indent=4)

    except Exception as e:
        print("History Error :", e)


def get_history():
    """
    Return complete history
    """

    try:

        if not os.path.exists(HISTORY_FILE):
            return []

        with open(HISTORY_FILE, "r") as file:
            try:
                history = json.load(file)
            except json.JSONDecodeError:
                history = []

        return history

    except Exception as e:
        print("History Error :", e)
        return []


def clear_history():
    """
    Delete all history
    """

    try:

        with open(HISTORY_FILE, "w") as file:
            json.dump([], file)

        return "History Cleared"

    except Exception as e:
        return f"History Error : {e}"