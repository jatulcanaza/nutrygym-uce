from app.core.logger import get_logger
from app.core.email_client import send_email
from app.core.mqtt_client import publish
from app.core.config import (
    MQTT_TOPIC,
    ADMIN_EMAIL,
    SEND_USER_EMAILS,
    SEND_ADMIN_ALERTS,
    ADMIN_ALERT_SEVERITIES,
)
from app.schemas.notification_event import NotificationEvent

log = get_logger("notification-service")

class NotificationService:
    @staticmethod
    def _build_email_subject(event: NotificationEvent) -> str:
        sev = (event.severity or "info").upper()
        src = event.source_service or "unknown"
        return f"[{sev}] {event.title} ({src})"

    @staticmethod
    def _build_email_body(event: NotificationEvent) -> str:
        lines = [
            f"Title: {event.title}",
            f"Severity: {event.severity}",
            f"Source: {event.source_service}",
            "",
            event.message or "",
            "",
        ]
        if event.meta:
            lines.append("Meta:")
            for k, v in event.meta.items():
                lines.append(f"- {k}: {v}")
        return "\n".join(lines)

    @staticmethod
    def handle_event(event: NotificationEvent) -> None:
        """
        Behavior:
        1) Always publish to MQTT (dashboard)
        2) Email routing:
           - If event.email is present -> send to user (if enabled)
           - Else -> send to ADMIN_EMAIL for warning/error severities (if enabled)
           - event.type can remain "alert" (no need to force "email")
        """
        log.info(
            "Handling event type=%s title=%s source=%s severity=%s email=%s",
            event.type, event.title, event.source_service, event.severity, event.email
        )

        # 1) MQTT (always)
        publish(
            topic=MQTT_TOPIC,
            payload=event.model_dump()
        )

        # 2) Email routing
        severity = (event.severity or "info").lower()
        subject = NotificationService._build_email_subject(event)
        body = NotificationService._build_email_body(event)

        # 2.1) User email (if provided)
        if event.email:
            if SEND_USER_EMAILS:
                send_email(to=str(event.email), subject=subject, body=body)
            else:
                log.info("User email present but SEND_USER_EMAILS=false. Skipping user email.")
            return

        # 2.2) Admin email for alerts
        if SEND_ADMIN_ALERTS and ADMIN_EMAIL and severity in ADMIN_ALERT_SEVERITIES:
            send_email(to=str(ADMIN_EMAIL), subject=subject, body=body)
        else:
            log.info(
                "Admin email skipped (enabled=%s admin_email_set=%s severity=%s rule=%s).",
                SEND_ADMIN_ALERTS, bool(ADMIN_EMAIL), severity, ",".join(sorted(ADMIN_ALERT_SEVERITIES))
            )
