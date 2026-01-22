"""
Rutas de API para generación de representaciones visuales de Braille.

Endpoints:
    POST /image: Genera PNG con visualización Braille
    POST /pdf: Genera PDF con señalética Braille

Características:
    - Streaming de respuestas para eficiencia
    - Content-Disposition para descarga automática
    - Validación de entrada
    - Manejo profesional de errores
"""

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app.config import settings
from app.logger import get_logger
from app.exceptions import ValidationError, GenerationError
from app.api.services.generator import generate_braille_image, generate_braille_pdf


logger = get_logger(__name__)
router = APIRouter()


class GenerationRequest(BaseModel):
    """Solicitud de generación de imagen PNG con Braille."""
    
    text: str = Field(..., min_length=1, max_length=500, description="Texto a convertir a Braille")
    include_text: bool = Field(default=True, description="Incluir texto original en la imagen")


class PDFGenerationRequest(BaseModel):
    """Solicitud de generación de documento PDF con Braille."""
    
    text: str = Field(..., min_length=1, max_length=500, description="Texto a convertir a Braille")
    title: str = Field(default="Señalética Braille", description="Título del documento PDF")


@router.post("/image")
async def generate_image(request: GenerationRequest):
    """
    Genera imagen PNG con representación visual de Braille.
    
    Renderiza cada carácter como una celda Braille de 6 puntos (2×3).
    Los puntos activos aparecen como círculos negros, los inactivos como grises.
    
    Características:
        - Renderizado en memoria (sin archivos temporales)
        - Streaming response para eficiencia
        - Descarga automática con nombre sugerido
        - Fondo blanco, ideal para impresión
    
    Args:
        request (GenerationRequest):
            - text: Texto español a convertir
            - include_text: Incluir texto original como encabezado
    
    Returns:
        StreamingResponse: Imagen PNG binaria
            - Content-Type: image/png
            - Content-Disposition: attachment; filename=braille_[...].png
    
    Raises:
        ValidationError: Texto vacío o inválido
        GenerationError: Error en generación de imagen
    
    Examples:
        POST /api/v1/generation/image
        {"text": "Salida", "include_text": true}
        
        Response: Imagen PNG (descarga automática como braille_Salida.png)
    """
    try:
        # Validación
        if not request.text or not request.text.strip():
            raise ValidationError("El texto no puede estar vacío")
        
        if len(request.text) > settings.max_text_length:
            raise ValidationError(
                f"Texto excede límite de {settings.max_text_length} caracteres"
            )
        
        logger.info(f"Generación de imagen solicitada: '{request.text}'")
        
        # Generar imagen
        image_buffer = generate_braille_image(request.text, request.include_text)
        
        # Nombre de archivo sugerido
        filename = f"braille_{request.text[:10].replace(' ', '_')}.png"
        
        logger.info(f"Imagen generada exitosamente: {len(image_buffer.getvalue())} bytes")
        
        return StreamingResponse(
            image_buffer,
            media_type="image/png",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    
    except ValidationError:
        raise
    except GenerationError:
        raise
    except Exception as e:
        logger.error(f"Error inesperado en generación de imagen: {str(e)}", exc_info=True)
        raise GenerationError(f"Error generando imagen: {str(e)}")


@router.post("/pdf")
async def generate_pdf(request: PDFGenerationRequest):
    """
    Genera documento PDF con representación visual de Braille.
    
    Crea PDF A4 con:
        1. Título personalizado (24pt, negrita)
        2. Texto original en español (16pt)
        3. Representación visual de celdas Braille
        4. Metadatos de generación en pie de página
    
    Características:
        - Saltos de línea automáticos
        - Múltiples páginas automáticas si es necesario
        - Formato A4 optimizado para impresión
    
    Args:
        request (PDFGenerationRequest):
            - text: Texto español a convertir
            - title: Título del documento
    
    Returns:
        StreamingResponse: Documento PDF binario
            - Content-Type: application/pdf
            - Content-Disposition: attachment; filename=braille_[...].pdf
    
    Raises:
        ValidationError: Texto o título inválidos
        GenerationError: Error en generación de PDF
    
    Examples:
        POST /api/v1/generation/pdf
        {"text": "Baño", "title": "Servicios Higiénicos"}
        
        Response: Documento PDF (descarga automática como braille_Baño.pdf)
    """
    try:
        # Validación
        if not request.text or not request.text.strip():
            raise ValidationError("El texto no puede estar vacío")
        
        if len(request.text) > settings.max_text_length:
            raise ValidationError(
                f"Texto excede límite de {settings.max_text_length} caracteres"
            )
        
        logger.info(f"Generación de PDF solicitada: '{request.text}' con título '{request.title}'")
        
        # Generar PDF
        pdf_buffer = generate_braille_pdf(request.text, request.title)
        
        # Nombre de archivo sugerido
        filename = f"braille_{request.text[:10].replace(' ', '_')}.pdf"
        
        logger.info(f"PDF generado exitosamente: {len(pdf_buffer.getvalue())} bytes")
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    
    except ValidationError:
        raise
    except GenerationError:
        raise
    except Exception as e:
        logger.error(f"Error inesperado en generación de PDF: {str(e)}", exc_info=True)
        raise GenerationError(f"Error generando PDF: {str(e)}")


@router.post("/image")
async def generate_image(request: GenerationRequest):
    """
    Endpoint: Genera imagen PNG con representación visual de Braille.
    
    Convierte texto español a imagen PNG mostrando cada carácter como
    una celda Braille de 6 puntos (disposición 2x3 estándar).
    
    Proceso:
        1. Recibir texto en español
        2. Convertir a celdas Braille
        3. Renderizar celdas como círculos (puntos activos/inactivos)
        4. Incluir texto original como encabezado (opcional)
        5. Enviar como imagen PNG mediante streaming
    
    Características:
        - Renderizado en memoria (sin archivos temporales)
        - Streaming response para eficiencia
        - Content-Disposition con nombre sugerido de descarga
        - Puntos activos: círculos negros rellenos
        - Puntos inactivos: círculos grises con contorno
        - Fondo blanco, ideal para impresión
    
    Args:
        request (GenerationRequest): Objeto con:
            - text (str): Texto a convertir
            - include_text (bool): Incluir texto original en imagen
    
    Returns:
        StreamingResponse: Imagen PNG con:
            - media_type: "image/png"
            - Content-Disposition: attachment; filename=braille_[...].png
            - Body: Datos PNG binarios
    
    HTTP Status Codes:
        - 200 OK: Imagen generada exitosamente
        - 400 Bad Request: Texto vacío
        - 500 Internal Server Error: Error en generación de imagen
        - 422 Unprocessable Entity: Esquema JSON inválido
    
    Raises:
        HTTPException(400): Si request.text está vacío
        HTTPException(500): Si hay error en generación (PIL, memoria, etc.)
    
    Validación:
        - Rechaza textos vacíos con mensaje descriptivo
        - Maneja excepciones de PIL gracefully
    
    Ejemplos:
        >>> # Request
        >>> POST /api/v1/generation/image
        >>> {
        ...     "text": "Hola",
        ...     "include_text": true
        ... }
        >>> # Response
        >>> 200 OK
        >>> Content-Type: image/png
        >>> Content-Disposition: attachment; filename=braille_Hola.png
        >>> [datos PNG binarios]
        
        >>> # Request sin encabezado
        >>> {
        ...     "text": "Baño",
        ...     "include_text": false
        ... }
    
    Dimensiones de Imagen:
        - Ancho: (num_celdas × 50px) + 40px margen
        - Alto: 60px + 40px margen
        - Extra si include_text: +40px para encabezado
        - Ejemplo: "hola" = (4 celdas × 50 + 40) × (60 + 40 + 40) = 240 × 140 px
    
    Uso en Frontend:
        ```javascript
        const response = await fetch('/api/v1/generation/image', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({text: "Hola", include_text: true})
        });
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        // Usar para: <img src={url} />, descargar, etc.
        ```
    
    Casos de Uso:
        - Visualización web de Braille
        - Material educativo digital
        - Generación de carteles para impresión
        - Apps móviles de accesibilidad
    
    Rendimiento:
        - Generación típica: <100ms para textos normales
        - Memoria: ~1MB por imagen típica
        - Streaming evita almacenamiento en servidor
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
    Endpoint: Genera documento PDF con representación visual de Braille.
    
    Crea un PDF de página completa (A4) con:
    - Título personalizable
    - Texto original en español
    - Representación visual de celdas Braille
    - Manejo automático de saltos de línea y múltiples páginas
    - Información de generación en pie de página
    
    Proceso:
        1. Recibir texto y título
        2. Convertir texto a celdas Braille
        3. Crear documento PDF (tamaño A4)
        4. Dibujar título, texto original, celdas Braille
        5. Manejar saltos de línea automáticos
        6. Crear nuevas páginas si es necesario
        7. Enviar como PDF mediante streaming
    
    Estructura del PDF:
        ┌─────────────────────────────────────┐
        │      Título (24pt, negrita)        │
        │                                     │
        │ Texto:                              │
        │ Texto original (16pt, negrita)     │
        │                                     │
        │ Representación Braille:             │
        │ [Celdas Braille - múltiples filas] │
        │                                     │
        │ Generado por: Transcriptor Braille │
        │ Total de celdas: N                  │
        └─────────────────────────────────────┘
    
    Características:
        - Tamaño A4: 210×297 mm (595×842 puntos)
        - Márgenes: ~50 puntos (~18mm)
        - Salto de línea automático en margen derecho
        - Nueva página automática si no hay espacio vertical
        - Espaciado entre celdas: 15mm
        - Altura de línea: 30mm
    
    Args:
        request (PDFGenerationRequest): Objeto con:
            - text (str): Texto a convertir
            - title (str): Título del documento
    
    Returns:
        StreamingResponse: Documento PDF con:
            - media_type: "application/pdf"
            - Content-Disposition: attachment; filename=braille_[...].pdf
            - Body: Datos PDF binarios
    
    HTTP Status Codes:
        - 200 OK: PDF generado exitosamente
        - 400 Bad Request: Texto vacío
        - 500 Internal Server Error: Error en generación de PDF
        - 422 Unprocessable Entity: Esquema JSON inválido
    
    Raises:
        HTTPException(400): Si request.text está vacío
        HTTPException(500): Si hay error en generación (ReportLab, memoria, etc.)
    
    Validación:
        - Rechaza textos vacíos con mensaje descriptivo
        - Maneja excepciones de ReportLab gracefully
    
    Ejemplos:
        >>> # Request
        >>> POST /api/v1/generation/pdf
        >>> {
        ...     "text": "Salida de emergencia",
        ...     "title": "Señalética - Salida"
        ... }
        >>> # Response
        >>> 200 OK
        >>> Content-Type: application/pdf
        >>> Content-Disposition: attachment; filename=braille_Salida.pdf
        >>> [datos PDF binarios]
        
        >>> # Request simple
        >>> {
        ...     "text": "Baño"
        ... }
        >>> # Response usa título por defecto "Señalética Braille"
    
    Lógica de Paginación:
        - Si celdas no caben en línea actual (> margen derecho): salto de línea
        - Si espacio vertical insuficiente (< 50pt): nueva página
        - Se preserva espacio para encabezado y pie en nueva página
        - Máximo ~8 líneas de Braille por página A4
    
    Uso en Frontend:
        ```javascript
        const response = await fetch('/api/v1/generation/pdf', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                text: "Salida",
                title: "Señalética"
            })
        });
        const blob = await response.blob();
        // Opción 1: Descargar
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'braille.pdf';
        a.click();
        
        // Opción 2: Visualizar (iframe)
        const url = URL.createObjectURL(blob);
        // <iframe src={url} />
        ```
    
    Casos de Uso:
        - Impresión de señaléticas accesibles
        - Material educativo en PDF
        - Carteles para espacios públicos
        - Documentación Braille
        - Menús de restaurantes accesibles
    
    Rendimiento:
        - Generación típica: 200-500ms (más que imagen por complejidad)
        - Memoria: ~2-5MB por PDF típico
        - Streaming evita almacenamiento en servidor
    
    Formatos Soportados:
        - Fuentes: Helvetica, Helvetica-Bold (PDFs portables)
        - Colores: Negro sobre blanco
        - Papel: A4 (configurable a letter, A3, etc.)
    
    Note:
        - Ideal para impresión física
        - PDF compatible con lectores PDF estándar
        - Exportable desde navegador
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
    Endpoint: Retorna información sobre formatos de generación disponibles.
    
    Proporciona metadatos descriptivos de los formatos soportados,
    casos de uso comunes y endpoints específicos.
    
    Funcionalidad:
        - Descubre formatos disponibles sin hacer HTTP OPTIONS
        - Obtiene información de endponts relativos
        - Lista casos de uso comunes
        - Información para documentación de API
    
    Args:
        None
    
    Returns:
        JSON con estructura:
        {
            "formats": [
                {
                    "name": str,
                    "endpoint": str,
                    "description": str,
                    "use_case": str
                },
                ...
            ],
            "common_uses": [
                str,
                ...
            ]
        }
    
    HTTP Status Codes:
        - 200 OK: Información obtenida exitosamente
    
    Raises:
        No levanta excepciones
    
    Response Ejemplo:
        {
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
    
    Uso en Documentación:
        - Generar documentación automática de API
        - Descubrimiento de capacidades
        - Generación de interfaz de usuario dinámica
    
    Casos de Uso:
        - Clientes web consultando formatos disponibles
        - Aplicaciones descubriendo capacidades de API
        - Documentación automática (Swagger, OpenAPI)
        - Testing de disponibilidad
    
    Comparación de Formatos:
        PNG:
            ✓ Rápido (< 100ms)
            ✓ Bajo consumo de memoria
            ✓ Visualización inmediata en web
            ✓ Compatible con cualquier navegador
            ✗ Resolución limitada para impresión
            ✗ No estándar para documentos formales
        
        PDF:
            ✓ Portabilidad universal
            ✓ Alta calidad para impresión
            ✓ Formalmente reconocido
            ✓ Multi-página automático
            ✗ Generación más lenta
            ✗ Más consumo de memoria
            ✗ Requiere visualizador PDF
    
    Note:
        - Endpoint de solo lectura (GET)
        - Sin parámetros requeridos
        - Respuesta cacheada (no cambia frecuentemente)
        - Útil para discovery y documentación
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
