from itsdangerous import URLSafeTimedSerializer
import smtplib
from email.message import EmailMessage
import os

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")
SALT = "email-confirmation"
EMAIL_FROM = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

def generate_confirmation_token(email: str):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt=SALT)

def verify_confirmation_token(token: str, expiration=3600):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        return serializer.loads(token, salt=SALT, max_age=expiration)
    except Exception:
        return None

async def send_email_async(to_email: str, subject: str, body: str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = to_email
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_FROM, SMTP_PASSWORD)
        smtp.send_message(msg)
