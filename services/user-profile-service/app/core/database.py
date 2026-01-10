import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError
from tenacity import retry, stop_after_attempt, wait_fixed
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "user-profile-db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "user_profile_db")
DB_USER = os.getenv("DB_USER", "user_profile_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "user_profile_pass")

DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

logger.info(f"Configurando conexión a: {DB_HOST}:{DB_PORT}/{DB_NAME}")

@retry(
    stop=stop_after_attempt(5),
    wait=wait_fixed(5),
    reraise=True
)
def create_engine_with_retry():
    """Crear engine con retries automáticos"""
    return create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Verificar conexión antes de usar
        pool_recycle=300,    # Reciclar conexiones cada 5 minutos
        echo=True            # Cambiar a False en producción
    )

try:
    engine = create_engine_with_retry()
    logger.info("✅ Engine de SQLAlchemy creado exitosamente")
except OperationalError as e:
    logger.error(f"❌ Error creando engine después de varios intentos: {e}")
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()