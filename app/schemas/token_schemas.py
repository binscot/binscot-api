from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str
    username: EmailStr


class TokenData(BaseModel):
    username: str | None = None



