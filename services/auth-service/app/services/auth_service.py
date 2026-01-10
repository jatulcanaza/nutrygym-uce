from sqlalchemy.orm import Session
from app.models.user import UserDB
from app.models.user import User
from app.core.database import SessionLocal
from app.core.security import create_access_token

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def register_user(user: User, db: Session):
    db_user = UserDB(email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {
        "message": "User registered successfully",
        "user": {
            "email": db_user.email
        }
    }

def login_user(user: User, db: Session):
    db_user = db.query(UserDB).filter(UserDB.email == user.email).first()
    if not db_user or db_user.password != user.password:
        return {"message": "Invalid credentials"}

    token = create_access_token({"sub": db_user.email})
    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer"
    }
