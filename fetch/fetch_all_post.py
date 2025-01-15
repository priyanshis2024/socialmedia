from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from api.schemas.schema import ShowPost  # Adjust import based on your schema location
from api.database import get_db
from api.models.model import PostModel

router = APIRouter()

@router.get("/posts", response_model=List[ShowPost])
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(PostModel).all()
    return posts
