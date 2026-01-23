import json
import os
import time
from typing import Any, Dict, Optional

import pika


RABBITMQ_URL = os.getenv("RABBITMQ_URL", "")
NOTIF_QUEUE = os.getenv("NOTIF_QUEUE", "notifications.queue")
PUBLISH_RETRIES = int(os.getenv("NOTIF_PUBLISH_RETRIES", "3"))
PUBLISH_RETRY_DELAY = float(os.getenv("NOTIF_PUBLISH_RETRY_DELAY", "0.5"))


def publish_notification(event: Dict[str, Any]) -> bool:
    """
    Publishes a notification event to RabbitMQ.
    Returns True if published, False otherwise.

    Notes:
    - If RABBITMQ_URL is not set, it fails gracefully (does not break the API).
    - Retries are small to avoid delaying requests too much.
    """
    if not RABBITMQ_URL:
        return False

    body = json.dumps(event, ensure_ascii=False).encode("utf-8")

    last_error: Optional[Exception] = None
    for _ in range(PUBLISH_RETRIES):
        try:
            params = pika.URLParameters(RABBITMQ_URL)
            params.socket_timeout = 3
            params.connection_attempts = 1
            params.retry_delay = 0

            conn = pika.BlockingConnection(params)
            ch = conn.channel()
            ch.queue_declare(queue=NOTIF_QUEUE, durable=True)

            ch.basic_publish(
                exchange="",
                routing_key=NOTIF_QUEUE,
                body=body,
                properties=pika.BasicProperties(
                    delivery_mode=2  # persistent message
                ),
            )

            conn.close()
            return True

        except Exception as e:
            last_error = e
            time.sleep(PUBLISH_RETRY_DELAY)

    # Si quieres loguear el error, hazlo donde lo llames (para no acoplar logger aquí).
    return False
