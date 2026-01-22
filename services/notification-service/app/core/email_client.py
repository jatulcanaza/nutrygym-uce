import smtplib
from email.message import EmailMessage

from app.core.config import (
    SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, SMTP_FROM,
    SMTP_USE_TLS, MAX_EMAIL_BODY_CHARS
)
from app.core.logger import get_logger

log = get_logger("email-client")

def send_email(to: str, subject: str, body: str) -> None:
    body_safe = (body or "")[:MAX_EMAIL_BODY_CHARS]

    msg = EmailMessage()
    msg["From"] = SMTP_FROM
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body_safe)

    try:
        if SMTP_USE_TLS:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(SMTP_USER, SMTP_PASS)
                server.send_message(msg)
        else:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20) as server:
                server.ehlo()
                server.login(SMTP_USER, SMTP_PASS)
                server.send_message(msg)

        log.info("Email sent to=%s subject=%s", to, subject)
    except Exception as e:
        log.exception("Failed to send email to=%s subject=%s error=%s", to, subject, str(e))
        raise
