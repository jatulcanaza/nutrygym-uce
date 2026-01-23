from __future__ import annotations

import asyncio
import json
import logging
import threading
from typing import Set

import paho.mqtt.client as mqtt

from app.core.config import MQTT_HOST, MQTT_PORT, MQTT_TOPIC, MQTT_USERNAME, MQTT_PASSWORD, LOG_LEVEL

logger = logging.getLogger("mqtt-bridge")
logging.basicConfig(level=LOG_LEVEL)

# Set de websockets conectados (se registra en web.py)
WS_CLIENTS: Set["WebSocketLike"] = set()

# Cola thread-safe para pasar mensajes del thread MQTT al event loop
_message_queue: asyncio.Queue[str] | None = None
_loop: asyncio.AbstractEventLoop | None = None

_mqtt_client: mqtt.Client | None = None
_thread: threading.Thread | None = None
_stop_event = threading.Event()

class WebSocketLike:
    # typing helper; en runtime son fastapi.websockets.WebSocket
    async def send_text(self, data: str) -> None:
        ...

def _on_connect(client: mqtt.Client, userdata, flags, rc, properties=None):
    if rc == 0:
        logger.info(f"MQTT connected host={MQTT_HOST} port={MQTT_PORT} topic={MQTT_TOPIC}")
        client.subscribe(MQTT_TOPIC)
    else:
        logger.error(f"MQTT connect failed rc={rc}")

def _on_message(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
    payload = msg.payload.decode("utf-8", errors="replace")

    # Validación suave: si no es JSON igual lo mandamos
    try:
        obj = json.loads(payload)
        payload = json.dumps(obj, ensure_ascii=False)
    except Exception:
        pass

    if _loop and _message_queue:
        _loop.call_soon_threadsafe(_message_queue.put_nowait, payload)

async def _fanout_task():
    # corre dentro del event loop
    assert _message_queue is not None

    while not _stop_event.is_set():
        data = await _message_queue.get()
        dead = []
        for ws in list(WS_CLIENTS):
            try:
                await ws.send_text(data)
            except Exception:
                dead.append(ws)

        for ws in dead:
            WS_CLIENTS.discard(ws)

def _mqtt_thread_main():
    global _mqtt_client

    client = mqtt.Client()
    if MQTT_USERNAME and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

    client.on_connect = _on_connect
    client.on_message = _on_message

    # Reintentos automáticos
    client.reconnect_delay_set(min_delay=1, max_delay=10)

    _mqtt_client = client

    while not _stop_event.is_set():
        try:
            client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
            client.loop_forever()
        except Exception as e:
            logger.error(f"MQTT loop error: {e}. Retrying in 3s")
            try:
                client.loop_stop()
            except Exception:
                pass
            _stop_event.wait(3)

def start_mqtt_bridge():
    global _loop, _message_queue, _thread

    if _thread and _thread.is_alive():
        return

    _stop_event.clear()
    _loop = asyncio.get_event_loop()
    _message_queue = asyncio.Queue()

    # arrancar fanout en el loop
    asyncio.create_task(_fanout_task())

    # arrancar mqtt en thread
    _thread = threading.Thread(target=_mqtt_thread_main, daemon=True)
    _thread.start()

def stop_mqtt_bridge():
    _stop_event.set()
    try:
        if _mqtt_client:
            _mqtt_client.loop_stop()
            _mqtt_client.disconnect()
    except Exception:
        pass
