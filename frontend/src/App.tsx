import React, { useState } from 'react';
import TextInput from './components/TextInput';
import BrailleDisplay from './components/BrailleDisplay';
import { brailleApi } from './services/api';
import './App.css';

function App() {
  const [originalText, setOriginalText] = useState('');
  const [brailleCells, setBrailleCells] = useState<number[][]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleTranslate = async (text: string) => {
    setIsLoading(true);
    setError('');
    try {
      const result = await brailleApi.translate(text);
      setOriginalText(result.original_text);
      setBrailleCells(result.braille_cells);
    } catch (err) {
      console.error(err);
      setError('Error al conectar con el servidor de traducción.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App" style={{ maxWidth: '800px', margin: '0 auto', padding: '2rem' }}>
      <h1 style={{ textAlign: 'center', color: '#333' }}>Traductor Español - Braille</h1>

      <TextInput onTranslate={handleTranslate} isLoading={isLoading} />

      {error && <div style={{ color: 'red', marginBottom: '1rem' }}>{error}</div>}

      <BrailleDisplay
        originalText={originalText}
        brailleCells={brailleCells}
      />
    </div>
  );
}

export default App;