import os
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)

class Settings:
    PORT = int(os.getenv("PORT", 3006))

    # Kafka (LOCAL)
    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    KAFKA_TOPIC_GENERATE = os.getenv("KAFKA_TOPIC_GENERATE")

    # Groq
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL")

    # Mongo
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DB = os.getenv("MONGO_DB")

    # External Services
    PLAN_MANAGEMENT_SERVICE_URL = os.getenv("PLAN_MANAGEMENT_SERVICE_URL")
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    def __init__(self):
        """Valida configuración crítica"""
        errors = []
        
        if not self.KAFKA_BOOTSTRAP_SERVERS:
            errors.append("KAFKA_BOOTSTRAP_SERVERS no configurado")
        if not self.KAFKA_TOPIC_GENERATE:
            errors.append("KAFKA_TOPIC_GENERATE no configurado")
        if not self.GROQ_API_KEY:
            errors.append("GROQ_API_KEY no configurado")
        if not self.GROQ_MODEL:
            errors.append("GROQ_MODEL no configurado")
        if not self.MONGO_URI:
            errors.append("MONGO_URI no configurado")
        if not self.MONGO_DB:
            errors.append("MONGO_DB no configurado")
        if not self.PLAN_MANAGEMENT_SERVICE_URL:
            errors.append("PLAN_MANAGEMENT_SERVICE_URL no configurado")
        
        if errors:
            error_msg = "\n".join([f"❌ {err}" for err in errors])
            logger.error(f"Errores de configuración:\n{error_msg}")
            raise ValueError(f"Configuración incompleta:\n{error_msg}")
        
        logger.info("✅ Configuración validada correctamente")

settings = Settings()
