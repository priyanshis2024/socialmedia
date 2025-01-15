from api.database import Base
from sqlalchemy import Column, String, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from sqlalchemy.orm import relationship

class UserModel(Base):
    __tablename__ = "user"
    
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    fname = Column(String, nullable=False)
    lname = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    dob = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    posts = relationship("PostModel", back_populates="user")  # Matches PostModel's 'user'
    comments = relationship("CommentModel", back_populates="user")  # Matches CommentModel's 'user'

class PostModel(Base):
    __tablename__ = "post"
    
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    title = Column(String, nullable=False)
    image = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("UserModel", back_populates="posts")  # Matches UserModel's 'posts'
    comments = relationship("CommentModel", back_populates="post")  # Matches CommentModel's 'post'

class CommentModel(Base):
    __tablename__ = "comment"
    
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    post_id = Column(UUID(as_uuid=True), ForeignKey('post.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    comment = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    post = relationship("PostModel", back_populates="comments")  # Matches PostModel's 'comments'
    user = relationship("UserModel", back_populates="comments")  # Matches UserModel's 'comments'