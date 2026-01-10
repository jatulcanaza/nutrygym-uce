# main.py
import os
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# =========================
# Cargar variables de entorno
# =========================
load_dotenv()

print("=" * 60)
print("🚀 AUTH SERVICE UCE - POSTGRESQL")
print("=" * 60)
print(f"📧 Dominio permitido: @{os.getenv('ALLOWED_EMAIL_DOMAIN', 'uce.edu.ec')}")
print(f"🗄️  Base de datos: {os.getenv('DB_NAME', 'auth_db')}")
print("=" * 60)

# =========================
# App FastAPI
# =========================
app = FastAPI(
    title="Auth Service UCE",
    description="Servicio de autenticación exclusivo para la Universidad Central del Ecuador",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
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

# =========================
# Startup: inicializar DB
# =========================
@app.on_event("startup")
def startup_event():
    try:
        from app.core.database import engine, Base
        from app.models.user import UserDB  # asegura que el modelo se registre

        Base.metadata.create_all(bind=engine)
        print("✅ Base de datos conectada y tablas verificadas")

    except Exception as e:
        print(f"❌ Error en startup DB: {e}")

# =========================
# Rutas
# =========================
from app.routes import auth, users

app.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
app.include_router(users.router, prefix="/users", tags=["Usuarios"])

# =========================
# Rutas base
# =========================
@app.get("/")
def root():
    return {
        "service": "Auth Service UCE",
        "version": "2.0.0",
        "description": "Autenticación exclusiva para @uce.edu.ec",
        "docs": "/docs",
        "health": "/health",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
def health_check():
    from app.core.database import engine
    from sqlalchemy import text

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "service": "auth-service",
            "database": "connected",
            "allowed_domain": f"@{os.getenv('ALLOWED_EMAIL_DOMAIN', 'uce.edu.ec')}",
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "auth-service",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

# =========================
# Solo para modo local
# =========================
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 3001)),
        reload=True  # SOLO modo local, Docker no entra aquí
    )
