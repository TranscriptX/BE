import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import traceback

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

SERVER_URL = os.getenv("SERVER_URL")

def send_email(to_email: str, subject: str, body: str):
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = SMTP_USERNAME
        msg["To"] = to_email
        msg.set_content(body)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
            smtp.send_message(msg)

        return True
    except Exception as e:
        print(traceback.format_exc())
        return False


def send_verification_email(email: str, token: str):
    subject = "Email Verification - TranscriptX"
    body = f"Hello,\n\nPlease verify your email by clicking link below:\n\n{SERVER_URL}/api/auth/verify-email?token={token}\n\nThank you!"
    return send_email(email, subject, body)


def send_reset_password_email(email: str, token: str):
    subject = "Reset Password - TranscriptX"
    body = f"Hello,\n\nUse the following token to reset your password:\n\n{token}\n\nThank you!"
    return send_email(email, subject, body)