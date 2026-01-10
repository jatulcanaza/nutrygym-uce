from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.user import User, UserDB
from app.services.auth_service import register_user, login_user, get_db


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(user: User, db: Session = Depends(get_db)):
    return register_user(user, db)

@router.post("/login")
def login(user: User, db: Session = Depends(get_db)):
    return login_user(user, db)
