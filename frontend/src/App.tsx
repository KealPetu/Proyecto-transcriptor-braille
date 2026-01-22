import React, { useState, useEffect } from 'react';
import TextInput from './components/TextInput';
import BrailleDisplay from './components/BrailleDisplay';
import { brailleApi } from './services/api';
import type { TranslationResponse } from './types';
import './App.css';

/**
 * Componente principal de la aplicación.
 * 
 * Gestiona:
 * - Estado de traducción
 * - Comunicación con API
 * - Errores y estados de carga
 * - Descarga de archivos
 */
function App() {
  const [originalText, setOriginalText] = useState('');
  const [brailleCells, setBrailleCells] = useState<number[][]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [isApiHealthy, setIsApiHealthy] = useState(false);

  // Verificar salud de API al montar el componente
  useEffect(() => {
    const checkApi = async () => {
      try {
        const healthy = await brailleApi.healthCheck();
        setIsApiHealthy(healthy);
      } catch {
        setIsApiHealthy(false);
      }
    };

    checkApi();
  }, []);

  /**
   * Maneja la traducción de texto a Braille.
   */
  const handleTranslate = async (text: string) => {
    setIsLoading(true);
    setError('');
    
    try {
      const result: TranslationResponse = await brailleApi.translate(text);
      setOriginalText(result.original_text);
      setBrailleCells(result.braille_cells);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error desconocido';
      setError(errorMessage);
      console.error('Error en traducción:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App" style={{ maxWidth: '900px', margin: '0 auto', padding: '2rem' }}>
      {/* Header */}
      <header style={{ marginBottom: '2rem', textAlign: 'center' }}>
        <h1
          style={{
            color: '#ffffff',
            fontSize: '2.5rem',
            fontWeight: '700',
            letterSpacing: '-0.5px',
            marginBottom: '0.5rem',
            fontFamily: '"Segoe UI", "Roboto", sans-serif'
          }}
        >
          📖 Traductor Español ↔ Braille
        </h1>
        <p style={{ color: '#b0b0b0', marginTop: '0.5rem' }}>
          Traducción profesional con generación de materiales visuales
        </p>
      </header>

      {/* Input de texto */}
      <TextInput
        onTranslate={handleTranslate}
        isLoading={isLoading}
      />

      {/* Mensaje de error */}
      {error && (
        <div
          style={{
            backgroundColor: '#ffebee',
            color: '#c62828',
            padding: '1rem',
            borderRadius: '4px',
            marginBottom: '1rem',
            borderLeft: '4px solid #c62828'
          }}
        >
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* Resultado de traducción */}
      <BrailleDisplay
        originalText={originalText}
        brailleCells={brailleCells}
      />
    </div>
  );
}

export default App;