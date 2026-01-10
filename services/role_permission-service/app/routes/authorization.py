from fastapi import APIRouter, Depends, Query
from app.core.security import get_current_user

router = APIRouter(
    prefix="/authorize",
    tags=["Authorization"]
)

@router.get("/check")
def check_access(
    required_role: str = Query(..., description="Required role: ADMIN or ESTUDIANTE"),
    current_user: dict = Depends(get_current_user)
):
    # Normalizar (mayúsculas)
    user_role = current_user.get("role", "ESTUDIANTE").upper()
    required_role_upper = required_role.upper()
    
    # Solo permitir ADMIN o ESTUDIANTE
    if required_role_upper not in ["ADMIN", "ESTUDIANTE"]:
        return {
            "error": "Invalid role",
            "allowed_roles": ["ADMIN", "ESTUDIANTE"]
        }
    
    is_allowed = user_role == required_role_upper
    
    return {
        "user_id": current_user.get("user_id"),
        "email": current_user.get("email"),
        "user_role": user_role,
        "required_role": required_role_upper,
        "allowed": is_allowed,
        "message": "✅ Access granted" if is_allowed else f"❌ Access denied. Your role: {user_role}"
    }

@router.get("/my-role")
def get_my_role(current_user: dict = Depends(get_current_user)):
    """Endpoint para que el usuario vea su rol"""
    return {
        "user_id": current_user.get("user_id"),
        "email": current_user.get("email"),
        "role": current_user.get("role", "ESTUDIANTE"),
        "is_admin": current_user.get("role") == "ADMIN"
    }