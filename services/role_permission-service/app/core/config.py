import os

JWT_SECRET_KEY = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
SERVICE_NAME = os.getenv("SERVICE_NAME", "authorization-service")
