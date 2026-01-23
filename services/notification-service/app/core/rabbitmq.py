import json
import time
import pika

from app.core.config import (
    RABBITMQ_URL, RABBITMQ_QUEUE, RABBITMQ_PREFETCH, CONSUMER_RETRY_SECONDS
)
from app.core.logger import get_logger
from app.schemas.notification_event import NotificationEvent
from app.services.notification_service import NotificationService

log = get_logger("rabbitmq-consumer")

def _process_message(body: bytes) -> None:
    data = json.loads(body.decode("utf-8"))
    event = NotificationEvent(**data)
    NotificationService.handle_event(event)

def start_consumer_forever() -> None:
    """
    Robust consumer:
    - reconnect loop if RabbitMQ is not ready
    - manual ack
    Strategy:
    - If payload is invalid/unparseable => NACK requeue (producer bug or transient)
    - If processing fails (SMTP/MQTT) => ACK to avoid infinite requeue loops
    """
    while True:
        try:
            params = pika.URLParameters(RABBITMQ_URL)
            connection = pika.BlockingConnection(params)
            channel = connection.channel()

            channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
            channel.basic_qos(prefetch_count=RABBITMQ_PREFETCH)

            log.info("Consuming RabbitMQ queue=%s", RABBITMQ_QUEUE)

            def callback(ch, method, properties, body):
                try:
                    _process_message(body)
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                except (json.JSONDecodeError, ValueError, TypeError) as e:
                    log.exception("Invalid message format; requeueing. error=%s", str(e))
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
                except Exception as e:
                    # Do not requeue forever on SMTP/MQTT failures
                    log.exception("Processing failed; ACK to avoid infinite loop. error=%s", str(e))
                    ch.basic_ack(delivery_tag=method.delivery_tag)

            channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback)
            channel.start_consuming()

        except Exception as e:
            log.error("RabbitMQ consumer error: %s. Retrying in %ss", str(e), CONSUMER_RETRY_SECONDS)
            time.sleep(CONSUMER_RETRY_SECONDS)
