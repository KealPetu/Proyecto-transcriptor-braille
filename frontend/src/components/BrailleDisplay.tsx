// frontend/src/components/BrailleDisplay.tsx
import React, { useState } from 'react';
import BrailleCell from './BrailleCell';
import { brailleApi } from '../services/api';
import './BrailleDisplay.css';

interface BrailleDisplayProps {
  originalText: string;
  brailleCells: number[][];
}

const BrailleDisplay: React.FC<BrailleDisplayProps> = ({ originalText, brailleCells }) => {
  // Estado para controlar la carga de los botones de descarga
  const [isDownloading, setIsDownloading] = useState<'pdf' | 'img' | null>(null);

  // Función genérica para manejar la descarga de Blobs
  const handleDownload = async (type: 'pdf' | 'img') => {
    if (!originalText) return;
    
    setIsDownloading(type);
    try {
      let blob: Blob;
      let filename: string;

      if (type === 'img') {
        blob = await brailleApi.downloadImage(originalText);
        filename = `braille-${originalText.substring(0, 10)}.png`;
      } else {
        blob = await brailleApi.downloadPdf(originalText);
        filename = `braille-${originalText.substring(0, 10)}.pdf`;
      }

      // Truco para descargar archivos en el navegador:
      // 1. Crear una URL temporal que apunte al Blob en memoria
      const url = window.URL.createObjectURL(blob);
      
      // 2. Crear un elemento <a> invisible
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', filename);
      
      // 3. Simular clic y limpiar
      document.body.appendChild(link);
      link.click();
      link.parentNode?.removeChild(link);
      window.URL.revokeObjectURL(url); // Liberar memoria

    } catch (error) {
      console.error("Error en descarga:", error);
      alert("Hubo un error al generar el archivo. Revisa la consola.");
    } finally {
      setIsDownloading(null);
    }
  };

  return (
    <div className="braille-display-container">
      <div className="display-section">
        <h3>Texto Original:</h3>
        <div className="text-box original-text">
          {originalText || "Esperando texto..."}
        </div>
      </div>

      <div className="display-section">
        <h3>Traducción Visual (Cuadratines):</h3>
        <div className="braille-grid-container">
          {brailleCells.length > 0 ? (
            brailleCells.map((cell, index) => (
              <BrailleCell key={index} activeDots={cell} />
            ))
          ) : (
            <span style={{ color: '#999' }}>La traducción aparecerá aquí...</span>
          )}
        </div>

        {/* Solo mostramos los botones si hay una traducción activa */}
        {brailleCells.length > 0 && (
          <div className="actions-bar">
             <button 
               onClick={() => handleDownload('img')} 
               className="btn-download btn-img"
               disabled={isDownloading !== null}
             >
               {isDownloading === 'img' ? 'Generando...' : '🖼️ Descargar Imagen'}
             </button>
             
             <button 
               onClick={() => handleDownload('pdf')} 
               className="btn-download btn-pdf"
               disabled={isDownloading !== null}
             >
               {isDownloading === 'pdf' ? 'Generando...' : '📄 Descargar PDF'}
             </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default BrailleDisplay;