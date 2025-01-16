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

    class Config:
        orm_mode = True

class ShowPost(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    image: str
    description: str

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
    title: str
    image: str
    description: str
    comments: Dict[str, UserComments]  # Grouped comments by user_id

    class Config:
        orm_mode = True

class PostWithUserAndComments(BaseModel):
    id: UUID
    user: ShowUser
    title: str
    image: str
    description: str
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
    comments: List[str]

class UserPostComment(BaseModel):
    id: UUID
    fname: str
    lname: str
    gender: str
    dob: date
    post: Postdetail