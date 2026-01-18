# app/services/nutrition_form_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
import logging

from app.models.nutrition_form import NutritionForm
from app.core.redis import redis_client
from app.core.kafka import publish_event

logger = logging.getLogger(__name__)

def _cache_key(user_id: str) -> str:
    return f"nutrition_form:{user_id}"

def get_form(db: Session, user_id: str) -> NutritionForm | None:
    return db.query(NutritionForm).filter(NutritionForm.user_id == user_id).first()

def create_form(db: Session, user_id: str, data) -> NutritionForm:
    existing = get_form(db, user_id)
    if existing:
        # ✅ estándar: 409
        raise HTTPException(status_code=409, detail="Nutrition form already exists")

    form = NutritionForm(
        user_id=user_id,
        meals_per_day=data.meals_per_day,
        diet_type=data.diet_type,
        allergies=",".join(data.allergies) if data.allergies else "",
        preferences=",".join(data.preferences) if data.preferences else "",
        caloric_goal=data.caloric_goal,
        water_intake=data.water_intake
    )

    try:
        db.add(form)
        db.commit()
        db.refresh(form)
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Failed to create nutrition form for user {user_id}: {e}")
        raise

    # limpiar cache
    try:
        redis_client.delete(_cache_key(user_id))
    except Exception as redis_error:
        logger.warning(f"⚠️ Failed to clear Redis cache: {redis_error}")

    # evento kafka
    try:
        publish_event({
            "event": "nutrition_form.completed",
            "user_id": user_id,
            "form_id": form.id,
            "diet_type": data.diet_type,
            "caloric_goal": data.caloric_goal,
            "meals_per_day": data.meals_per_day,
            "has_allergies": bool(data.allergies),
            "has_preferences": bool(data.preferences),
            "water_intake": data.water_intake
        })
    except Exception as kafka_error:
        logger.error(f"❌ Failed to publish Kafka event: {kafka_error}")

    return form

def update_form(db: Session, user_id: str, data) -> NutritionForm:
    form = get_form(db, user_id)
    if not form:
        raise HTTPException(status_code=404, detail="Nutrition form not found")

    form.meals_per_day = data.meals_per_day
    form.diet_type = data.diet_type
    form.allergies = ",".join(data.allergies) if data.allergies else ""
    form.preferences = ",".join(data.preferences) if data.preferences else ""
    form.caloric_goal = data.caloric_goal
    form.water_intake = data.water_intake

    try:
        db.commit()
        db.refresh(form)
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Failed to update nutrition form for user {user_id}: {e}")
        raise

    try:
        redis_client.delete(_cache_key(user_id))
    except Exception as redis_error:
        logger.warning(f"⚠️ Failed to clear Redis cache: {redis_error}")

    return form

def delete_form(db: Session, user_id: str) -> None:
    form = get_form(db, user_id)
    if not form:
        raise HTTPException(status_code=404, detail="Nutrition form not found")

    try:
        db.delete(form)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Failed to delete nutrition form for user {user_id}: {e}")
        raise

    try:
        redis_client.delete(_cache_key(user_id))
    except Exception as redis_error:
        logger.warning(f"⚠️ Failed to clear Redis cache: {redis_error}")
