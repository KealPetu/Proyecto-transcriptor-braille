import React, { useState } from 'react';
import './BrailleInput.css';

interface BrailleInputProps {
  onTranslate: (brailleCells: number[][]) => void;
  isLoading: boolean;
}

const BrailleInput: React.FC<BrailleInputProps> = ({ onTranslate, isLoading }) => {
  const [brailleCode, setBrailleCode] = useState('');
  const [error, setError] = useState('');

  /**
   * Convierte código numérico Braille a celdas
   * Ejemplo: "125 135 123 1" -> [[1,2,5], [1,3,5], [1,2,3], [1]]
   */
  const parseBrailleCode = (code: string): number[][] | null => {
    if (!code || !code.trim()) {
      setError('Por favor ingresa un código Braille');
      return null;
    }

    try {
      // Separar por espacios
      const cells = code.trim().split(/\s+/);
      const parsedCells: number[][] = [];

      for (const cell of cells) {
        // Cada celda es una cadena de dígitos (ej: "125")
        // Convertir a array de números [1, 2, 5]
        const dots = cell.split('').map(d => {
          const num = parseInt(d, 10);
          if (isNaN(num) || num < 1 || num > 6) {
            throw new Error(`Dígito inválido: ${d}. Usa solo 1-6`);
          }
          return num;
        });

        // Validar que no haya duplicados
        if (new Set(dots).size !== dots.length) {
          throw new Error(`Celda "${cell}" contiene puntos duplicados`);
        }

        // Ordenar los puntos
        parsedCells.push(dots.sort((a, b) => a - b));
      }

      if (parsedCells.length === 0) {
        throw new Error('No se encontraron celdas Braille válidas');
      }

      setError('');
      return parsedCells;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Formato inválido';
      setError(message);
      return null;
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const cells = parseBrailleCode(brailleCode);
    if (cells) {
      onTranslate(cells);
    }
  };

  const handleClear = () => {
    setBrailleCode('');
    setError('');
  };

  return (
    <div className="braille-input-container">
      <form onSubmit={handleSubmit} className="braille-input-form">
        <div className="form-section">
          <label htmlFor="braille-code" className="form-label">
            📱 Código Numérico Braille
          </label>
          <p className="form-helper">
            Usa guiones para separar puntos (1-6) y espacios para separar celdas.
            <br />
            Ejemplo: <code>125 135 123 1</code> = "hola"
          </p>

          <textarea
            id="braille-code"
            value={brailleCode}
            onChange={(e) => setBrailleCode(e.target.value)}
            placeholder="Ingresa código como: 125 135 123 1"
            className="braille-textarea"
            disabled={isLoading}
            rows={3}
          />

          {error && (
            <div className="error-message">
              <span>⚠️ {error}</span>
            </div>
          )}

          <div className="button-group">
            <button
              type="submit"
              className="btn-translate"
              disabled={isLoading || !brailleCode.trim()}
            >
              {isLoading ? '⏳ Traduciendo...' : '🔄 Traducir a Español'}
            </button>
            <button
              type="button"
              className="btn-clear"
              onClick={handleClear}
              disabled={isLoading}
            >
              🗑️ Limpiar
            </button>
          </div>
        </div>
      </form>
    </div>
  );
};

export default BrailleInput;
