from fastapi import FastAPI
from app.routes.authorization import router as authorization_router

app = FastAPI(
    title="Authorization Service",
    description="Access control service for NutriGym platform",
    version="1.0.0"
)

app.include_router(authorization_router)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "authorization-service"
    }
