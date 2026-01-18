from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.authorization import router as authorization_router
from dotenv import load_dotenv
import os

app = FastAPI(
    title="Authorization Service",
    description="Access control service for NutriGym platform",
    version="1.0.0"
)

# ---- CORS (permite llamadas desde el frontend Vite) ----
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authorization_router)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "authorization-service"
    }
