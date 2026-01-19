# app/models/meal_plan.py
from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.sql import func
from app.core.database import Base
import uuid

class MealPlan(Base):
    __tablename__ = "meal_plans"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, index=True, nullable=False)

    # Campos nutricionales
    calories = Column(Integer, nullable=False)
    protein = Column(Integer, nullable=False)
    carbs = Column(Integer, nullable=False)
    fats = Column(Integer, nullable=False)
    
    # Metadata
    title = Column(String, default="Mi Plan Alimenticio")
    description = Column(String, nullable=True)
    
    # Estado y versión
    status = Column(String, default="draft")  # draft, active, archived
    version = Column(Integer, default=1)
    is_current = Column(Boolean, default=False)  # Para saber cuál es el plan activo
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())  # NUEVO