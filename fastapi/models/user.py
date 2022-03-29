from typing import List
from databases.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from pydantic import BaseModel


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True)
    email = Column(String(255), unique=True)
    password = Column(String(255))
    posts = relationship("Post", back_populates="user")


class PostBase(BaseModel):
    id: int
    image_url: str
    image_url_type: str
    caption: str

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    id: int
    username: str
    email: str
    password: str
    posts: List[PostBase] = []

    class Config:
        orm_mode = True


class UserSchemaCreate(BaseModel):
    username: str
    email: str
    password: str


class UserSchemaUpdate(BaseModel):
    username: str
    email: str
    password: str
