from pydantic import BaseModel, field_validator
from typing import List, Optional

class NutritionFormBase(BaseModel):
    meals_per_day: int
    diet_type: str
    allergies: List[str] = []
    preferences: List[str] = []
    caloric_goal: int
    water_intake: float

class NutritionFormCreate(NutritionFormBase):
    pass

class NutritionFormUpdate(BaseModel):
    meals_per_day: Optional[int] = None
    diet_type: Optional[str] = None
    allergies: Optional[List[str]] = None
    preferences: Optional[List[str]] = None
    caloric_goal: Optional[int] = None
    water_intake: Optional[float] = None

class NutritionFormResponse(BaseModel):
    id: str
    user_id: str
    meals_per_day: int
    diet_type: str
    allergies: List[str]
    preferences: List[str]
    caloric_goal: int
    water_intake: float

    @field_validator("allergies", "preferences", mode="before")
    @classmethod
    def split_string_to_list(cls, v):
        if isinstance(v, str):
            if v.strip() == "":
                return []
            return [item.strip() for item in v.split(",") if item.strip()]
        return v
