"""
Servicio de generación de representaciones visuales de Braille.

Este módulo genera imágenes PNG y documentos PDF con representaciones
visuales de las celdas Braille, útiles para impresión de señaléticas
y material educativo.

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
    """Generador de imágenes PNG con representación visual de Braille."""
    
    def __init__(self, cell_width: int = CELL_WIDTH, cell_height: int = CELL_HEIGHT):
        """
        Inicializa el generador de imágenes.
        
        Args:
            cell_width: Ancho de cada celda en píxeles
            cell_height: Alto de cada celda en píxeles
        """
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.dot_radius = DOT_RADIUS
        self.margin = MARGIN
        self.spacing = SPACING
    
    def _get_dot_position(self, dot_number: int) -> Tuple[int, int]:
        """
        Calcula la posición (x, y) de un punto Braille dentro de una celda.
        
        Los puntos están numerados así:
        1 4
        2 5
        3 6
        
        Args:
            dot_number: Número del punto (1-6)
            
        Returns:
            Tupla (x, y) con la posición relativa del punto
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
        Dibuja una celda Braille en la imagen.
        
        Args:
            draw: Objeto ImageDraw para dibujar
            cell: Lista de puntos activos (1-6)
            offset_x: Desplazamiento horizontal de la celda
            offset_y: Desplazamiento vertical de la celda
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
    
    def generate_image(self, text: str, include_text: bool = True) -> BytesIO:
        """
        Genera una imagen PNG con el texto en Braille.
        
        Args:
            text: Texto a convertir en Braille
            include_text: Si True, incluye el texto original encima del Braille
            
        Returns:
            BytesIO con la imagen PNG generada
        """
        # Convertir texto a celdas Braille
        braille_cells = text_to_braille(text)
        
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
        
        # Guardar en BytesIO
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        return buffer


class BraillePDFGenerator:
    """Generador de documentos PDF con texto y Braille para señaléticas."""
    
    def __init__(self, page_size=A4):
        """
        Inicializa el generador de PDF.
        
        Args:
            page_size: Tamaño de página (por defecto A4)
        """
        self.page_size = page_size
    
    def generate_pdf(self, text: str, title: str = "Señalética Braille") -> BytesIO:
        """
        Genera un PDF con el texto en formato visual y Braille.
        
        Args:
            text: Texto a convertir
            title: Título del documento
            
        Returns:
            BytesIO con el PDF generado
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
        Dibuja una celda Braille en el PDF.
        
        Args:
            c: Canvas de ReportLab
            cell: Lista de puntos activos
            x, y: Coordenadas base de la celda
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
def generate_braille_image(text: str, include_text: bool = True) -> BytesIO:
    """
    Genera una imagen PNG con representación Braille del texto.
    
    Args:
        text: Texto a convertir
        include_text: Si incluir el texto original
        
    Returns:
        BytesIO con la imagen PNG
    """
    generator = BrailleImageGenerator()
    return generator.generate_image(text, include_text)


def generate_braille_pdf(text: str, title: str = "Señalética Braille") -> BytesIO:
    """
    Genera un PDF con texto y Braille para señaléticas.
    
    Args:
        text: Texto a convertir
        title: Título del documento
        
    Returns:
        BytesIO con el PDF generado
    """
    generator = BraillePDFGenerator()
    return generator.generate_pdf(text, title)
