import React, { useState } from 'react';
import BrailleCell from './BrailleCell';
import { brailleApi } from '../services/api';
import './BrailleMirror.css';

interface BrailleMirrorProps {
  originalText: string;
  brailleCells: number[][];
}

const BrailleMirror: React.FC<BrailleMirrorProps> = ({ originalText, brailleCells }) => {
  const [isDownloading, setIsDownloading] = useState<'mirror-pdf' | 'mirror-img' | null>(null);

  /**
   * Espeja una celda de braille
   * Los puntos 1,2,3 se convierten en 4,5,6 y viceversa
   * 1 4  ->  4 1
   * 2 5  ->  5 2
   * 3 6  ->  6 3
   */
  const mirrorBrailleCell = (cell: number[]): number[] => {
    const mirrorMap: { [key: number]: number } = {
      1: 4,
      2: 5,
      3: 6,
      4: 1,
      5: 2,
      6: 3
    };

    return cell.map(dot => mirrorMap[dot]).sort((a, b) => a - b);
  };

  // Crear las celdas espejeadas
  const mirroredCells = brailleCells.map(cell => mirrorBrailleCell(cell));

  // Función genérica para manejar la descarga de Blobs
  const handleDownload = async (type: 'mirror-pdf' | 'mirror-img') => {
    if (!originalText) return;
    
    setIsDownloading(type);
    try {
      let blob: Blob;
      let filename: string;

      if (type === 'mirror-img') {
        blob = await brailleApi.downloadImage(originalText, true);
        filename = `braille-espejo-${originalText.substring(0, 10)}.png`;
      } else {
        blob = await brailleApi.downloadPdf(originalText, true);
        filename = `braille-espejo-${originalText.substring(0, 10)}.pdf`;
      }

      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      link.parentNode?.removeChild(link);
      window.URL.revokeObjectURL(url);

    } catch (error) {
      console.error("Error en descarga:", error);
      alert("Hubo un error al generar el archivo. Revisa la consola.");
    } finally {
      setIsDownloading(null);
    }
  };

  // No mostrar si no hay datos
  if (brailleCells.length === 0) {
    return null;
  }

  return (
    <div className="braille-mirror-container">
      <div className="mirror-section">
        <h3 style={{
          fontSize: '1.3rem',
          fontWeight: '600',
          color: '#2c3e50',
          marginBottom: '0.8rem',
          letterSpacing: '-0.3px',
          fontFamily: '"Segoe UI", "Roboto", sans-serif'
        }}>
          🔄 Resultado (Espejo)
        </h3>
        <div className="braille-grid-container mirror">
          {mirroredCells.map((cell, index) => (
            <BrailleCell key={index} activeDots={cell} />
          ))}
        </div>

        <div className="actions-bar">
          <button 
            onClick={() => handleDownload('mirror-img')} 
            className="btn-download btn-img"
            disabled={isDownloading !== null}
          >
            {isDownloading === 'mirror-img' ? 'Generando...' : '⬇️ Descargar Espejo'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default BrailleMirror;
