import os
from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", "3012"))

MQTT_HOST = os.getenv("MQTT_HOST", "mosquitto")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "nutrygym/notifications")

MQTT_USERNAME = os.getenv("MQTT_USERNAME", "").strip() or None
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "").strip() or None

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
