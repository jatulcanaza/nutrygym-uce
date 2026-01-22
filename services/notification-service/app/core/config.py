import os

def _required(name: str) -> str:
    val = os.getenv(name)
    if not val:
        raise RuntimeError(f"Missing required env var: {name}")
    return val

# Service
SERVICE_NAME = os.getenv("SERVICE_NAME", "notification-service")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# RabbitMQ
RABBITMQ_URL = _required("RABBITMQ_URL")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "notifications.queue")
RABBITMQ_PREFETCH = int(os.getenv("RABBITMQ_PREFETCH", "20"))

# MQTT
MQTT_HOST = _required("MQTT_HOST")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "nutrygym/notifications")
MQTT_QOS = int(os.getenv("MQTT_QOS", "0"))

# SMTP
SMTP_HOST = _required("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = _required("SMTP_USER")
SMTP_PASS = _required("SMTP_PASS")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER)
SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "true").lower() == "true"

# Runtime behavior
CONSUMER_RETRY_SECONDS = int(os.getenv("CONSUMER_RETRY_SECONDS", "5"))
MAX_EMAIL_BODY_CHARS = int(os.getenv("MAX_EMAIL_BODY_CHARS", "8000"))
