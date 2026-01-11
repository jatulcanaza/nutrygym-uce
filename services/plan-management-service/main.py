from fastapi import FastAPI
from app.routes.meal_plan import router
from app.core.database import Base, engine
import os
import time

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Plan Management Service",
    version="1.0.0"
)

app.include_router(router)

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "plan-management",
        "timestamp": time.time(),
        "environment": os.getenv("ENVIRONMENT")
    }
