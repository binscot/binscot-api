from typing import Optional

from pydantic import BaseModel, field_validator


class PostBase(BaseModel):
    title: str
    content: Optional[str] = None
    image: str


class PostResDTO(PostBase):
    id: int
    owner_id: int
    owner_name: str

    class Config:
        from_attributes = True


# class PostResDTO(BaseModel):
#     id: int
#     title: str
#     content: str
#     image: str
#     owner_id: int
#     owner_name: str


class PostCreateReqDTO(PostBase):
    pass

    @field_validator('title', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError(v, '빈 값은 허용되지 않습니다.')
        return v
