"""
Configuración centralizada de la aplicación.

Este módulo contiene todas las variables de configuración utilizadas
en la aplicación, permitiendo fácil mantenimiento y cambios de ambiente.

Características:
    - Configuración por ambiente (development, production, testing)
    - Variables de entorno para valores sensibles
    - Valores por defecto seguros
    - Validación básica de configuración

Uso:
    from app.config import Settings
    settings = Settings()
    
    # Acceder a configuraciones
    DEBUG = settings.debug
    CORS_ORIGINS = settings.cors_origins
"""

from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    Configuración centralizada de la aplicación.
    
    Lee variables de .env y proporciona valores por defecto seguros.
    """
    
    # Básico
    app_name: str = Field(default="Braille Translator API", description="Nombre de la aplicación")
    app_version: str = Field(default="1.0.0", description="Versión de la aplicación")
    environment: str = Field(default="development", description="Ambiente (development, production, testing)")
    debug: bool = Field(default=False, description="Modo debug")
    
    # API
    api_prefix: str = Field(default="/api/v1", description="Prefijo de rutas de API")
    host: str = Field(default="0.0.0.0", description="Host para el servidor")
    port: int = Field(default=8000, description="Puerto para el servidor")
    
    # CORS
    cors_origins: List[str] = Field(
        default=[
            "http://localhost",
            "http://localhost:3000",
            "http://localhost:5173",
        ],
        description="Orígenes permitidos para CORS"
    )
    cors_allow_credentials: bool = Field(default=True, description="Permitir credenciales en CORS")
    cors_allow_methods: List[str] = Field(default=["*"], description="Métodos permitidos en CORS")
    cors_allow_headers: List[str] = Field(default=["*"], description="Headers permitidos en CORS")
    
    # Logging
    log_level: str = Field(default="INFO", description="Nivel de logging")
    
    # Límites
    max_text_length: int = Field(default=10000, description="Longitud máxima de texto a traducir")
    max_braille_cells: int = Field(default=10000, description="Máximo de celdas Braille a procesar")
    
    class Config:
        """Configuración de Pydantic Settings."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Instancia global de configuración
settings = Settings()
