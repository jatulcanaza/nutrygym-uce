# app/services/meal_plan_service.py

from __future__ import annotations

import os
import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.notification_publisher import publish_notification
from app.models.meal_plan import MealPlan
from app.schemas.meal_plan import MealPlanCreate, MealPlanUpdate


# =========================
# CRUD EXISTENTE
# =========================

def create_meal_plan(plan: MealPlanCreate, user_id: str, db: Session):
    new_plan = MealPlan(
        user_id=user_id,
        calories=plan.calories,
        protein=plan.protein,
        carbs=plan.carbs,
        fats=plan.fats,
        title=plan.title,
        description=plan.description,
        status="draft",
        is_current=False,
    )

    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)

    return new_plan


def get_user_plans(user_id: str, db: Session):
    return db.query(MealPlan).filter(MealPlan.user_id == user_id).all()


def get_plan_by_id(plan_id: str, user_id: str, db: Session):
    plan = (
        db.query(MealPlan)
        .filter(MealPlan.id == plan_id, MealPlan.user_id == user_id)
        .first()
    )

    if not plan:
        raise HTTPException(status_code=404, detail="Plan no encontrado")

    return plan


def update_meal_plan(plan_id: str, plan_update: MealPlanUpdate, user_id: str, db: Session):
    plan = get_plan_by_id(plan_id, user_id, db)
    data = plan_update.dict(exclude_unset=True)

    # ✅ Regla: si pasa a completed/canceled, deja de ser current
    if "status" in data and data["status"] in ("completed", "canceled"):
        data["is_current"] = False

    # ✅ Regla: si pasa a active, debe ser current y NO puede haber otro active current
    if "status" in data and data["status"] == "active":
        other_active = (
            db.query(MealPlan)
            .filter(
                MealPlan.user_id == user_id,
                MealPlan.is_current == True,
                MealPlan.status == "active",
                MealPlan.id != plan_id,
            )
            .first()
        )
        if other_active:
            raise HTTPException(
                status_code=409,
                detail="Another active plan already exists. End or cancel it first.",
            )
        data["is_current"] = True

    # ✅ Aplicar cambios
    for field, value in data.items():
        setattr(plan, field, value)

    db.commit()
    db.refresh(plan)
    return plan


def delete_meal_plan(plan_id: str, user_id: str, db: Session):
    plan = get_plan_by_id(plan_id, user_id, db)
    db.delete(plan)
    db.commit()


def get_current_plan(user_id: str, db: Session):
    plan = (
        db.query(MealPlan)
        .filter(
            MealPlan.user_id == user_id,
            MealPlan.is_current == True,
            MealPlan.status == "active",  # ✅ clave
        )
        .order_by(MealPlan.created_at.desc())
        .first()
    )

    if not plan:
        raise HTTPException(status_code=404, detail="No active plan found")

    return plan


# =========================
# NUEVO: GUARDADO "ACTIVE/CURRENT"
# (reutiliza la lógica del endpoint interno)
# =========================
def create_active_plan_from_ai(plan: MealPlanCreate, db: Session):
    # 1) Si hay plan activo/current, terminarlo automáticamente (completed)
    existing_active = (
        db.query(MealPlan)
        .filter(
            MealPlan.user_id == plan.user_id,
            MealPlan.is_current == True,
            MealPlan.status == "active",
        )
        .all()
    )

    for p in existing_active:
        p.status = "completed"
        p.is_current = False

    db.commit()

    # 2) Crear el nuevo plan como ACTIVE y CURRENT
    new_plan = MealPlan(
        user_id=plan.user_id,
        calories=plan.calories,
        protein=plan.protein,
        carbs=plan.carbs,
        fats=plan.fats,
        title=plan.title,
        description=plan.description,
        status="active",
        is_current=True,
    )

    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    return new_plan


# =========================
# HELPERS
# =========================
def _safe_user_name(profile: dict) -> str:
    first = (profile.get("first_name") or "").strip()
    last = (profile.get("last_name") or "").strip()
    full = f"{first} {last}".strip()
    return full or "Unknown user"


# =========================
# NUEVO: ORQUESTACIÓN
# Lee Profile + Nutrition Form y llama AI Generator
# =========================
async def generate_plan_from_forms(user_id: str, bearer_token: str, db: Session):
    profile_base = os.getenv("USER_PROFILE_SERVICE_URL")
    nutrition_base = os.getenv("NUTRITION_FORM_SERVICE_URL")
    ai_base = os.getenv("AI_GENERATOR_SERVICE_URL")

    if not profile_base:
        raise HTTPException(status_code=500, detail="Missing USER_PROFILE_SERVICE_URL")
    if not nutrition_base:
        raise HTTPException(status_code=500, detail="Missing NUTRITION_FORM_SERVICE_URL")
    if not ai_base:
        raise HTTPException(status_code=500, detail="Missing AI_GENERATOR_SERVICE_URL")

    headers = {"Authorization": f"Bearer {bearer_token}"}

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            # 1) Obtener perfil
            prof_res = await client.get(f"{profile_base}/profiles/me", headers=headers)
            if prof_res.status_code != 200:
                raise HTTPException(
                    status_code=502,
                    detail=f"Profile service error ({prof_res.status_code}): {prof_res.text}",
                )
            profile = prof_res.json()
            user_name = _safe_user_name(profile)

            # 2) Obtener nutrition form
            nut_res = await client.get(f"{nutrition_base}/nutrition-form/me", headers=headers)
            if nut_res.status_code != 200:
                raise HTTPException(
                    status_code=502,
                    detail=f"Nutrition service error ({nut_res.status_code}): {nut_res.text}",
                )
            nutrition = nut_res.json()

            # 3) Validar profile mínimo
            weight = profile.get("weight_kg")
            height = profile.get("height_cm")
            goal = profile.get("goal")

            if weight is None or height is None or not goal:
                raise HTTPException(
                    status_code=400,
                    detail="Profile incomplete: missing weight_kg, height_cm or goal",
                )

            # 4) Payload IA (tu mapping)
            ai_payload = {
                "user_id": user_id,
                # Profile
                "first_name": profile.get("first_name"),
                "last_name": profile.get("last_name"),
                "gender": profile.get("gender"),
                "age_or_birth_date": profile.get("birth_date"),
                "height_cm": profile.get("height_cm"),
                "weight_kg": profile.get("weight_kg"),
                "goal": profile.get("goal"),
                "activity_level": profile.get("activity_level"),
                # Nutrition form
                "meals_per_day": nutrition.get("meals_per_day"),
                "diet_type": nutrition.get("diet_type"),
                "preferences": nutrition.get("preferences") or [],
                "allergies": nutrition.get("allergies") or [],
                "caloric_goal": nutrition.get("caloric_goal"),
                "water_intake": nutrition.get("water_intake"),
            }

            # 5) Llamar AI Generator
            ai_res = await client.post(f"{ai_base}/generate", json=ai_payload)
            if ai_res.status_code != 200:
                raise HTTPException(
                    status_code=502,
                    detail=f"AI generator error ({ai_res.status_code}): {ai_res.text}",
                )
            ai_data = ai_res.json()

        # 6) Validar respuesta IA
        if not all(k in ai_data for k in ["calories", "protein", "carbs", "fats"]):
            raise HTTPException(
                status_code=500,
                detail="AI response missing macros (calories/protein/carbs/fats). Update AI Generator response.",
            )

        # 7) Crear plan y guardar
        plan_create = MealPlanCreate(
            user_id=user_id,
            calories=ai_data["calories"],
            protein=ai_data["protein"],
            carbs=ai_data["carbs"],
            fats=ai_data["fats"],
            title=ai_data.get("title", "Mi Plan Alimenticio"),
            description=ai_data.get("description", ""),
        )

        created = create_active_plan_from_ai(plan_create, db)

        # ✅ NOTIFICACIÓN ÉXITO (con nombre)
        publish_notification(
            {
                "type": "alert",
                "title": "Plan generated",
                "message": f"Meal plan generated successfully for {user_name}",
                "source_service": "plan-management-service",
                "severity": "info",
                "meta": {
                    "user_id": user_id,
                    "user_name": user_name,
                    "plan_id": str(created.id),
                    "status": created.status,
                    "is_current": created.is_current,
                },
            }
        )

        return created

    except HTTPException as e:
        # ✅ NOTIFICACIÓN ERROR (HTTPException)
        publish_notification(
            {
                "type": "alert",
                "title": "Plan generation failed",
                "message": f"Failed to generate plan for user_id={user_id}: {e.detail}",
                "source_service": "plan-management-service",
                "severity": "error",
                "meta": {"user_id": user_id, "status_code": e.status_code},
            }
        )
        raise

    except Exception as e:
        # ✅ NOTIFICACIÓN ERROR (GENÉRICO)
        publish_notification(
            {
                "type": "alert",
                "title": "Plan generation failed",
                "message": f"Unexpected error generating plan for user_id={user_id}: {str(e)}",
                "source_service": "plan-management-service",
                "severity": "error",
                "meta": {"user_id": user_id},
            }
        )
        raise


def _unset_current_for_user(user_id: str, db: Session):
    db.query(MealPlan).filter(
        MealPlan.user_id == user_id,
        MealPlan.is_current == True,
    ).update({"is_current": False})
    db.commit()


async def regenerate_current_plan(user_id: str, bearer_token: str, db: Session):
    # 1) Verifica que exista plan active/current
    current = (
        db.query(MealPlan)
        .filter(
            MealPlan.user_id == user_id,
            MealPlan.is_current == True,
            MealPlan.status == "active",
        )
        .order_by(MealPlan.created_at.desc())
        .first()
    )
    if not current:
        raise HTTPException(status_code=404, detail="No active plan to regenerate")

    profile_base = os.getenv("USER_PROFILE_SERVICE_URL")
    nutrition_base = os.getenv("NUTRITION_FORM_SERVICE_URL")
    ai_base = os.getenv("AI_GENERATOR_SERVICE_URL")

    if not profile_base or not nutrition_base or not ai_base:
        raise HTTPException(status_code=500, detail="Missing external service URLs")

    headers = {"Authorization": f"Bearer {bearer_token}"}

    async with httpx.AsyncClient(timeout=20.0) as client:
        prof_res = await client.get(f"{profile_base}/profiles/me", headers=headers)
        if prof_res.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail=f"Profile service error ({prof_res.status_code}): {prof_res.text}",
            )
        profile = prof_res.json()
        user_name = _safe_user_name(profile)

        nut_res = await client.get(f"{nutrition_base}/nutrition-form/me", headers=headers)
        if nut_res.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail=f"Nutrition service error ({nut_res.status_code}): {nut_res.text}",
            )
        nutrition = nut_res.json()

        weight = profile.get("weight_kg")
        height = profile.get("height_cm")
        goal = profile.get("goal")
        if weight is None or height is None or not goal:
            raise HTTPException(
                status_code=400,
                detail="Profile incomplete: missing weight_kg, height_cm or goal",
            )

        ai_payload = {
            "user_id": user_id,
            # Profile
            "first_name": profile.get("first_name"),
            "last_name": profile.get("last_name"),
            "gender": profile.get("gender"),
            "age_or_birth_date": profile.get("birth_date"),
            "height_cm": profile.get("height_cm"),
            "weight_kg": profile.get("weight_kg"),
            "goal": profile.get("goal"),
            "activity_level": profile.get("activity_level"),
            # Nutrition form
            "meals_per_day": nutrition.get("meals_per_day"),
            "diet_type": nutrition.get("diet_type"),
            "preferences": nutrition.get("preferences") or [],
            "allergies": nutrition.get("allergies") or [],
            "caloric_goal": nutrition.get("caloric_goal"),
            "water_intake": nutrition.get("water_intake"),
        }

        ai_res = await client.post(f"{ai_base}/generate", json=ai_payload)
        if ai_res.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail=f"AI generator error ({ai_res.status_code}): {ai_res.text}",
            )
        ai_data = ai_res.json()

    if not all(k in ai_data for k in ["calories", "protein", "carbs", "fats"]):
        raise HTTPException(
            status_code=500,
            detail="AI response missing macros (calories/protein/carbs/fats).",
        )

    # 3) Actualiza el plan actual (sube versión)
    current.calories = ai_data["calories"]
    current.protein = ai_data["protein"]
    current.carbs = ai_data["carbs"]
    current.fats = ai_data["fats"]
    current.title = ai_data.get("title", current.title)
    current.description = ai_data.get("description", current.description)
    current.version = (current.version or 1) + 1

    db.commit()
    db.refresh(current)

    publish_notification(
        {
            "type": "alert",
            "title": "Plan regenerated",
            "message": f"Meal plan regenerated successfully for {user_name}",
            "source_service": "plan-management-service",
            "severity": "info",
            "meta": {
                "user_id": user_id,
                "user_name": user_name,
                "plan_id": str(current.id),
                "version": current.version,
            },
        }
    )

    return current


def end_current_plan(user_id: str, db: Session):
    active_plans = (
        db.query(MealPlan)
        .filter(
            MealPlan.user_id == user_id,
            MealPlan.is_current == True,
            MealPlan.status == "active",
        )
        .order_by(MealPlan.created_at.desc())
        .all()
    )

    if not active_plans:
        raise HTTPException(status_code=404, detail="No active plan to end")

    # Si hay más de uno por errores anteriores, termina TODOS
    for p in active_plans:
        p.status = "completed"
        p.is_current = False

    db.commit()
    db.refresh(active_plans[0])

    # Nota: aquí no tenemos token => no podemos pedir profile para nombre
    publish_notification(
        {
            "type": "alert",
            "title": "Plan ended",
            "message": f"Active plan ended for user_id={user_id}",
            "source_service": "plan-management-service",
            "severity": "info",
            "meta": {"user_id": user_id},
        }
    )

    return active_plans[0]


def cancel_current_plan(user_id: str, db: Session):
    active_plans = (
        db.query(MealPlan)
        .filter(
            MealPlan.user_id == user_id,
            MealPlan.is_current == True,
            MealPlan.status == "active",
        )
        .order_by(MealPlan.created_at.desc())
        .all()
    )

    if not active_plans:
        raise HTTPException(status_code=404, detail="No active plan to cancel")

    for p in active_plans:
        p.status = "canceled"
        p.is_current = False

    db.commit()
    db.refresh(active_plans[0])

    # Nota: aquí no tenemos token => no podemos pedir profile para nombre
    publish_notification(
        {
            "type": "alert",
            "title": "Plan canceled",
            "message": f"Active plan canceled for user_id={user_id}",
            "source_service": "plan-management-service",
            "severity": "warning",
            "meta": {"user_id": user_id},
        }
    )

    return active_plans[0]
