"""
===========================================
        AI Voice Assistant
        NLP Module
===========================================
Author : Anjali Thakur
Project : AI Voice Assistant
Internship : OASIS INFOBYTE
===========================================
"""


# ==========================================
# Identify Command
# ==========================================

def identify_command(command):

    command = command.lower().strip()


    # ==========================================
    # Greeting
    # ==========================================

    greeting = [

        "hi",

        "hello",

        "hey",

        "good morning",

        "good afternoon",

        "good evening"

    ]

    if any(word in command for word in greeting):

        return "hello"


    # ==========================================
    # Time
    # ==========================================

    if any(word in command for word in [

        "time",

        "current time",

        "what time is it",

        "tell me the time"

    ]):

        return "time"


    # ==========================================
    # Date
    # ==========================================

    if any(word in command for word in [

        "date",

        "today",

        "today date",

        "current date"

    ]):

        return "date"


    # ==========================================
    # Weather
    # ==========================================

    if any(word in command for word in [

        "weather",

        "temperature",

        "climate"

    ]):

        return "weather"


    # ==========================================
    # Open Applications
    # ==========================================

    app_commands = {

        "google": [

            "open google",

            "launch google"

        ],

        "youtube": [

            "open youtube",

            "launch youtube"

        ],

        "gmail": [

            "open gmail"

        ],

        "whatsapp": [

            "open whatsapp"

        ],

        "chrome": [

            "open chrome"

        ],

        "notepad": [

            "open notepad"

        ],

        "calculator": [

            "open calculator",

            "calc"

        ],

        "camera": [

            "open camera"

        ],

        "github": [

            "open github"

        ],

        "linkedin": [

            "open linkedin"

        ],

        "vscode": [

            "open vscode",

            "open vs code"

        ]

    }

    for app, phrases in app_commands.items():

        if any(p in command for p in phrases):

            return f"open {app}"


    # ==========================================
    # Music
    # ==========================================

    if "play music" in command:

        return "play music"

    if "pause music" in command:

        return "pause music"

    if "resume music" in command:

        return "resume music"

    if "stop music" in command:

        return "stop music"

    if "next song" in command:

        return "next song"


    # ==========================================
    # Search
    # ==========================================

    if command.startswith("search"):

        return command


    # ==========================================
    # Wikipedia
    # ==========================================

    if command.startswith("who is"):

        return command


    # ==========================================
    # Joke
    # ==========================================

    if "joke" in command:

        return "joke"


    # ==========================================
    # System Information
    # ==========================================

    if any(word in command for word in [

        "system information",

        "computer information",

        "system info",

        "pc information"

    ]):

        return "system information"


    # ==========================================
    # Reminder
    # ==========================================

    if "reminder" in command:

        return "set reminder"


    # ==========================================
    # Email
    # ==========================================

    if "send email" in command:

        return "send email"


    # ==========================================
    # Exit
    # ==========================================

    if any(word in command for word in [

        "bye",

        "goodbye",

        "exit"

    ]):

        return "exit"


    # ==========================================
    # Default
    # ==========================================

    return command
