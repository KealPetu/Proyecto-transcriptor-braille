"""
Utilidades comunes para la aplicación.

Funciones auxiliares y helpers reutilizables:
    - Validación
    - Formateo
    - Conversión de datos
    - Utilidades de string

Uso:
    from app.utils import sanitize_text, format_braille_cells
"""


def sanitize_text(text: str, max_length: int = 1000) -> str:
    """
    Sanitiza texto de entrada.
    
    Args:
        text (str): Texto a sanitizar
        max_length (int): Longitud máxima permitida
    
    Returns:
        str: Texto sanitizado
    
    Raises:
        ValueError: Si texto está vacío o excede límite
    """
    if not text:
        raise ValueError("Texto no puede estar vacío")
    
    text = text.strip()
    
    if len(text) > max_length:
        raise ValueError(f"Texto excede {max_length} caracteres")
    
    return text


def format_braille_cells(cells: list) -> str:
    """
    Formatea celdas Braille para visualización/logging.
    
    Args:
        cells (list): Lista de celdas [[1,2,3], [1], ...]
    
    Returns:
        str: Representación formateada "123|1|..."
    
    Examples:
        >>> format_braille_cells([[1,2,3], [1], []])
        "123|1|_"
    """
    return "|".join(
        "".join(map(str, cell)) if cell else "_"
        for cell in cells
    )


def validate_braille_cell(cell: list) -> bool:
    """
    Valida que una celda Braille sea correcta.
    
    Args:
        cell (list): Celda a validar
    
    Returns:
        bool: True si es válida
    
    Examples:
        >>> validate_braille_cell([1, 2, 3])
        True
        >>> validate_braille_cell([1, 7])  # 7 está fuera de rango
        False
    """
    if not isinstance(cell, list):
        return False
    
    if not cell:  # Lista vacía es válida (representa espacio)
        return True
    
    return all(isinstance(p, int) and 1 <= p <= 6 for p in cell)


def truncate_text(text: str, length: int = 50, suffix: str = "...") -> str:
    """
    Trunca texto a una longitud específica.
    
    Args:
        text (str): Texto a truncar
        length (int): Longitud máxima
        suffix (str): Sufijo si se trunca
    
    Returns:
        str: Texto truncado
    
    Examples:
        >>> truncate_text("Hola mundo esto es largo", 10)
        "Hola mun..."
    """
    if len(text) <= length:
        return text
    return text[:length - len(suffix)] + suffix
