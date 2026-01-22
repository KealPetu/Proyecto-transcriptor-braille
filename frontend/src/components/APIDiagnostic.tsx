import React, { useState, useEffect } from 'react';

interface DiagnosticInfo {
  backendUrl: string;
  backendStatus: 'connected' | 'disconnected' | 'checking';
  corsStatus: 'ok' | 'error' | 'checking';
  responseTime: number | null;
  errorMessage: string | null;
}

const APIDiagnostic: React.FC = () => {
  const [diagnostic, setDiagnostic] = useState<DiagnosticInfo>({
    backendUrl: process.env.REACT_APP_API_URL || 'http://localhost:8000',
    backendStatus: 'checking',
    corsStatus: 'checking',
    responseTime: null,
    errorMessage: null
  });

  useEffect(() => {
    const checkBackend = async () => {
      const startTime = Date.now();
      const backendUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';

      try {
        console.log(`[Diagnóstico] Intentando conectar a: ${backendUrl}/health`);
        
        const response = await fetch(`${backendUrl}/health`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        const responseTime = Date.now() - startTime;

        if (response.ok) {
          const data = await response.json();
          console.log('[Diagnóstico] Respuesta del backend:', data);
          
          setDiagnostic(prev => ({
            ...prev,
            backendStatus: 'connected',
            corsStatus: 'ok',
            responseTime,
            errorMessage: null
          }));
        } else {
          console.error(`[Diagnóstico] Backend respondió con: ${response.status} ${response.statusText}`);
          setDiagnostic(prev => ({
            ...prev,
            backendStatus: 'disconnected',
            responseTime,
            errorMessage: `HTTP ${response.status}: ${response.statusText}`
          }));
        }
      } catch (error) {
        console.error('[Diagnóstico] Error de conexión:', error);
        const errorMsg = error instanceof Error ? error.message : 'Error desconocido';
        
        setDiagnostic(prev => ({
          ...prev,
          backendStatus: 'disconnected',
          corsStatus: 'error',
          responseTime: null,
          errorMessage: errorMsg
        }));
      }
    };

    checkBackend();
    const interval = setInterval(checkBackend, 5000); // Verificar cada 5 segundos

    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{
      padding: '1rem',
      marginBottom: '2rem',
      backgroundColor: diagnostic.backendStatus === 'connected' ? '#e8f5e9' : '#ffebee',
      border: `2px solid ${diagnostic.backendStatus === 'connected' ? '#4caf50' : '#f44336'}`,
      borderRadius: '8px',
      fontFamily: 'monospace',
      fontSize: '0.9rem'
    }}>
      <h4 style={{ marginTop: 0, color: diagnostic.backendStatus === 'connected' ? '#2e7d32' : '#c62828' }}>
        {diagnostic.backendStatus === 'checking' && '⏳ Verificando conexión...'}
        {diagnostic.backendStatus === 'connected' && '✓ Backend Conectado'}
        {diagnostic.backendStatus === 'disconnected' && '✗ Backend Desconectado'}
      </h4>
      
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
        <div>
          <strong>URL Backend:</strong>
          <div style={{ color: '#666', wordBreak: 'break-all' }}>{diagnostic.backendUrl}</div>
        </div>
        
        <div>
          <strong>Tiempo de Respuesta:</strong>
          <div style={{ color: '#666' }}>
            {diagnostic.responseTime !== null ? `${diagnostic.responseTime}ms` : 'N/A'}
          </div>
        </div>

        <div>
          <strong>Estado CORS:</strong>
          <div style={{ color: '#666' }}>
            {diagnostic.corsStatus === 'checking' && 'Verificando...'}
            {diagnostic.corsStatus === 'ok' && '✓ OK'}
            {diagnostic.corsStatus === 'error' && '✗ Error'}
          </div>
        </div>

        <div>
          <strong>Estado Backend:</strong>
          <div style={{ color: '#666' }}>
            {diagnostic.backendStatus === 'checking' && 'Verificando...'}
            {diagnostic.backendStatus === 'connected' && '✓ Operativo'}
            {diagnostic.backendStatus === 'disconnected' && '✗ No responde'}
          </div>
        </div>
      </div>

      {diagnostic.errorMessage && (
        <div style={{
          marginTop: '1rem',
          padding: '0.5rem',
          backgroundColor: '#ffcdd2',
          borderRadius: '4px',
          color: '#b71c1c'
        }}>
          <strong>Error:</strong> {diagnostic.errorMessage}
        </div>
      )}

      <div style={{ marginTop: '1rem', fontSize: '0.85rem', color: '#666' }}>
        <strong>Consejos:</strong>
        <ul style={{ margin: '0.5rem 0', paddingLeft: '1.5rem' }}>
          <li>Si ves "Backend Desconectado", verifica que el servidor esté corriendo en {diagnostic.backendUrl}</li>
          <li>Abre {diagnostic.backendUrl}/docs en otra pestaña para verificar que el backend responde</li>
          <li>Si ves error de CORS, verifica la configuración del backend</li>
          <li>Este diagnóstico se actualiza cada 5 segundos automáticamente</li>
        </ul>
      </div>
    </div>
  );
};

export default APIDiagnostic;
