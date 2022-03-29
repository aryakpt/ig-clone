import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List
from databases.database import engine
from models import models
from routers import users, posts, comments
from auth import auth

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)


@app.get("/")
def root():
    return "Hello world"


app.mount('/public/images/',
          StaticFiles(directory="public/images/"), name="images")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1",
                port=5000, reload=True)
