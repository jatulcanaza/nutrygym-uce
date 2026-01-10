# app/routes/auth.py - VERSIÓN COMPLETA CORREGIDA
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, validator, Field
import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
import bcrypt
import hashlib
from uuid import UUID

from app.core.database import get_db
from app.models.user import UserDB

router = APIRouter()

# Configuración
SECRET_KEY = os.getenv("JWT_SECRET")
if not SECRET_KEY:
    raise ValueError("❌ JWT_SECRET no está configurado en .env")

ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
ALLOWED_DOMAIN = os.getenv("ALLOWED_EMAIL_DOMAIN", "uce.edu.ec")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ========= SCHEMAS CORREGIDOS =========
class UserRegister(BaseModel):
    email: str
    password: str
    name: str
    
    @validator('email')
    def validate_email_domain(cls, v):
        if not v.endswith(f"@{ALLOWED_DOMAIN}"):
            raise ValueError(f"Solo se permiten emails @{ALLOWED_DOMAIN}")
        return v
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")
        return v

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    is_active: bool
    created_at: datetime
    
    @validator('id', pre=True)
    def convert_uuid_to_str(cls, v):
        """Convierte UUID a string si es necesario"""
        if isinstance(v, UUID):
            return str(v)
        return v
    
    class Config:
        from_attributes = True
        json_encoders = {
            UUID: str  # Asegura que UUID se serialice como string
        }

# ========= FUNCIONES DE UTILIDAD =========
def hash_password_safely(password: str) -> str:
    """Hash seguro para bcrypt con manejo de passwords largos"""
    password_bytes = password.encode('utf-8')
    
    if len(password_bytes) > 72:
        sha256_hash = hashlib.sha256(password_bytes).hexdigest()
        password_bytes = sha256_hash.encode('utf-8')
    
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password_safely(plain_password: str, hashed_password: str) -> bool:
    """Verificación segura de password"""
    try:
        if isinstance(hashed_password, str):
            hashed_bytes = hashed_password.encode('utf-8')
        else:
            hashed_bytes = hashed_password
        
        plain_bytes = plain_password.encode('utf-8')
        
        # Método 1: Con SHA-256 si es largo
        if len(plain_bytes) > 72:
            sha256_hash = hashlib.sha256(plain_bytes).hexdigest()
            sha256_bytes = sha256_hash.encode('utf-8')
            if bcrypt.checkpw(sha256_bytes, hashed_bytes):
                return True
        
        # Método 2: Con truncamiento
        if len(plain_bytes) > 72:
            truncated = plain_bytes[:72]
            if bcrypt.checkpw(truncated, hashed_bytes):
                return True
        else:
            if bcrypt.checkpw(plain_bytes, hashed_bytes):
                return True
        
        return False
        
    except Exception as e:
        print(f"Error en verify_password_safely: {e}")
        return False

# Alias para compatibilidad
get_password_hash = hash_password_safely
verify_password = verify_password_safely

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ========= RUTAS =========
@router.post("/register", response_model=UserResponse)
async def register(user: UserRegister, db: Session = Depends(get_db)):
    """Registrar nuevo usuario"""
    # Verificar si el usuario ya existe
    db_user = db.query(UserDB).filter(UserDB.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Validar dominio de email
    if not user.email.endswith(f"@{ALLOWED_DOMAIN}"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Solo se permiten emails @{ALLOWED_DOMAIN}"
        )
    
    # Validar longitud de password
    if len(user.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña debe tener al menos 6 caracteres"
        )
    
    # Crear nuevo usuario
    hashed_password = get_password_hash(user.password)
    db_user = UserDB(
        email=user.email,
        password_hash=hashed_password,
        name=user.name,
        is_active=True
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login de usuario"""
    # Validar dominio
    if not form_data.username.endswith(f"@{ALLOWED_DOMAIN}"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Solo se permiten emails @{ALLOWED_DOMAIN}"
        )
    
    # Buscar usuario
    user = db.query(UserDB).filter(UserDB.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    
    # Crear tokens
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=access_token_expires
    )
    
    refresh_token = create_refresh_token(
        data={"sub": str(user.id), "email": user.email}
    )
    
    # Guardar refresh token en la base de datos
    user.refresh_token = refresh_token
    db.commit()
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    """Refresh token"""
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
        
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
        
        # Verificar que el refresh token coincida con el almacenado
        user = db.query(UserDB).filter(UserDB.id == user_id).first()
        if not user or user.refresh_token != refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
        
        # Generar nuevos tokens
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        new_access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email},
            expires_delta=access_token_expires
        )
        
        new_refresh_token = create_refresh_token(
            data={"sub": str(user.id), "email": user.email}
        )
        
        # Actualizar refresh token en la base de datos
        user.refresh_token = new_refresh_token
        db.commit()
        
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )

@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Logout de usuario"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        
        if user_id:
            user = db.query(UserDB).filter(UserDB.id == user_id).first()
            if user:
                user.refresh_token = None
                db.commit()
        
        return {"message": "Logout exitoso"}
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

@router.get("/me", response_model=UserResponse)
async def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Obtener información del usuario actual"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas"
            )
        
        user = db.query(UserDB).filter(UserDB.id == user_id).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        return user
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )