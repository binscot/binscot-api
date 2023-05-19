from typing import Optional

from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: Optional[str] = None
    image: str


class Post(PostBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    pass
