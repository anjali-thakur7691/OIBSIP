"""
===========================================
        Email Sender Module
===========================================
Author : Anjali Thakur
Project : AI Voice Assistant
Internship : OASIS INFOBYTE
===========================================
"""

import smtplib
from email.message import EmailMessage

from config import EMAIL, PASSWORD


def send_email(receiver_email, subject, message):
    """
    Send Email using Gmail SMTP
    """

    if EMAIL == "" or PASSWORD == "":
        return "Email configuration is not completed."

    try:
        email = EmailMessage()

        email["From"] = EMAIL
        email["To"] = receiver_email
        email["Subject"] = subject

        email.set_content(message)

        server = smtplib.SMTP("smtp.gmail.com", 587)

        server.starttls()

        server.login(EMAIL, PASSWORD)

        server.send_message(email)

        server.quit()

        return "Email sent successfully."

    except smtplib.SMTPAuthenticationError:
        return "Authentication failed. Please check your Gmail App Password."

    except Exception as e:
        return f"Email Error: {e}"