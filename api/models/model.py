from api.database import Base
from sqlalchemy import Column, String, Date, DateTime, ForeignKey,Integer,Boolean
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
    
    post = relationship("PostModel", back_populates="user") 
    comments = relationship("CommentModel", back_populates="user")
    likes = relationship("LikeModel", back_populates="user")  

class PostModel(Base):
    __tablename__ = "post"
    
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    title = Column(String, nullable=False)
    image = Column(String, nullable=False)
    description = Column(String, nullable=False)
    likecount = Column(Integer,nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("UserModel", back_populates="post") 
    comments = relationship("CommentModel", back_populates="post") 
    likes = relationship("LikeModel", back_populates="post")  
 

class CommentModel(Base):
    __tablename__ = "comment"
    
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    post_id = Column(UUID(as_uuid=True), ForeignKey('post.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    comment = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    post = relationship("PostModel", back_populates="comments") 
    user = relationship("UserModel", back_populates="comments")  

class LikeModel(Base):
    __tablename__ = "like"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    post_id = Column(UUID(as_uuid=True), ForeignKey('post.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    is_liked = Column(Boolean, server_default="TRUE", nullable=False)  
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    post = relationship("PostModel", back_populates="likes")
    user = relationship("UserModel", back_populates="likes") 