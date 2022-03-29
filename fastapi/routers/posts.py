from typing import List, Optional
from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException
from sqlalchemy.orm import Session
from databases.database import get_db
from helpers.utils import generate_filename
from models.post import *
from auth.oauth2 import decode_token

router = APIRouter(
    prefix="/post",
    tags=["Post"]
)

ALLOWED_IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png']
IMAGE_UPLOAD_PATH = "public/images/"


@router.get("", response_model=List[PostSchema])
def get_all(db: Session = Depends(get_db)):
    items = db.query(Post).all()
    return items


@router.post("", response_model=PostSchema, dependencies=[Depends(decode_token)])
async def create_one(user_id: int = Form(...), image_url_type: str = Form(...), caption: str = Form(...), image: Optional[UploadFile] = File(None), db: Session = Depends(get_db)):
    if not image:
        new_item = Post(
            user_id=user_id,
            image_url_type=image_url_type,
            caption=caption,
            created_at=datetime.now()
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item
    filename = image.filename
    # getting extension from the file (test.png = ["test","png"])
    extension = filename.split(".")[1]
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(status_code=400,
                            detail=f"File extension is not allowed, should be {ALLOWED_IMAGE_EXTENSIONS}")

    token_name = generate_filename(extension=extension, counter=1)
    generated_name = IMAGE_UPLOAD_PATH + token_name

    file_content = await image.read()
    with open(generated_name, "wb") as file:
        file.write(file_content)
    image.close()

    new_item = Post(
        user_id=user_id,
        image_url=token_name,
        image_url_type=image_url_type,
        caption=caption,
        created_at=datetime.now()
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

# @router.post("", response_model=PostSchema, dependencies=[Depends(decode_token)])
# async def create_one(request: PostSchemaCreate, db: Session = Depends(get_db)):

#     new_item = Post(
#         user_id=request.user_id,
#         image_url=request.token_name,
#         image_url_type=request.image_url_type,
#         caption=request.caption,
#         created_at=datetime.now()
#     )
#     db.add(new_item)
#     db.commit()
#     db.refresh(new_item)
#     return new_item


@router.delete("/{id}", dependencies=[Depends(decode_token)])
def delete_one(id: int, user_id: int, db: Session = Depends(get_db)):
    item = db.query(Post).filter(Post.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail=f"Post not found!")
    if item.user_id != user_id:
        raise HTTPException(status_code=403, detail=f"Forbidden to delete!")
    db.delete(item)
    db.commit()
    return {}
