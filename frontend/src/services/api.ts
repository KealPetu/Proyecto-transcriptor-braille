const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export interface TranslationRequest {
  text: string;
}

export interface TranslationResponse {
  original_text: string;
  braille_text: string;
  timestamp: string;
}

export const brailleApi = {
  translate: async (text: string): Promise<TranslationResponse> => {
    const response = await fetch(`${API_BASE_URL}/api/translate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text }),
    });

    if (!response.ok) {
      throw new Error('Error en la traducción');
    }

    return response.json();
  },
};
