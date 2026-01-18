from pydantic import BaseModel
from datetime import date
from uuid import UUID

class ProfileCreate(BaseModel):
    first_name: str
    last_name: str
    birth_date: date | None = None
    gender: str | None = None
    height_cm: float | None = None
    weight_kg: float | None = None
    goal: str | None = None
    activity_level: str | None = None


# Para UPDATE: todo opcional (permite editar parcialmente)
class ProfileUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    birth_date: date | None = None
    gender: str | None = None
    height_cm: float | None = None
    weight_kg: float | None = None
    goal: str | None = None
    activity_level: str | None = None


class ProfileResponse(ProfileCreate):
    id: UUID
    user_id: UUID

    class Config:
        from_attributes = True
