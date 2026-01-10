from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.core.config import JWT_SECRET_KEY, JWT_ALGORITHM
import logging

logger = logging.getLogger(__name__)
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        # Decodificar token
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM]
        )
        
        user_id = payload.get("sub")
        email = payload.get("email")
        
        # ✅ LÓGICA SIMPLE DE 2 ROLES
        if not email:
            role = "ESTUDIANTE"  # Por defecto
        elif email == "admin@uce.edu.ec":
            role = "ADMIN"
        elif email.endswith("@uce.edu.ec"):
            role = "ESTUDIANTE"
        else:
            role = "ESTUDIANTE"  # Por defecto para otros emails
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found in token"
            )

        return {
            "user_id": user_id,
            "email": email,
            "role": role
        }

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )