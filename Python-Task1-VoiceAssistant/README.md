<div align="center">

# JARVIS — AI Voice Assistant

### A modern Python voice assistant built for the OASIS INFOBYTE internship

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Render](https://img.shields.io/badge/Deployed%20with-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com/)

<img src="https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=1200&q=80" alt="Abstract blue artificial intelligence visual" width="760" />

**Speak naturally. Get things done.**

</div>

---

## About the project

Jarvis is a responsive web-based voice assistant that understands spoken or typed commands, responds using browser text-to-speech, and performs useful actions such as searches, opening websites, checking time/date, weather lookup, reminders, and history tracking.

It is designed to be easy to demonstrate: no local microphone driver or PyAudio setup is required. Voice recognition runs securely in the browser.

## Highlights

| Area | What Jarvis can do |
| :-- | :-- |
| 🎙️ Voice interaction | Voice recognition plus text-to-speech responses |
| ⏰ Daily utilities | Current time, date, reminders and weather lookup |
| 🌐 Web actions | Open Google, YouTube, Gmail, WhatsApp Web and Maps |
| 🔎 Smart search | Google and general-knowledge searches from natural prompts |
| 📜 History | Stores the latest 30 text commands locally |
| 🔒 Privacy | No passwords are stored; speech is handled by the browser |

## Tech stack

```text
Backend       Python • Flask • Gunicorn
Frontend      HTML5 • CSS3 • JavaScript
Voice         Web Speech API • SpeechSynthesis API
Deployment    Render
```

## Run locally

```powershell
git clone https://github.com/anjali-thakur7691/OIBSIP.git
cd OIBSIP
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000** in Chrome or Microsoft Edge, then allow microphone access.

> If a browser does not support voice recognition, use the text-command field—every command still works.

## Try these commands

```text
Hello Jarvis
What is the time?
What is the date?
Open YouTube
Search Python voice assistant project
Who is A. P. J. Abdul Kalam?
Weather in Balaghat
Remind me to drink water
Send email
Show history
Privacy
```

## Deploy on Render

The repository includes [`render.yaml`](render.yaml), so deployment is already configured.

1. Push the latest code to GitHub.
2. In [Render](https://render.com/), select **New + → Blueprint**.
3. Select this repository and click **Apply**.
4. After the build completes, open the generated `onrender.com` URL.

For manual setup, use:

```text
Build Command  : pip install -r requirements.txt
Start Command  : gunicorn app:app
Health Check   : /health
```

## Project structure

```text
├── app.py                 # Flask routes and command engine
├── render.yaml            # Render deployment configuration
├── templates/index.html   # Voice-assistant dashboard
├── static/style.css       # Responsive visual design
├── static/script.js       # Voice input, speech and browser actions
└── data/history.json      # Created automatically at runtime
```

## Author

<div align="center">

### Anjali Thakur
**Python Developer • OASIS INFOBYTE Intern**

[![GitHub](https://img.shields.io/badge/GitHub-anjali--thakur7691-181717?style=flat-square&logo=github)](https://github.com/anjali-thakur7691)

</div>

---

<div align="center">
Made with Python and curiosity ✨
</div>
