from pydantic import BaseModel, EmailStr, field_validator


class EmailReqDTO(BaseModel):
    to_email: EmailStr
    subject: str
    body: str
    template: str

    @field_validator('to_email', 'subject', 'body', 'template')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError(v, '빈 값은 허용되지 않습니다.')
        return v
