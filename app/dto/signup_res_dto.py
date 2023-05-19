from pydantic import BaseModel, EmailStr


# DTO 정의
class User(BaseModel):
    id: int
    username: EmailStr
