"""
Tests para la funcionalidad de generación de imágenes y PDFs.

Autor: Isaac
"""

import pytest
from io import BytesIO
from PIL import Image
from PyPDF2 import PdfReader

from app.api.services.generator import (
    BrailleImageGenerator,
    BraillePDFGenerator,
    generate_braille_image,
    generate_braille_pdf
)


class TestBrailleImageGenerator:
    """Tests para el generador de imágenes."""
    
    def test_generator_initialization(self):
        """Verifica que el generador se inicialice correctamente."""
        generator = BrailleImageGenerator()
        assert generator.cell_width == 40
        assert generator.cell_height == 60
        assert generator.dot_radius == 6
    
    def test_generate_simple_image(self):
        """Verifica que se pueda generar una imagen simple."""
        generator = BrailleImageGenerator()
        image_buffer = generator.generate_image("a")
        
        # Verificar que se generó un buffer válido
        assert isinstance(image_buffer, BytesIO)
        assert image_buffer.tell() == 0  # Buffer en posición inicial
        
        # Verificar que es una imagen PNG válida
        img = Image.open(image_buffer)
        assert img.format == "PNG"
        assert img.size[0] > 0
        assert img.size[1] > 0
    
    def test_generate_image_with_text(self):
        """Verifica generación de imagen con texto incluido."""
        generator = BrailleImageGenerator()
        image_buffer = generator.generate_image("Hola", include_text=True)
        
        img = Image.open(image_buffer)
        # Con texto, la imagen debe ser más alta
        assert img.size[1] > 60 + 40  # cell_height + margin + texto
    
    def test_generate_image_without_text(self):
        """Verifica generación de imagen sin texto."""
        generator = BrailleImageGenerator()
        image_buffer = generator.generate_image("Hola", include_text=False)
        
        img = Image.open(image_buffer)
        # Sin texto, la imagen debe ser más pequeña
        assert img.size[1] <= 100  # Aproximadamente cell_height + margin
    
    def test_generate_image_multiple_cells(self):
        """Verifica que se genere imagen con múltiples celdas."""
        generator = BrailleImageGenerator()
        image_buffer = generator.generate_image("abc")
        
        img = Image.open(image_buffer)
        # La imagen debe tener ancho suficiente para 3 celdas
        min_width = 3 * (40 + 10) + 40  # 3 celdas + espaciado + márgenes
        assert img.size[0] >= min_width
    
    def test_convenience_function(self):
        """Verifica la función de conveniencia generate_braille_image."""
        image_buffer = generate_braille_image("test", include_text=True)
        
        assert isinstance(image_buffer, BytesIO)
        img = Image.open(image_buffer)
        assert img.format == "PNG"


class TestBraillePDFGenerator:
    """Tests para el generador de PDFs."""
    
    def test_generator_initialization(self):
        """Verifica que el generador de PDF se inicialice correctamente."""
        from reportlab.lib.pagesizes import A4
        generator = BraillePDFGenerator()
        assert generator.page_size == A4
    
    def test_generate_simple_pdf(self):
        """Verifica que se pueda generar un PDF simple."""
        generator = BraillePDFGenerator()
        pdf_buffer = generator.generate_pdf("Baño")
        
        # Verificar que se generó un buffer válido
        assert isinstance(pdf_buffer, BytesIO)
        assert pdf_buffer.tell() == 0  # Buffer en posición inicial
        
        # Verificar que es un PDF válido leyéndolo
        pdf_reader = PdfReader(pdf_buffer)
        assert len(pdf_reader.pages) >= 1
    
    def test_generate_pdf_with_title(self):
        """Verifica generación de PDF con título personalizado."""
        generator = BraillePDFGenerator()
        pdf_buffer = generator.generate_pdf("Salida", title="Señalética Salida")
        
        pdf_reader = PdfReader(pdf_buffer)
        assert len(pdf_reader.pages) >= 1
        
        # Verificar que el PDF tiene contenido
        page = pdf_reader.pages[0]
        text = page.extract_text()
        assert "Salida" in text or len(text) > 0  # Verificar que hay contenido
    
    def test_generate_pdf_long_text(self):
        """Verifica generación de PDF con texto largo."""
        generator = BraillePDFGenerator()
        long_text = "Salida de emergencia - Mantener despejado"
        pdf_buffer = generator.generate_pdf(long_text)
        
        pdf_reader = PdfReader(pdf_buffer)
        assert len(pdf_reader.pages) >= 1
    
    def test_convenience_function(self):
        """Verifica la función de conveniencia generate_braille_pdf."""
        pdf_buffer = generate_braille_pdf("test", title="Test PDF")
        
        assert isinstance(pdf_buffer, BytesIO)
        pdf_reader = PdfReader(pdf_buffer)
        assert len(pdf_reader.pages) >= 1


class TestIntegration:
    """Tests de integración para verificar el flujo completo."""
    
    def test_complete_workflow_image(self):
        """Verifica el flujo completo de generación de imagen."""
        text = "Baño"
        
        # Generar imagen
        image_buffer = generate_braille_image(text, include_text=True)
        
        # Verificar que se puede abrir y es válida
        img = Image.open(image_buffer)
        assert img.format == "PNG"
        assert img.mode == "RGB"
        assert img.size[0] > 0
        assert img.size[1] > 0
    
    def test_complete_workflow_pdf(self):
        """Verifica el flujo completo de generación de PDF."""
        text = "Entrada principal"
        title = "Señalética Entrada"
        
        # Generar PDF
        pdf_buffer = generate_braille_pdf(text, title)
        
        # Verificar que se puede leer
        pdf_reader = PdfReader(pdf_buffer)
        assert len(pdf_reader.pages) == 1
    
    def test_special_characters(self):
        """Verifica manejo de caracteres especiales españoles."""
        text = "Baño - Señalización"
        
        # Imagen
        image_buffer = generate_braille_image(text)
        img = Image.open(image_buffer)
        assert img.format == "PNG"
        
        # PDF
        pdf_buffer = generate_braille_pdf(text)
        pdf_reader = PdfReader(pdf_buffer)
        assert len(pdf_reader.pages) >= 1
    
    def test_numbers_in_generation(self):
        """Verifica generación con números."""
        text = "Piso 3"
        
        image_buffer = generate_braille_image(text)
        img = Image.open(image_buffer)
        assert img.format == "PNG"
        
        pdf_buffer = generate_braille_pdf(text)
        pdf_reader = PdfReader(pdf_buffer)
        assert len(pdf_reader.pages) >= 1
