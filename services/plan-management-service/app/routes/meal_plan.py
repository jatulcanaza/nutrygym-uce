# app/routes/meal_plan.py

from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
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
    get_current_plan,
    create_active_plan_from_ai,
    generate_plan_from_forms,
    end_current_plan,
    cancel_current_plan,
    regenerate_current_plan,
)

import os

security = HTTPBearer()

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

# =========================
# ENDPOINTS PÚBLICOS (JWT)
# =========================

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


# =========================
# IMPORTANTE: RUTAS FIJAS ANTES DE /{plan_id}
# =========================

@router.get("/current", response_model=MealPlanResponse)
def get_current_active_plan(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_current_plan(user["user_id"], db)


@router.post("/generate", response_model=MealPlanResponse, status_code=status.HTTP_201_CREATED)
async def generate_plan(
    user=Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    user_id = user["user_id"]
    token = credentials.credentials
    return await generate_plan_from_forms(user_id, token, db)

@router.post("/current/end", response_model=MealPlanResponse)
def end_plan(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return end_current_plan(user["user_id"], db)


@router.post("/current/cancel", response_model=MealPlanResponse)
def cancel_plan(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return cancel_current_plan(user["user_id"], db)


# =========================
# CRUD POR ID (DEBE IR DESPUÉS)
# =========================

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
    return update_meal_plan(plan_id, plan_update, user["user_id"], db)


@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plan(
    plan_id: str,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    delete_meal_plan(plan_id, user["user_id"], db)
    return None


# =========================
# ENDPOINT INTERNO (SOLO IA – SIN JWT)
# =========================

@router.post("/internal/ai/plans", response_model=MealPlanResponse, status_code=status.HTTP_201_CREATED)
def create_plan_from_ai(
    plan: MealPlanCreate,
    x_internal_key: str = Header(...),
    db: Session = Depends(get_db)
):
    INTERNAL_KEY = os.getenv("INTERNAL_API_KEY")
    if x_internal_key != INTERNAL_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized internal call")

    return create_active_plan_from_ai(plan, db)

@router.post("/current/regenerate", response_model=MealPlanResponse)
async def regenerate_plan(
    user=Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    user_id = user["user_id"]
    token = credentials.credentials
    return await regenerate_current_plan(user_id, token, db)
