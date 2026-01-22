import React from 'react';
import './ReverseTranslationDisplay.css';

interface ReverseTranslationDisplayProps {
  brailleCode: string;
  translatedText: string;
}

const ReverseTranslationDisplay: React.FC<ReverseTranslationDisplayProps> = ({
  brailleCode,
  translatedText
}) => {
  // No mostrar si no hay datos
  if (!translatedText) {
    return null;
  }

  const handleCopyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(translatedText);
      // Mostrar feedback visual
      const button = document.querySelector('.btn-copy') as HTMLButtonElement;
      if (button) {
        const originalText = button.innerText;
        button.innerText = '✅ ¡Copiado!';
        setTimeout(() => {
          button.innerText = originalText;
        }, 2000);
      }
    } catch (err) {
      alert('Error al copiar al portapapeles');
    }
  };

  return (
    <div className="reverse-translation-container">
      <div className="translation-result">
        <h3 style={{
          fontSize: '1.3rem',
          fontWeight: '600',
          color: '#2c3e50',
          marginBottom: '0.8rem',
          letterSpacing: '-0.3px',
          fontFamily: '"Segoe UI", "Roboto", sans-serif'
        }}>
          📖 Texto en Español
        </h3>
        
        <div className="result-box">
          {translatedText}
        </div>

        <div className="result-actions">
          <button
            onClick={handleCopyToClipboard}
            className="btn-copy"
            title="Copiar al portapapeles"
          >
            📋 Copiar Resultado
          </button>
        </div>

        <div className="result-info">
          <p className="info-item">
            <strong>Código Braille:</strong> {brailleCode}
          </p>
          <p className="info-item">
            <strong>Caracteres:</strong> {translatedText.length}
          </p>
        </div>
      </div>
    </div>
  );
};

export default ReverseTranslationDisplay;
