from fastapi import FastAPI
from app.core.database import Base, engine
from app.routes.profiles import router
import time
import logging
import os
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="User Profile Service",
    version="1.0.0"
)
# ---- CORS (permite llamadas desde el frontend Vite) ----
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def wait_for_db(max_retries=5, delay=5):
    """Esperar a que la base de datos esté disponible"""
    for attempt in range(max_retries):
        try:
            with engine.connect() as conn:
                logger.info("✅ Conexión a base de datos exitosa")
                return True
        except OperationalError as e:
            logger.warning(f"❌ Intento {attempt + 1}/{max_retries}: No se pudo conectar a la BD: {e}")
            if attempt < max_retries - 1:
                logger.info(f"Esperando {delay} segundos antes de reintentar...")
                time.sleep(delay)
    
    logger.error("❌ No se pudo conectar a la base de datos después de varios intentos")
    return False

@app.on_event("startup")
def startup():
    logger.info("🚀 Iniciando User Profile Service...")
    
    # Esperar a que la BD esté disponible
    if not wait_for_db():
        raise RuntimeError("No se pudo conectar a la base de datos")
    
    # Crear tablas
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tablas creadas correctamente")
    except Exception as e:
        logger.error(f"❌ Error creando tablas: {e}")
        raise

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "User Profile Service", "status": "running"}

@app.get("/health")
async def health():
    # Verificar estado de la BD
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        db_status = "healthy"
    except Exception:
        db_status = "unhealthy"
    
    return {
        "status": "ok",
        "service": "user-profile-service",
        "database": db_status,
        "version": "1.0.0"
    }