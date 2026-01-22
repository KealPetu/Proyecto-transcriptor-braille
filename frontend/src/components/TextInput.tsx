import React, { useState } from 'react';
import './TextInput.css';

interface TextInputProps {
  onTranslate: (text: string) => Promise<void>;
  isLoading: boolean;
}

const TextInput: React.FC<TextInputProps> = ({
  onTranslate,
  isLoading
}) => {
  const [text, setText] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (text.trim()) {
      onTranslate(text);
    }
  };

  const handleClear = () => {
    setText('');
  };

  return (
    <div className="text-input-container">
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <label htmlFor="text-input">Ingrese el texto a transcribir:</label>
          <textarea
            id="text-input"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Escriba aquí el texto que desea convertir a Braille..."
            rows={6}
            disabled={isLoading}
            maxLength={500}
          />
          <div className="character-count">
            {text.length}/500 caracteres
          </div>
        </div>

        <div className="button-group">
          <button
            type="submit"
            disabled={!text.trim() || isLoading}
            className="btn-primary"
          >
            {isLoading ? 'Traduciendo...' : 'Traducir a Braille'}
          </button>
          <button
            type="button"
            onClick={handleClear}
            disabled={!text || isLoading}
            className="btn-secondary"
          >
            Limpiar
          </button>
        </div>
      </form>
    </div>
  );
};

export default TextInput;
