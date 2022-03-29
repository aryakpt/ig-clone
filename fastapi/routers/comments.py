from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from databases.database import get_db
from models.comment import *
from auth.oauth2 import decode_token

router = APIRouter(
    prefix="/comment",
    tags=["Comment"]
)


@router.get("", response_model=List[CommentSchema])
def get_all(db: Session = Depends(get_db)):
    items = db.query(Comment).all()
    return items


@router.get("/post_id", response_model=List[CommentSchema])
def get_comment_by_post_id(post_id: int, db: Session = Depends(get_db)):
    return db.query(Comment).filter(Comment.post_id == post_id).all()


@router.post("", response_model=CommentSchema, dependencies=[Depends(decode_token)])
def create_one(request: CommentSchemaCreate, db: Session = Depends(get_db)):
    item = Comment(
        user_id=request.user_id,
        post_id=request.post_id,
        comment=request.comment,
        created_at=datetime.now(),
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
