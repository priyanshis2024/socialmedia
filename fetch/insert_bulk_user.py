from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.schemas.schema import User, UserCreate
from uuid import uuid4
from api.database import get_db
from api.models.model import UserModel
from exceptions.exceptions import DatabaseError

router = APIRouter()

@router.post("/users", response_model=list[User], status_code=201)
def create_bulk_users(users: list[UserCreate], db: Session = Depends(get_db)):
    try:
        user_objects = [UserModel(id=uuid4(), **user.dict()) for user in users]
        
        db.add_all(user_objects)
        
        db.commit()
        
        for user_data in user_objects:
            db.refresh(user_data)
        
        return user_objects 
    except Exception:
        db.rollback()  
        raise DatabaseError("An error occurred while inserting bulk users.")
