from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.profile import ProfileCreate, ProfileUpdate, ProfileResponse
from app.services.profile_service import create_profile, get_profile, update_profile, delete_profile

router = APIRouter()


@router.post("/profiles", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
def create_user_profile(
    data: ProfileCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if get_profile(db, user["sub"]):
        # Mejor que 400: es un conflicto de estado
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Profile already exists")

    return create_profile(db, user["sub"], data)


@router.get("/profiles/me", response_model=ProfileResponse)
def read_my_profile(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    profile = get_profile(db, user["sub"])
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile


@router.put("/profiles/me", response_model=ProfileResponse)
def update_my_profile(
    data: ProfileUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    profile = update_profile(db, user["sub"], data)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile


@router.delete("/profiles/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_profile(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    ok = delete_profile(db, user["sub"])
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return None
