from pydantic import BaseModel, EmailStr


class TokenData(BaseModel):
    username: str | None = None


class TokenResDTO(BaseModel):
    access_token: str
    token_type: str
    username: EmailStr
