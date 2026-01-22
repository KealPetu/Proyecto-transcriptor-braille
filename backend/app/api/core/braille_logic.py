# backend/app/core/braille_logic.py

"""
Módulo de Lógica de Mapeo Braille.

Este módulo implementa el sistema de traducción Español-Braille basado en
las Series Braille españolas y el Símbolo Generador. Proporciona mapeos
bidireccionales entre caracteres españoles y sus representaciones en Braille.

Sistema de Series:
    - Serie 1 (a-j): Matriz primitiva, utiliza puntos 1-5
    - Serie 2 (k-t): Serie 1 + punto 3
    - Serie 3 (u-z): Serie 1 + puntos 3 y 6

Caracteres Soportados:
    - 26 letras minúsculas (a-z)
    - 6 letras acentuadas (á, é, í, ó, ú) + ü (diéresis)
    - Letra ñ con tilde
    - 10 dígitos (0-9) con prefijo especial
    - Signos de puntuación: . , ; : ! ? - ( ) + = / " '
    - Espacio

Prefijos Especiales:
    - Número: [3, 4, 5, 6] (precede a dígitos)
    - Mayúscula: [4, 6] (precede a letras mayúsculas)

Ejemplo:
    >>> from braille_logic import BRAILLE_MAP, text_to_braille
    >>> BRAILLE_MAP['a']
    [1]
    >>> BRAILLE_MAP['ñ']
    [1, 2, 4, 5, 6]
"""

# Definición de la Serie 1 (Matriz Primitiva: a-j)
SERIE_1_BASE = {
    'a': [1],
    'b': [1, 2],
    'c': [1, 4],
    'd': [1, 4, 5],
    'e': [1, 5],
    'f': [1, 2, 4],
    'g': [1, 2, 4, 5],
    'h': [1, 2, 5],
    'i': [2, 4],
    'j': [2, 4, 5]
}

def generar_mapa_completo():
    """
    Genera el diccionario completo de traducción Español -> Braille.
    
    Construye un mapeo exhaustivo que incluye:
    - Serie 1 (a-j): Matriz primitiva
    - Serie 2 (k-t): Serie 1 + punto 3
    - Serie 3 (u-z): Serie 1 + puntos 3 y 6
    - Letras especiales españolas (ñ, acentos, ü)
    - Dígitos 0-9 (traducción manual, prefijo en translator.py)
    - Signos de puntuación y caracteres especiales
    - Prefijos especiales para números y mayúsculas
    
    Los duplicados se resuelven mediante prioridades:
    - ñ = [1,2,4,5,6] (prioridad sobre ú)
    - ú = [1,2,4,5,6] (alternativo a ñ)
    
    Returns:
        dict: Diccionario {carácter: [puntos_activos]}
            Ejemplo: {'a': [1], 'b': [1, 2], 'ñ': [1, 2, 4, 5, 6]}
    
    Note:
        Los números se representan usando la Serie 1 (a-j) más prefijo especial.
        El mapeo de dígitos se define en translator.py para claridad.
    """
    braille_map = SERIE_1_BASE.copy()
    
    letras_serie_1 = list(SERIE_1_BASE.keys())
    
    # --- Serie 2 (k-t): Serie 1 + punto 3 ---
    letras_serie_2 = ['k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't']
    for i, letra in enumerate(letras_serie_2):
        letra_base = letras_serie_1[i]
        puntos_base = SERIE_1_BASE[letra_base].copy()
        puntos_base.append(3)
        braille_map[letra] = sorted(puntos_base)
    
    # --- Serie 3 (u-z): Serie 1 + puntos 3 y 6 ---
    # u->a, v->b, w->c (letra especial), x->d, y->e, z->f
    mapa_serie_3 = [
        ('u', 'a'), ('v', 'b'), ('w', 'c'), ('x', 'd'), ('y', 'e'), ('z', 'f')
    ]
    for letra_dest, letra_base in mapa_serie_3:
        puntos = SERIE_1_BASE[letra_base].copy()
        puntos.extend([3, 6])
        braille_map[letra_dest] = sorted(puntos)
    
    # --- Letras especiales del español ---
    especiales = {
        'ñ': [1, 2, 4, 5, 6],  # Ñ
        'á': [1, 2, 3, 5, 6],  # Á acentuada
        'é': [2, 3, 4, 6],     # É acentuada
        'í': [3, 4],           # Í acentuada
        'ó': [1, 3, 4, 6],     # Ó acentuada
        'ú': [1, 2, 4, 5, 6],  # Ú acentuada (mismo que ñ, prioridad para ñ)
        'ü': [1, 2, 5, 6],     # Ü diéresis
    }
<<<<<<< HEAD
    braille_map.update(adicionales)

    # --- Signos Especiales ---
    # Números, Mayúsculas [cite: 142]
    braille_map['num'] = [3, 4, 5, 6] # Prefijo de número
    braille_map['cap'] = [4, 6]       # Prefijo de mayúscula (común) o según [cite: 142] puntos 4 y 6? 
                                      # En el gráfico [cite: 130] el prefijo mayúscula son puntos 4-6.
    braille_map[' '] = []             # Espacio vacío

    # --- Signos de Puntuación ---
    # Traducción de signos de puntuación españoles al Braille
    signos_puntuacion = {
        '.': [3],             # Punto
        ',': [2],             # Coma
        ':': [2, 5],          # Dos puntos
        ';': [2, 3],          # Punto y coma
        '"': [2, 3, 6],       # Comillas
        '?': [2, 6],          # Interrogación (cierre)
        '¿': [2, 6],          # Interrogación (apertura)
        '!': [2, 3, 5],       # Exclamación (cierre)
        '¡': [2, 3, 5],       # Exclamación (apertura)
        '-': [3, 6],          # Guion/Raya
        '(': [1, 2, 6],       # Abre Paréntesis
        ')': [3, 4, 5],       # Cierra Paréntesis
        '+': [2, 3, 5],       # Suma
        '*': [2, 3, 6],       # Multiplicacion
        '/': [2, 5, 6],       # Division
        '=': [2, 3, 5, 6]     # Igual
=======
    braille_map.update(especiales)
    
    # --- Números (0-9) ---
    # Los números utilizan el prefijo de número + letras de Serie 1
    # El mapeo se define en el translator.py
    
    # --- Signos especiales ---
    signos = {
        ' ': [],                # Espacio
        '.': [2, 5, 6],         # Punto final
        ',': [2],               # Coma
        ';': [2, 3],            # Punto y coma
        ':': [2, 5],            # Dos puntos
        '!': [2, 3, 5],         # Exclamación
        '?': [2, 3, 6],         # Interrogación
        '-': [3, 6],            # Guion/raya
        '(': [1, 2, 3, 5, 6],   # Paréntesis apertura
        ')': [2, 3, 4, 5, 6],   # Paréntesis cierre
        '+': [1, 2, 4, 6],      # Suma
        '=': [1, 2, 3, 4, 5, 6],# Igual
        '/': [3, 4, 5],         # División
        '"': [2, 3, 5, 6],      # Comillas
        "'": [3],               # Apóstrofo
>>>>>>> develop
    }
    braille_map.update(signos)
    
    # --- Prefijos especiales ---
    braille_map['_NUM_PREFIX_'] = [3, 4, 5, 6]     # Prefijo para números
    braille_map['_CAPS_PREFIX_'] = [4, 6]          # Prefijo para mayúsculas
    braille_map['_MAYUSCULAS_'] = [6]              # Prefijo de mayúsculas en algunos contextos
    
    return braille_map

# Constante global
BRAILLE_MAP = generar_mapa_completo()

# Mapeo inverso para Braille -> Español
# Prioriza en este orden: letras acentuadas > ñ > signos > letras normales
def _generar_reverse_map():
    """
    Genera un mapeo inverso Braille -> Español con resolución de conflictos.
    
    Cuando múltiples caracteres comparten la misma representación Braille
    (ej. ñ y ú ambos [1,2,4,5,6]), el mapeo inverso necesita decidir cuál
    usar. Esta función implementa un sistema de prioridades:
    
    Orden de Prioridad (menor número = mayor prioridad):
        1. Letras acentuadas: á, é, í, ó (máxima prioridad)
        2. Ñ y ú: ñ > ú
        3. Diéresis: ü
        4. Signos de puntuación: . , ; : ! ? - ( ) + = / " '
        5. Letras normales: a-z (prioridad baja)
    
    Mapeo Inverso:
        La clave es una tupla de puntos ordenados, ej. (1, 2, 4, 5, 6)
        El valor es el carácter elegido según las prioridades.
    
    Returns:
        dict: Diccionario {(puntos_tupla): carácter}
            Ejemplo: {(1,): 'a', (1, 2): 'b', (1, 2, 4, 5, 6): 'ñ'}
    
    Example:
        >>> reverse_map = _generar_reverse_map()
        >>> reverse_map[(1, 2, 4, 5, 6)]  # ñ tiene prioridad sobre ú
        'ñ'
    
    Note:
        Los prefijos especiales (_NUM_PREFIX_, _CAPS_PREFIX_) se ignoran
        en el mapeo inverso, igual que espacios vacíos ([]).
    """
    reverse_map = {}
    priority = {
        # Acentos (prioridad muy alta) - preferir acentos sobre letras normales
        'á': 1, 'é': 2, 'ó': 3, 'í': 4,
        # Ñ y ú - ñ tiene mayor prioridad que ú
        'ñ': 5, 'ú': 6, 'ü': 7,
        # Signos
        '.': 10, ',': 11, ';': 12, ':': 13,
        '!': 14, '?': 15,
        '-': 16, '(': 17, ')': 18, '+': 19, '=': 20, '/': 21, '"': 22, "'": 23,
    }
    
    for k, v in BRAILLE_MAP.items():
        if k.startswith('_') or v == []:
            continue
        
        key = tuple(sorted(v))
        current_priority = priority.get(k, 100)  # 100 = prioridad baja (letras normales)
        
        # Si la clave ya existe, comparar prioridades
        if key in reverse_map:
            existing_char = reverse_map[key]
            existing_priority = priority.get(existing_char, 100)
            # Mantener el que tenga mayor prioridad (número menor)
            if current_priority < existing_priority:
                reverse_map[key] = k
        else:
            reverse_map[key] = k
    
    return reverse_map

REVERSE_BRAILLE_MAP = _generar_reverse_map()