import os

def _required(name: str) -> str:
    val = os.getenv(name)
    if not val:
        raise RuntimeError(f"Missing required env var: {name}")
    return val

def _bool(name: str, default: str = "true") -> bool:
    return os.getenv(name, default).lower() == "true"

def _csv(name: str, default: str = "") -> list[str]:
    raw = os.getenv(name, default)
    return [x.strip() for x in raw.split(",") if x.strip()]

# Service
SERVICE_NAME = os.getenv("SERVICE_NAME", "notification-service")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# RabbitMQ
RABBITMQ_URL = _required("RABBITMQ_URL")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "notifications.queue")
RABBITMQ_PREFETCH = int(os.getenv("RABBITMQ_PREFETCH", "20"))
CONSUMER_RETRY_SECONDS = int(os.getenv("CONSUMER_RETRY_SECONDS", "5"))

# MQTT
MQTT_HOST = _required("MQTT_HOST")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "nutrygym/notifications")
MQTT_QOS = int(os.getenv("MQTT_QOS", "0"))

# Optional MQTT auth (dashboard usually doesn't need it)
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")

# SMTP
SMTP_HOST = _required("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = _required("SMTP_USER")
SMTP_PASS = _required("SMTP_PASS")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER)
SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
MAX_EMAIL_BODY_CHARS = int(os.getenv("MAX_EMAIL_BODY_CHARS", "8000"))

# Email routing behavior
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "")
SEND_USER_EMAILS = _bool("SEND_USER_EMAILS", "true")
SEND_ADMIN_ALERTS = _bool("SEND_ADMIN_ALERTS", "true")
ADMIN_ALERT_SEVERITIES = set(s.lower() for s in _csv("ADMIN_ALERT_SEVERITIES", "warning,error"))
