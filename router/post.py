from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import uuid4
from api.schemas.schema import Post, PostCreate
from api.database import get_db
from api.models.model import PostModel, UserModel
from exceptions.exceptions import UserNotFound,DatabaseError

router = APIRouter()

@router.post("/post", response_model=Post, status_code=201)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    try:
        # Check if the user exists
        user = db.query(UserModel).filter(UserModel.id == post.user_id).first()
        if not user:
            raise UserNotFound(detail="No User found")

        # Create post
        post_data = PostModel(id=uuid4(), **post.dict())
        db.add(post_data)
        db.commit()
        db.refresh(post_data)
        return post_data
    except Exception:
        raise DatabaseError("An error occurred while fetching data")