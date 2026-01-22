import React, { useState, useEffect } from 'react';
import TextInput from './components/TextInput';
import BrailleInput from './components/BrailleInput';
import BrailleDisplay from './components/BrailleDisplay';
import BrailleMirror from './components/BrailleMirror';
import ReverseTranslationDisplay from './components/ReverseTranslationDisplay';
import { brailleApi } from './services/api';
import type { TranslationResponse, ReverseTranslationResponse } from './types';
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
  
  // Estado para traducción inversa
  const [brailleCode, setBrailleCode] = useState('');
  const [translatedText, setTranslatedText] = useState('');
  const [reverseError, setReverseError] = useState('');
  const [isReverseLoading, setIsReverseLoading] = useState(false);

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

  /**
   * Maneja la traducción inversa de Braille a texto.
   */
  const handleReverseTranslate = async (brailleCellsInput: number[][]) => {
    setIsReverseLoading(true);
    setReverseError('');
    
    try {
      const result: ReverseTranslationResponse = await brailleApi.reverseTranslate(brailleCellsInput);
      setTranslatedText(result.translated_text);
      
      // Guardar el código Braille para mostrar en la respuesta
      const codeStr = brailleCellsInput
        .map(cell => cell.sort((a, b) => a - b).join(''))
        .join(' ');
      setBrailleCode(codeStr);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error desconocido';
      setReverseError(errorMessage);
      console.error('Error en traducción inversa:', err);
    } finally {
      setIsReverseLoading(false);
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

      {/* Sección de traducción normal: Español → Braille */}
      <section style={{ marginBottom: '3rem' }}>
        <h2 style={{
          fontSize: '1.5rem',
          fontWeight: '700',
          color: '#667eea',
          marginBottom: '1.5rem',
          textAlign: 'center',
          letterSpacing: '-0.3px'
        }}>
          ✍️ Traducción Español → Braille
        </h2>

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

        {/* Vista de espejo */}
        <BrailleMirror
          originalText={originalText}
          brailleCells={brailleCells}
        />
      </section>

      {/* Divisor */}
      <div style={{
        height: '2px',
        background: 'linear-gradient(90deg, transparent, #667eea, transparent)',
        margin: '2rem 0',
        borderRadius: '1px'
      }} />

      {/* Sección de traducción inversa: Braille → Español */}
      <section>
        <h2 style={{
          fontSize: '1.5rem',
          fontWeight: '700',
          color: '#764ba2',
          marginBottom: '1.5rem',
          textAlign: 'center',
          letterSpacing: '-0.3px'
        }}>
          🔄 Traducción Braille → Español
        </h2>

        {/* Input de código Braille */}
        <BrailleInput
          onTranslate={handleReverseTranslate}
          isLoading={isReverseLoading}
        />

        {/* Mensaje de error traducción inversa */}
        {reverseError && (
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
            <strong>Error:</strong> {reverseError}
          </div>
        )}

        {/* Resultado de traducción inversa */}
        <ReverseTranslationDisplay
          brailleCode={brailleCode}
          translatedText={translatedText}
        />
      </section>
    </div>
  );
}

export default App;