from sqlalchemy import Column, String, Integer, Float
from app.core.database import Base
import uuid

class NutritionForm(Base):
    __tablename__ = "nutrition_forms"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)

    meals_per_day = Column(Integer)
    diet_type = Column(String)
    allergies = Column(String)
    preferences = Column(String)
    caloric_goal = Column(Integer)
    water_intake = Column(Float)
