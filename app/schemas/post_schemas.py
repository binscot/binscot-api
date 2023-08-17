from typing import Optional

from pydantic import BaseModel, field_validator


class PostBase(BaseModel):
    title: str
    content: Optional[str] = None
    image: str


class Post(PostBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class PostCreate(PostBase):
    pass

    @field_validator('title', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError(v, '빈 값은 허용되지 않습니다.')
        return v
