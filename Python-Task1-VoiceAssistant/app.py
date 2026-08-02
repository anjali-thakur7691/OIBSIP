"""
===========================================
        AI Voice Assistant
===========================================
Author      : Anjali Thakur
Project     : AI Voice Assistant
Internship  : OASIS INFOBYTE
===========================================
"""

from flask import Flask, render_template, jsonify, request
import os
from config import ASSISTANT_NAME

# ==========================================
# Safe Import (Render Compatible)
# ==========================================

try:
    from modules.listen import listen
    VOICE_AVAILABLE = True
except Exception as e:
    print("Listen Module Disabled :", e)

    VOICE_AVAILABLE = False

    def listen():
        return ""

from modules.commands import execute_command
from modules.nlp import identify_command
from modules.history import get_history, clear_history

# ==========================================
# Flask App
# ==========================================

app = Flask(__name__)

# ==========================================
# Home
# ==========================================

@app.route("/")
def home():

    return render_template("index.html")

# ==========================================
# Process Command Route (For JavaScript)
# ==========================================

@app.route("/process", methods=["POST"])
def process_command():
    try:
        data = request.get_json()
        command = data.get("command", "")

        if not command:
            return jsonify({
                "success": False,
                "command": "",
                "response": "Sorry, I didn't receive any command."
            })

        print("User :", command)

        # NLP Processing
        detected_command = identify_command(command)
        print("Detected :", detected_command)

        # Execute Command
        response = execute_command(detected_command)
        print("Jarvis :", response)

        return jsonify({
            "success": True,
            "command": detected_command,
            "response": response
        })

    except Exception as e:
        print("ERROR :", e)
        return jsonify({
            "success": False,
            "command": "",
            "response": str(e)
        })

# ==========================================
# Listen Route
# ==========================================

@app.route("/listen")
def voice():

    try:

        # ----------------------------------
        # Command from Browser / JavaScript
        # ----------------------------------

        command = request.args.get("command")


        # ----------------------------------
        # Voice Input (Only Local PC)
        # ----------------------------------

        if not command:

            if VOICE_AVAILABLE:

                print("🎤 Listening...")

                command = listen()

            else:

                return jsonify({

                    "success": False,

                    "command": "",

                    "response": "Voice input is not available on server."

                })


        if not command:

            return jsonify({

                "success": False,

                "command": "",

                "response": "Sorry, I couldn't hear anything."

            })


        print("User :", command)


        # ----------------------------------
        # NLP Processing
        # ----------------------------------

        detected_command = identify_command(command)


        print("Detected :", detected_command)


        # ----------------------------------
        # Execute Command
        # ----------------------------------

        response = execute_command(
            detected_command
        )


        print("Jarvis :", response)


        return jsonify({

            "success": True,

            "command": detected_command,

            "response": response

        })


    except Exception as e:


        print("ERROR :", e)


        return jsonify({

            "success": False,

            "command": "",

            "response": str(e)

        })


    # ==========================================
# History Route
# ==========================================

@app.route("/history", methods=["GET", "DELETE"])
def history():

    if request.method == "GET":
        return jsonify(get_history())

    clear_history()

    return jsonify({
        "success": True,
        "message": "History cleared successfully."
    })
    # ==========================================
# Health Check Route
# ==========================================

@app.route("/health")
def health():

    return jsonify({

        "status": "running",

        "assistant": ASSISTANT_NAME,

        "voice": VOICE_AVAILABLE

    })

# ==========================================
# Main
# ==========================================

if __name__ == "__main__":

    print("=" * 60)

    print("🤖 AI Voice Assistant Started")

    print("🌐 http://127.0.0.1:5000")

    print("=" * 60)

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )