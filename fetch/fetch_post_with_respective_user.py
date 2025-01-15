from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session,joinedload
from typing import List
from api.database import get_db
from api.models.model import PostModel
from api.schemas.schema import ShowPostWithUser

router = APIRouter()

@router.get("/userpost", response_model=List[ShowPostWithUser])
def get_posts_with_respective_user(db: Session = Depends(get_db)):
    posts = db.query(PostModel).options(joinedload(PostModel.user)).all()
    return posts