from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from api.schemas.schema import ShowComment  # Adjust import based on your schema location
from api.database import get_db
from api.models.model import CommentModel

router = APIRouter()

@router.get("/comments", response_model=List[ShowComment])
def get_all_comments(db: Session = Depends(get_db)):
    comments = db.query(CommentModel).all()
    return comments