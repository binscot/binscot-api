import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi import FastAPI, HTTPException

from app.core.config import settings

app = FastAPI()

# Gmail SMTP 설정
SMTP_SERVER = settings.SMTP_SERVER
SMTP_PORT = settings.SMTP_PORT
SMTP_USERNAME = settings.SMTP_USERNAME
SMTP_PASSWORD = settings.SMTP_PASSWORD


def send_email(email_data):

    try:
        # 이메일 설정
        msg = MIMEMultipart()
        msg['From'] = SMTP_USERNAME
        msg['To'] = email_data.to_email
        msg['Subject'] = email_data.subject
        html_body = f"""
              {email_data.body}
               """
        msg.attach(MIMEText(html_body, 'html'))

        # SMTP 서버 연결 및 메일 전송
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, email_data.to_email, msg.as_string())
        server.quit()

        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
