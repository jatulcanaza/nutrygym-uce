# app/schemas/nutrition_form.py
from pydantic import BaseModel, field_validator
from typing import List

class NutritionFormCreate(BaseModel):
    meals_per_day: int
    diet_type: str
    allergies: List[str]
    preferences: List[str]
    caloric_goal: int
    water_intake: float


class NutritionFormResponse(BaseModel):
    id: str
    user_id: str
    meals_per_day: int
    diet_type: str
    allergies: List[str]
    preferences: List[str]
    caloric_goal: int
    water_intake: float
    
    @field_validator('allergies', 'preferences', mode='before')
    @classmethod
    def split_string_to_list(cls, v):
        """Convierte string separado por comas a lista"""
        if isinstance(v, str):
            if v.strip() == "":
                return []
            return [item.strip() for item in v.split(',') if item.strip()]
        return v