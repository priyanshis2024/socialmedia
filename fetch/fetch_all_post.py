from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from api.schemas.schema import ShowPost  # Adjust import based on your schema location
from api.database import get_db
from api.models.model import PostModel
from exceptions.exceptions import DatabaseError

router = APIRouter()

@router.get("/posts", response_model=List[ShowPost])
def get_all_posts(db: Session = Depends(get_db)):
    try:
        posts = db.query(PostModel).all()
        return posts
    except Exception:
        raise DatabaseError("An error occurred while fetching data")