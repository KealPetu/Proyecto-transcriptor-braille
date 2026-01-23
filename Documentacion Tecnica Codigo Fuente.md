# DOCUMENTACIÓN TÉCNICA DEL CÓDIGO FUENTE PYTHON
## Proyecto Transcriptor Braille - Estilo JavaDoc

---

## ÍNDICE GENERAL

1. [Introducción](#introducción)
2. [Estructura de Archivos](#estructura-de-archivos)
3. [Módulo: braille_logic](#módulo-braille_logic)
4. [Módulo: translator](#módulo-translator)
5. [Módulo: generator](#módulo-generator)
6. [Patrones de Diseño](#patrones-de-diseño)
7. [Guía de Uso](#guía-de-uso)
8. [Ejemplos Prácticos](#ejemplos-prácticos)

---

## INTRODUCCIÓN

Esta documentación técnica proporciona una descripción detallada del código fuente Python del Proyecto Transcriptor Braille. Utiliza un formato inspirado en JavaDoc adaptado a convenciones de Python para mantener un nivel profesional de documentación.

**Objetivo**: Servir como referencia técnica completa para desarrolladores que trabajan con el codebase, facilitando comprensión de arquitectura, flujos de datos, y decisiones de implementación.

---

## ESTRUCTURA DE ARCHIVOS

```
backend/app/
├── api/
│   ├── core/
│   │   ├── braille_logic.py         # Módulo 1: Lógica de mapeo Braille
│   │   └── config.py
│   ├── routes/
│   │   ├── translation.py           # Endpoints API
│   │   └── generation.py            # Endpoints de generación
│   └── services/
│       ├── translator.py            # Módulo 2: Funciones de traducción
│       └── generator.py             # Módulo 3: Generación visual
├── schemas/
│   └── translation.py               # Modelos Pydantic
├── main.py                          # Punto de entrada
├── config.py                        # Configuración
├── exceptions.py                    # Excepciones personalizadas
└── logger.py                        # Sistema de logging
```

---

## MÓDULO: braille_logic

**Ubicación**: `backend/app/api/core/braille_logic.py`

**Propósito**: Implementa la lógica fundamental de mapeo entre caracteres españoles y representaciones Braille.

### Visión General

Este módulo contiene la definición completa del sistema Braille español basado en las tres Series Braille estándar. No contiene lógica de negocio compleja; en su lugar, proporciona mapeos de datos (diccionarios) que son consumidos por otros módulos.

### Componentes Principales

#### 1. Constante: SERIE_1_BASE

```python
SERIE_1_BASE = {
    'a': [1],          'b': [1, 2],      'c': [1, 4],
    'd': [1, 4, 5],    'e': [1, 5],      'f': [1, 2, 4],
    'g': [1, 2, 4, 5], 'h': [1, 2, 5],   'i': [2, 4],
    'j': [2, 4, 5]
}
```

**Tipo**: `dict[str, list[int]]`

**Descripción**:
- Define la matriz primitiva de puntos Braille para letras a-j
- Cada clave es una letra del alfabeto español
- Cada valor es una lista de números (1-6) indicando puntos activos
- Base para generación de Series 2 y 3

**Estructura de Puntos Braille** (formato estándar 2×3):
```
Columna 1    Columna 2
   1            4
   2            5
   3            6
```

**Ejemplo de Interpretación**:
- 'a': [1] → Solo punto 1 activo (esquina superior izquierda)
- 'b': [1, 2] → Puntos 1 y 2 activos (columna izquierda)
- 'i': [2, 4] → Puntos 2 y 4 activos (diagonales medias)

**Complejidad**: O(1) acceso directo

#### 2. Función: generar_mapa_completo()

```python
def generar_mapa_completo() -> dict[str, list[int]]:
```

**Tipo de Retorno**: `dict` con claves string y valores `list[int]`

**Descripción**:
Genera de manera programática el diccionario completo de traducción Español → Braille. Esta función es determinística y se ejecuta una sola vez al importar el módulo.

**Algoritmo**:

1. **Inicialización**: Copia SERIE_1_BASE como base

2. **Generación de Serie 2** (letras k-t):
   ```
   Para cada letra en ['k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't']:
       letra_base = Serie1[i]  # Mapeo posicional
       puntos = Serie1[letra_base].copy()
       puntos.append(3)  # Agregar punto 3
       resultado[letra] = sorted(puntos)
   ```
   - Cada letra de Serie 2 es la letra correspondiente de Serie 1 + punto 3
   - Ejemplo: 'k' = 'a' ([1]) + punto 3 = [1, 3]

3. **Generación de Serie 3** (letras u-z):
   ```
   Mapeo: u→a, v→b, w→c, x→d, y→e, z→f
   Para cada par (letra_dest, letra_base):
       puntos = Serie1[letra_base].copy()
       puntos.extend([3, 6])  # Agregar puntos 3 y 6
       resultado[letra_dest] = sorted(puntos)
   ```
   - Cada letra de Serie 3 es la letra correspondiente de Serie 1 + puntos 3 y 6
   - Ejemplo: 'u' = 'a' ([1]) + puntos 3, 6 = [1, 3, 6]

4. **Agregar Caracteres Especiales Españoles**:
   ```
   Especiales = {
       'ñ': [1, 2, 4, 5, 6],  # Letra española
       'á': [1, 2, 3, 5, 6],  # Acentos
       'é': [2, 3, 4, 6],
       'í': [3, 4],
       'ó': [1, 3, 4, 6],
       'ú': [1, 2, 4, 5, 6],  # Conflicto: mismo que ñ
       'ü': [1, 2, 5, 6]      # Diéresis
   }
   ```
   - Nota: ñ y ú comparten la misma representación [1,2,4,5,6]
   - La resolución de conflictos ocurre en REVERSE_BRAILLE_MAP

5. **Agregar Signos de Puntuación**:
   ```
   {'.': [2,5,6], ',': [2], ';': [2,3], ':': [2,5],
    '!': [2,3,5], '?': [2,3,6], '-': [3,6], ...}
   ```

6. **Agregar Prefijos Especiales**:
   ```
   '_NUM_PREFIX_': [3, 4, 5, 6]     # Precede números
   '_CAPS_PREFIX_': [4, 6]          # Precede mayúsculas
   '_MAYUSCULAS_': [6]              # Alternativa
   ```

**Complejidad**:
- Tiempo: O(n) donde n = número total de caracteres (~52)
- Espacio: O(n) para almacenar todas las entradas

**Resultado Final**: 52+ caracteres mapeados (a-z, A-Z, ñ, acentos, dígitos, signos, prefijos)

#### 3. Constante Global: BRAILLE_MAP

```python
BRAILLE_MAP = generar_mapa_completo()
```

**Tipo**: `dict[str, list[int]]`

**Descripción**:
Instancia global generada una sola vez. Se usa en toda la aplicación como fuente de verdad para traducción Español → Braille.

**Acceso**:
```python
from app.api.core.braille_logic import BRAILLE_MAP
BRAILLE_MAP['á']      # Retorna: [1, 2, 3, 5, 6]
BRAILLE_MAP['ñ']      # Retorna: [1, 2, 4, 5, 6]
BRAILLE_MAP[' ']      # Retorna: [] (espacio)
```

**Garantías**:
- Inmutable en tiempo de ejecución (buena práctica: no modificar)
- Predecible: mismo contenido cada ejecución
- Completo: cubre todos los caracteres españoles soportados

#### 4. Función: _generar_reverse_map()

```python
def _generar_reverse_map() -> dict[tuple[int, ...], str]:
```

**Tipo de Retorno**: `dict` donde claves son tuplas de puntos ordenados, valores son caracteres

**Propósito**:
Genera un mapeo inverso Braille → Español. Es necesario porque múltiples caracteres comparten la misma representación Braille (ej. ñ y ú ambos = [1,2,4,5,6]).

**Problema Resuelto - Conflictos de Mapeo**:

```
Representación Braille [1,2,4,5,6] puede ser:
  → 'ñ' (letra española)
  → 'ú' (letra acentuada)

Solución: Sistema de Prioridades
  Prioridad 1 (máxima):  Acentos (á, é, ó, í)
  Prioridad 2:          Letra especial (ñ)
  Prioridad 3:          Letra acentuada (ú)
  Prioridad 4:          Diéresis (ü)
  Prioridad 5:          Signos de puntuación
  Prioridad 6 (mínima):  Letras normales (a-z)
```

**Algoritmo de Resolución**:

```python
priority_dict = {
    'á': 1, 'é': 2, 'ó': 3, 'í': 4,      # Acentos
    'ñ': 5, 'ú': 6, 'ü': 7,              # Especiales
    '.': 10, ',': 11, ... (signos),      # Puntuación
    # Letras normales: no en dict, default 100
}

# Para cada carácter en BRAILLE_MAP:
if braille_points_ya_mapeados:
    existing_priority = priority_dict[existing_char]
    new_priority = priority_dict[new_char]
    if new_priority < existing_priority:  # Menor = mayor prioridad
        reemplazar_con_nuevo
else:
    agregar_nuevo_mapeo
```

**Ejemplo de Aplicación**:

```python
# Al procesar ñ primero:
reverse_map[(1,2,4,5,6)] = 'ñ'  # prioridad 5

# Luego al procesar ú:
existing_priority = 5 (ñ)
new_priority = 6 (ú)
# 6 > 5, así que no reemplazar
# reverse_map[(1,2,4,5,6)] sigue siendo 'ñ'
```

**Acceso**:
```python
from app.api.core.braille_logic import REVERSE_BRAILLE_MAP
REVERSE_BRAILLE_MAP[(1,2,4,5,6)]  # Retorna: 'ñ' (NO 'ú')
REVERSE_BRAILLE_MAP[(1,)]          # Retorna: 'a'
REVERSE_BRAILLE_MAP[(2,3,4,6)]    # Retorna: 'é'
```

**Complejidad**:
- Tiempo: O(n log n) por ordenamiento de tuplas
- Espacio: O(n) para almacenar mapeos

#### 5. Constante Global: REVERSE_BRAILLE_MAP

```python
REVERSE_BRAILLE_MAP = _generar_reverse_map()
```

**Tipo**: `dict[tuple[int, ...], str]`

**Uso**: Empleado en `translator.braille_to_text()` para desambiguar caracteres

---

## MÓDULO: translator

**Ubicación**: `backend/app/api/services/translator.py`

**Propósito**: Proporciona funciones de conversión bidireccional Español ↔ Braille

### Componentes Principales

#### 1. Constantes de Prefijos

```python
PREFIJO_NUMERO = [3, 4, 5, 6]      # Prefijo para números
PREFIJO_MAYUSCULA = [4, 6]         # Prefijo para mayúsculas
```

**Propósito**:
- PREFIJO_NUMERO: Precede a cada secuencia de dígitos para indicarle al lector que los siguientes caracteres son números
- PREFIJO_MAYUSCULA: Precede a cada letra mayúscula para indicarle al lector que la siguiente letra es mayúscula

**Utilización**:
```python
text_to_braille("A1b")
# Proceso:
# 'A': [4,6] (prefijo) + [1] (a) = [[4,6], [1]]
# '1': [3,4,5,6] (prefijo) + [1] (a) = [[3,4,5,6], [1]]
# 'b': [1,2] = [[1,2]]
# Resultado: [[4,6], [1], [3,4,5,6], [1], [1,2]]
```

#### 2. Mapeos de Dígitos

```python
DIGIT_TO_LETTER = {
    '0': 'j', '1': 'a', '2': 'b', '3': 'c', '4': 'd',
    '5': 'e', '6': 'f', '7': 'g', '8': 'h', '9': 'i'
}
LETTER_TO_DIGIT = {v: k for k, v in DIGIT_TO_LETTER.items()}
```

**Justificación**:
- Los dígitos en Braille se representan usando los códigos de la Serie 1 (a-j)
- 0 es excepcional: se mapea a 'j' (10ª letra, para mantener secuencia 1-9 → a-i)
- Estos mapeos permiten detectar automáticamente si un carácter es un número en contexto de número_mode

#### 3. Función: text_to_braille()

```python
def text_to_braille(text: str) -> List[List[int]]:
```

**Firma**:
- **Parámetro**: `text` (str) - Texto en español a convertir
- **Retorno**: `List[List[int]]` - Lista de celdas Braille

**Descripción Completa**:
Convierte texto español a celdas Braille aplicando reglas contextuales complejas.

**Máquina de Estados**:

La función mantiene un estado (`is_number_mode`) que modifica cómo se interpretan los caracteres:

```
Estado: is_number_mode = False (inicial)

Carácter 'a':
  → Buscar en BRAILLE_MAP['a'] = [1]
  → Agregar [1] a resultado
  → Estado sigue False

Carácter 'A' (mayúscula):
  → Agregar PREFIJO_MAYUSCULA [4,6] a resultado
  → Convertir a minúscula: 'a'
  → Buscar en BRAILLE_MAP['a'] = [1]
  → Agregar [1] a resultado

Carácter '1' (dígito):
  → is_number_mode es False, así que:
    - Agregar PREFIJO_NUMERO [3,4,5,6] a resultado
    - Establecer is_number_mode = True
  → Convertir '1' a 'a' usando DIGIT_TO_LETTER
  → Buscar en BRAILLE_MAP['a'] = [1]
  → Agregar [1] a resultado

Carácter '2' (dígito siguiente):
  → is_number_mode es True, así que:
    - NO agregar prefijo (ya estamos en modo número)
  → Convertir '2' a 'b'
  → Agregar BRAILLE_MAP['b'] = [1,2] a resultado

Carácter ' ' (espacio):
  → Establecer is_number_mode = False
  → Agregar BRAILLE_MAP[' '] = [] (celda vacía)
```

**Algoritmo Paso a Paso**:

```
1. Inicializar result = [], is_number_mode = False, i = 0

2. Mientras i < len(text):

   a) Si text[i] es dígito:
      - Si NO is_number_mode:
        * Agregar PREFIJO_NUMERO a result
        * Establecer is_number_mode = True
      - Convertir dígito a letra: letter = DIGIT_TO_LETTER[text[i]]
      - Agregar BRAILLE_MAP[letter] a result
      - Continuar siguiente

   b) Sino si text[i] es '.' o ',' (separadores numéricos):
      - Si is_number_mode:
        * Agregar BRAILLE_MAP[text[i]] a result
        * Continuar siguiente

   c) Sino si text[i] no es dígito:
      - Establecer is_number_mode = False

   d) Si text[i] es espacio:
      - Agregar BRAILLE_MAP[' '] a result
      - Continuar siguiente

   e) Si text[i] es mayúscula:
      - Agregar PREFIJO_MAYUSCULA a result
      - Convertir a minúscula: c = text[i].lower()
      - Si c en BRAILLE_MAP:
        * Agregar BRAILLE_MAP[c] a result
      - Continuar siguiente

   f) Si text[i] en BRAILLE_MAP:
      - Agregar BRAILLE_MAP[text[i]] a result

   g) Continuar siguiente

3. Retornar result
```

**Ejemplos de Ejecución**:

Ejemplo 1: Texto simple
```python
text_to_braille("hola")
# Iteraciones:
# 'h': [1,2,5]
# 'o': [1,3,5]
# 'l': [1,2,3]
# 'a': [1]
# Resultado: [[1,2,5], [1,3,5], [1,2,3], [1]]
```

Ejemplo 2: Con mayúsculas
```python
text_to_braille("Hola")
# Iteraciones:
# 'H' (mayúscula):
#   Agregar [4,6] (prefijo)
#   Convertir a 'h'
#   Agregar [1,2,5]
# 'o': [1,3,5]
# 'l': [1,2,3]
# 'a': [1]
# Resultado: [[4,6], [1,2,5], [1,3,5], [1,2,3], [1]]
```

Ejemplo 3: Con números
```python
text_to_braille("hola 123")
# Iteraciones:
# 'h': [1,2,5]
# 'o': [1,3,5]
# 'l': [1,2,3]
# 'a': [1]
# ' ': []
# '1': is_number_mode=False
#   Agregar [3,4,5,6] (prefijo)
#   is_number_mode=True
#   '1'→'a': [1]
# '2': is_number_mode=True
#   '2'→'b': [1,2]
# '3': is_number_mode=True
#   '3'→'c': [1,4]
# Resultado: [[1,2,5], [1,3,5], [1,2,3], [1], [], 
#             [3,4,5,6], [1], [1,2], [1,4]]
```

**Manejo de Errores**:
- Caracteres no reconocidos: Se ignoran silenciosamente (sin lanzar excepción)
- Ejemplo: Saltos de línea (\n) se descartan
- Filosofía: "Ser permisivo en entrada"

**Complejidad**:
- Tiempo: O(n) donde n es longitud del texto
- Espacio: O(m) donde m es número de celdas (típicamente ≈ n)

#### 4. Función: braille_to_text()

```python
def braille_to_text(braille_cells: List[List[int]]) -> str:
```

**Firma**:
- **Parámetro**: `braille_cells` (List[List[int]]) - Celdas Braille a convertir
- **Retorno**: `str` - Texto español reconstruido

**Descripción**:
Convierte celdas Braille nuevamente a texto español. Es la operación inversa de `text_to_braille()`.

**Máquina de Estados**:

Mantiene dos estados:
- `is_number_mode`: Si True, próximas letras a-j se convierten a dígitos 1-0
- `capitalize_next`: Si True, próximo carácter alfabético se convierte a mayúscula

```
Estado Inicial: is_number_mode=False, capitalize_next=False

Si celda == PREFIJO_NUMERO [3,4,5,6]:
  → Establecer is_number_mode=True
  → Pasar a siguiente celda (sin agregar carácter)

Si celda == PREFIJO_MAYUSCULA [4,6]:
  → Establecer capitalize_next=True
  → Pasar a siguiente celda (sin agregar carácter)

Si celda == []:
  → Agregar espacio ' '
  → Establecer is_number_mode=False

Si celda en REVERSE_BRAILLE_MAP:
  → Obtener carácter: char = REVERSE_BRAILLE_MAP[celda]
  → Si is_number_mode y char en 'abcdefghij':
    * Convertir a dígito: char = LETTER_TO_DIGIT[char]
    * Salida: '1' (si char era 'a'), etc.
  → Si capitalize_next y char es alfabético:
    * Convertir a mayúscula: char = char.upper()
    * Establecer capitalize_next=False
  → Agregar char a resultado

Si celda no en REVERSE_BRAILLE_MAP:
  → Agregar '?' (placeholder para punto no reconocido)
```

**Algoritmo**:

```
1. Inicializar result = "", is_number_mode=False, capitalize_next=False, i=0

2. Mientras i < len(braille_cells):

   a) celda = braille_cells[i]
   b) celda_tuple = tuple(sorted(celda))

   c) Si celda_tuple == PREFIJO_NUMERO:
      - is_number_mode = True
      - Continuar siguiente

   d) Si celda_tuple == PREFIJO_MAYUSCULA:
      - capitalize_next = True
      - Continuar siguiente

   e) Si celda_tuple vacía:
      - Agregar ' ' a result
      - is_number_mode = False
      - Continuar siguiente

   f) char = REVERSE_BRAILLE_MAP.get(celda_tuple, None)

   g) Si char es None:
      - char = '?'

   h) Si is_number_mode y char en LETTER_TO_DIGIT:
      - char = LETTER_TO_DIGIT[char]
      - is_number_mode sigue activo para próximos caracteres

   i) Si capitalize_next y char.isalpha():
      - char = char.upper()
      - capitalize_next = False

   j) Agregar char a result

   k) Continuar siguiente

3. Retornar result
```

**Ejemplos de Ejecución**:

Ejemplo 1: Traducción simple
```python
braille_to_text([[1,2,5], [1,3,5], [1,2,3], [1]])
# Iteraciones:
# [1,2,5] → 'h'
# [1,3,5] → 'o'
# [1,2,3] → 'l'
# [1] → 'a'
# Resultado: "hola"
```

Ejemplo 2: Con prefijo de mayúscula
```python
braille_to_text([[4,6], [1,2,5], [1,3,5], [1,2,3], [1]])
# Iteraciones:
# [4,6] → Prefijo mayúscula, capitalize_next=True
# [1,2,5] → 'h', capitalize_next=True → 'H', capitalize_next=False
# [1,3,5] → 'o'
# [1,2,3] → 'l'
# [1] → 'a'
# Resultado: "Hola"
```

Ejemplo 3: Con números
```python
braille_to_text([[3,4,5,6], [1], [1,2]])
# Iteraciones:
# [3,4,5,6] → Prefijo número, is_number_mode=True
# [1] → 'a', is_number_mode=True → '1'
# [1,2] → 'b', is_number_mode=True → '2'
# Resultado: "12"
```

**Desambigüación Automática**:
El REVERSE_BRAILLE_MAP resuelve conflictos automáticamente:
```python
braille_to_text([[1,2,4,5,6]])
# [1,2,4,5,6] normalizados a (1,2,4,5,6)
# REVERSE_BRAILLE_MAP[(1,2,4,5,6)] = 'ñ' (prioridad > 'ú')
# Resultado: "ñ" (NO "ú")
```

**Complejidad**:
- Tiempo: O(n) donde n es número de celdas
- Espacio: O(m) donde m es longitud del texto resultante

---

## MÓDULO: generator

**Ubicación**: `backend/app/api/services/generator.py`

**Propósito**: Generar representaciones visuales de Braille (PNG, PDF)

### Clase: BrailleImageGenerator

#### Descripción
Generador de imágenes PNG con celdas Braille renderizadas visualmente. Cada celda se dibuja como 6 círculos posicionados en una grilla 2×3.

#### Configuración Global

```python
CELL_WIDTH = 40      # Ancho de celda (píxeles)
CELL_HEIGHT = 60     # Alto de celda (píxeles)
DOT_RADIUS = 6       # Radio de puntos (píxeles)
MARGIN = 20          # Margen alrededor (píxeles)
SPACING = 10         # Espacio entre celdas (píxeles)
```

#### Constructor

```python
def __init__(self, cell_width: int = 40, cell_height: int = 60):
```

**Parámetros**:
- `cell_width`: Personalización de ancho (por defecto 40px)
- `cell_height`: Personalización de alto (por defecto 60px)

**Atributos Inicializados**:
```python
self.cell_width = cell_width       # Ancho de celda
self.cell_height = cell_height     # Alto de celda
self.dot_radius = DOT_RADIUS       # 6px
self.margin = MARGIN               # 20px
self.spacing = SPACING             # 10px
```

#### Método: _get_dot_position()

```python
def _get_dot_position(self, dot_number: int) -> Tuple[int, int]:
```

**Propósito**: Calcular coordenadas (x, y) de un punto Braille dentro de una celda

**Lógica**:
```
Puntos Braille distribuidos en grilla 2×3:

Punto 1: Columna izquierda, fila 1 → (cell_width/3, cell_height/4)
Punto 2: Columna izquierda, fila 2 → (cell_width/3, cell_height*2/4)
Punto 3: Columna izquierda, fila 3 → (cell_width/3, cell_height*3/4)
Punto 4: Columna derecha, fila 1   → (cell_width*2/3, cell_height/4)
Punto 5: Columna derecha, fila 2   → (cell_width*2/3, cell_height*2/4)
Punto 6: Columna derecha, fila 3   → (cell_width*2/3, cell_height*3/4)
```

**Fórmulas**:
```python
col = 0 if dot_number in [1,2,3] else 1     # 0 = izquierda, 1 = derecha
row = (dot_number - 1) % 3                   # 0, 1, 2
x = cell_width//3 + col * (cell_width//3)
y = cell_height//4 + row * (cell_height//4)
```

**Ejemplo**:
Para `cell_width=40, cell_height=60`:
- Punto 1: x=13, y=15 (esquina superior izquierda)
- Punto 6: x=26, y=45 (esquina inferior derecha)

#### Método: _draw_braille_cell()

```python
def _draw_braille_cell(self, draw, cell, offset_x, offset_y):
```

**Propósito**: Renderizar una celda Braille individual

**Proceso**:
```
1. Para cada punto 1-6:
   a) Calcular posición relativa: _get_dot_position(punto)
   b) Aplicar offset: x_global = x_relativo + offset_x
   c) Si punto en `cell` (activo):
      - Dibujar círculo negro relleno
   d) Si punto no en `cell` (inactivo):
      - Dibujar círculo blanco con contorno gris
```

**Ejemplo Gráfico**:
Para `cell=[1,2,4]` (puntos 1, 2, 4 activos):
```
●  ○         (puntos 1 y 4, 1 activo)
●  ●         (puntos 2 y 5, ambos mostrados pero solo 2 activo)
○  ○         (puntos 3 y 6, ambos inactivos)
```

#### Método: generate_image()

```python
def generate_image(self, text: str, include_text: bool = True, 
                   mirror: bool = False) -> BytesIO:
```

**Parámetros**:
- `text` (str): Texto a convertir a Braille
- `include_text` (bool): Si agregar encabezado con texto (Default: True)
- `mirror` (bool): Si generar imagen espejada (Default: False)

**Retorno**: `BytesIO` - Buffer de imagen PNG en memoria

**Proceso**:

1. **Conversión a Braille**:
   ```python
   braille_cells = text_to_braille(text)  # Usar módulo translator
   ```

2. **Aplicar Espejo (si requested)**:
   ```python
   if mirror:
       mirror_map = {1:4, 2:5, 3:6, 4:1, 5:2, 6:3}
       braille_cells = [
           sorted([mirror_map[dot] for dot in cell])
           for cell in braille_cells
       ]
   # Invierte cada punto dentro de la celda
   ```

3. **Calcular Dimensiones**:
   ```python
   num_cells = len(braille_cells)
   img_width = num_cells * (cell_width + spacing) + 2*margin
   img_height = cell_height + 2*margin
   if include_text:
       img_height += 40  # Espacio para texto
   ```
   - Ejemplo: 5 celdas → width = 5*50 + 40 = 290px

4. **Crear Imagen**:
   ```python
   img = Image.new('RGB', (img_width, img_height), 'white')
   draw = ImageDraw.Draw(img)
   ```

5. **Renderizar Texto (si requested)**:
   ```python
   font = ImageFont.truetype("arial.ttf", 20)  # Fuente truetype
   text_bbox = draw.textbbox((0,0), text, font)
   text_x = (img_width - text_width) // 2  # Centrar
   draw.text((text_x, margin), text, fill='black', font)
   ```

6. **Renderizar Celdas Braille**:
   ```python
   y_offset = margin + 40 if include_text else margin
   for i, cell in enumerate(braille_cells):
       x_offset = margin + i*(cell_width + spacing)
       _draw_braille_cell(draw, cell, x_offset, y_offset)
   ```

7. **Guardar como PNG**:
   ```python
   buffer = BytesIO()
   img.save(buffer, format='PNG')
   buffer.seek(0)  # Posicionar al inicio para lectura
   return buffer
   ```

**Ejemplo de Uso**:
```python
generator = BrailleImageGenerator()
buffer = generator.generate_image("Hola", include_text=True, mirror=False)

# Guardar a archivo
with open("hola.png", "wb") as f:
    f.write(buffer.getvalue())

# O usar directamente en respuesta HTTP
return StreamingResponse(buffer, media_type="image/png")
```

**Modo Espejo - Propósito**:
Permite que una persona vidente vea la imagen de Braille como la vería un usuario no vidente si tocara la página desde el lado opuesto. Útil para verificación de documentos.

---

## PATRONES DE DISEÑO

### Patrón 1: Máquina de Estados

**Ubicación**: `text_to_braille()` y `braille_to_text()`

**Propósito**: Manejar cambios de contexto durante conversión

**Estados**:
- `is_number_mode`: Boolean que indica si estamos dentro de una secuencia numérica
- `capitalize_next`: Boolean que indica si el próximo carácter debe capitalizarse

**Transiciones**:
```
text_to_braille:
  Número → Número: Mantener is_number_mode
  Número → No-número: Salir is_number_mode
  No-número → Número: Entrar is_number_mode, agregar prefijo

braille_to_text:
  Prefijo-número → Caracteres: Activar is_number_mode
  Espacio: Desactivar is_number_mode
  Prefijo-mayúscula → Carácter: Activar capitalize_next una vez
```

### Patrón 2: Mapeo de Datos

**Ubicación**: `BRAILLE_MAP`, `REVERSE_BRAILLE_MAP`

**Propósito**: Separar datos de lógica

**Ventajas**:
- Mantenibilidad: Cambiar mapeo no requiere cambiar código
- Testabilidad: Datos son verificables independientemente
- Performance: O(1) lookup en lugar de búsqueda lineal

### Patrón 3: Resolución de Conflictos por Prioridades

**Ubicación**: `_generar_reverse_map()`

**Propósito**: Manejar múltiples caracteres con misma representación Braille

**Estrategia**:
```
priority_dict[carácter] = número
Menor número = mayor prioridad

En conflicto: mantener carácter con menor número
```

### Patrón 4: Factory para Generador

**Ubicación**: `BrailleImageGenerator.__init__()`

**Propósito**: Permitir customización de parámetros de renderizado

**Beneficio**: Sin factory, necesitaríamos parámetros globales no-configurables

---

## GUÍA DE USO

### Uso Básico: Texto a Braille

```python
from app.api.services.translator import text_to_braille

result = text_to_braille("Hola")
print(result)
# [[4,6], [1,2,5], [1,3,5], [1,2,3], [1]]
```

### Uso Básico: Braille a Texto

```python
from app.api.services.translator import braille_to_text

result = braille_to_text([[1,2,5], [1,3,5], [1,2,3], [1]])
print(result)
# "hola"
```

### Uso Avanzado: Generar Imagen

```python
from app.api.services.generator import BrailleImageGenerator

gen = BrailleImageGenerator(cell_width=50, cell_height=70)
buffer = gen.generate_image("Hola", include_text=True, mirror=True)

# Usar buffer en respuesta HTTP
from fastapi import StreamingResponse
return StreamingResponse(buffer, media_type="image/png")
```

### Acceder Directamente a Mapeos

```python
from app.api.core.braille_logic import BRAILLE_MAP, REVERSE_BRAILLE_MAP

# Traducción directa
puntos = BRAILLE_MAP['ñ']  # [1,2,4,5,6]

# Traducción inversa
carácter = REVERSE_BRAILLE_MAP[(1,)]  # 'a'
```

---

## EJEMPLOS PRÁCTICOS

### Ejemplo 1: Texto con Números y Mayúsculas

```python
text = "Piso 3A"
result = text_to_braille(text)

# Proceso:
# P (mayúscula): [4,6] (prefijo) + [1,2,3,5] (p)
# i: [2,4]
# s: [2,3,4]
# o: [1,3,5]
# (espacio): []
# 3 (número): [3,4,5,6] (prefijo) + [1,4] (c)
# A (mayúscula): [4,6] (prefijo) + [1] (a)

# Salida: [[4,6], [1,2,3,5], [2,4], [2,3,4], [1,3,5], [], [3,4,5,6], [1,4], [4,6], [1]]
```

### Ejemplo 2: Caracteres Especiales Españoles

```python
text = "Español"
result = text_to_braille(text)

# E: [4,6] + [2,3,4,6] (é)
# s: [2,3,4]
# p: [1,2,3,5]
# a: [1]
# ñ: [1,2,4,5,6]  # Letra especial
# o: [1,3,5]
# l: [1,2,3]
```

### Ejemplo 3: Impresión en Espejo

```python
text = "ABC"
result_normal = text_to_braille(text)
# A: [[4,6], [1]]
# B: [[4,6], [1,2]]
# C: [[4,6], [1,4]]

generator = BrailleImageGenerator()
buffer = generator.generate_image(text, mirror=True)

# La imagen resultante muestra:
# - A invertida (puntos 4,1 → 1,4... en la visualización)
# - Útil para verificar que se vería correcto desde el lado opuesto
```

---

## CONCLUSIONES

Esta documentación técnica proporciona una referencia completa del código fuente Python del Proyecto Transcriptor Braille. Cubre:

1. **Arquitectura**: Estructura de módulos y responsabilidades
2. **Lógica**: Algoritmos detallados paso a paso
3. **API**: Firmas de funciones y tipos de datos
4. **Patrones**: Estrategias de diseño empleadas
5. **Ejemplos**: Casos prácticos de uso

El código está diseñado para ser mantenible, testeable, y extensible, facilitando futuras mejoras y ampliaciones de funcionalidad.

---

**Documento Generado**: Enero 22, 2026
**Versión**: 1.0
**Formato**: Inspirado en JavaDoc adaptado a Python
**Estado**: Documentación Técnica Completa y Detallada
