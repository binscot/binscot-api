from pydantic import BaseModel, EmailStr


class EmailData(BaseModel):
    to_email: EmailStr
    subject: str
    body: str
