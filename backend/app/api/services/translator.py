"""
Módulo de Traducción Braille Bidireccional.

Proporciona funciones de conversión entre español y Braille en ambas direcciones:
- text_to_braille(): Español → Braille (transcripción)
- braille_to_text(): Braille → Español (traducción inversa)

Maneja automáticamente:
- Números (0-9) con prefijo especial
- Mayúsculas con prefijo especial
- Acentos y caracteres especiales españoles (ñ, ü)
- Signos de puntuación
- Espacios y separadores

Ejemplo:
    >>> text_to_braille("Hola 123")
    [[4, 6], [1, 2, 5], [1, 3, 5], [1, 2, 3], [1], [3, 4, 5, 6], [1], 
     [3, 4, 5, 6], [1, 2], [3, 4, 5, 6], [2, 4]]
    
    >>> braille_to_text([[4, 6], [1], [1, 5], [1]])
    'Hale'
"""

from typing import List, Union
from ..core.braille_logic import BRAILLE_MAP, REVERSE_BRAILLE_MAP

# Definición de prefijos especiales
PREFIJO_NUMERO = [3, 4, 5, 6]  # Prefijo que indica seguimiento de dígitos
PREFIJO_MAYUSCULA = [4, 6]     # Prefijo que indica letra mayúscula siguiente

# Mapeo de Dígitos a Letras de la Serie 1
# Los dígitos se representan usando puntos Braille mapeados a letras a-j:
# 1→a, 2→b, 3→c, 4→d, 5→e, 6→f, 7→g, 8→h, 9→i, 0→j
DIGIT_TO_LETTER = {
    '1': 'a', '2': 'b', '3': 'c', '4': 'd', '5': 'e',
    '6': 'f', '7': 'g', '8': 'h', '9': 'i', '0': 'j'
}
LETTER_TO_DIGIT = {v: k for k, v in DIGIT_TO_LETTER.items()}

def text_to_braille(text: str) -> List[List[int]]:
    """
    Convierte texto español a representación Braille.
    
    Realiza transcripción completa incluyendo:
    - Conversión de caracteres a puntos Braille según Series
    - Prefijo especial para secuencias numéricas
    - Prefijo especial para mayúsculas
    - Manejo de acentos y caracteres españoles
    - Preservación de espacios y signos de puntuación
    
    Máquina de Estados:
        - is_number_mode: Detecta si está dentro de una secuencia numérica
        - Transición de números a otros caracteres reinicia el modo
    
    Args:
        text (str): Texto en español a convertir a Braille.
                   Puede contener letras, números, acentos, mayúsculas,
                   espacios y signos de puntuación.
    
    Returns:
        List[List[int]]: Lista de celdas Braille donde cada celda es una
                        lista de números (1-6) representando puntos activos.
                        Celdas vacías [] representan espacios.
    
    Raises:
        No levanta excepciones directamente, los caracteres no reconocidos
        se ignoran silenciosamente (ej. saltos de línea).
    
    Examples:
        >>> text_to_braille("a")
        [[1]]
        
        >>> text_to_braille("hola")
        [[1, 2, 5], [1, 3, 5], [1, 2, 3], [1]]
        
        >>> text_to_braille("1")
        [[3, 4, 5, 6], [1]]  # Prefijo número + celda 'a'
        
        >>> text_to_braille("A")
        [[4, 6], [1]]  # Prefijo mayúscula + celda 'a'
        
        >>> text_to_braille("Café")
        [[4, 6], [1, 2], [1, 2, 4], [2, 3, 4, 6]]
        
        >>> text_to_braille("Bus 15")
        [[1, 2], [1, 3, 5, 6], [3, 4, 5, 6], [1, 2, 5], 
         [3, 4, 5, 6], [1]]  # 'Bus' + prefijo + '1' + '5'
    
    Note:
        - Los números consecutivos comparten el mismo prefijo especial
        - Separadores como puntos decimales (.) y comas (,) se incluyen
        - La detección de fin de número se activa con cualquier carácter no-dígito
    """
    result = []
    is_number_mode = False
    i = 0
    
    while i < len(text):
        char = text[i]
        
        # Detectar inicio de secuencia numérica
        if char.isdigit():
            if not is_number_mode:
                result.append(PREFIJO_NUMERO)
                is_number_mode = True
            
            # Traducir dígito a letra de Serie 1 y luego a braille
            target_letter = DIGIT_TO_LETTER[char]
            result.append(BRAILLE_MAP[target_letter])
            i += 1
            continue
        
<<<<<<< HEAD
        else:
            # Si encontramos un carácter que no es dígito ni espacio ni puntuación, salimos del modo numérico
            if char not in ['.', ',', ':', '?', '!', '-', '¿', '¡']:
                is_number_mode = False

        # --- Lógica de Texto General ---
        char_lower = char.lower()
=======
        # Manejar separadores de números (puntos y comas)
        if char in ',.':
            if is_number_mode:
                # Agregar el punto o coma como separador numérico
                if char == '.':
                    result.append(BRAILLE_MAP['.'])
                elif char == ',':
                    result.append(BRAILLE_MAP[','])
                i += 1
                continue
>>>>>>> develop
        
        # Salir del modo numérico con espacio u otros caracteres
        if is_number_mode and char not in '0123456789,.':
            is_number_mode = False
        
        # Manejar espacios
        if char == ' ':
            result.append(BRAILLE_MAP[' '])
            i += 1
            continue
        
        # Manejar mayúsculas
        if char.isupper():
            result.append(PREFIJO_MAYUSCULA)
            char_lower = char.lower()
            if char_lower in BRAILLE_MAP:
                result.append(BRAILLE_MAP[char_lower])
            i += 1
            continue
        
        # Manejar caracteres normales (minúsculas, acentos, signos)
        if char in BRAILLE_MAP:
            result.append(BRAILLE_MAP[char])
        # Si el carácter no está en el mapa, se ignora (ej. saltos de línea)
        
        i += 1
    
    return result


def braille_to_text(braille_cells: List[List[int]]) -> str:
    """
    Convierte celdas Braille a texto español (traducción inversa).
    
    Realiza traducción completa con máquina de estados:
    - is_number_mode: Detecta secuencias numéricas tras prefijo especial
    - capitalize_next: Detecta mayúsculas tras prefijo especial
    - Prioridades de desambigüación para duplicados (ñ > ú)
    
    Características:
    - Maneja múltiples caracteres con misma representación Braille
    - Preserva espacios (celdas vacías)
    - Convierte letras a números cuando está en modo numérico
    - Capitaliza letras cuando hay prefijo de mayúscula
    - Usa mapeo inverso con sistema de prioridades
    
    Máquina de Estados:
        1. Si célda = PREFIJO_NUMERO: Activar modo número, pasar siguiente
        2. Si célda = PREFIJO_MAYUSCULA: Marcar para capitalizar, pasar siguiente
        3. Si célda = []: Agregar espacio, desactivar modo número
        4. Si está en modo número: Convertir a dígito (a=1, b=2, ..., j=0)
        5. Si hay capitalización pendiente: Convertir a mayúscula
        6. Else: Buscar carácter en mapeo inverso
    
    Args:
        braille_cells (List[List[int]]): Lista de celdas Braille donde cada
                                         celda es una lista de números (1-6)
                                         representando puntos activos.
    
    Returns:
        str: Texto español traducido.
    
    Raises:
        No levanta excepciones, usa '?' para representar puntos no reconocidos.
    
    Examples:
        >>> braille_to_text([[1, 2, 5], [1, 3, 5], [1, 2, 3], [1]])
        "hola"
        
        >>> braille_to_text([[3, 4, 5, 6], [1]])
        "1"  # Prefijo número + 'a' = '1'
        
        >>> braille_to_text([[4, 6], [1]])
        "A"  # Prefijo mayúscula + 'a' = 'A'
        
        >>> braille_to_text([[3, 4, 5, 6], [1], [3, 4, 5, 6], [1, 2]])
        "12"  # Prefijo + 'a' + prefijo + 'b' = "12"
        
        >>> braille_to_text([[3, 4, 5, 6], [1], [], [3, 4, 5, 6], [1, 2]])
        "1 2"  # Espacio entre números
    
    Note:
        - Usa REVERSE_BRAILLE_MAP con sistema de prioridades
        - Los duplicados (ñ/ú) se resuelven automáticamente según prioridades
        - Celdas no reconocidas se reemplazan con '?'
    """
    result = []
    is_number_mode = False
    capitalize_next = False
    i = 0
    
    while i < len(braille_cells):
        cell = braille_cells[i]
        cell_tuple = tuple(sorted(cell))
        
        # Detectar prefijo de número
        if cell_tuple == tuple(sorted(PREFIJO_NUMERO)):
            is_number_mode = True
            i += 1
            continue
        
        # Detectar prefijo de mayúsculas
        if cell_tuple == tuple(sorted(PREFIJO_MAYUSCULA)):
            capitalize_next = True
            i += 1
            continue
        
        # Manejar espacios (celda vacía)
        if not cell_tuple:
            result.append(' ')
            is_number_mode = False
            i += 1
            continue
        
        # Buscar el carácter en el mapeo inverso
        char = REVERSE_BRAILLE_MAP.get(cell_tuple, None)
        
        if char is None:
            # Si no encontramos en mapeo inverso, buscar en BRAILLE_MAP
            for k, v in BRAILLE_MAP.items():
                if not k.startswith('_') and tuple(sorted(v)) == cell_tuple:
                    char = k
                    break
        
        # Si aún no encontramos, usar placeholder
        if char is None:
            char = '?'
        
        # Aplicar transformaciones de contexto
        if is_number_mode:
            if char in LETTER_TO_DIGIT:
                # Convertir letra (a-j) a número (1-0)
                char = LETTER_TO_DIGIT[char]
            else:
                # Si encontramos un no-letra en modo número, salir del modo
                is_number_mode = False
        
        # Aplicar mayúscula si está activo
        if capitalize_next and char.isalpha():
            char = char.upper()
            capitalize_next = False
        
        result.append(char)
        i += 1
    
    return "".join(result)

