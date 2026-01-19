from fastapi import FastAPI
from app.routes.meal_plan import router
from app.core.database import Base, engine
import os
import time
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Plan Management Service",
    version="1.0.0"
)
# =========================
# CORS
# =========================
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
