import React from 'react';
import './BrailleDisplay.css';

interface BrailleDisplayProps {
  originalText: string;
  brailleText: string;
}

const BrailleDisplay: React.FC<BrailleDisplayProps> = ({ originalText, brailleText }) => {
  const handleCopy = () => {
    navigator.clipboard.writeText(brailleText);
    alert('Texto Braille copiado al portapapeles');
  };

  return (
    <div className="braille-display-container">
      <div className="display-section">
        <h3>Texto Original:</h3>
        <div className="text-box original-text">
          {originalText}
        </div>
      </div>

      <div className="display-section">
        <h3>Texto en Braille:</h3>
        <div className="text-box braille-text">
          {brailleText}
        </div>
        <button onClick={handleCopy} className="btn-copy">
          📋 Copiar Braille
        </button>
      </div>
    </div>
  );
};

export default BrailleDisplay;
