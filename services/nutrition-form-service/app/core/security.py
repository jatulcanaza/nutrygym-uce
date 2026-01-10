from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
import os

security = HTTPBearer()
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return {
            "user_id": payload.get("sub"),
            "email": payload.get("email"),
            "role": payload.get("role")
        }
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
