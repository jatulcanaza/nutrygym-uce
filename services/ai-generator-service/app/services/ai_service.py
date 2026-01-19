# ai-generator-service/app/services/ai_service.py

import json
import logging
from datetime import datetime
from typing import Optional

from app.core.groq_client import generate_meal_plan
from app.core.database import ai_logs

logger = logging.getLogger(__name__)

def _safe_list(x):
    if x is None:
        return []
    if isinstance(x, list):
        return x
    if isinstance(x, str) and x.strip() == "":
        return []
    return [str(x)]

async def process_generation(data: dict) -> Optional[dict]:
    user_id = data.get("user_id")
    start_time = datetime.utcnow()

    try:
        if not user_id:
            raise ValueError("user_id es requerido")

        # ✅ Datos esperados (desde Plan Management)
        gender = data.get("gender")
        birth_date = data.get("birth_date")

        weight = data.get("weight_kg")
        height = data.get("height_cm")
        goal = data.get("goal")
        activity = data.get("activity_level")
        diet_type = data.get("diet_type")
        meals_per_day = data.get("meals_per_day")
        caloric_goal = data.get("caloric_goal")
        water_intake = data.get("water_intake")

        preferences = _safe_list(data.get("preferences"))
        allergies = _safe_list(data.get("allergies"))

        if weight is None or height is None or not goal:
            raise ValueError("Datos incompletos: weight_kg, height_cm, goal son requeridos")

        if not meals_per_day:
            raise ValueError("meals_per_day es requerido (nutrition form)")

        # ✅ Prompt: SOLO JSON, sin markdown, sin repetición
        prompt = f"""
Eres un nutricionista profesional.

Devuelve SOLO un JSON válido (sin markdown, sin ```), siguiendo exactamente este esquema:

{{
  "title": "string",
  "summary": "string",
  "macros": {{
    "calories": number,
    "protein_g": number,
    "carbs_g": number,
    "fats_g": number
  }},
  "week": [
    {{
      "day": "Monday",
      "meals": [
        {{
          "type": "Breakfast|Lunch|Dinner|Snack",
          "name": "string",
          "notes": "string"
        }}
      ]
    }}
  ],
  "tips": ["string", "string"]
}}

Reglas IMPORTANTES:
- Languaje: responde en English.
- Devuelve SOLO JSON válido, sin markdown.
- NO repitas contenido.
- "week" SIEMPRE debe contener 7 días: Monday..Sunday en ese orden.
- "meals" por día debe tener EXACTAMENTE {meals_per_day} items.
- Respeta alergias estrictamente (nunca incluir esos alimentos).

Reglas de MACROS:
- Si "caloric_goal" existe y es > 0, entonces macros.calories DEBE ser EXACTAMENTE caloric_goal.
- Si "caloric_goal" es null o 0, calcula macros.calories según: weight, height, gender, birth_date (edad), goal y activity_level.
- Los gramos de proteína, carbs y fats deben ser coherentes con el objetivo:
  - gain_muscle: proteína alta
  - lose_weight: proteína alta, carbs moderados/bajos
  - maintain: balanceado


Datos del usuario:
- Weight (kg): {weight}
- Height (cm): {height}
- Goal: {goal}
- Activity level: {activity}

Nutrición:
- Meals per day: {meals_per_day}
- Diet type: {diet_type}
- Caloric goal: {caloric_goal}
- Water intake (liters): {water_intake}
- Preferences: {", ".join(preferences) if preferences else "None"}
- Allergies (MUST AVOID): {", ".join(allergies) if allergies else "None"}
"""

        plan_obj = generate_meal_plan(prompt)  # debe retornar dict

        macros = plan_obj.get("macros") or {}
        calories = int(round(float(macros.get("calories", 0) or 0)))
        protein  = int(round(float(macros.get("protein_g", 0) or 0)))
        carbs    = int(round(float(macros.get("carbs_g", 0) or 0)))
        fats     = int(round(float(macros.get("fats_g", 0) or 0)))


        if not all([calories, protein, carbs, fats]):
            raise ValueError("JSON missing macros fields (calories/protein_g/carbs_g/fats_g)")

        description = json.dumps(plan_obj, ensure_ascii=False)

        response_payload = {
            "user_id": user_id,
            "title": plan_obj.get("title") or "Plan Nutricional IA",
            "description": description,
            "calories": calories,
            "protein": protein,
            "carbs": carbs,
            "fats": fats,
        }

        ai_logs.insert_one({
            "user_id": user_id,
            "input": data,
            "output": plan_obj,
            "created_at": start_time,
            "processing_time_ms": (datetime.utcnow() - start_time).total_seconds() * 1000,
            "status": "success"
        })

        return response_payload

    except Exception as e:
        logger.error(f"❌ Error en process_generation: {e}", exc_info=True)
        try:
            ai_logs.insert_one({
                "user_id": user_id,
                "input": data,
                "error": str(e),
                "created_at": start_time,
                "processing_time_ms": (datetime.utcnow() - start_time).total_seconds() * 1000,
                "status": "error"
            })
        except Exception:
            pass
        return None
