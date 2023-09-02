from typing import List

from pydantic import BaseModel, EmailStr, field_validator
from pydantic_core.core_schema import FieldValidationInfo

from app.schemas.post_schemas import Post


class UserBase(BaseModel):
    id: int
    username: EmailStr
    disabled: bool | None = None
    posts: List[Post] = []


class UserInDB(UserBase):
    hashed_password: str

    class Config:
        from_attributes = True


class UserCreateReqDTO(BaseModel):
    username: EmailStr
    password1: str
    password2: str

    @field_validator('username', 'password1', 'password2')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError(v, '빈 값은 허용되지 않습니다.')
        return v

    @field_validator('password2')
    def passwords_match(cls, v, info: FieldValidationInfo):
        if 'password1' in info.data and v != info.data['password1']:
            raise ValueError(v, 'passwords do not match')
        return v


class UserResDTO(UserBase):
    pass
