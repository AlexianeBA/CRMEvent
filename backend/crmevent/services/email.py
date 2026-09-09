import os
import smtplib
from email.message import EmailMessage

from fastapi import HTTPException


def _as_bool(value: str | None) -> bool:
    return str(value or "").lower() in {"1", "true", "yes", "on"}


def send_email(recipient: str, subject: str, body: str, reply_to: str | None = None):
    host = os.getenv("SMTP_HOST")
    port = int(os.getenv("SMTP_PORT", "587"))
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")
    sender = os.getenv("SMTP_FROM_EMAIL") or username
    use_tls = _as_bool(os.getenv("SMTP_USE_TLS", "true"))
    use_ssl = _as_bool(os.getenv("SMTP_USE_SSL", "false"))

    if not host or not sender:
        raise HTTPException(
            status_code=503,
            detail="Le serveur SMTP n'est pas configuré",
        )
    if use_tls and use_ssl:
        raise HTTPException(
            status_code=500,
            detail="Configuration SMTP invalide : TLS et SSL ne peuvent pas être activés ensemble",
        )

    message = EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    if reply_to:
        message["Reply-To"] = reply_to
    message.set_content(body)

    smtp_class = smtplib.SMTP_SSL if use_ssl else smtplib.SMTP
    try:
        with smtp_class(host, port, timeout=15) as smtp:
            if use_tls:
                smtp.starttls()
            if username and password:
                smtp.login(username, password)
            smtp.send_message(message)
    except (smtplib.SMTPException, OSError) as error:
        raise HTTPException(
            status_code=502,
            detail="L'envoi de l'email a échoué. Vérifiez la configuration SMTP",
        ) from error
