# app/services/meal_plan_service.py
from sqlalchemy.orm import Session
from app.models.meal_plan import MealPlan
from app.schemas.meal_plan import MealPlanCreate, MealPlanUpdate
from fastapi import HTTPException, status
from uuid import UUID

def create_meal_plan(data: MealPlanCreate, user_id: str, db: Session):
    plan = MealPlan(
        user_id=user_id,
        calories=data.calories,
        protein=data.protein,
        carbs=data.carbs,
        fats=data.fats,
        title=data.title,
        description=data.description
    )
    
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan

def get_user_plans(user_id: str, db: Session):
    return (
        db.query(MealPlan)
        .filter(MealPlan.user_id == user_id)
        .order_by(MealPlan.created_at.desc())
        .all()
    )

def get_plan_by_id(plan_id: str, user_id: str, db: Session):
    plan = db.query(MealPlan).filter(
        MealPlan.id == plan_id,
        MealPlan.user_id == user_id
    ).first()
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan no encontrado"
        )
    return plan

def update_meal_plan(plan_id: str, data: MealPlanUpdate, user_id: str, db: Session):
    plan = get_plan_by_id(plan_id, user_id, db)
    
    # Actualizar solo los campos proporcionados
    update_data = data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(plan, field, value)
    
    # Si se activa este plan, desactivar otros
    if data.status == "active":
        db.query(MealPlan).filter(
            MealPlan.user_id == user_id,
            MealPlan.id != plan_id,
            MealPlan.is_current == True
        ).update({"is_current": False})
        plan.is_current = True
    
    db.commit()
    db.refresh(plan)
    return plan

def delete_meal_plan(plan_id: str, user_id: str, db: Session):
    plan = get_plan_by_id(plan_id, user_id, db)
    
    # En lugar de eliminar, cambiamos a archived
    plan.status = "archived"
    plan.is_current = False
    
    db.commit()
    return {"message": "Plan archivado correctamente"}

def get_current_plan(user_id: str, db: Session):
    plan = db.query(MealPlan).filter(
        MealPlan.user_id == user_id,
        MealPlan.is_current == True,
        MealPlan.status == "active"
    ).first()
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay un plan activo"
        )
    return plan