# app/routes/nutrition_form.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.nutrition_form import NutritionFormCreate, NutritionFormResponse

from app.services.nutrition_form_service import (
    create_form,
    get_form,
    update_form,
    delete_form
)

router = APIRouter(prefix="/nutrition-form", tags=["Nutrition Form"])

@router.post("", response_model=NutritionFormResponse)
def create_my_form(
    form: NutritionFormCreate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_form(db, user["user_id"], form)

@router.get("/me", response_model=NutritionFormResponse)
def read_my_form(
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    found = get_form(db, user["user_id"])
    if not found:
        # para mantener coherencia con profile
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Nutrition form not found")
    return found

@router.put("/me", response_model=NutritionFormResponse)
def update_my_form(
    form: NutritionFormCreate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return update_form(db, user["user_id"], form)

@router.delete("/me")
def delete_my_form(
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    delete_form(db, user["user_id"])
    return {"detail": "Nutrition form deleted"}
