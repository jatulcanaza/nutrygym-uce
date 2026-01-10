from app.models.nutrition_form import NutritionForm
from app.core.redis import redis_client
from app.core.kafka import publish_event  # ← ESTA FUNCIÓN AHORA ES SINC RÓNICA
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

def save_form(db: Session, user_id: str, data):
    """
    Save nutrition form to database and publish event to Kafka
    
    Args:
        db: Database session
        user_id: User ID submitting the form
        data: Nutrition form data
    
    Returns:
        NutritionForm: The saved form object
    """
    try:
        logger.info(f"💾 Saving nutrition form for user {user_id}")
        
        # Create form object
        form = NutritionForm(
            user_id=user_id,
            meals_per_day=data.meals_per_day,
            diet_type=data.diet_type,
            allergies=",".join(data.allergies) if data.allergies else "",
            preferences=",".join(data.preferences) if data.preferences else "",
            caloric_goal=data.caloric_goal,
            water_intake=data.water_intake
        )

        # Save to database
        db.add(form)
        db.commit()
        db.refresh(form)

        logger.info(f"✅ Nutrition form saved with ID: {form.id}")

        # Clear Redis cache for this user
        try:
            cache_key = f"nutrition_form:{user_id}"
            redis_client.delete(cache_key)
            logger.debug(f"🧹 Redis cache cleared for key: {cache_key}")
        except Exception as redis_error:
            logger.warning(f"⚠️ Failed to clear Redis cache: {redis_error}")

        # Publish Kafka event (ahora es sincrónico pero rápido)
        try:
            event_data = {
                "event": "nutrition_form.completed",
                "user_id": user_id,
                "form_id": form.id,
                "diet_type": data.diet_type,
                "caloric_goal": data.caloric_goal,
                "meals_per_day": data.meals_per_day,
                "has_allergies": len(data.allergies) > 0 if data.allergies else False,
                "has_preferences": len(data.preferences) > 0 if data.preferences else False,
                "water_intake": data.water_intake
            }
            
            # Llamada sincrónica (pero no bloqueante gracias al callback)
            publish_event(event_data)
            
            logger.info(f"📨 Kafka event published for form {form.id}")
            
        except Exception as kafka_error:
            logger.error(f"❌ Failed to publish Kafka event: {kafka_error}")
            # Don't fail the request if Kafka fails

        return form
        
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Failed to save nutrition form for user {user_id}: {e}")
        raise