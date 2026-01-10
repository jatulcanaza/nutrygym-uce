from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.nutrition_form import NutritionFormCreate, NutritionFormResponse
from app.core.security import get_current_user
from app.services.nutrition_form_service import save_form

router = APIRouter(prefix="/nutrition-form", tags=["Nutrition Form"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", response_model=NutritionFormResponse)
def create_form(
    form: NutritionFormCreate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return save_form(db, user["user_id"], form)
