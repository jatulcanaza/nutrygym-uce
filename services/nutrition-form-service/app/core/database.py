# app/core/database.py - ARCHIVO COMPLETO CORREGIDO

from sqlalchemy import create_engine, text  # ← AGREGAR text aquí
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import time
import logging
from sqlalchemy.exc import OperationalError

# Configure logging
logger = logging.getLogger(__name__)

# Database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(bind=engine)

# Base class for models
Base = declarative_base()

# Function to wait for database
def wait_for_db(max_retries: int = 30, wait_seconds: int = 2):
    """
    Espera a que la base de datos esté disponible.
    Esta es una función síncrona, NO async.
    """
    logger.info(f"⏳ Waiting for database connection (max {max_retries} retries)...")
    
    for attempt in range(1, max_retries + 1):
        try:
            # Intenta establecer una conexión - CORREGIDO
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))  # ← USAR text() aquí
            logger.info(f"✅ Database connection established (attempt {attempt}/{max_retries})")
            return True
        except OperationalError as e:
            if attempt < max_retries:
                logger.warning(
                    f"⚠️ Database not ready (attempt {attempt}/{max_retries}): {str(e)[:100]}..."
                )
                time.sleep(wait_seconds)
            else:
                logger.error(f"❌ Failed to connect to database after {max_retries} attempts")
                logger.error(f"Last error: {e}")
                raise
    return False

# Dependency function for FastAPI
def get_db():
    """
    Dependency function to get database session.
    Used in FastAPI route dependencies.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()