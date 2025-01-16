from fastapi import APIRouter, Depends
from uuid import uuid4
from sqlalchemy.orm import Session
# from api.schemas.schema import Like, DoLike,ShowLike
from api.database import get_db
# from api.models.model import UserModel, PostModel,LikeModel
from api.schemas import schema
from api.models import model
from datetime import datetime
from exceptions.exceptions import UserNotFound,PostNotFound,DatabaseError,LikeNotFound

router = APIRouter()


@router.post("/like", response_model=schema.ShowLike)
def like_post(like: schema.DoLike, db: Session = Depends(get_db)):
    try:
        # Check if the post exists
        post = db.query(model.PostModel).filter(model.PostModel.id == like.post_id).first()
        if not post:
            raise PostNotFound(detail="Post not found")

        # Check if the user exists
        user = db.query(model.UserModel).filter(model.UserModel.id == like.user_id).first()
        if not user:
            raise UserNotFound(detail="User not found")

        # Check if the user has already liked the post
        existing_like = db.query(model.LikeModel).filter(
            model.LikeModel.post_id == like.post_id, model.LikeModel.user_id == like.user_id
        ).first()

        if existing_like:
            # If the user already liked the post, update the like status
            existing_like.is_liked = like.is_liked
            existing_like.updated_at = datetime.utcnow()  # Update timestamp
            db.commit()

            like_count = db.query(model.LikeModel).filter(
                model.LikeModel.post_id == like.post_id, model.LikeModel.is_liked == True).count()

            post.likecount = like_count  # Update the likecount in PostModel
            db.commit()
            
            return schema.ShowLike(
                id=existing_like.id,
                post_id=existing_like.post_id,
                user_id=existing_like.user_id,
                is_liked=existing_like.is_liked
            )
        else:
                # If no like exists, create a new like record
                new_like = model.LikeModel(
                    post_id=like.post_id,
                    user_id=like.user_id,
                    is_liked=like.is_liked,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.add(new_like)
                db.commit()
                db.refresh(new_like)

                like_count = db.query(model.LikeModel).filter(
                model.LikeModel.post_id == like.post_id, model.LikeModel.is_liked == True).count()

                post.likecount = like_count  # Update the likecount in PostModel
                db.commit()
                
                return schema.ShowLike(
                    id=new_like.id,
                    post_id=new_like.post_id,
                    user_id=new_like.user_id,
                    is_liked=new_like.is_liked
                )
            # else:
            #     raise LikeNotFound(detail="No Like entry found for unliking")
    except Exception as e:
        db.rollback()
        raise DatabaseError(f"An error occurred: {e}")
