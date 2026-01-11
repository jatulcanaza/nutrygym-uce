# app/routes/meal_plan.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.security import get_current_user
from app.schemas.meal_plan import MealPlanCreate, MealPlanResponse, MealPlanUpdate
from app.services.meal_plan_service import (
    create_meal_plan, 
    get_user_plans, 
    get_plan_by_id,
    update_meal_plan,
    delete_meal_plan,
    get_current_plan
)
import os

API_PREFIX = os.getenv("API_PREFIX", "")

router = APIRouter(
    prefix=f"{API_PREFIX}/plans",
    tags=["Meal Plans"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ENDPOINTS EXISTENTES
@router.post("", response_model=MealPlanResponse, status_code=status.HTTP_201_CREATED)
def create_plan(
    plan: MealPlanCreate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_meal_plan(plan, user["user_id"], db)

@router.get("", response_model=list[MealPlanResponse])
def my_plans(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_user_plans(user["user_id"], db)

# ENDPOINTS NUEVOS
@router.get("/{plan_id}", response_model=MealPlanResponse)
def get_plan(
    plan_id: str,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_plan_by_id(plan_id, user["user_id"], db)

@router.put("/{plan_id}", response_model=MealPlanResponse)
def update_plan(
    plan_id: str,
    plan_update: MealPlanUpdate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Endpoint para editar plan (¡EL QUE PREGUNTASTE!)"""
    return update_meal_plan(plan_id, plan_update, user["user_id"], db)

@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plan(
    plan_id: str,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    delete_meal_plan(plan_id, user["user_id"], db)
    return None

@router.get("/current", response_model=MealPlanResponse)
def get_current_active_plan(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_current_plan(user["user_id"], db)