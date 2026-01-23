from typing import Any, Dict, Optional, Literal
from pydantic import BaseModel, EmailStr, Field

NotificationType = Literal["email", "alert", "system"]

class NotificationEvent(BaseModel):
    """
    Contrato de evento entrante desde RabbitMQ.
    """
    type: NotificationType = Field(default="system")
    title: str = Field(min_length=1, max_length=200)
    message: str = Field(min_length=1, max_length=20000)

    # Email
    email: Optional[EmailStr] = None

    # Metadata (opcional)
    source_service: Optional[str] = None
    severity: Optional[Literal["info", "warning", "error"]] = "info"
    meta: Dict[str, Any] = Field(default_factory=dict)
