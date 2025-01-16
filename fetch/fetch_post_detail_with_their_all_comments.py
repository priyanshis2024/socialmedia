from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import get_db
from api.models import model
from api.schemas import schema
from uuid import UUID
from exceptions.exceptions import DatabaseError,PostNotFound

router = APIRouter()

@router.get("/post/{post_id}/comments", response_model=schema.PostWithComments)
def get_post_detail_with_all_comments(post_id: UUID, db: Session = Depends(get_db)):
    try:
        # Fetch the post
        post = db.query(model.PostModel).filter(model.PostModel.id == post_id).first()
        if not post:
            raise PostNotFound(detail="No Post found")
        
        # Fetch comments for the post
        comments = db.query(model.CommentModel).filter(model.CommentModel.post_id == post_id).all()
        
        # Extract only the comment text from the CommentModel
        comment_texts = [comment.comment for comment in comments]
        
        # Return the formatted response
        return schema.PostWithComments(
            id=post.id,
            user_id=post.user_id,
            title=post.title,
            image=post.image,
            description=post.description,
            likecount=post.likecount,
            comments=comment_texts
        )
    except Exception:
        raise DatabaseError("An error occurred while fetching data")