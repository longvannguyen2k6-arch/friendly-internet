"""Tiny e-mail helper built on the standard library (smtplib)."""
import logging
import smtplib
import ssl
from email.message import EmailMessage

import config

log = logging.getLogger(__name__)


def send_email(to, subject, body):
    """Send a plain-text e-mail. Returns True on success, False otherwise.

    If SMTP_HOST is not configured (local development) nothing is sent and the
    message is printed to the server console so the flow can still be tested.
    """
    if not config.SMTP_HOST:
        print(f"\n--- E-mail not sent (SMTP not configured) ---\nTo: {to}\nSubject: {subject}\n\n{body}\n---")
        return False

    msg = EmailMessage()
    msg["From"] = config.SMTP_FROM or config.SMTP_USER
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    context = ssl.create_default_context()
    try:
        if config.SMTP_SSL:
            server = smtplib.SMTP_SSL(config.SMTP_HOST, config.SMTP_PORT, timeout=10, context=context)
        else:
            server = smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT, timeout=10)
        with server:
            if not config.SMTP_SSL and config.SMTP_TLS:
                server.starttls(context=context)
            if config.SMTP_USER:
                server.login(config.SMTP_USER, config.SMTP_PASSWORD)
            server.send_message(msg)
        return True
    except (smtplib.SMTPException, OSError):
        log.exception("Could not send e-mail to %s", to)
        return False


def send_reset_code(to, username, code, minutes):
    return send_email(
        to,
        "Your Friendly Internet password reset code",
        f"Hi {username},\n\n"
        f"Your password reset code is: {code}\n\n"
        f"It expires in {minutes} minutes. If you did not ask for this, you can ignore this e-mail "
        f"and your password will stay the same.\n\n"
        f"Friendly Internet",
    )
