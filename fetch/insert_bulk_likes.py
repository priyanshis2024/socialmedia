from fastapi import APIRouter, Depends
from api.schemas.schema import DoLike, ShowLike
from uuid import uuid4
from sqlalchemy.orm import Session
from api.database import get_db
from api.models.model import LikeModel, PostModel, UserModel
from exceptions.exceptions import DatabaseError

router = APIRouter()

@router.post("/likes", response_model=list[ShowLike], status_code=201)
def create_bulk_likes(likes: list[DoLike], db: Session = Depends(get_db)):
    try:
        # Prepare bulk like objects for each like request
        like_objects = []
        for like in likes:
            # Get the post and user from the database (Assuming we have access to PostModel and UserModel)
            post = db.query(PostModel).filter(PostModel.id == like.post_id).first()
            user = db.query(UserModel).filter(UserModel.id == like.user_id).first()
            
            if not post or not user:
                raise DatabaseError("Post or User not found")
            
            like_objects.append(LikeModel(
                id=uuid4(),
                post_id=like.post_id,
                user_id=like.user_id,
                is_liked=like.is_liked
            ))

        # Add all like objects to the session
        db.add_all(like_objects)
        
        # Commit the transaction
        db.commit()
        
        # Refresh the instances to get any auto-generated fields (if applicable)
        for like in like_objects:
            db.refresh(like)
        
        return like_objects  # Return the created like records

    except Exception:
        db.rollback()  # Rollback in case of error
        raise DatabaseError("An error occurred while inserting bulk likes.")