from typing import List, Union
from ..core.braille_logic import BRAILLE_MAP, REVERSE_BRAILLE_MAP

# Definición de prefijos especiales según el documento
PREFIJO_NUMERO = [3, 4, 5, 6]  # [cite: 111]
PREFIJO_MAYUSCULA = [4, 6]     # [cite: 142]

# Mapeo de Dígitos a Letras de la Serie 1 (a-j)
# "Los diez dígitos se obtienen anteponiendo el signo de número a la primera serie" [cite: 111]
DIGIT_TO_LETTER = {
    '1': 'a', '2': 'b', '3': 'c', '4': 'd', '5': 'e',
    '6': 'f', '7': 'g', '8': 'h', '9': 'i', '0': 'j'
}
# Inverso para traducción Braille -> Texto
LETTER_TO_DIGIT = {v: k for k, v in DIGIT_TO_LETTER.items()}

def text_to_braille(text: str) -> List[List[int]]:
    """
    Convierte una cadena de texto en una lista de celdas Braille.
    Retorna: Una lista de listas, donde cada sub-lista son los puntos activos.
    Ejemplo: "Hola" -> [[4,6], [1,2,5], [1,3,5], [1,2,3], [1]]
    """
    result = []
    is_number_mode = False # Flag para controlar el contexto numérico

    for char in text:
        # --- Lógica de Números ---
        if char.isdigit():
            if not is_number_mode:
                # Si es el primer número de la secuencia, agregar prefijo 
                result.append(PREFIJO_NUMERO)
                is_number_mode = True
            
            # Traducir dígito usando el mapeo de la Serie 1
            target_letter = DIGIT_TO_LETTER[char]
            result.append(BRAILLE_MAP[target_letter])
            continue
        
        else:
            # Si encontramos un carácter que no es dígito, salimos del modo numérico
            # (Nota: El espacio en blanco separa números )
            is_number_mode = False

        # --- Lógica de Texto General ---
        char_lower = char.lower()
        
        # Si no existe en el mapa (ej. salto de línea), lo ignoramos o ponemos espacio
        if char_lower not in BRAILLE_MAP and char != ' ':
            continue 

        # Manejo de Mayúsculas
        if char.isupper():
            result.append(PREFIJO_MAYUSCULA) # [cite: 142]
        
        # Añadir la celda correspondiente
        if char == ' ':
            result.append([]) # Espacio vacío
        else:
            result.append(BRAILLE_MAP[char_lower])

    return result

def braille_to_text(braille_cells: List[List[int]]) -> str:
    """
    Convierte una lista de celdas Braille (listas de puntos) a texto español.
    Maneja la lógica de estado para prefijos de número y mayúsculas.
    """
    result = []
    is_number_mode = False
    capitalize_next = False

    for cell in braille_cells:
        # Convertir la lista de puntos a tupla ordenable para buscar en diccionario
        cell_tuple = tuple(sorted(cell))

        # 1. Detectar Prefijos
        if cell_tuple == tuple(PREFIJO_NUMERO):
            is_number_mode = True
            continue
        
        if cell_tuple == tuple(PREFIJO_MAYUSCULA):
            capitalize_next = True
            continue

        # 2. Manejo de Espacios (rompen el modo numérico)
        if not cell_tuple: # Lista vacía es espacio
            result.append(" ")
            is_number_mode = False
            continue

        # 3. Buscar carácter
        char = REVERSE_BRAILLE_MAP.get(cell_tuple, "?") # '?' si no reconoce

        # 4. Aplicar Transformaciones de Contexto
        if is_number_mode:
            # Si estamos en modo numérico, 'a' se convierte en '1', etc.
            if char in LETTER_TO_DIGIT:
                char = LETTER_TO_DIGIT[char]
            else:
                # Si aparece algo que no es a-j, ¿asumimos que corta el número?
                # Por simplicidad, lo mantenemos como letra o desactivamos modo
                is_number_mode = False 
        
        if capitalize_next:
            char = char.upper()
            capitalize_next = False
            
        result.append(char)

    return "".join(result)