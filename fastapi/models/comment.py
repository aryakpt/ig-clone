from typing import Optional
from datetime import datetime
from databases.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from pydantic import BaseModel


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    post_id = Column(Integer, ForeignKey(
        "posts.id", ondelete="CASCADE"), nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime, nullable=True)
    user = relationship("User")
    post = relationship("Post", back_populates="comments")


class PostBase(BaseModel):
    id: int
    image_url: str
    image_url_type: str
    caption: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class CommentSchema(BaseModel):
    id: int
    comment: str
    created_at: datetime
    updated_at: Optional[datetime]
    user: UserBase
    post: PostBase

    class Config:
        orm_mode = True


class CommentSchemaCreate(BaseModel):
    user_id: int
    post_id: int
    comment: str


class CommentSchemaUpdate(BaseModel):
    user_id: int
    post_id: int
    comment: str
