import React from 'react';
import BrailleCell from './BrailleCell'; // Importamos el nuevo componente
import './BrailleDisplay.css';

interface BrailleDisplayProps {
  originalText: string;
  brailleCells: number[][]; // Recibimos la matriz de puntos
}

const BrailleDisplay: React.FC<BrailleDisplayProps> = ({ originalText, brailleCells }) => {

  // Función auxiliar para copiar texto (convertimos los puntos a texto unicode para el clipboard)
  const handleCopy = () => {
    // Lógica simplificada para demo: solo avisa
    alert('Función de copiado pendiente de implementar con caracteres Unicode');
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
        {/* Contenedor Flex para alinear las celdas */}
        <div className="braille-grid-container" style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', padding: '1rem', background: '#f8f9fa', borderRadius: '6px' }}>
          {brailleCells.length > 0 ? (
            brailleCells.map((cell, index) => (
              <BrailleCell key={index} activeDots={cell} />
            ))
          ) : (
            <span style={{ color: '#999' }}>La traducción aparecerá aquí...</span>
          )}
        </div>
      </div>
    </div>
  );
};

export default BrailleDisplay;