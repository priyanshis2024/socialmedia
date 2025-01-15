from fastapi import APIRouter, Depends, HTTPException
from api.schemas.schema import User, UserCreate
from uuid import uuid4
from sqlalchemy.orm import Session
from api.database import get_db
from api.models.model import UserModel

router = APIRouter()

@router.post("/user", response_model=User, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        user_data = UserModel(id=uuid4(), **user.dict())
        db.add(user_data)
        db.commit()
        db.refresh(user_data)
        return user_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))