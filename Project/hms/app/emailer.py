import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.exceptions import EmailError
from app.logger import logger

# Configs (in real-world projects, load from env vars)
FROM_ADDRESS = "lasyamacs08@gmail.com"
APP_PASSWORD = "rcnyfgaqitydptht"  # App password from Google
TO_ADDRESS = "lasyam2023@gmail.com"


def send_email(to_address, subject, body):
    """Send an email using Gmail SMTP"""
    try:
        msg = MIMEMultipart()
        msg["From"] = FROM_ADDRESS
        msg["To"] = to_address
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(FROM_ADDRESS, APP_PASSWORD)
        server.send_message(msg)
        server.quit()

        logger.info(f"Email sent successfully to {to_address} with subject: {subject}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        raise EmailError(str(e))
