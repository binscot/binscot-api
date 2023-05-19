from typing import List
from pydantic import BaseModel, EmailStr, validator
from app.schemas.post_schemas import Post


class UserBase(BaseModel):
    username: EmailStr


class User(BaseModel):
    id: int
    username: EmailStr
    disabled: bool | None = None
    posts: List[Post] = []


class UserInDB(User):
    hashed_password: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: EmailStr
    password1: str
    password2: str

    @validator('username', 'password1', 'password2')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

    @validator('password2')
    def passwords_match(cls, v, values):
        if 'password1' in values and v != values['password1']:
            raise ValueError('비밀번호가 일치하지 않습니다')
        return v
