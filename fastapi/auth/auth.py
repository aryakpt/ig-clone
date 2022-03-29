from fastapi import APIRouter, Depends, HTTPException
import fastapi
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from databases.database import get_db
from models.user import User
from helpers.utils import Hash, email_validation
from auth.oauth2 import *

router = APIRouter(
    prefix="/auth",
    tags=['Auth']
)


@router.post("")
def auth(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    if email_validation(request.username, False):
        user = db.query(User).filter(User.email == request.username).first()
    else:
        user = db.query(User).filter(User.username == request.username).first()

    if not user:
        raise HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND, detail=f"Invalid Credential!")
    if not Hash.verify(request.password, user.password):
        raise HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND, detail=f"Incorrect Password!")
    payload = {
        "id": user.id,
        "email": user.email
    }
    access_token = create_access_token(data=payload)
    # Response
    res = {
        "access_token": access_token,
        "token_type": "bearer",
    }
    return res


@router.get("/decode")
async def decode_token(token_access: str = Depends(OAUTH2_SCHEME)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token_access, SECRET_KEY,
                             algorithms=[ENCRYPTION_ALGORITHM])
        print(get_timestamp())
        print(payload['exp'])
        if get_timestamp() > payload['exp']:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Expired token!",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload
    except JWTError:
        raise credentials_exception
