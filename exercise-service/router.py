
from fastapi import APIRouter
from . database import SessionLocal


 

problems = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
