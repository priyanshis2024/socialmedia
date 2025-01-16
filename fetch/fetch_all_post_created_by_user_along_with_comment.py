from sqlalchemy.orm import Session
from fastapi import Depends,APIRouter
from typing import List
from api.schemas.schema import UserPostComment,Postdetail
from api.models.model import UserModel,CommentModel
from api.database import get_db
from uuid import UUID
from exceptions.exceptions import UserNotFound,DatabaseError

router = APIRouter()

@router.get("/user/{user_id}", response_model=List[UserPostComment])
def get_post_created_by_user_along_with_comments(user_id: UUID,db: Session = Depends(get_db)):
    try:
        user_id_post = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user_id_post:
            raise UserNotFound(detail= f"No User found for the {user_id}")
        # return user_id_post
        response = []
        
        for post in user_id_post.post:  # Access the posts relationship
            # Fetch comments for the current post
            comments = db.query(CommentModel).filter(CommentModel.post_id == post.id).all()
            comment_texts = [comment.comment for comment in comments]

            # Prepare post details
            post_details = Postdetail(
                id=post.id,
                title=post.title,
                image=post.image,
                description=post.description,
                comments=comment_texts
            )

            # Construct UserPostComment
            user_post_comment = UserPostComment(
                id=user_id_post.id,
                fname=user_id_post.fname,
                lname=user_id_post.lname,
                gender=user_id_post.gender,
                dob=user_id_post.dob,
                post=post_details
            )

            response.append(user_post_comment)

        return response
    except Exception:
        raise DatabaseError("An error occurred while fetching data")