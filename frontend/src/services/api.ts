/**
 * Servicio de API para traducción Braille.
 * 
 * Proporciona métodos para:
 * - Traducción Español → Braille
 * - Traducción Braille → Español
 * - Descarga de imágenes PNG
 * - Descarga de documentos PDF
 * 
 * Manejo de errores centralizado y type-safe.
 */

import type { TranslationResponse, ReverseTranslationResponse, ApiError } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const API_PREFIX = '/api/v1';

/**
 * Maneja respuestas de error de la API.
 */
async function handleErrorResponse(response: Response): Promise<never> {
  let errorData: ApiError;
  
  try {
    errorData = await response.json();
  } catch {
    errorData = {
      error: 'UNKNOWN_ERROR',
      message: `Error HTTP ${response.status}: ${response.statusText}`,
      status_code: response.status
    };
  }
  
  throw new Error(errorData.message || 'Error desconocido en la API');
}

/**
 * API client para traducción Braille.
 */
export const brailleApi = {
  /**
   * Traduce texto español a Braille.
   * 
   * @param text - Texto en español
   * @returns Respuesta con celdas Braille
   */
  translate: async (text: string): Promise<TranslationResponse> => {
    if (!text || !text.trim()) {
      throw new Error('El texto no puede estar vacío');
    }

    const response = await fetch(`${API_BASE_URL}${API_PREFIX}/translation/to-braille`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text: text.trim() }),
    });

    if (!response.ok) {
      return handleErrorResponse(response);
    }

    return response.json();
  },

  /**
   * Traduce Braille a texto español.
   * 
   * @param brailleCells - Celdas Braille como listas de puntos
   * @returns Respuesta con texto traducido
   */
  reverseTranslate: async (brailleCells: number[][]): Promise<ReverseTranslationResponse> => {
    if (!brailleCells || brailleCells.length === 0) {
      throw new Error('Las celdas Braille no pueden estar vacías');
    }

    const response = await fetch(`${API_BASE_URL}${API_PREFIX}/translation/to-text`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ braille_cells: brailleCells }),
    });

    if (!response.ok) {
      return handleErrorResponse(response);
    }

    return response.json();
  },

  /**
   * Descarga imagen PNG con Braille.
   * 
   * @param text - Texto a convertir
   * @param mirror - Generar imagen en modo espejo
   * @param includeText - Incluir texto original en imagen
   * @returns Blob con imagen PNG
   */
  downloadImage: async (text: string, mirror: boolean = false, includeText: boolean = true): Promise<Blob> => {
    if (!text || !text.trim()) {
      throw new Error('El texto no puede estar vacío');
    }

    const response = await fetch(`${API_BASE_URL}${API_PREFIX}/generation/image`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: text.trim(),
        mirror: mirror,
        include_text: includeText
      }),
    });

    if (!response.ok) {
      return handleErrorResponse(response);
    }

    return response.blob();
  },

  /**
   * Descarga documento PDF con Braille.
   * 
   * @param text - Texto a convertir
   * @param mirror - Generar PDF en modo espejo
   * @param title - Título del PDF
   * @returns Blob con documento PDF
   */
  downloadPdf: async (text: string, mirror: boolean = false, title: string = "Traducción Braille"): Promise<Blob> => {
    if (!text || !text.trim()) {
      throw new Error('El texto no puede estar vacío');
    }

    const response = await fetch(`${API_BASE_URL}${API_PREFIX}/generation/pdf`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: text.trim(),
        mirror: mirror,
        title: title || "Traducción Braille"
      }),
    });

    if (!response.ok) {
      return handleErrorResponse(response);
    }

    return response.blob();
  },

  /**
   * Verifica la salud de la API.
   * 
   * @returns true si la API está operativa
   */
  healthCheck: async (): Promise<boolean> => {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      return response.ok;
    } catch {
      return false;
    }
  }
};

