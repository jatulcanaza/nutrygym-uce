from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import json
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

producer = None
consumer = None

async def init_kafka():
    """Inicializa Kafka producer y consumer"""
    global producer, consumer
    try:
        producer = AIOKafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )
        await producer.start()
        logger.info("✅ Kafka Producer iniciado")

        consumer = AIOKafkaConsumer(
            settings.KAFKA_TOPIC_GENERATE,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            group_id="ai-generator-group"
        )
        await consumer.start()
        logger.info("✅ Kafka Consumer iniciado")
    except Exception as e:
        logger.error(f"❌ Error inicializando Kafka: {e}")
        raise

async def close_kafka():
    """Cierra conexiones de Kafka"""
    global producer, consumer
    try:
        if producer:
            await producer.stop()
            logger.info("✅ Kafka Producer cerrado")
        if consumer:
            await consumer.stop()
            logger.info("✅ Kafka Consumer cerrado")
    except Exception as e:
        logger.error(f"❌ Error cerrando Kafka: {e}")

async def send_message(topic: str, value: dict):
    """Envía mensaje a Kafka de forma asíncrona"""
    try:
        await producer.send_and_wait(topic, value)
        logger.debug(f"📤 Mensaje enviado a {topic}")
    except Exception as e:
        logger.error(f"❌ Error enviando mensaje a Kafka: {e}")
        raise
