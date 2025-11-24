# backend/app/schemas/translation.py
from pydantic import BaseModel
from typing import List, Optional

class TranslationRequest(BaseModel):
    text: str

class TranslationResponse(BaseModel):
    original_text: str
    # Retornamos una lista de listas de enteros: [[1, 2], [1, 5]]
    braille_cells: List[List[int]] 
    # Opcional: Una representación en string para debug (ej: "12-15")
    braille_string_repr: Optional[str] = None 

class ReverseTranslationRequest(BaseModel):
    braille_cells: List[List[int]]

class ReverseTranslationResponse(BaseModel):
    translated_text: str