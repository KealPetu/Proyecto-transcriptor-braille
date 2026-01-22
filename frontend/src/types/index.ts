/**
 * Tipos y interfaces de la aplicación.
 * 
 * Define tipos TypeScript para:
 * - Respuestas de API
 * - Estados de componentes
 * - Configuración
 */

/**
 * Respuesta de traducción Español → Braille.
 */
export interface TranslationResponse {
  /** Texto original de entrada */
  original_text: string;
  
  /** Celdas Braille como listas de puntos (1-6) */
  braille_cells: number[][];
  
  /** Representación textual para debugging */
  braille_string_repr: string;
}

/**
 * Respuesta de traducción inversa Braille → Español.
 */
export interface ReverseTranslationResponse {
  /** Texto traducido desde Braille */
  translated_text: string;
}

/**
 * Error de API.
 */
export interface ApiError {
  /** Código de error */
  error: string;
  
  /** Mensaje descriptivo */
  message: string;
  
  /** Código HTTP */
  status_code: number;
}

/**
 * Estado de carga de la aplicación.
 */
export type LoadingState = 'idle' | 'loading' | 'success' | 'error';

/**
 * Configuración de la aplicación.
 */
export interface AppConfig {
  /** URL base del servidor API */
  apiBaseUrl: string;
  
  /** Ambiente (development, production) */
  environment: string;
  
  /** Timeout de requests en ms */
  requestTimeout: number;
}
