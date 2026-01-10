"""
Kafka producer using confluent-kafka (sincrónico, más estable)
"""
import json
import os
import logging
from confluent_kafka import Producer
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

# Load from environment variables
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_TOPIC_NUTRITION_EVENTS = os.getenv("KAFKA_TOPIC_NUTRITION_EVENTS", "nutrition.events")
ENABLE_KAFKA = os.getenv("ENABLE_KAFKA", "true").lower() == "true"

# Global producer instance
_producer = None

def get_producer():
    """Get or create Kafka producer instance"""
    global _producer
    
    if not ENABLE_KAFKA:
        logger.info("Kafka is disabled via ENABLE_KAFKA environment variable")
        return None
        
    if _producer is None:
        try:
            logger.info(f"🔌 Connecting to Kafka at: {KAFKA_BOOTSTRAP_SERVERS}")
            
            # Configuration for Confluent Kafka Producer
            conf = {
                'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
                'client.id': 'nutrition-form-service',
                'acks': 'all',  # Wait for all replicas to acknowledge
                'compression.type': 'gzip',
                'retries': 3,
                'linger.ms': 5,
                'batch.size': 16384,
                'request.timeout.ms': 30000,
                'message.timeout.ms': 30000,
                'socket.keepalive.enable': True,
                'enable.idempotence': False,  # Set to True for exactly-once semantics
            }
            
            _producer = Producer(conf)
            logger.info("✅ Confluent Kafka producer created successfully")
            
            # Test connection by flushing
            _producer.flush(timeout=5)
            logger.info("✅ Kafka connection test successful")
            
        except Exception as e:
            logger.error(f"❌ Failed to create Kafka producer: {e}")
            raise
    
    return _producer

def delivery_callback(err, msg):
    """Callback for message delivery reports"""
    if err:
        logger.error(f"❌ Message delivery failed: {err}")
    else:
        logger.debug(f"✅ Message delivered to {msg.topic()} [{msg.partition()}] @ offset {msg.offset()}")

def publish_event(event: dict, topic: str = None) -> bool:
    """
    Publish an event to Kafka (asynchronous with callback)
    
    Args:
        event: Dictionary containing event data
        topic: Kafka topic to publish to (defaults to KAFKA_TOPIC_NUTRITION_EVENTS)
    
    Returns:
        bool: True if successful, False otherwise
    """
    if not ENABLE_KAFKA:
        logger.debug("Kafka disabled, skipping event publishing")
        return True
        
    try:
        producer = get_producer()
        
        if producer is None:
            logger.error("Kafka producer not initialized")
            return False
        
        # Use default topic if not specified
        if topic is None:
            topic = KAFKA_TOPIC_NUTRITION_EVENTS
        
        # Enrich event with metadata
        _enrich_event(event)
        
        # Generate key for partitioning
        key = _generate_key(event)
        
        logger.debug(f"📤 Publishing event '{event.get('event')}' to topic '{topic}'")
        
        # Send to Kafka (asynchronous with callback)
        producer.produce(
            topic=topic,
            key=key,
            value=json.dumps(event),
            callback=delivery_callback
        )
        
        # Poll for delivery reports (non-blocking)
        producer.poll(0)
        
        logger.info(f"✅ Event queued for publishing: {event.get('event')} (user: {event.get('user_id', 'system')})")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to publish event to Kafka: {e}")
        return False

def _enrich_event(event: dict):
    """Add metadata to event"""
    if 'timestamp' not in event:
        event['timestamp'] = datetime.utcnow().isoformat() + 'Z'
    
    if 'service' not in event:
        event['service'] = 'nutrition-form'
    
    if 'version' not in event:
        event['version'] = '1.0'
    
    if 'correlation_id' not in event:
        event['correlation_id'] = str(uuid.uuid4())

def _generate_key(event: dict) -> str:
    """Generate key for Kafka partitioning"""
    user_id = event.get('user_id')
    if user_id:
        return f"user_{user_id}"
    
    return event.get('correlation_id', event.get('service', 'system'))

def shutdown_kafka():
    """Shutdown Kafka producer gracefully"""
    global _producer
    if _producer:
        try:
            logger.info("🛑 Flushing Kafka producer...")
            _producer.flush(timeout=10)
            logger.info("✅ Kafka producer flushed and closed")
        except Exception as e:
            logger.error(f"❌ Error flushing Kafka producer: {e}")
        finally:
            _producer = None

def ensure_kafka_ready():
    """Ensure Kafka is ready before starting the application"""
    if not ENABLE_KAFKA:
        logger.info("✅ Kafka is disabled, skipping health check")
        return True
        
    try:
        get_producer()
        logger.info("✅ Kafka is ready")
        return True
    except Exception as e:
        logger.warning(f"⚠️ Kafka not ready: {e}")
        return False