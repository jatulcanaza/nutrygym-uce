import json
import time
import paho.mqtt.client as mqtt

from app.core.config import MQTT_HOST, MQTT_PORT, MQTT_QOS
from app.core.logger import get_logger

log = get_logger("mqtt-client")

_client: mqtt.Client | None = None
_connected: bool = False

def _on_connect(client, userdata, flags, reason_code, properties=None):
    # paho-mqtt v2 usa reason_code (int-like)
    global _connected
    try:
        rc = int(reason_code)
    except Exception:
        rc = 1

    if rc == 0:
        _connected = True
        log.info("MQTT connected host=%s port=%s", MQTT_HOST, MQTT_PORT)
    else:
        _connected = False
        log.error("MQTT connection failed rc=%s", rc)

def _on_disconnect(client, userdata, reason_code, properties=None):
    global _connected
    _connected = False
    try:
        rc = int(reason_code)
    except Exception:
        rc = None
    log.warning("MQTT disconnected rc=%s", rc)

def _get_client() -> mqtt.Client:
    global _client
    if _client:
        return _client

    client = mqtt.Client()
    client.on_connect = _on_connect
    client.on_disconnect = _on_disconnect

    # Conecta en modo bloqueante (más confiable para demo)
    try:
        client.connect(MQTT_HOST, MQTT_PORT, keepalive=30)
    except Exception as e:
        log.error("MQTT connect error: %s", str(e))

    client.loop_start()
    _client = client
    return client

def publish(topic: str, payload: dict) -> None:
    client = _get_client()

    # Espera hasta 10s para conexión real
    start = time.time()
    while not _connected and (time.time() - start) < 10:
        time.sleep(0.1)

    if not _connected:
        log.error("MQTT not connected; cannot publish topic=%s", topic)
        return

    data = json.dumps(payload, ensure_ascii=False)
    info = client.publish(topic, data, qos=MQTT_QOS)

    # wait_for_publish ayuda a confirmar envío
    try:
        info.wait_for_publish(timeout=3)
    except Exception:
        pass

    if info.rc != 0:
        log.warning("MQTT publish non-zero rc=%s topic=%s", info.rc, topic)
    else:
        log.info("MQTT published topic=%s", topic)
