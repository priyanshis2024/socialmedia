from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from api.database import get_db
from api.schemas import schema
from api.models import model
from sqlalchemy import func
from exceptions.exceptions import PostNotFound, DatabaseError

router = APIRouter()

@router.get("/post/{post_id}", response_model=schema.Post)
def get_post_with_like_count(post_id: UUID, db: Session = Depends(get_db)):
    try:
        # Query to get the post details
        post = db.query(model.PostModel).filter(model.PostModel.id == post_id).first()
        if not post:
            raise PostNotFound(detail="Post not found")

        # Count only the likes where is_liked is True
        like_count = db.query(func.count(model.LikeModel.id)).filter(
            model.LikeModel.post_id == post_id,
            model.LikeModel.is_liked == True  # Only count likes where is_liked is True
        ).scalar()

        return schema.Post(
            id=post.id,
            user_id=post.user_id,
            title=post.title,
            image=post.image,
            description=post.description,
            likecount=like_count,  # Return the like count (only 'True' likes)
            created_at=post.created_at,
            updated_at=post.updated_at
        )
    except Exception as e:
        raise DatabaseError(f"An error occurred: {e}")
