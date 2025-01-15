from fastapi import APIRouter, Depends, HTTPException
from uuid import uuid4
from sqlalchemy.orm import Session
from api.schemas.schema import Comment, CommentCreate
from api.database import get_db
from api.models.model import CommentModel, UserModel, PostModel

router = APIRouter()

@router.post("/comment", response_model=Comment, status_code=201)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    # Validate that the user and post exist
    user = db.query(UserModel).filter(UserModel.id == comment.user_id).first()
    post = db.query(PostModel).filter(PostModel.id == comment.post_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Create the comment
    comment_data = CommentModel(id=uuid4(), **comment.dict())
    db.add(comment_data)
    db.commit()
    db.refresh(comment_data)
    return comment_data