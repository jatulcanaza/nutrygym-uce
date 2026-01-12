import logging
from fastapi import FastAPI, BackgroundTasks, HTTPException, status
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
import asyncio

from app.core.kafka import init_kafka, close_kafka, send_message
from app.core.config import settings
from app.consumers.nutrition_consumer import run_consumer

# Configurar logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Modelos de validación
class GenerateRequest(BaseModel):
    user_id: str = Field(..., description="ID del usuario")
    weight: float = Field(..., description="Peso en kg", gt=0)
    height: float = Field(..., description="Altura en cm", gt=0)
    goal: str = Field(..., description="Objetivo de fitness")
    preferences: str = Field(default="", description="Preferencias de comida")
    restrictions: str = Field(default="", description="Restricciones dietéticas")

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str = "1.0.0"

class GenerateResponse(BaseModel):
    status: str
    message: str
    request_id: str

# Lifespan para inicializar/cerrar Kafka
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        await init_kafka()
        logger.info("✅ Servicio iniciado correctamente")
        
        # Iniciar consumer en background
        asyncio.create_task(run_consumer())
        
    except Exception as e:
        logger.error(f"❌ Error en startup: {e}")
        raise
    
    yield
    
    # Shutdown
    try:
        await close_kafka()
        logger.info("✅ Servicio cerrado correctamente")
    except Exception as e:
        logger.error(f"❌ Error en shutdown: {e}")

app = FastAPI(
    title="AI Generator Service",
    description="Generación asíncrona de planes nutricionales con IA",
    version="1.0.0",
    lifespan=lifespan
)

@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest, background_tasks: BackgroundTasks):
    """
    Genera un plan nutricional personalizado
    
    - **user_id**: ID único del usuario
    - **weight**: Peso en kg
    - **height**: Altura en cm
    - **goal**: Objetivo (e.g., weight_loss, muscle_gain, maintenance)
    - **preferences**: Preferencias de comida (opcional)
    - **restrictions**: Restricciones dietéticas (opcional)
    """
    try:
        data = request.dict()
        request_id = f"{data['user_id']}_{data['weight']}_{data['height']}"
        
        logger.info(f"📨 Solicitud de generación recibida para user {request.user_id}")
        
        # Enviar mensaje a Kafka de forma asíncrona
        await send_message(settings.KAFKA_TOPIC_GENERATE, data)
        
        return GenerateResponse(
            status="queued",
            message="Plan nutricional en cola para generación",
            request_id=request_id
        )
        
    except Exception as e:
        logger.error(f"❌ Error en /generate: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar solicitud: {str(e)}"
        )

@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check del servicio"""
    return HealthResponse(
        status="ok",
        service="ai-generator-service"
    )

@app.get("/metrics")
async def metrics():
    """Métricas del servicio"""
    return {
        "service": "ai-generator-service",
        "status": "running",
        "kafka": "connected",
        "mongo": "connected"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=settings.PORT,
        log_level=settings.LOG_LEVEL.lower()
    )
