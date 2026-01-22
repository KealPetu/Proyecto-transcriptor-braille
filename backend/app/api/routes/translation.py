"""
Rutas de API para traducción Braille bidireccional.

Endpoints:
    POST /to-braille: Español → Braille (transcripción)
    POST /to-text: Braille → Español (traducción inversa)

Respuestas:
    - Format: JSON con metadata y resultados
    - Error handling: HTTPException con códigos estándar
    - Validación: Entrada verificada contra limites configurables
"""

from fastapi import APIRouter, HTTPException
from app.config import settings
from app.logger import get_logger
from app.exceptions import ValidationError, TranslationError

from app.schemas.translation import (
    TranslationRequest, 
    TranslationResponse, 
    ReverseTranslationRequest, 
    ReverseTranslationResponse
)
from app.api.services.translator import text_to_braille, braille_to_text


logger = get_logger(__name__)
router = APIRouter()


@router.post("/to-braille", response_model=TranslationResponse)
def translate_to_braille(request: TranslationRequest):
    """
    Convierte texto español a representación Braille.
    
    Realiza transcripción completa:
    - Mayúsculas, minúsculas, números y acentos
    - Prefijos especiales para números [3,4,5,6] y mayúsculas [4,6]
    - Preserva espacios y signos de puntuación
    - Genera representación textual para debugging
    
    Args:
        request (TranslationRequest): {"text": "Hola"}
    
    Returns:
        TranslationResponse:
            - original_text: Texto de entrada
            - braille_cells: [[4,6], [1,2,5], ...] puntos activos
            - braille_string_repr: "46|125|135|1" (representación textual)
    
    Raises:
        ValidationError: Texto vacío o excede límite
        TranslationError: Error en proceso de traducción
    
    Examples:
        POST /api/v1/translation/to-braille
        {"text": "Hola"}
        
        Response:
        {
            "original_text": "Hola",
            "braille_cells": [[4,6], [1,2,5], [1,3,5], [1]],
            "braille_string_repr": "46|125|135|1"
        }
    """
    try:
        # Validar entrada
        if not request.text or not request.text.strip():
            raise ValidationError("El texto no puede estar vacío")
        
        if len(request.text) > settings.max_text_length:
            raise ValidationError(
                f"El texto excede la longitud máxima de {settings.max_text_length} caracteres"
            )
        
        logger.info(f"Traducción a Braille solicitada: {len(request.text)} caracteres")
        
        # Traducir
        braille_cells = text_to_braille(request.text)
        
        # Validar resultado
        if len(braille_cells) > settings.max_braille_cells:
            raise TranslationError(
                f"La traducción resultaría en {len(braille_cells)} celdas, exceeds límite"
            )
        
        # Generar representación textual
        braille_string = "|".join(
            "".join(map(str, cell)) if cell else "_" 
            for cell in braille_cells
        )
        
        logger.info(f"Traducción exitosa: {len(braille_cells)} celdas generadas")
        
        return TranslationResponse(
            original_text=request.text,
            braille_cells=braille_cells,
            braille_string_repr=braille_string
        )
    
    except ValidationError:
        raise
    except TranslationError:
        raise
    except Exception as e:
        logger.error(f"Error inesperado en traducción: {str(e)}", exc_info=True)
        raise TranslationError(f"Error durante traducción: {str(e)}")


@router.post("/to-text", response_model=ReverseTranslationResponse)
def translate_to_text(request: ReverseTranslationRequest):
    """
    Convierte Braille a texto español (traducción inversa).
    
    Realiza reversión de traducción:
    - Procesa celdas Braille [1-6] puntos
    - Detecta y maneja prefijos especiales
    - Reconstruye números y mayúsculas
    - Retorna texto español
    
    Args:
        request (ReverseTranslationRequest): 
            {"braille_cells": [[1,2,5], [1,3,5]]}
    
    Returns:
        ReverseTranslationResponse:
            - translated_text: "ho" (resultado)
    
    Raises:
        ValidationError: Celdas vacías o inválidas
        TranslationError: Error en proceso de traducción inversa
    
    Examples:
        POST /api/v1/translation/to-text
        {"braille_cells": [[4,6], [1,2,5], [1,3,5], [1]]}
        
        Response:
        {"translated_text": "Hola"}
    """
    try:
        # Validar entrada
        if not request.braille_cells:
            raise ValidationError("Las celdas Braille no pueden estar vacías")
        
        if len(request.braille_cells) > settings.max_braille_cells:
            raise ValidationError(
                f"Excede el límite de {settings.max_braille_cells} celdas"
            )
        
        # Validar que cada celda sea válida
        for i, cell in enumerate(request.braille_cells):
            if not isinstance(cell, list):
                raise ValidationError(f"Celda {i}: debe ser lista, recibido {type(cell)}")
            if not all(1 <= p <= 6 for p in cell):
                raise ValidationError(
                    f"Celda {i}: puntos deben estar entre 1-6, recibido {cell}"
                )
        
        logger.info(f"Traducción inversa solicitada: {len(request.braille_cells)} celdas")
        
        # Traducir
        text = braille_to_text(request.braille_cells)
        
        logger.info(f"Traducción inversa exitosa: '{text}'")
        
        return ReverseTranslationResponse(translated_text=text)
    
    except ValidationError:
        raise
    except TranslationError:
        raise
    except Exception as e:
        logger.error(f"Error inesperado en traducción inversa: {str(e)}", exc_info=True)
        raise TranslationError(f"Error durante traducción inversa: {str(e)}")
        ...     "braille_string_repr": "3456|1"
        ... }
    
    Note:
        - Prefijo número [3,4,5,6] precede a cada secuencia de dígitos
        - Prefijo mayúscula [4,6] precede a cada letra mayúscula
        - Los caracteres desconocidos se ignoran silenciosamente
        - Ideal para aplicaciones educativas y accesibilidad
    
    Casos de Uso:
        - Visualización de Braille en interfaces web
        - Generación de material imprimible
        - Integración con lectores Braille
        - Material educativo sobre Braille
    """
    if not request.text:
        raise HTTPException(status_code=400, detail="El texto no puede estar vacío")
    
    cells = text_to_braille(request.text)
    
    # Generamos una representación legible para facilitar el debug
    # Ej: [[1], [1,2]] -> "1|12"
    str_repr = "|".join(["".join(map(str, c)) if c else "_" for c in cells])
    
    return TranslationResponse(
        original_text=request.text,
        braille_cells=cells,
        braille_string_repr=str_repr
    )

@router.post("/to-text", response_model=ReverseTranslationResponse)
def translate_to_text(request: ReverseTranslationRequest):
    """
    Endpoint: Convierte celdas Braille a texto español (traducción inversa).
    
    Realiza traducción inversa del formato Braille a español:
    - Detecta y procesa prefijos especiales (número, mayúscula)
    - Desambigua caracteres duplicados usando sistema de prioridades
    - Preserva espacios (celdas vacías [])
    - Maneja máquina de estados para números y mayúsculas
    
    Validación:
    - No rechaza listas vacías (devuelve texto vacío)
    
    Args:
        request (ReverseTranslationRequest): Objeto con campo 'braille_cells'
                                            Ej: {"braille_cells": [[1], [1,2]]}
    
    Returns:
        ReverseTranslationResponse: Objeto con campo:
            - translated_text (str): Texto español traducido
    
    HTTP Status Codes:
        - 200 OK: Conversión exitosa
        - 422 Unprocessable Entity: Esquema JSON inválido
    
    Raises:
        No levanta HTTPException directamente.
    
    Máquina de Estados Implementada:
        1. DETECTAR PREFIJO NÚMERO [3,4,5,6]:
           - Activar modo número
           - Siguiente letra (a-j) se convierte a dígito (1-0)
        2. DETECTAR PREFIJO MAYÚSCULA [4,6]:
           - Marcar capitalización pendiente
           - Siguiente letra se convierte a mayúscula
        3. DETECTAR CELDAS VACÍAS []:
           - Insertar espacio
           - Desactivar modo número
        4. DESAMBIGUACIÓN:
           - Prioridad: acentos > ñ > signos > letras normales
           - Usa REVERSE_BRAILLE_MAP con sistema de prioridades
    
    Examples:
        >>> # Request - conversión simple
        >>> {"braille_cells": [[1, 2, 5], [1, 3, 5], [1, 2, 3], [1]]}
        >>> # Response
        >>> {"translated_text": "hola"}
        
        >>> # Request - con número
        >>> {"braille_cells": [[3, 4, 5, 6], [1]]}
        >>> # Response
        >>> {"translated_text": "1"}  # Prefijo número + 'a' = '1'
        
        >>> # Request - con mayúscula
        >>> {"braille_cells": [[4, 6], [1]]}
        >>> # Response
        >>> {"translated_text": "A"}  # Prefijo mayúscula + 'a' = 'A'
        
        >>> # Request - mixto
        >>> {"braille_cells": [[4, 6], [1], [1, 5], [1]]}
        >>> # Response
        >>> {"translated_text": "Alae"}
    
    Resolución de Duplicados:
        Algunos caracteres comparten representación Braille:
        - ñ y ú comparten [1,2,4,5,6]: Se elige 'ñ' (prioridad mayor)
        - v y ó comparten [1,3,4,6]: Se elige 'ó' (acento tiene prioridad)
        - s y í podrían coincidir: Sistema de prioridades evita conflictos
        
    Note:
        - Usa REVERSE_BRAILLE_MAP con sistema de prioridades multi-nivel
        - Celdas no reconocidas se reemplazan con '?'
        - Ideal para procesamiento de entrada Braille de dispositivos
        - Compatible con salida de any Braille-to-text converter
    
    Casos de Uso:
        - Entrada desde teclados Braille
        - Procesamiento de datos de sensores Braille
        - Validación bidireccional (roundtrip testing)
        - Interfaces accesibles
    """
    text = braille_to_text(request.braille_cells)
    return ReverseTranslationResponse(translated_text=text)