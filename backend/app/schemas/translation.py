# backend/app/schemas/translation.py

"""
Esquemas Pydantic para traducción Braille.

Define los modelos de datos para solicitudes y respuestas HTTP
en los endpoints de traducción Español ↔ Braille.

Esquemas Definidos:
    - TranslationRequest: Entrada para traducción (Español → Braille)
    - TranslationResponse: Salida de traducción (Español → Braille)
    - ReverseTranslationRequest: Entrada para traducción inversa (Braille → Español)
    - ReverseTranslationResponse: Salida de traducción inversa (Braille → Español)

Representación de Celdas Braille:
    Cada celda se representa como List[int] con números 1-6 indicando
    puntos activos. Ejemplo:
    - [1] = punto 1 activo (letra 'a')
    - [1, 2] = puntos 1 y 2 activos (letra 'b')
    - [] = celda vacía (espacio)

Ejemplo de Uso:
    # Traducción
    TranslationRequest(text="Hola")
    → TranslationResponse(
        original_text="Hola",
        braille_cells=[[4,6], [1,2,5], [1,3,5], [1]],
        braille_string_repr="46|125|135|1"
    )
    
    # Traducción inversa
    ReverseTranslationRequest(braille_cells=[[1,2,5], [1,3,5], [1,2,3], [1]])
    → ReverseTranslationResponse(translated_text="hola")
"""

from pydantic import BaseModel
from typing import List, Optional


class TranslationRequest(BaseModel):
    """
    Esquema para solicitud de traducción Español → Braille.
    
    Attributes:
        text (str): Texto en español a traducir a Braille.
                   Puede contener: letras minúsculas, mayúsculas, números,
                   acentos españoles (á, é, í, ó, ú, ü), ñ, y signos.
                   Máximo: Sin límite especificado.
    
    Examples:
        TranslationRequest(text="Hola")
        TranslationRequest(text="Café con azúcar")
        TranslationRequest(text="¡Bienvenido!")
        TranslationRequest(text="Piso 3")
    
    Validación:
        - Campo requerido (no puede ser None)
        - Puede estar vacío ("") pero se rechaza en endpoint con HTTP 400
    """
    text: str


class TranslationResponse(BaseModel):
    """
    Esquema para respuesta de traducción Español → Braille.
    
    Contiene el texto original, las celdas Braille traducidas y una
    representación textual para debugging.
    
    Attributes:
        original_text (str): El texto de entrada sin modificar.
                            Utilizado para verificación y logging.
        
        braille_cells (List[List[int]]): Celdas Braille como lista de listas.
                                        Cada celda es List[int] con puntos 1-6.
                                        Celda vacía [] representa espacio.
                                        Ejemplo: [[1], [1,2], [1,5], []]
        
        braille_string_repr (Optional[str]): Representación textual para debugging.
                                            Concatena puntos con separador |.
                                            Espacios representados como _.
                                            Ejemplo: "1|12|15|_"
                                            Default: None
    
    Examples:
        TranslationResponse(
            original_text="a",
            braille_cells=[[1]],
            braille_string_repr="1"
        )
        
        TranslationResponse(
            original_text="hola",
            braille_cells=[[1,2,5], [1,3,5], [1,2,3], [1]],
            braille_string_repr="125|135|123|1"
        )
        
        TranslationResponse(
            original_text="Bus 15",
            braille_cells=[[1,2], [1,3,5,6], [3,4,5,6], [3,4,5,6], [1], [3,4,5,6], [1,2]],
            braille_string_repr="12|1356|3456|3456|1|3456|12"
        )
    
    Interpretación:
        - Cada elemento de braille_cells es una celda
        - Los números en cada celda son puntos Braille (1-6)
        - Puntos se organizan: 1,4 en columna izq, 2,5 en media, 3,6 en derecha
        - braille_string_repr concatena puntos de cada celda con |
        - braille_string_repr facilita logging y debugging
    """
    original_text: str
    braille_cells: List[List[int]]
    braille_string_repr: Optional[str] = None


class ReverseTranslationRequest(BaseModel):
    """
    Esquema para solicitud de traducción Braille → Español.
    
    Attributes:
        braille_cells (List[List[int]]): Celdas Braille a traducir.
                                        Cada celda es List[int] con puntos activos (1-6).
                                        Celda vacía [] representa espacio.
                                        Máximo: Sin límite especificado.
    
    Formato de Entrada:
        Cada celda es una lista de números 1-6:
        - [1] = punto 1 activo
        - [1, 2, 5] = puntos 1, 2, 5 activos
        - [] = celda vacía (espacio)
    
    Examples:
        ReverseTranslationRequest(braille_cells=[[1]])
        
        ReverseTranslationRequest(
            braille_cells=[[1,2,5], [1,3,5], [1,2,3], [1]]
        )
        
        ReverseTranslationRequest(
            braille_cells=[[3,4,5,6], [1,2]]
        )  # "12" con prefijo número
    
    Validación:
        - Campo requerido (no puede ser None)
        - Puede estar vacío ([]) resultando en texto vacío
        - Puntos deben estar en rango 1-6 (validación implícita)
    
    Note:
        - Manejo de prefijos automático (número y mayúscula)
        - Desambigüación de caracteres duplicados automática
    """
    braille_cells: List[List[int]]


class ReverseTranslationResponse(BaseModel):
    """
    Esquema para respuesta de traducción Braille → Español.
    
    Attributes:
        translated_text (str): Texto en español traducido desde Braille.
                              Incluye: letras, números, acentos, signos.
                              Puede estar vacío si entrada estaba vacía.
    
    Examples:
        ReverseTranslationResponse(translated_text="a")
        
        ReverseTranslationResponse(translated_text="hola")
        
        ReverseTranslationResponse(translated_text="1")
        
        ReverseTranslationResponse(translated_text="Café")
        
        ReverseTranslationResponse(translated_text="Bus 15")
    
    Notas sobre Traducción Inversa:
        - Prefijo número [3,4,5,6] activa modo número para siguiente letra
        - Prefijo mayúscula [4,6] capitaliza siguiente letra
        - Caracteres no reconocidos se reemplazan con '?'
        - Desambigüación automática (ñ tiene prioridad sobre ú)
        - Espacios (celdas vacías) se preservan
    
    Roundtrip Property:
        text_to_braille(text) → braille_cells
        braille_to_text(braille_cells) → text
        En casi todos los casos: text == texto_recuperado
        Excepto cuando hay caracteres ambiguos (ñ/ú comparten representación)
    """
    translated_text: str