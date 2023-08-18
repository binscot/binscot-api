import json
import smtplib
from email.message import EmailMessage

from fastapi import HTTPException
from fastapi.templating import Jinja2Templates

from app.core.config import settings

# Gmail SMTP 설정
SMTP_SERVER = settings.SMTP_SERVER
SMTP_PORT = settings.SMTP_PORT
SMTP_USERNAME = settings.SMTP_USERNAME
SMTP_PASSWORD = settings.SMTP_PASSWORD

templates = Jinja2Templates(directory="resource/templates")


def send_email_server_state(email_data):
    try:
        email = EmailMessage()
        email["From"] = SMTP_USERNAME
        email["To"] = email_data.to_email
        email["Subject"] = email_data.subject

        template_context = json.loads(email_data.body)
        email_content = templates.get_template(email_data.template).render(**template_context)
        email.set_content(email_content, subtype="html")

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
            smtp.send_message(email)

        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def send_email(email_data):
    try:
        # 이메일 설정
        email = EmailMessage()
        email["From"] = SMTP_USERNAME
        email["To"] = email_data.to_email
        email["Subject"] = email_data.subject

        template_context = {"body": email_data.body}
        email_content = templates.get_template(email_data.template).render(**template_context)
        email.set_content(email_content, subtype="html")

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
            smtp.send_message(email)

        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
