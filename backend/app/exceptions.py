"""
Excepciones personalizadas para la aplicación.

Define excepciones específicas del dominio de traducción Braille,
permitiendo mejor manejo de errores y respuestas HTTP coherentes.

Jerarquía de Excepciones:
    BrailleException (base)
    ├── TranslationError: Error en traducción
    ├── ValidationError: Error en validación de entrada
    ├── GenerationError: Error en generación de imágenes/PDFs
    └── InternalError: Error interno del servidor

Uso:
    from app.exceptions import TranslationError, ValidationError
    
    try:
        result = translate(text)
    except ValidationError as e:
        logger.warning(f"Validación fallida: {e}")
    except TranslationError as e:
        logger.error(f"Error en traducción: {e}")
"""


class BrailleException(Exception):
    """Excepción base para todas las excepciones de la aplicación."""
    
    def __init__(self, message: str, code: str = "INTERNAL_ERROR", status_code: int = 500):
        """
        Inicializa la excepción.
        
        Args:
            message (str): Mensaje de error descriptivo
            code (str): Código de error interno (para debugging)
            status_code (int): Código HTTP correspondiente
        """
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)


class ValidationError(BrailleException):
    """Error en validación de entrada (400 Bad Request)."""
    
    def __init__(self, message: str, code: str = "VALIDATION_ERROR"):
        super().__init__(message, code, status_code=400)


class TranslationError(BrailleException):
    """Error durante la traducción Braille."""
    
    def __init__(self, message: str, code: str = "TRANSLATION_ERROR"):
        super().__init__(message, code, status_code=500)


class GenerationError(BrailleException):
    """Error durante la generación de imágenes o PDFs."""
    
    def __init__(self, message: str, code: str = "GENERATION_ERROR"):
        super().__init__(message, code, status_code=500)


class InternalError(BrailleException):
    """Error interno del servidor."""
    
    def __init__(self, message: str, code: str = "INTERNAL_ERROR"):
        super().__init__(message, code, status_code=500)
