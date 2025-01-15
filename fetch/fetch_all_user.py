from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from api.database import get_db
from api.models.model import UserModel
from api.schemas.schema import ShowUser

router = APIRouter()

@router.get("/users", response_model=List[ShowUser])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users  # Directly return the SQLAlchemy query result