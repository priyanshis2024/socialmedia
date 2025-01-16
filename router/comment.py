from fastapi import APIRouter, Depends
from uuid import uuid4
from sqlalchemy.orm import Session
from api.schemas.schema import Comment, CommentCreate
from api.database import get_db
from api.models.model import CommentModel, UserModel, PostModel
from exceptions.exceptions import UserNotFound,PostNotFound,DatabaseError,CommentNotFound

router = APIRouter()

@router.post("/comment", response_model=Comment, status_code=201) # response payload 
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)): # request payload
    try:
        # Validate that the user and post exist
        user = db.query(UserModel).filter(UserModel.id == comment.user_id).first()
        post = db.query(PostModel).filter(PostModel.id == comment.post_id).first()

        if not user:
            raise UserNotFound(detail="No User found")
        if not post:
            raise PostNotFound(detail="No Post found")

        # Create the comment
        comment_data = CommentModel(id=uuid4(), **comment.dict())
        if not comment_data:
            raise CommentNotFound(detail="Comment data not found")
        db.add(comment_data)
        db.commit()
        db.refresh(comment_data)
        return comment_data
    except Exception:
        raise DatabaseError("An error occurred while fetching data")