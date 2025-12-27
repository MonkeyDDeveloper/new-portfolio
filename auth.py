"""
Sistema de autenticación con JWT y whitelist de IPs
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from config import settings
from database import get_db, Client

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer(auto_error=False)


def get_whitelisted_ips() -> set:
    """Obtener conjunto de IPs en whitelist"""
    return set(ip.strip() for ip in settings.WHITELISTED_IPS.split(",") if ip.strip())


def get_client_ip(request: Request) -> str:
    """Obtener IP del cliente considerando proxies"""
    # Verificar headers de proxy
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip.strip()
    
    return request.client.host if request.client else "unknown"


def is_ip_whitelisted(request: Request) -> bool:
    """Verificar si la IP está en la whitelist"""
    client_ip = get_client_ip(request)
    whitelisted = get_whitelisted_ips()
    return client_ip in whitelisted


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar contraseña"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generar hash de contraseña"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Crear token JWT"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    """Decodificar y validar token JWT"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None


def authenticate_client(db: Session, client_id: str, client_secret: str) -> Optional[Client]:
    """Autenticar cliente con credenciales"""
    client = db.query(Client).filter(Client.client_id == client_id).first()
    if not client:
        return None
    if not client.is_active:
        return None
    if not verify_password(client_secret, client.client_secret_hash):
        return None
    return client


async def get_current_client_or_whitelisted(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[dict]:
    """
    Dependency que permite acceso si:
    1. La IP está en whitelist, O
    2. Se proporciona un token válido
    
    Retorna información del cliente o None si es acceso por whitelist
    """
    # Primero verificar whitelist
    if is_ip_whitelisted(request):
        return {"access_type": "whitelist", "ip": get_client_ip(request)}
    
    # Si no está en whitelist, requiere token
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Se requiere autenticación. Proporcione un token válido o acceda desde una IP autorizada.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    payload = decode_token(credentials.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    client_id = payload.get("sub")
    if not client_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido: no contiene identificador de cliente",
        )
    
    # Verificar que el cliente existe y está activo
    client = db.query(Client).filter(Client.client_id == client_id).first()
    if not client or not client.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cliente no encontrado o inactivo",
        )
    
    return {"access_type": "token", "client_id": client_id, "client_name": client.name}


async def require_token_auth(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    db: Session = Depends(get_db)
) -> dict:
    """
    Dependency que SIEMPRE requiere token (ignora whitelist)
    Útil para endpoints sensibles como crear/eliminar clientes
    """
    payload = decode_token(credentials.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    client_id = payload.get("sub")
    client = db.query(Client).filter(Client.client_id == client_id).first()
    if not client or not client.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cliente no encontrado o inactivo",
        )
    
    return {"client_id": client_id, "client_name": client.name}
