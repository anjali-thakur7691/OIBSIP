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

from modules.listen import listen
from modules.commands import execute_command
from modules.nlp import identify_command

app = Flask(__name__)


# ==========================================
# Home
# ==========================================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================================
# Listen Route
# ==========================================

@app.route("/listen")
def voice():

    try:

        # ----------------------------------
        # Quick Command From JavaScript
        # ----------------------------------

        command = request.args.get("command")

        # ----------------------------------
        # Voice Command
        # ----------------------------------

        if not command:

            print("\n🎤 Listening...")

            command = listen()

        if not command:

            return jsonify({

                "success": False,

                "command": "",

                "response": "Sorry, I couldn't hear anything."

            })

        print("User :", command)

        command = identify_command(command)

        print("Detected :", command)

        response = execute_command(command)

        print("Jarvis :", response)

        return jsonify({

            "success": True,

            "command": command,

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
# Health Check
# ==========================================

@app.route("/health")
def health():

    return jsonify({

        "status": "running",

        "project": "AI Voice Assistant"

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

        host="127.0.0.1",

        port=5000,

        debug=True

    )

    