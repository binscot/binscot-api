from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, ARRAY
from sqlalchemy.orm import relationship

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)

    posts = relationship("Post", back_populates="owner")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    image = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner_name = Column(String)

    owner = relationship("User", back_populates="posts")


class ChatRoom(Base):
    __tablename__ = "chat_rooms"

    id = Column(Integer, primary_key=True, index=True)
    room_name = Column(String, index=True)
    lock = Column(Boolean)
    hashed_password = Column(String)
    limit_number_rooms = Column(Integer)
    user_in_room = Column(String)
