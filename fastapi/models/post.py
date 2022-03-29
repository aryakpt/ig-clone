from typing import List, Optional
from datetime import date, datetime
from databases.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from models.comment import CommentSchema


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    image_url = Column(String(255), default="default.jpg")
    image_url_type = Column(String(255))
    caption = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime, nullable=True)
    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete",
                            passive_deletes=True)


class UserBase(BaseModel):
    id: int
    username: str
    email: str
    password: str

    class Config:
        orm_mode = True


class PostSchema(BaseModel):
    id: int
    image_url: str
    image_url_type: str
    caption: str
    created_at: datetime
    updated_at: Optional[datetime]
    user: UserBase
    comments: List[CommentSchema] = []

    class Config:
        orm_mode = True


class PostSchemaCreate(BaseModel):
    user_id: int
    image_url: Optional[str] = "default.jpg"
    image_url_type: str
    caption: str


class PostSchemaUpdate(BaseModel):
    user_id: int
    image_url: str
    image_url_type: str
    caption: str
