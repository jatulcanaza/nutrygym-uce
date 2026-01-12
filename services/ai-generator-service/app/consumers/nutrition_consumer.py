import asyncio
import logging
# Importación removida de aquí
from app.services.ai_service import process_generation

logger = logging.getLogger(__name__)

async def start_consumer():
    """Consume mensajes de Kafka de forma asíncrona"""
    # Importar aquí después de que Kafka esté inicializado
    from app.core.kafka import consumer
    
    if consumer is None:
        logger.error("❌ Consumer no inicializado. ¿Se llamó a init_kafka()?")
        return
    
    logger.info("🚀 Iniciando consumer de Kafka...")
    try:
        async for message in consumer:
            try:
                logger.info(f"📥 Mensaje recibido: {message.value}")
                await process_generation(message.value)
            except Exception as e:
                logger.error(f"❌ Error procesando mensaje: {e}", exc_info=True)
                # Continuar con el siguiente mensaje
                continue
    except Exception as e:
        logger.error(f"❌ Error en consumer: {e}", exc_info=True)
        raise

async def run_consumer():
    """Wrapper para ejecutar el consumer en background"""
    try:
        await start_consumer()
    except Exception as e:
        logger.error(f"❌ Error en run_consumer: {e}", exc_info=True)