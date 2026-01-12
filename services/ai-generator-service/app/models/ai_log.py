from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime

class AILog(BaseModel):
    """Modelo para registrar generaciones de IA"""
    user_id: str
    input: Dict[str, Any]
    output: Optional[str] = None
    error: Optional[str] = None
    created_at: datetime = datetime.utcnow()
    processing_time_ms: float = 0.0
    status: str  # "success" o "error"
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
