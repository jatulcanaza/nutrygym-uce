from sqlalchemy.orm import Session
from app.models.user_profile import UserProfile
from app.schemas.profile import ProfileCreate, ProfileUpdate
from uuid import UUID


def create_profile(db: Session, user_id: UUID, data: ProfileCreate):
    profile = UserProfile(user_id=user_id, **data.model_dump())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def get_profile(db: Session, user_id: UUID):
    return db.query(UserProfile).filter(UserProfile.user_id == user_id).first()


def update_profile(db: Session, user_id: UUID, data: ProfileUpdate):
    profile = get_profile(db, user_id)
    if not profile:
        return None

    updates = data.model_dump(exclude_unset=True)

    for key, value in updates.items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)
    return profile


def delete_profile(db: Session, user_id: UUID) -> bool:
    profile = get_profile(db, user_id)
    if not profile:
        return False

    db.delete(profile)
    db.commit()
    return True
