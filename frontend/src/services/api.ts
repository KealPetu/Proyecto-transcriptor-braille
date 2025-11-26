// frontend/src/services/api.ts
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export interface TranslationResponse {
  original_text: string;
  // El backend devuelve una lista de listas de números (ej: [[1,2,5], [1]])
  braille_cells: number[][];
  braille_string_repr: string;
}

export const brailleApi = {
  translate: async (text: string): Promise<TranslationResponse> => {
    // Nota la ruta actualizada para coincidir con el backend
    const response = await fetch(`${API_BASE_URL}/api/v1/translation/to-braille`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || 'Error en la traducción');
    }

    return response.json();
  },
};