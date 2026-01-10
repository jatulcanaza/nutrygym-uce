from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.profile import ProfileCreate, ProfileResponse
from app.services.profile_service import create_profile, get_profile

router = APIRouter()

@router.post("/profiles", response_model=ProfileResponse)
def create_user_profile(
    data: ProfileCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if get_profile(db, user["sub"]):
        raise HTTPException(status_code=400, detail="Profile already exists")

    return create_profile(db, user["sub"], data)

@router.get("/profiles/me", response_model=ProfileResponse)
def read_my_profile(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    profile = get_profile(db, user["sub"])
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
