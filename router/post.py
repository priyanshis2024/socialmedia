from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from api.schemas.schema import Post, PostCreate
from api.database import get_db
from api.models.model import PostModel, UserModel

router = APIRouter()

@router.post("/post", response_model=Post, status_code=201)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    # Check if the user exists
    user = db.query(UserModel).filter(UserModel.id == post.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create post
    post_data = PostModel(id=uuid4(), **post.dict())
    db.add(post_data)
    db.commit()
    db.refresh(post_data)
    return post_data