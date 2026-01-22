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

  /**
   * Maneja la descarga de imagen PNG.
   */
  const handleDownloadImage = async () => {
    if (!originalText) {
      setError('Primero traduce un texto');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const blob = await brailleApi.downloadImage(originalText, true);
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `braille_${originalText.substring(0, 10).replace(/\s+/g, '_')}.png`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error al descargar imagen';
      setError(errorMessage);
      console.error('Error descargando imagen:', err);
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Maneja la descarga de documento PDF.
   */
  const handleDownloadPdf = async () => {
    if (!originalText) {
      setError('Primero traduce un texto');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const blob = await brailleApi.downloadPdf(originalText, `Braille: ${originalText}`);
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `braille_${originalText.substring(0, 10).replace(/\s+/g, '_')}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error al descargar PDF';
      setError(errorMessage);
      console.error('Error descargando PDF:', err);
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
        
        {/* Estado de API */}
        <div style={{ marginTop: '1rem' }}>
          <span
            style={{
              display: 'inline-block',
              padding: '0.5rem 1rem',
              borderRadius: '4px',
              fontSize: '0.875rem',
              fontWeight: '500',
              backgroundColor: isApiHealthy ? '#4CAF50' : '#f44336',
              color: 'white'
            }}
          >
            {isApiHealthy ? '✓ API Conectada' : '✗ API No disponible'}
          </span>
        </div>
      </header>

      {/* Input de texto */}
      <TextInput
        onTranslate={handleTranslate}
        isLoading={isLoading}
        onDownloadImage={handleDownloadImage}
        onDownloadPdf={handleDownloadPdf}
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