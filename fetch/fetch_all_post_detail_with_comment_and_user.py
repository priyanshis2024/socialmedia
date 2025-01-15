from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from api.database import get_db
from api.models import model
from api.schemas import schema
from typing import List

router = APIRouter()

@router.get("/allposts", response_model=List[schema.PostWithUserAndComments])
def get_all_posts_detail_with_comments_and_user(db: Session = Depends(get_db)):
    # Fetch all posts with their user details and comments
    posts = (
        db.query(model.PostModel)
        .options(
            joinedload(model.PostModel.user),  # Load user details
            joinedload(model.PostModel.comments).joinedload(model.CommentModel.user)  # Load comments and their users
        )
        .all()
    )
    
    # Format the response
    result = []
    for post in posts:
        # Group comments by user
        grouped_comments = {}
        for comment in post.comments:
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
        
        # Add post with user and grouped comments to result
        result.append(
            schema.PostWithUserAndComments(
                id=post.id,
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
                comments=grouped_comments
            )
        )
    
    return result
