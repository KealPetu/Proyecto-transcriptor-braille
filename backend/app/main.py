"""
Punto de entrada principal de la aplicación FastAPI.

Configura:
    - Middleware CORS
    - Rutas de API
    - Handlers de excepciones
    - Documentación OpenAPI

Estructura:
    GET  /                          → Información de la API
    GET  /docs                      → Documentación interactiva (Swagger)
    GET  /redoc                     → Documentación ReDoc
    
    POST /api/v1/translation/to-braille       → Español → Braille
    POST /api/v1/translation/to-text          → Braille → Español
    POST /api/v1/generation/image             → Generar PNG
    POST /api/v1/generation/pdf               → Generar PDF
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.logger import app_logger
from app.exceptions import BrailleException
from app.api.routes import translation, generation


def create_app() -> FastAPI:
    """
    Factory para crear la aplicación FastAPI.
    
    Returns:
        FastAPI: Aplicación configurada
    """
    # Crear aplicación
    app = FastAPI(
        title=settings.app_name,
        description="API profesional para traducción bidireccional Español ↔ Braille con generación de materiales visuales",
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
    
    # Middleware CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )
    
    # Handler de excepciones personalizado
    @app.exception_handler(BrailleException)
    async def braille_exception_handler(request, exc: BrailleException):
        """Maneja excepciones personalizadas de la aplicación."""
        app_logger.error(f"Error [{exc.code}]: {exc.message}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.code,
                "message": exc.message,
                "status_code": exc.status_code
            }
        )
    
    # Incluir routers de API
    app.include_router(
        translation.router,
        prefix=f"{settings.api_prefix}/translation",
        tags=["Translation"]
    )
    app.include_router(
        generation.router,
        prefix=f"{settings.api_prefix}/generation",
        tags=["Generation"]
    )
    
    # Rutas de salud
    @app.get("/", tags=["Health"])
    def health_check():
        """Verifica que la API está operativa."""
        return {
            "status": "healthy",
            "application": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment
        }
    
    @app.get("/health", tags=["Health"])
    def health_detailed():
        """Información detallada de salud."""
        return {
            "status": "operational",
            "app_name": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment,
            "features": {
                "translation": "Español ↔ Braille",
                "image_generation": "PNG",
                "pdf_generation": "PDF A4"
            }
        }
    
    # Log de inicialización
    app_logger.info(f"Aplicación iniciada: {settings.app_name} v{settings.app_version}")
    app_logger.info(f"Ambiente: {settings.environment}")
    
    return app


# Crear instancia global
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )