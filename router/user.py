from fastapi import APIRouter, Depends
from api.schemas.schema import User, UserCreate
from uuid import uuid4
from sqlalchemy.orm import Session
from api.database import get_db
from api.models.model import UserModel
from exceptions.exceptions import DatabaseError

router = APIRouter()

@router.post("/user", response_model=User, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        user_data = UserModel(id=uuid4(), **user.dict())
        db.add(user_data)
        db.commit()
        db.refresh(user_data)
        return user_data
    except Exception:
        raise DatabaseError("An error occurred while fetching data")