from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from api.database import get_db
from api.models import model
from api.schemas import schema
from uuid import UUID
from exceptions.exceptions import DatabaseError,PostNotFound

router = APIRouter()

@router.get("/post/{post_id}/allcomments", response_model=schema.CommentsOnPost)
def get_single_post_detail_with_respective_user_and_comments(post_id: UUID, db: Session = Depends(get_db)):
    try:
        # Fetch the post
        post = db.query(model.PostModel).filter(model.PostModel.id == post_id).first()
        if not post:
            raise PostNotFound(detail="Post not found")
        
        # Fetch comments for the post along with user details
        comments = (
            db.query(model.CommentModel)
            .options(joinedload(model.CommentModel.user))  # Load user details
            .filter(model.CommentModel.post_id == post_id)
            .all()
        )
        
        # Group comments by user
        grouped_comments = {}
        for comment in comments:
            user_id = str(comment.user.id)
            user_name = f"{comment.user.fname} {comment.user.lname}"
            comment_data = {
                "comment": comment.comment,
                "created_at": comment.created_at
            }
            
            if user_id not in grouped_comments:
                grouped_comments[user_id] = {
                    "user_name": user_name,
                    "comments": []
                }
            
            grouped_comments[user_id]["comments"].append(comment_data)
        
        # Return the formatted response
        return schema.CommentsOnPost(
            id=post.id,
            user_id=post.user_id,
            title=post.title,
            image=post.image,
            description=post.description,
            comments=grouped_comments
        )
    except Exception:
        raise DatabaseError("An error occurred while fetching data")