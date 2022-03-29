from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./ig_api.db'
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root@localhost:3306/belajar_fastapi?charset=utf8mb4"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
#                        "check_same_thread": False})
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
