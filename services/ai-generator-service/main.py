# ai-generator-service/main.py

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

from app.core.config import settings
from app.core.kafka import init_kafka, close_kafka
from app.consumers.nutrition_consumer import run_consumer
from app.services.ai_service import process_generation

# =========================
# Logging
# =========================
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# =========================
# Schemas
# =========================
class GenerateRequest(BaseModel):
    user_id: str

    # Profile
    height_cm: float = Field(..., gt=0)
    weight_kg: float = Field(..., gt=0)
    goal: str
    activity_level: Optional[str] = None

    gender: Optional[str] = None
    birth_date: Optional[str] = None  # YYYY-MM-DD (o lo que venga)

    # Nutrition form
    meals_per_day: int = Field(..., ge=3, le=5)
    diet_type: Optional[str] = None
    preferences: list[str] = Field(default_factory=list)
    allergies: list[str] = Field(default_factory=list)
    caloric_goal: Optional[float] = None
    water_intake: Optional[float] = None


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str = "1.0.0"


class GeneratePlanResponse(BaseModel):
    # Lo que usa Plan Management
    calories: float
    protein: float
    carbs: float
    fats: float
    title: str
    # OJO: aquí va el JSON string (serializado) con week/tips/etc.
    description: str


# =========================
# Lifespan
# =========================
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_kafka()
        logger.info("✅ Servicio iniciado correctamente")

        # Consumer opcional (si no hay Kafka, puedes comentar esta línea)
        asyncio.create_task(run_consumer())

    except Exception as e:
        logger.error(f"❌ Error en startup: {e}")
        raise

    yield

    try:
        await close_kafka()
        logger.info("✅ Servicio cerrado correctamente")
    except Exception as e:
        logger.error(f"❌ Error en shutdown: {e}")


app = FastAPI(
    title="AI Generator Service",
    description="Generación de planes nutricionales con IA",
    version="1.0.0",
    lifespan=lifespan
)


# =========================
# Endpoints
# =========================
@app.post("/generate", response_model=GeneratePlanResponse)
async def generate(request: GenerateRequest):
    """
    Genera un plan nutricional personalizado (SINCRÓNICO)
    Devuelve macros + title + description (JSON serializado).
    """
    try:
        data = request.dict()
        logger.info(f"📨 Solicitud de generación recibida para user {request.user_id}")

        result = await process_generation(data)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo generar el plan (result vacío)."
            )

        # process_generation ya devuelve el payload listo
        return GeneratePlanResponse(
            calories=float(result["calories"]),
            protein=float(result["protein"]),
            carbs=float(result["carbs"]),
            fats=float(result["fats"]),
            title=result.get("title", "Plan Nutricional IA"),
            description=result["description"]
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error en /generate: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar solicitud: {str(e)}"
        )


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="ok",
        service="ai-generator-service"
    )


@app.get("/metrics")
async def metrics():
    return {
        "service": "ai-generator-service",
        "status": "running",
        "kafka": "connected",
        "mongo": "connected"
    }
