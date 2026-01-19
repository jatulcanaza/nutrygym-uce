# app/schemas/meal_plan.py

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class MealPlanBase(BaseModel):
    calories: int = Field(..., ge=0)
    protein: int = Field(..., ge=0)
    carbs: int = Field(..., ge=0)
    fats: int = Field(..., ge=0)
    title: str = Field("Mi Plan Alimenticio", min_length=1)
    description: Optional[str] = None


class MealPlanCreate(MealPlanBase):
    user_id: str


# app/schemas/meal_plan.py

class MealPlanUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    calories: Optional[int] = Field(None, ge=0)
    protein: Optional[int] = Field(None, ge=0)
    carbs: Optional[int] = Field(None, ge=0)
    fats: Optional[int] = Field(None, ge=0)

    # ✅ ampliar estados
    status: Optional[str] = Field(None, pattern="^(draft|active|completed|canceled)$")


class MealPlanResponse(MealPlanBase):
    id: str
    user_id: str
    status: str
    version: int
    is_current: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
