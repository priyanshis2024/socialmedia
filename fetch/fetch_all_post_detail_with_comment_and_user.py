from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload
from api.database import get_db
from api.models.model import PostModel,CommentModel
from api.schemas.schema import AllPostDetail, CommentDetail, ShowUser
from api.schemas import schema
from api.models import model
from typing import List,Optional
from exceptions.exceptions import DatabaseError,PostNotFound
from sqlalchemy import desc, asc

router = APIRouter()

@router.get("/allposts", response_model=List[schema.PostWithUserAndComments])
def get_all_posts_detail_with_comments_and_user(db: Session = Depends(get_db)):
    try:
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
                    likecount=post.likecount,
                    comments=grouped_comments
                )
            )
        return result
    except Exception:
        raise DatabaseError("An error occurred while fetching data")


@router.get("/allpostsdetails", response_model=List[AllPostDetail])
def get_all_posts_detail_with_comments_and_user(
    db: Session = Depends(get_db),
    text: Optional[str] = Query(None, description="Search text for posts"),
    sort_by: str = Query("created_at", description="Field to sort by (e.g., 'created_at')"),
    sort_order: str = Query("desc", description="Sort order ('asc' or 'desc')"),
    limit: int = Query(5, description="Number of posts to retrieve"),
    offset: int = Query(0, description="Number of posts to skip")
):
    try:
        # Base query
        query = db.query(model.PostModel).options(
            joinedload(model.PostModel.user),
            joinedload(model.PostModel.comments).joinedload(model.CommentModel.user)
        )

        # Apply search filter
        if text:
            query = query.filter(model.PostModel.title.ilike(f"%{text}%"))

        # Apply sorting
        if sort_order == "desc":
            query = query.order_by(asc(getattr(model.PostModel, sort_by)))
        else:
            query = query.order_by(desc(getattr(model.PostModel, sort_by)))

        # Apply limit and offset for pagination
        posts = query.limit(limit).offset(offset).all()

        # Format the response
        result = []
        for post in posts:
            # Prepare the comments
            formatted_comments = [
                CommentDetail(
                    comment=comment.comment,
                    created_at=comment.created_at,
                    user_id=comment.user.id,
                    user=ShowUser(
                        id=comment.user.id,
                        fname=comment.user.fname,
                        lname=comment.user.lname,
                        gender=comment.user.gender,
                        dob=comment.user.dob
                    )
                )
                for comment in post.comments
            ]
            
            # Add post with user and comments to result
            result.append(
                AllPostDetail(
                    id=post.id,
                    title=post.title,
                    image=post.image,
                    description=post.description,
                    likecount=post.likecount,
                    user_id=post.user_id,
                    user=ShowUser(
                        id=post.user.id,
                        fname=post.user.fname,
                        lname=post.user.lname,
                        gender=post.user.gender,
                        dob=post.user.dob
                    ),
                    comments=formatted_comments
                )
            )
        return result
    except Exception as e:
        raise DatabaseError(f"An error occurred while fetching data: {str(e)}")
