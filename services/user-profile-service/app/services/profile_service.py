from sqlalchemy.orm import Session
from app.models.user_profile import UserProfile
from app.schemas.profile import ProfileCreate
from uuid import UUID

def create_profile(db: Session, user_id: UUID, data: ProfileCreate):
    profile = UserProfile(user_id=user_id, **data.model_dump())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

def get_profile(db: Session, user_id: UUID):
    return db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
