from fastapi import APIRouter, Depends,Query
from sqlalchemy.orm import Session, joinedload
from api.database import get_db
from api.models import model
from api.schemas import schema
from api.schemas.schema import ShowUser
from uuid import UUID
from typing import Optional
from exceptions.exceptions import DatabaseError,PostNotFound
from sqlalchemy import asc,desc

router = APIRouter()

@router.get("/post/{post_id}/allcomments", response_model=schema.CommentsOnPost)
def get_single_post_detail_with_respective_user_and_comments(
    post_id: UUID, db: Session = Depends(get_db),
    text: Optional[str] = Query(None, description="Search text for posts"),
    sort_by: str = Query("created_at", description="Field to sort by (e.g., 'created_at')"),
    sort_order: str = Query("desc", description="Sort order ('asc' or 'desc')"),
    limit: int = Query(5, description="Number of posts to retrieve"),
    offset: int = Query(0, description="Number of posts to skip")):

    try:
        # Fetch the post
        post = db.query(model.PostModel).filter(model.PostModel.id == post_id).first()
        if not post:
            raise PostNotFound(detail="Post not found")
        
        # Fetch comments for the post along with user details
        query = db.query(model.CommentModel).options(joinedload(model.CommentModel.user)).filter(
                model.CommentModel.post_id == post_id)
        
        if text:
            query = query.filter(model.PostModel.title.ilike(f"%{text}%"))

        if sort_order=="asc":
            query = query.order_by(asc(getattr(model.PostModel, sort_by)))
        else:
            query = query.order_by(desc(getattr(model.PostModel, sort_by)))

        comments = query.limit(limit).offset(offset).all()

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
                user=schema.ShowUser(
                id=post.user.id,
                fname=post.user.fname,
                lname=post.user.lname,
                gender=post.user.gender,
                dob=post.user.dob
            ),
            title=post.title,
            image=post.image,
            description=post.description,
            likecount=post.likecount,
            comments=grouped_comments
        )
    except Exception:
        raise DatabaseError("An error occurred while fetching data")