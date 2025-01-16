from pydantic import BaseModel, ConfigDict
from datetime import datetime, date
from uuid import UUID
from typing import List,Dict

class User(BaseModel):
    id: UUID
    fname: str
    lname: str
    gender: str
    dob: date
    created_at: datetime
    updated_at: datetime

    class Config:
        model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)
        orm_mode = True  # Ensure compatibility with ORM objects

class UserCreate(BaseModel):
    fname: str
    lname: str
    gender: str
    dob: date

class Post(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    image: str
    description: str
    likecount: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class PostCreate(BaseModel):
    user_id: UUID
    title: str
    image: str
    description: str

class Comment(BaseModel):
    id: UUID
    post_id: UUID
    user_id: UUID
    comment: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CommentCreate(BaseModel):
    post_id: UUID
    user_id: UUID
    comment: str 

class ShowUser(BaseModel):
    id: UUID
    fname: str
    lname: str
    gender: str
    dob: date

    model_config = ConfigDict(from_attributes=True)

class ShowPost(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    image: str
    description: str
    likecount: int

    class Config:
        orm_mode = True

class ShowComment(BaseModel):
    id: UUID
    post_id: UUID
    user_id: UUID
    comment: str

    class Config:
        orm_mode = True

class ShowPostWithUser(BaseModel):
    id: UUID
    user_id: UUID
    user: ShowUser
    title: str
    image: str
    description: str
    likecount: int

class Comments(BaseModel):
    comment: str

    class Config:
        orm_mode = True

class PostWithComments(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    image: str
    description: str
    likecount: int
    comments: List[str]  # List of comment strings

    class Config:
        orm_mode = True 

class CommentDetails(BaseModel):
    comment: str
    created_at: datetime

class UserComments(BaseModel):
    user_name: str
    comments: List[Comments]

class CommentsOnPost(BaseModel):
    id: UUID
    user_id: UUID
    user: ShowUser
    title: str
    image: str
    description: str
    likecount: int
    comments: Dict[str, UserComments]  # Grouped comments by user_id

    # class Config:
    #     orm_mode = True
    model_config = ConfigDict(from_attributes=True)

class PostWithUserAndComments(BaseModel):
    id: UUID
    user: ShowUser
    title: str
    image: str
    description: str
    likecount: int
    comments: Dict[str, UserComments]  # Grouped comments by user_id

    class Config:
        orm_mode = True

class OnlyPostComments(BaseModel):
    id: UUID
    comments: List[str]

class Postdetail(BaseModel):
    id: UUID
    title: str
    image: str
    description: str
    likecount: int    
    comments: List[str]

class UserPostComment(BaseModel):
    id: UUID
    fname: str
    lname: str
    gender: str
    dob: date
    post: Postdetail
class Like(BaseModel):
    id: UUID
    post_id: UUID
    user_id: UUID
    is_liked: bool
    created_at: datetime
    updated_at: datetime

class DoLike(BaseModel):
    post_id: UUID
    user_id: UUID
    is_liked: bool

class ShowLike(BaseModel):
    id: UUID
    post_id: UUID
    user_id: UUID
    is_liked: bool

    class Config:
        orm_mode = True

class all_likes(BaseModel):
    # like:int
    is_liked: bool
class LikeOnPost(BaseModel):
    post_id: UUID
    likes: all_likes

class CommentDetail(BaseModel):
    comment: str
    created_at: datetime
    user_id: UUID
    user: ShowUser

    model_config = ConfigDict(from_attributes=True)

class AllPostDetail(BaseModel):
    id: UUID
    title: str
    image: str
    description: str
    likecount: int
    user_id: UUID
    user: ShowUser
    comments: List[CommentDetail]

    model_config = ConfigDict(from_attributes=True)