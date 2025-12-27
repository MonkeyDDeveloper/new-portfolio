"""
Configuración de la aplicación
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Base de datos
    DATABASE_URL: str = "sqlite:///./app.db"
    
    # JWT
    SECRET_KEY: str = "tu-clave-secreta-muy-segura-cambiar-en-produccion"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # IPs permitidas sin autenticación (separadas por coma)
    WHITELISTED_IPS: str = "127.0.0.1,192.168.1.100"
    
    # Puerto del servidor (Seenode requiere especificarlo)
    PORT: int = 8000
    
    # Entorno
    ENVIRONMENT: str = "development"
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
