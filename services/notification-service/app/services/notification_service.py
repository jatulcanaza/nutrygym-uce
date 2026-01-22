from app.core.logger import get_logger
from app.core.email_client import send_email
from app.core.mqtt_client import publish
from app.core.config import MQTT_TOPIC
from app.schemas.notification_event import NotificationEvent

log = get_logger("notification-service")

class NotificationService:
    @staticmethod
    def handle_event(event: NotificationEvent) -> None:
        """
        Regla simple:
        - Si type=email y hay email => enviar email
        - Siempre publicar a MQTT para dashboard
        """
        log.info(
            "Handling event type=%s title=%s source=%s severity=%s",
            event.type, event.title, event.source_service, event.severity
        )

        # 1) Email
        if event.type == "email":
            if not event.email:
                log.warning("Email event received but missing email field. Skipping email send.")
            else:
                send_email(
                    to=str(event.email),
                    subject=event.title,
                    body=event.message
                )

        # 2) MQTT
        publish(
            topic=MQTT_TOPIC,
            payload=event.model_dump()
        )
