from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from databases.database import get_db
from helpers.utils import Hash, email_validation
from models.user import *
from auth.oauth2 import decode_token

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.get("", response_model=List[UserSchema])
def get_all(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.get("/{id}", response_model=UserSchema)
def get_one(id: int, db: Session = Depends(get_db)):
    item = db.query(User).filter(User.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail=f"User not found!")
    return item


@router.post("", response_model=UserSchema)
def create_one(request: UserSchemaCreate, db: Session = Depends(get_db)):
    # email validation
    email_validation(request.email)
    email_existed = db.query(User).filter(User.email == request.email).first()
    if email_existed:
        raise HTTPException(status_code=409, detail=f"Email already exist!")
    # username validation
    username_existed = db.query(User).filter(
        User.username == request.username).first()
    if username_existed:
        raise HTTPException(status_code=409, detail=f"Username already exist!")
    # create
    item = User(
        email=request.email,
        username=request.username,
        password=Hash.bcrypt(request.password),
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{id}", dependencies=[Depends(decode_token)])
def delete_one(id: int, db: Session = Depends(get_db)):
    item = db.query(User).filter(User.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail=f"User not found!")
    db.delete(item)
    db.commit()
    return {}


@router.delete("", dependencies=[Depends(decode_token)])
def delete_all(db: Session = Depends(get_db)):
    db.query(User).delete(synchronize_session=False)
    db.commit()
    return []
