"""
emailer.py - Utility module for sending email notifications in HMS.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from hms.app.exceptions import EmailError
from hms.app.logger import logger

# Configs (in real-world projects, load from environment variables or secrets manager)
FROM_ADDRESS = "lasyamacs08@gmail.com"
APP_PASSWORD = "rcnyfgaqitydptht"  # Gmail app-specific password
TO_ADDRESS = "lasyam2023@gmail.com"


def send_email(to_address, subject, body):
    """
    Send an email using Gmail's SMTP service.

    Args:
        to_address (str): Recipient email address.
        subject (str): Email subject.
        body (str): Email body.

    Returns:
        bool: True if the email was sent successfully.

    Raises:
        EmailError: If sending the email fails.
    """
    try:
        msg = MIMEMultipart()
        msg["From"] = FROM_ADDRESS
        msg["To"] = to_address
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(FROM_ADDRESS, APP_PASSWORD)
            server.send_message(msg)

        logger.info("Email sent successfully to %s with subject: %s", to_address, subject)
        return True
    except Exception as e:
        logger.error("Failed to send email to %s: %s", to_address, e)
        raise EmailError(str(e)) from e
