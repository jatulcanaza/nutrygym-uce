# app/models/nutrition_form.py
from sqlalchemy import Column, String, Integer, Float
from app.core.database import Base
import uuid

class NutritionForm(Base):
    __tablename__ = "nutrition_forms"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)

    meals_per_day = Column(Integer, nullable=False)
    diet_type = Column(String, nullable=False)

    allergies = Column(String, default="", nullable=False)     # guardas CSV
    preferences = Column(String, default="", nullable=False)   # guardas CSV

    caloric_goal = Column(Integer, nullable=False)
    water_intake = Column(Float, nullable=False)
