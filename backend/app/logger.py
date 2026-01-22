"""
Configuración de logging centralizado.

Este módulo configura logging estructurado para toda la aplicación.

Características:
    - Logs con niveles (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    - Formato consistente con timestamp y módulo
    - Rotación de archivos (si aplica)
    - Outputs: consola y archivo

Uso:
    from app.logger import get_logger
    
    logger = get_logger(__name__)
    logger.info("Mensaje informativo")
    logger.error("Error detectado", extra={"user_id": 123})
"""

import logging
import sys
from typing import Optional


def get_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    Obtiene un logger configurado para un módulo específico.
    
    Args:
        name (str): Nombre del logger (usualmente __name__)
        level (str, optional): Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        logging.Logger: Logger configurado
    
    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Aplicación iniciada")
    """
    logger = logging.getLogger(name)
    
    # Evitar agregar handlers múltiples
    if logger.hasHandlers():
        return logger
    
    # Configurar nivel
    if level:
        logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    else:
        logger.setLevel(logging.INFO)
    
    # Formato del log
    formatter = logging.Formatter(
        fmt='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


# Logger global de la aplicación
app_logger = get_logger("braille-translator")
