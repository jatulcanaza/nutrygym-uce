# main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
import time
import logging
import os
from fastapi.middleware.cors import CORSMiddleware

from app.routes.nutrition_form import router
from app.core.database import Base, engine, wait_for_db
from app.core.kafka import shutdown_kafka, ensure_kafka_ready

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Starting Nutrition Form Service...")
    
    # Wait for database to be ready - SIN await porque es función síncrona
    logger.info("⏳ Waiting for database connection...")
    wait_for_db()  # ← CAMBIO IMPORTANTE: SIN 'await'
    
    # Create database tables
    logger.info("🗄️ Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Database tables created successfully")
    
    # Initialize Kafka
    logger.info("🔌 Initializing Kafka connection...")
    try:
        ensure_kafka_ready()
    except Exception as e:
        logger.warning(f"⚠️ Kafka initialization failed (will retry on first use): {e}")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Nutrition Form Service...")
    shutdown_kafka()  # Esto ya está bien (síncrono)

app = FastAPI(
    title="Nutrition Form Service",
    description="Microservice for capturing nutritional data in NutriGym system",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# =========================
# CORS
# =========================
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(router)

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "nutrition-form",
        "timestamp": time.time(),
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Nutrition Form Service API",
        "description": "Microservice for capturing nutritional data",
        "endpoints": {
            "submit_form": "POST /nutrition-form",
            "health": "GET /health",
            "documentation": "GET /docs"
        },
        "version": "1.0.0"
    }