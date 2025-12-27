"""
Router de autenticación
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import timedelta

from database import get_db, Client
from schemas import TokenRequest, Token, ClientCreate, ClientResponse, MessageResponse
from auth import (
    authenticate_client,
    create_access_token,
    get_password_hash,
    require_token_auth,
    get_client_ip,
    is_ip_whitelisted,
    get_whitelisted_ips,
)
from config import settings

router = APIRouter()


@router.post("/token", response_model=Token, summary="Obtener token de acceso")
async def get_token(credentials: TokenRequest, db: Session = Depends(get_db)):
    """
    Obtener un token de acceso usando client_id y client_secret.
    
    El token tiene una validez configurable (por defecto 30 minutos).
    """
    client = authenticate_client(db, credentials.client_id, credentials.client_secret)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": client.client_id, "name": client.name},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post("/clients", response_model=ClientResponse, status_code=status.HTTP_201_CREATED, summary="Crear nuevo cliente")
async def create_client(
    client_data: ClientCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_token_auth)  # Solo usuarios autenticados pueden crear clientes
):
    """
    Crear un nuevo cliente de la API.
    
    Requiere autenticación con token (no se permite whitelist para esta operación).
    """
    # Verificar si ya existe
    existing = db.query(Client).filter(Client.client_id == client_data.client_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un cliente con ese client_id"
        )
    
    new_client = Client(
        client_id=client_data.client_id,
        client_secret_hash=get_password_hash(client_data.client_secret),
        name=client_data.name
    )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    
    return new_client


@router.post("/clients/seed", response_model=ClientResponse, status_code=status.HTTP_201_CREATED, summary="Crear cliente inicial (solo si no hay clientes)")
async def seed_initial_client(client_data: ClientCreate, db: Session = Depends(get_db)):
    """
    Crear el primer cliente de la API.
    
    Este endpoint solo funciona si no existe ningún cliente en la base de datos.
    Útil para configuración inicial.
    """
    # Solo permitir si no hay clientes
    client_count = db.query(Client).count()
    if client_count > 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ya existen clientes. Use el endpoint /auth/clients con autenticación."
        )
    
    new_client = Client(
        client_id=client_data.client_id,
        client_secret_hash=get_password_hash(client_data.client_secret),
        name=client_data.name
    )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    
    return new_client


@router.get("/me", summary="Información del acceso actual")
async def get_current_access_info(request: Request):
    """
    Obtener información sobre el tipo de acceso actual.
    
    Muestra si el acceso es por token o por whitelist de IP.
    """
    client_ip = get_client_ip(request)
    is_whitelisted = is_ip_whitelisted(request)
    
    return {
        "client_ip": client_ip,
        "is_whitelisted": is_whitelisted,
        "whitelisted_ips": list(get_whitelisted_ips()),
        "message": "IP en whitelist - no requiere token" if is_whitelisted else "Requiere token de autenticación"
    }


@router.delete("/clients/{client_id}", response_model=MessageResponse, summary="Desactivar cliente")
async def deactivate_client(
    client_id: str,
    db: Session = Depends(get_db),
    current: dict = Depends(require_token_auth)
):
    """
    Desactivar un cliente de la API.
    
    Requiere autenticación con token. No se puede desactivar a uno mismo.
    """
    if current["client_id"] == client_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes desactivarte a ti mismo"
        )
    
    client = db.query(Client).filter(Client.client_id == client_id).first()
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )
    
    client.is_active = False
    db.commit()
    
    return MessageResponse(message="Cliente desactivado exitosamente")
