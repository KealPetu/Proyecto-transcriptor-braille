# backend/app/core/braille_logic.py

"""
Lógica de mapeo basada en el Símbolo Generador y las Series del Braille.
Referencia: Documento de Requisitos - Páginas 5, 6 y 7.
"""

# Definición de la Serie 1 (Matriz Primitiva: a-j)
# Basado en[cite: 43]. Se usan los puntos superiores (1, 2, 4, 5).
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
    Genera el diccionario completo de traducción Español -> Braille (lista de puntos)
    aplicando las reglas de derivación de series del documento.
    """
    braille_map = SERIE_1_BASE.copy()
    
    # Mapeo inverso para traducir Braille -> Español
    # Se llenará al final
    reverse_map = {}

    letras_serie_1 = list(SERIE_1_BASE.keys()) # ['a', 'b', ... 'j']

    # --- Generación de la Serie 2 (k-t) ---
    # Regla: "Resulta simplemente de añadir a la primera el punto 3" [cite: 64]
    # Nota: La 'ñ' no entra en la lógica estándar de series internacionales, 
    # pero el documento muestra letras k-t alineadas con a-j.
    
    letras_serie_2 = ['k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't']
    
    for i, letra in enumerate(letras_serie_2):
        letra_base = letras_serie_1[i]
        puntos_base = SERIE_1_BASE[letra_base].copy()
        puntos_base.append(3) # Añadir punto 3
        puntos_base.sort()
        braille_map[letra] = puntos_base

    # --- Generación de la Serie 3 (u-z) ---
    # Regla: "Es el resultado de añadir a la primera serie los puntos 3 y 6" [cite: 86]
    # El documento lista: u, v, x, y, z (la 'w' es una excepción histórica y va aparte)
    
    # Mapeo manual de índices según el orden del alfabeto vs serie 1
    # u -> a (1+3+6), v -> b (1+2+3+6), x -> c (1+4+3+6), y -> d (1+4+5+3+6), z -> e (1+5+3+6)
    mapa_serie_3 = [
        ('u', 'a'), ('v', 'b'), ('x', 'c'), ('y', 'd'), ('z', 'e')
    ]

    for letra_dest, letra_base in mapa_serie_3:
        puntos = SERIE_1_BASE[letra_base].copy()
        puntos.extend([3, 6]) # Añadir puntos 3 y 6
        puntos.sort()
        braille_map[letra_dest] = puntos

    # --- Casos Especiales y Letras Adicionales [cite: 87, 96] ---
    # La 'w' (no estaba en el francés original de Braille) y vocales acentuadas
    # se definen explícitamente según el cuadro de resumen [cite: 96, 97-101].
    
    adicionales = {
        'w': [2, 4, 5, 6], # [cite: 96]
        'ñ': [1, 2, 4, 5, 6], # Verificada en cuadro visual [cite: 171]
        'á': [1, 2, 3, 5, 6], # [cite: 97]
        'é': [2, 3, 4, 6],    # [cite: 98]
        'í': [3, 4],          # [cite: 99] (OJO: verificar visualmente, parece ser 3-4 en [cite: 99])
        'ó': [3, 4, 6],       # [cite: 99]
        'ú': [2, 3, 4, 5, 6], # [cite: 100]
        'ü': [1, 2, 5, 6],    # [cite: 101]
    }
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
    }
    braille_map.update(signos_puntuacion)

    return braille_map

# Constante global para usar en el resto de la app
BRAILLE_MAP = generar_mapa_completo()

# Mapeo inverso para la función de Braille a Texto
REVERSE_BRAILLE_MAP = {tuple(v): k for k, v in BRAILLE_MAP.items()}