import React, { useState } from 'react';
import TextInput from './components/TextInput';
import BrailleDisplay from './components/BrailleDisplay';
import { brailleApi, TranslationResponse } from './services/api';
import './App.css';

function App() {
  const [translation, setTranslation] = useState<TranslationResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleTranslate = async (text: string) => {
    setIsLoading(true);
    setError(null);

    try {
      const result = await brailleApi.translate(text);
      setTranslation(result);
    } catch (err) {
      setError('Error al traducir el texto. Por favor, intente nuevamente.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🔤 Transcriptor a Braille</h1>
        <p>Convierte texto normal a sistema Braille de forma instantánea</p>
      </header>

      <main className="App-main">
        <TextInput onTranslate={handleTranslate} isLoading={isLoading} />

        {error && (
          <div className="error-message">
            ⚠️ {error}
          </div>
        )}

        {translation && (
          <BrailleDisplay
            originalText={translation.original_text}
            brailleText={translation.braille_text}
          />
        )}
      </main>

      <footer className="App-footer">
        <p>Proyecto Transcriptor Braille © 2025</p>
      </footer>
    </div>
  );
}

export default App;
