# backend/app/api/routes/translation.py
from fastapi import APIRouter, HTTPException

from app.schemas.translation import (
    TranslationRequest, 
    TranslationResponse, 
    ReverseTranslationRequest, 
    ReverseTranslationResponse
)
from app.api.services.translator import text_to_braille, braille_to_text

router = APIRouter()

@router.post("/to-braille", response_model=TranslationResponse)
def translate_to_braille(request: TranslationRequest):
    """
    Convierte texto español a celdas Braille.
    Maneja números, mayúsculas y caracteres especiales básicos.
    """
    if not request.text:
        raise HTTPException(status_code=400, detail="El texto no puede estar vacío")
    
    cells = text_to_braille(request.text)
    
    # Generamos una representación legible para facilitar el debug
    # Ej: [[1], [1,2]] -> "1|12"
    str_repr = "|".join(["".join(map(str, c)) if c else "_" for c in cells])
    
    return TranslationResponse(
        original_text=request.text,
        braille_cells=cells,
        braille_string_repr=str_repr
    )

@router.post("/to-text", response_model=ReverseTranslationResponse)
def translate_to_text(request: ReverseTranslationRequest):
    """
    Convierte una lista de celdas Braille (listas de puntos) a texto español.
    """
    text = braille_to_text(request.braille_cells)
    return ReverseTranslationResponse(translated_text=text)