"""
Módulo de Generación de Representaciones Visuales de Braille.

Proporciona servicios para generar visualizaciones de texto en Braille
para uso en señaléticas accesibles, material educativo y documentación.

Formatos Soportados:
    - PNG: Imágenes rasterizadas con celdas Braille visuales
    - PDF: Documentos de página completa con texto y Braille

Características:
    - Renderizado de celdas Braille estándar (6 puntos)
    - Diseño responsive con configuración de tamaños
    - Generación de PDFs multi-página automática
    - Streaming de respuestas para integración con APIs
    - Soporte para títulos y textos descriptivos

Configuración de Renderizado:
    - CELL_WIDTH: Ancho de celda en píxeles (PNG) o milímetros (PDF)
    - CELL_HEIGHT: Alto de celda en píxeles (PNG) o milímetros (PDF)
    - DOT_RADIUS: Radio de puntos Braille
    - MARGIN: Margen alrededor del contenido
    - SPACING: Espacio entre celdas

Ejemplo:
    >>> from generator import generate_braille_image
    >>> image_buffer = generate_braille_image("Salida", include_text=True)
    >>> # image_buffer puede guardarse como archivo PNG
    
Autor: Isaac
"""

from typing import List, Tuple
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

from .translator import text_to_braille


# Configuración de tamaños para renderizado
CELL_WIDTH = 40  # Ancho de cada celda Braille en píxeles
CELL_HEIGHT = 60  # Alto de cada celda Braille en píxeles
DOT_RADIUS = 6  # Radio de cada punto Braille
MARGIN = 20  # Margen alrededor de la imagen
SPACING = 10  # Espacio entre celdas


class BrailleImageGenerator:
    """
    Generador de imágenes PNG con representación visual de celdas Braille.
    
    Convierte texto en español a representación gráfica de Braille usando
    la biblioteca PIL (Pillow). Cada carácter se renderiza como una celda
    Braille de 6 puntos (disposición estándar 2x3).
    
    Disposición de Puntos Braille:
        1 4
        2 5
        3 6
    
    Los puntos se renderizan como:
        - Puntos activos: Círculos negros rellenos
        - Puntos inactivos: Círculos grises con contorno
    
    Configuración Personalizable:
        - cell_width: Ancho de cada celda (en píxeles)
        - cell_height: Alto de cada celda (en píxeles)
        - dot_radius: Radio de cada punto (en píxeles)
        - margin: Margen alrededor de la imagen
        - spacing: Espacio entre celdas
    
    Ejemplo:
        >>> generator = BrailleImageGenerator(cell_width=40, cell_height=60)
        >>> image_buffer = generator.generate_image("Hola")
        >>> # image_buffer es BytesIO que puede guardarse como PNG
    """
    
    def __init__(self, cell_width: int = CELL_WIDTH, cell_height: int = CELL_HEIGHT):
        """
        Inicializa el generador de imágenes PNG.
        
        Args:
            cell_width (int): Ancho de cada celda Braille en píxeles.
                            Default: 40px
            cell_height (int): Alto de cada celda Braille en píxeles.
                             Default: 60px
        
        Attributes:
            cell_width: Ancho configurado para renderizado
            cell_height: Alto configurado para renderizado
            dot_radius: Radio de puntos (6px por defecto)
            margin: Margen alrededor de imagen (20px)
            spacing: Espacio entre celdas (10px)
        
        Note:
            Los valores por defecto producen celdas visibles y legibles.
            Para impresión de alta calidad, aumentar cell_width/height.
        """
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.dot_radius = DOT_RADIUS
        self.margin = MARGIN
        self.spacing = SPACING
    
    def _get_dot_position(self, dot_number: int) -> Tuple[int, int]:
        """
        Calcula la posición (x, y) de un punto Braille dentro de una celda.
        
        Distribución de puntos en la celda (6 puntos, disposición 2x3):
            Punto 1: Columna izquierda, fila superior
            Punto 2: Columna izquierda, fila media
            Punto 3: Columna izquierda, fila inferior
            Punto 4: Columna derecha, fila superior
            Punto 5: Columna derecha, fila media
            Punto 6: Columna derecha, fila inferior
        
        Cálculo:
            - Columna: 0 si punto en [1,2,3], 1 si punto en [4,5,6]
            - Fila: (punto-1) % 3, produce 0, 1, 2
            - Coordenadas: Distribuidas uniformemente en la celda
        
        Args:
            dot_number (int): Número del punto Braille (1-6)
        
        Returns:
            Tuple[int, int]: Coordenadas (x, y) del punto relativas a la
                           esquina superior izquierda de la celda.
        
        Raises:
            Implícitamente maneja números fuera de rango (1-6)
        
        Example:
            >>> gen = BrailleImageGenerator(cell_width=40, cell_height=60)
            >>> gen._get_dot_position(1)  # Esquina superior izquierda
            (13, 15)
            >>> gen._get_dot_position(6)  # Esquina inferior derecha
            (26, 45)
        """
        # Posiciones en columnas
        col = 0 if dot_number in [1, 2, 3] else 1
        row = (dot_number - 1) % 3
        
        x = self.cell_width // 3 + col * (self.cell_width // 3)
        y = self.cell_height // 4 + row * (self.cell_height // 4)
        
        return (x, y)
    
    def _draw_braille_cell(self, draw: ImageDraw.Draw, cell: List[int], 
                          offset_x: int, offset_y: int):
        """
        Dibuja una celda Braille individual en la imagen.
        
        Renderiza todos los 6 puntos posibles de una celda Braille:
        - Puntos activos [en `cell`]: Círculos negros rellenos
        - Puntos inactivos [no en `cell`]: Círculos vacíos con contorno gris
        
        Proceso:
            1. Iterar sobre puntos 1-6
            2. Calcular posición relativa del punto
            3. Aplicar offset (posición de la celda en la imagen)
            4. Dibujar círculo relleno (negro) o vacío (gris) según estado
        
        Args:
            draw (ImageDraw.Draw): Objeto dibujo de PIL para renderizar
            cell (List[int]): Lista de puntos activos (ej. [1, 2, 4])
            offset_x (int): Desplazamiento horizontal de la celda (en píxeles)
            offset_y (int): Desplazamiento vertical de la celda (en píxeles)
        
        Returns:
            None (modifica `draw` directamente)
        
        Side Effects:
            Dibuja 6 círculos en el objeto ImageDraw proporcionado.
        
        Example:
            >>> from PIL import Image, ImageDraw
            >>> img = Image.new('RGB', (100, 100), 'white')
            >>> draw = ImageDraw.Draw(img)
            >>> gen = BrailleImageGenerator()
            >>> gen._draw_braille_cell(draw, [1, 2, 4], 20, 20)
            >>> # Dibuja una celda Braille con puntos 1, 2, 4 activos
        """
        # Dibujar todos los 6 puntos posibles (vacíos o llenos)
        for dot in range(1, 7):
            x, y = self._get_dot_position(dot)
            x += offset_x
            y += offset_y
            
            # Si el punto está activo, dibujar relleno, sino solo contorno
            if dot in cell:
                draw.ellipse(
                    [x - self.dot_radius, y - self.dot_radius,
                     x + self.dot_radius, y + self.dot_radius],
                    fill='black',
                    outline='black'
                )
            else:
                draw.ellipse(
                    [x - self.dot_radius, y - self.dot_radius,
                     x + self.dot_radius, y + self.dot_radius],
                    fill='white',
                    outline='gray'
                )
    
    def generate_image(self, text: str, include_text: bool = True, mirror: bool = False) -> BytesIO:
        """
        Genera una imagen PNG con representación visual de texto en Braille.
        
        Proceso:
            1. Convertir texto español a celdas Braille
            2. Calcular dimensiones de imagen basadas en cantidad de celdas
            3. Crear imagen en blanco con PIL
            4. Dibujar texto original (opcional) en la parte superior
            5. Dibujar cada celda Braille debajo del texto
            6. Guardar como PNG en BytesIO
        
        Dimensiones Calculadas:
            - Ancho: (num_celdas × (cell_width + spacing)) + 2×margin
            - Alto: cell_height + 2×margin + (40px extra si include_text)
        
        Args:
            text (str): Texto en español a convertir a Braille.
                       Puede contener: letras, números, acentos, signos.
            include_text (bool): Si True, incluir el texto original como
                               encabezado de la imagen (Default: True)
            mirror (bool): Si True, generar imagen en modo espejo
                         (invertida horizontalmente) (Default: False)
        
        Returns:
            BytesIO: Buffer de imagen PNG en memoria, posicionado al inicio
                    (seek(0)) para lectura. Puede ser:
                    - Guardado en archivo: buffer.save(file)
                    - Enviado como respuesta HTTP con media_type="image/png"
                    - Convertido a bytes: buffer.getvalue()
        
        Raises:
            Implícitamente puede fallar si:
            - Las fuentes ("arial.ttf") no están disponibles (usa default)
            - Memoria insuficiente para imagen muy grande
        
        Side Effects:
            - Carga fuente "arial.ttf" si está disponible
            - Si no: usa fuente por defecto (más pequeña)
        
        Example:
            >>> gen = BrailleImageGenerator()
            >>> buffer = gen.generate_image("Hola", mirror=True)
            >>> # Guardar como archivo
            >>> with open("hola_espejo.png", "wb") as f:
            ...     f.write(buffer.getvalue())
            >>> # O reutilizar buffer
            >>> buffer.seek(0)
            >>> img = Image.open(buffer)
        
        Note:
            - Imagen siempre tiene fondo blanco
            - Texto original en negro (si include_text=True)
            - Celdas Braille en negro/gris
            - Modo espejo invierte horizontalmente toda la imagen
            - Ideal para impresión o visualización web
        """
        # Convertir texto a celdas Braille
        braille_cells = text_to_braille(text)
        
        # Si modo espejo, invertir cada celda
        if mirror:
            mirror_map = {1: 4, 2: 5, 3: 6, 4: 1, 5: 2, 6: 3}
            braille_cells = [
                sorted([mirror_map[dot] for dot in cell])
                for cell in braille_cells
            ]
        
        # Calcular dimensiones de la imagen
        num_cells = len(braille_cells)
        img_width = (num_cells * (self.cell_width + self.spacing)) + (2 * self.margin)
        img_height = self.cell_height + (2 * self.margin)
        
        if include_text:
            img_height += 40  # Espacio extra para el texto
        
        # Crear imagen en blanco
        img = Image.new('RGB', (img_width, img_height), 'white')
        draw = ImageDraw.Draw(img)
        
        # Dibujar texto original si se solicita
        if include_text:
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except:
                font = ImageFont.load_default()
            
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_x = (img_width - text_width) // 2
            draw.text((text_x, self.margin), text, fill='black', font=font)
        
        # Dibujar cada celda Braille
        y_offset = self.margin + (40 if include_text else 0)
        for i, cell in enumerate(braille_cells):
            x_offset = self.margin + i * (self.cell_width + self.spacing)
            self._draw_braille_cell(draw, cell, x_offset, y_offset)
        
        # Si modo espejo, invertir la imagen
        if mirror:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        
        # Guardar en BytesIO
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        return buffer


class BraillePDFGenerator:
    """
    Generador de documentos PDF con representación visual de Braille.
    
    Crea PDFs de página completa con:
    - Título personalizable
    - Texto original en español
    - Representación visual de celdas Braille
    - Manejo automático de saltos de línea y múltiples páginas
    - Información de generación (metadatos)
    
    Formato de Página:
    ┌─────────────────────────────────┐
    │         Título (24pt)           │
    │                                 │
    │ Texto:                          │
    │ Texto original (16pt bold)      │
    │                                 │
    │ Representación Braille:         │
    │ [Celdas Braille visuales]       │
    │ [Salto de línea automático]     │
    │                                 │
    │ Generado por: Transcriptor...   │
    │ Total de celdas: N              │
    └─────────────────────────────────┘
    
    Características:
    - Tamaño de página: A4 (210×297 mm) por defecto
    - Saltos de línea automáticos cuando celdas alcanzan margen derecho
    - Nuevas páginas automáticas cuando se agota espacio vertical
    - Espaciado configurable entre celdas (15mm)
    - Metadatos de generación en pie de página
    
    Ejemplo:
        >>> gen = BraillePDFGenerator()
        >>> pdf_buffer = gen.generate_pdf("Salida de emergencia", 
        ...                                title="Señalética - Salida")
    """
    
    def __init__(self, page_size=A4):
        """
        Inicializa el generador de PDF.
        
        Args:
            page_size: Tamaño de página (Default: A4 = 210×297 mm)
                      Alternativas: letter, legal, A3, A5, etc.
        
        Attributes:
            page_size: Tupla (ancho, alto) del tamaño de página en puntos
        
        Example:
            >>> from reportlab.lib.pagesizes import letter
            >>> gen = BraillePDFGenerator(page_size=letter)  # Tamaño US Letter
        """
        self.page_size = page_size
    
    def generate_pdf(self, text: str, title: str = "Señalética Braille", mirror: bool = False) -> BytesIO:
        """
        Genera un documento PDF con texto original y representación Braille.
        
        Estructura del documento:
            1. Título centrado (24pt, negrita)
            2. Etiqueta "Texto:" (18pt)
            3. Texto original (16pt, negrita, centrado)
            4. Etiqueta "Representación Braille:" (18pt)
            5. Celdas Braille visuales (organizadas en filas)
            6. Pie de página: Generador + cantidad de celdas
        
        Lógica de Saltos de Línea:
            - Se detecta si celda siguiente cabe en línea actual
            - Si no cabe: reiniciar línea en margen izquierdo
            - Si espacio vertical insuficiente: crear nueva página
            - Espaciado entre celdas: 15mm
            - Alto de línea: 30mm
        
        Args:
            text (str): Texto en español a convertir a PDF.
                       Se convierte internamente a celdas Braille.
            title (str): Título del documento (Default: "Señalética Braille")
                        Aparece centrado en la parte superior.
            mirror (bool): Si True, generar PDF en modo espejo
                         (celdas invertidas horizontalmente) (Default: False)
        
        Returns:
            BytesIO: Buffer PDF en memoria, posicionado al inicio (seek(0)).
                    Puede ser:
                    - Guardado en archivo: buffer.save(file) o buffer.getvalue()
                    - Enviado como respuesta HTTP (media_type="application/pdf")
                    - Abierto con PDF reader externo
        
        Raises:
            Implícitamente puede fallar si:
            - Memoria insuficiente para PDF muy grande
            - Problema con ReportLab en generación de canvas
        
        Side Effects:
            - Convierte texto a celdas Braille (llama text_to_braille)
            - Crea múltiples páginas si hay muchas celdas
            - Buffer es buscado a posición 0 para lectura
        
        Example:
            >>> gen = BraillePDFGenerator()
            >>> buffer = gen.generate_pdf("Salida", title="Salida de Emergencia", mirror=True)
            >>> # Guardar como archivo
            >>> with open("salida_espejo.pdf", "wb") as f:
            ...     f.write(buffer.getvalue())
            >>> # O enviar en respuesta HTTP
            >>> # return StreamingResponse(buffer, media_type="application/pdf")
        
        Note:
            - Formato ideal para impresión
            - A4 es 210×297 mm (595×842 puntos)
            - Márgenes: 50 puntos (aproximadamente 18mm)
            - Fuentes: Helvetica (estándar, siempre disponible)
            - Modo espejo: Invierte las celdas Braille horizontalmente
        """
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=self.page_size)
        width, height = self.page_size
        
        # Título
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(width / 2, height - 50, title)
        
        # Texto original
        c.setFont("Helvetica", 18)
        c.drawCentredString(width / 2, height - 100, "Texto:")
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width / 2, height - 130, text)
        
        # Dibujar representación Braille
        c.setFont("Helvetica", 18)
        c.drawCentredString(width / 2, height - 180, "Representación Braille:")
        
        # Convertir a Braille
        braille_cells = text_to_braille(text)
        
        # Si modo espejo, invertir cada celda
        if mirror:
            mirror_map = {1: 4, 2: 5, 3: 6, 4: 1, 5: 2, 6: 3}
            braille_cells = [
                sorted([mirror_map[dot] for dot in cell])
                for cell in braille_cells
            ]
            # También invertir el orden de las celdas
            braille_cells = braille_cells[::-1]

        # Dibujar celdas Braille
        start_x = 100
        current_x = start_x
        current_y = height - 250
        cell_spacing = 15 * mm
        line_height = 30 * mm
        right_margin_limit = width - 100
        
        for cell in braille_cells:
            
            # Verificamos si la celda ACTUAL cabe, si no, salto de línea ANTES de dibujar
            if current_x + cell_spacing > right_margin_limit:
                current_x = start_x      # Reset a la izquierda
                current_y -= line_height # Bajar una línea
                
                # Opcional: Si current_y es muy bajo, crear nueva página (c.showPage())
                if current_y < 50: 
                    c.showPage()
                    current_y = height - 100
                    current_x = start_x

            # Dibujar la celda en la posición actual
            self._draw_braille_cell_pdf(c, cell, current_x, current_y)
            
            # Avanzar el cursor para la siguiente celda
            current_x += cell_spacing

        # Información adicional
        c.setFont("Helvetica", 10)
        c.drawString(50, 50, f"Generado por: Transcriptor Braille")
        c.drawString(50, 35, f"Total de celdas: {len(braille_cells)}")
        
        c.save()
        buffer.seek(0)
        
        return buffer
    
    def _draw_braille_cell_pdf(self, c: canvas.Canvas, cell: List[int], 
                               x: float, y: float):
        """
        Dibuja una celda Braille individual en el canvas del PDF.
        
        Renderiza todos los 6 puntos Braille:
        - Puntos activos: Círculos negros rellenos (2mm de radio)
        - Puntos inactivos: Círculos vacíos con contorno gris
        
        Disposición de Puntos:
            1 4
            2 5
            3 6
        
        Espaciado:
        - Columnas: 5mm entre punto izquierdo y derecho
        - Filas: 5mm entre puntos verticalmente
        
        Args:
            c (canvas.Canvas): Canvas de ReportLab para dibujar en PDF.
            cell (List[int]): Lista de puntos activos (ej. [1, 2, 4]).
                            Vacía [] representa espacio.
            x (float): Coordenada X de la esquina superior izquierda (mm).
            y (float): Coordenada Y de la esquina superior izquierda (mm).
        
        Returns:
            None (modifica canvas directamente)
        
        Side Effects:
            - Dibuja 6 círculos en el canvas
            - Cambia colores de relleno/trazo según necesidad
            - No aplica cambios de página
        
        Technical Details:
            - Usa milímetros (mm) como unidad
            - Radio: 2mm para puntos rellenos y vacíos
            - Color puntos activos: Negro RGB(0, 0, 0)
            - Color puntos inactivos: Gris RGB(0.5, 0.5, 0.5)
        
        Example:
            >>> from reportlab.pdfgen import canvas
            >>> c = canvas.Canvas("test.pdf", pagesize=A4)
            >>> gen = BraillePDFGenerator()
            >>> gen._draw_braille_cell_pdf(c, [1, 2, 4], 100, 500)
            >>> c.save()
        """
        dot_radius = 2 * mm
        col_spacing = 5 * mm
        row_spacing = 5 * mm
        
        # Posiciones de los 6 puntos
        positions = [
            (x, y),                              # Punto 1
            (x, y - row_spacing),                # Punto 2
            (x, y - 2 * row_spacing),            # Punto 3
            (x + col_spacing, y),                # Punto 4
            (x + col_spacing, y - row_spacing),  # Punto 5
            (x + col_spacing, y - 2 * row_spacing)  # Punto 6
        ]
        
        for dot_num in range(1, 7):
            px, py = positions[dot_num - 1]
            if dot_num in cell:
                # Punto lleno (activo)
                c.setFillColorRGB(0, 0, 0)
                c.circle(px, py, dot_radius, fill=1)
            else:
                # Punto vacío (contorno)
                c.setStrokeColorRGB(0.5, 0.5, 0.5)
                c.setFillColorRGB(1, 1, 1)
                c.circle(px, py, dot_radius, fill=1, stroke=1)


# Funciones de conveniencia
def generate_braille_image(text: str, mirror: bool = False, include_text: bool = True) -> BytesIO:
    """
    Función de conveniencia para generar imagen PNG con Braille.
    
    Crea un BrailleImageGenerator con configuración por defecto y
    genera una imagen PNG del texto proporcionado.
    
    Esta es la función más simple para generar imágenes cuando no se
    necesita configuración personalizada.
    
    Args:
        text (str): Texto en español a convertir a Braille.
        mirror (bool): Si generar en modo espejo (Default: False)
        include_text (bool): Si incluir el texto original en la imagen.
                            Default: True
    
    Returns:
        BytesIO: Buffer de imagen PNG en memoria. Utilizable como:
                - Guardar: open("out.png", "wb").write(buffer.getvalue())
                - Respuesta HTTP: StreamingResponse(buffer, media_type="image/png")
                - Conversión: Image.open(buffer) con PIL
    
    Raises:
        Cualquier excepción de BrailleImageGenerator.generate_image()
    
    Example:
        >>> buffer = generate_braille_image("Hola", mirror=True)
        >>> with open("salida.png", "wb") as f:
        ...     f.write(buffer.getvalue())
    
    Note:
        - Usa configuración por defecto (40×60 píxeles por celda)
        - Para personalizar, usar BrailleImageGenerator directamente
    """
    generator = BrailleImageGenerator()
    return generator.generate_image(text, include_text, mirror)


def generate_braille_pdf(text: str, mirror: bool = False, title: str = "Señalética Braille") -> BytesIO:
    """
    Función de conveniencia para generar PDF con Braille.
    
    Crea un BraillePDFGenerator con tamaño A4 por defecto y genera
    un documento PDF del texto proporcionado con título personalizable.
    
    Esta es la forma más simple de generar PDFs cuando no se necesita
    configurar tamaño de página personalizado.
    
    Args:
        text (str): Texto en español a convertir a Braille.
        mirror (bool): Si generar en modo espejo (Default: False)
        title (str): Título del documento PDF.
                    Default: "Señalética Braille"
    
    Returns:
        BytesIO: Buffer PDF en memoria. Utilizable como:
                - Guardar: open("out.pdf", "wb").write(buffer.getvalue())
                - Respuesta HTTP: StreamingResponse(buffer, media_type="application/pdf")
                - Transmisión directo a cliente
    
    Raises:
        Cualquier excepción de BraillePDFGenerator.generate_pdf()
    
    Example:
        >>> buffer = generate_braille_pdf("Salida", mirror=True, title="Salida de Emergencia")
        >>> with open("salida.pdf", "wb") as f:
        ...     f.write(buffer.getvalue())
    
    Note:
        - Usa tamaño A4 (210×297 mm)
        - Para tamaños personalizados, usar BraillePDFGenerator directamente
        - Ideal para impresión de señaléticas
    """
    generator = BraillePDFGenerator()
    return generator.generate_pdf(text, title, mirror)
