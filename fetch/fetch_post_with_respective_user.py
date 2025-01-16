from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session,joinedload
from typing import List
from api.database import get_db
from api.models.model import PostModel
from api.schemas.schema import ShowPostWithUser
from exceptions.exceptions import DatabaseError

router = APIRouter()

@router.get("/userpost", response_model=List[ShowPostWithUser])
def get_posts_with_respective_user(db: Session = Depends(get_db)):
    try:
        posts = db.query(PostModel).options(joinedload(PostModel.user)).all()
        return posts
    except Exception:
        raise DatabaseError("An error occurred while fetching data")