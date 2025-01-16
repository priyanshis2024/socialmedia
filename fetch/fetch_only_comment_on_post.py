from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.database import get_db
from api.models import model
from typing import List
from api.schemas.schema import OnlyPostComments
from exceptions.exceptions import DatabaseError

router = APIRouter()

@router.get("/post_only_comments", response_model=List[OnlyPostComments])
def get_all_posts_with_grouped_only_comments(db: Session = Depends(get_db)):
    try: 
        # Fetch all posts
        posts = db.query(model.PostModel).all()
        
        # Structure the response
        response = []
        for post in posts:
            # Fetch comments for the current post
            comments = db.query(model.CommentModel).filter(model.CommentModel.post_id == post.id).all()
            
            # Append the result for the current post
            response.append({
                "id": post.id,
                "comments": [comment.comment for comment in comments]
            })
        
        return response
    except Exception:
        raise DatabaseError("An error occurred while fetching data")