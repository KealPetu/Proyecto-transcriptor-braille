"""
Rutas API para generación de representaciones visuales de Braille.

Endpoints para generar imágenes PNG y documentos PDF con representaciones
de texto en Braille, útiles para impresión y señalización.

Autor: Isaac
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.api.services.generator import generate_braille_image, generate_braille_pdf


router = APIRouter()


class GenerationRequest(BaseModel):
    """Modelo para solicitud de generación."""
    text: str
    include_text: bool = True
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "Baño",
                "include_text": True
            }
        }


class PDFGenerationRequest(BaseModel):
    """Modelo para solicitud de generación de PDF."""
    text: str
    title: str = "Señalética Braille"
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "Salida de emergencia",
                "title": "Señalética - Salida"
            }
        }


@router.post("/image")
async def generate_image(request: GenerationRequest):
    """
    Genera una imagen PNG con representación visual del texto en Braille.
    
    Esta funcionalidad es útil para:
    - Crear señaléticas accesibles
    - Material educativo
    - Visualización de traducciones
    
    Args:
        request: Objeto con el texto y opciones de generación
        
    Returns:
        Imagen PNG con las celdas Braille visualizadas
        
    Example:
        POST /api/v1/generation/image
        {
            "text": "Baño",
            "include_text": true
        }
    """
    if not request.text:
        raise HTTPException(status_code=400, detail="El texto no puede estar vacío")
    
    try:
        # Generar imagen
        image_buffer = generate_braille_image(request.text, request.include_text)
        
        # Retornar como respuesta de streaming
        return StreamingResponse(
            image_buffer,
            media_type="image/png",
            headers={
                "Content-Disposition": f"attachment; filename=braille_{request.text[:10]}.png"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar la imagen: {str(e)}"
        )


@router.post("/pdf")
async def generate_pdf(request: PDFGenerationRequest):
    """
    Genera un documento PDF con texto y representación Braille para señaléticas.
    
    Ideal para:
    - Impresión de señalización accesible
    - Carteles con información en Braille
    - Etiquetas para espacios públicos
    
    Args:
        request: Objeto con el texto y título del documento
        
    Returns:
        Documento PDF con el texto y su representación en Braille
        
    Example:
        POST /api/v1/generation/pdf
        {
            "text": "Salida de emergencia",
            "title": "Señalética - Salida"
        }
    """
    if not request.text:
        raise HTTPException(status_code=400, detail="El texto no puede estar vacío")
    
    try:
        # Generar PDF
        pdf_buffer = generate_braille_pdf(request.text, request.title)
        
        # Retornar como respuesta de streaming
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=braille_{request.text[:10]}.pdf"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar el PDF: {str(e)}"
        )


@router.get("/formats")
async def get_available_formats():
    """
    Retorna información sobre los formatos de generación disponibles.
    
    Returns:
        Diccionario con los formatos soportados y sus descripciones
    """
    return {
        "formats": [
            {
                "name": "PNG",
                "endpoint": "/api/v1/generation/image",
                "description": "Imagen PNG con representación visual de Braille",
                "use_case": "Visualización web, material digital"
            },
            {
                "name": "PDF",
                "endpoint": "/api/v1/generation/pdf",
                "description": "Documento PDF con texto y Braille",
                "use_case": "Impresión de señaléticas, carteles, etiquetas"
            }
        ],
        "common_uses": [
            "Señalización en edificios públicos",
            "Etiquetas de productos",
            "Material educativo",
            "Menús de restaurantes accesibles",
            "Indicadores de habitaciones"
        ]
    }
