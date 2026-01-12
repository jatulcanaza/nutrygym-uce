import logging
from datetime import datetime
from typing import Optional
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.groq_client import generate_meal_plan
from app.core.database import ai_logs
from app.core.config import settings
from app.core.kafka import send_message

logger = logging.getLogger(__name__)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
async def send_to_plan_service(user_id: str, plan: str) -> bool:
    """Envía plan generado al servicio de planes con reintentos"""
    try:
        response = requests.post(
            f"{settings.PLAN_MANAGEMENT_SERVICE_URL}/api/v1/plans/from-ai",
            json={
                "user_id": user_id,
                "plan": plan
            },
            timeout=10
        )
        response.raise_for_status()
        logger.info(f"✅ Plan enviado a plan-management-service para user {user_id}")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Error enviando plan: {e}")
        raise

async def process_generation(data: dict) -> Optional[dict]:
    """Procesa generación de plan de comida"""
    user_id = data.get("user_id")
    start_time = datetime.utcnow()
    
    try:
        # Validar datos de entrada
        if not user_id:
            raise ValueError("user_id es requerido")
        
        if not all(k in data for k in ["weight", "height", "goal"]):
            raise ValueError("Datos incompletos: weight, height, goal son requeridos")
        
        logger.info(f"🔄 Procesando generación para user {user_id}")
        
        # Construir prompt
        prompt = f"""
        Create a personalized meal plan:
        Weight: {data.get('weight')} kg
        Height: {data.get('height')} cm
        Goal: {data.get('goal')}
        Preferences: {data.get('preferences', 'None')}
        Restrictions: {data.get('restrictions', 'None')}
        """
        
        # Generar con Groq
        result = generate_meal_plan(prompt)
        
        if not result:
            raise ValueError("Groq retornó respuesta vacía")
        
        # Guardar en MongoDB
        log_entry = {
            "user_id": user_id,
            "input": data,
            "output": result,
            "created_at": start_time,
            "processing_time_ms": (datetime.utcnow() - start_time).total_seconds() * 1000,
            "status": "success"
        }
        
        ai_logs.insert_one(log_entry)
        logger.info(f"✅ Plan generado y guardado para user {user_id}")
        
        # Enviar a plan-management-service
        try:
            await send_to_plan_service(user_id, result)
        except Exception as e:
            logger.warning(f"⚠️ Plan generado pero no se pudo enviar a plan-service: {e}")
        
        return log_entry
        
    except Exception as e:
        logger.error(f"❌ Error en process_generation: {e}", exc_info=True)
        
        # Registrar error en MongoDB
        try:
            ai_logs.insert_one({
                "user_id": user_id,
                "input": data,
                "error": str(e),
                "created_at": start_time,
                "processing_time_ms": (datetime.utcnow() - start_time).total_seconds() * 1000,
                "status": "error"
            })
        except Exception as db_error:
            logger.error(f"❌ Error guardando error en MongoDB: {db_error}")
        
        return None
