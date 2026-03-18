/**
 * MIT License - Usar misma licencia que el repositorio
 *
 * QuantumTrafficLight - Componente React para demostración del circuito cuántico.
 *
 * Muestra un botón para ejecutar el circuito de semáforo cuántico via API
 * y visualiza los resultados JSON o los errores.
 */

import React, { useState } from 'react';

/**
 * Componente funcional QuantumTrafficLight.
 *
 * Realiza una petición POST a /api/quantum/run-circuit con el circuito
 * "traffic_light" y muestra los resultados obtenidos del simulador cuántico.
 */
function QuantumTrafficLight() {
  const [resultado, setResultado] = useState(null);
  const [error, setError] = useState(null);
  const [cargando, setCargando] = useState(false);

  const ejecutarCircuito = async () => {
    setCargando(true);
    setResultado(null);
    setError(null);

    try {
      const respuesta = await fetch('/api/quantum/run-circuit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          circuit_name: 'traffic_light',
          params: { qubits: 3, shots: 1024 },
        }),
      });

      const datos = await respuesta.json();

      if (!respuesta.ok) {
        setError(datos.error || `Error HTTP ${respuesta.status}`);
      } else {
        setResultado(datos);
      }
    } catch (err) {
      setError(`Error de red: ${err.message}`);
    } finally {
      setCargando(false);
    }
  };

  return (
    <div style={estilos.contenedor}>
      <h2 style={estilos.titulo}>⚛️ Semáforo Cuántico</h2>
      <p style={estilos.descripcion}>
        Ejecuta un circuito cuántico simulado que modela los estados de un semáforo
        usando superposición y entrelazamiento de qubits.
      </p>

      <button
        style={{
          ...estilos.boton,
          ...(cargando ? estilos.botonDesactivado : {}),
        }}
        onClick={ejecutarCircuito}
        disabled={cargando}
        aria-label="Ejecutar circuito cuántico"
      >
        {cargando ? '⏳ Ejecutando...' : '▶ Ejecutar circuito cuántico'}
      </button>

      {cargando && (
        <div style={estilos.spinner} role="status" aria-live="polite">
          <span>Simulando circuito cuántico...</span>
        </div>
      )}

      {error && (
        <div style={estilos.error} role="alert">
          <strong>Error:</strong> {error}
        </div>
      )}

      {resultado && !error && (
        <div style={estilos.resultado}>
          <h3 style={estilos.subtitulo}>Resultados del simulador</h3>
          <div style={estilos.infoRow}>
            <span>🖥️ Backend:</span>
            <strong>{resultado.backend}</strong>
          </div>
          <div style={estilos.infoRow}>
            <span>🔢 Shots:</span>
            <strong>{resultado.shots}</strong>
          </div>
          <div style={estilos.infoRow}>
            <span>⚛️ Qubits:</span>
            <strong>{resultado.circuit_qubits}</strong>
          </div>

          <h4 style={estilos.subtitulo}>Conteos de medición</h4>
          <div style={estilos.conteos}>
            {resultado.counts &&
              Object.entries(resultado.counts)
                .sort(([, a], [, b]) => b - a)
                .map(([estado, conteo]) => (
                  <div key={estado} style={estilos.filaConteo}>
                    <span style={estilos.estado}>|{estado}⟩</span>
                    <div style={estilos.barraContenedor}>
                      <div
                        style={{
                          ...estilos.barra,
                          width: `${Math.round((conteo / resultado.shots) * 100)}%`,
                        }}
                      />
                    </div>
                    <span style={estilos.conteoNum}>{conteo}</span>
                  </div>
                ))}
          </div>

          <details style={estilos.detalles}>
            <summary style={estilos.summary}>Ver JSON completo</summary>
            <pre style={estilos.pre}>{JSON.stringify(resultado, null, 2)}</pre>
          </details>
        </div>
      )}
    </div>
  );
}

const estilos = {
  contenedor: {
    fontFamily: 'monospace, sans-serif',
    maxWidth: '640px',
    margin: '2rem auto',
    padding: '1.5rem',
    borderRadius: '8px',
    background: '#0d1117',
    color: '#e6edf3',
    boxShadow: '0 4px 24px rgba(0,0,0,0.4)',
    border: '1px solid #30363d',
  },
  titulo: {
    fontSize: '1.5rem',
    marginBottom: '0.5rem',
    color: '#58a6ff',
  },
  subtitulo: {
    fontSize: '1rem',
    color: '#79c0ff',
    marginTop: '1rem',
    marginBottom: '0.4rem',
  },
  descripcion: {
    fontSize: '0.9rem',
    color: '#8b949e',
    marginBottom: '1rem',
  },
  boton: {
    background: '#238636',
    color: '#fff',
    border: 'none',
    padding: '0.6rem 1.4rem',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '1rem',
    fontWeight: 'bold',
    transition: 'background 0.2s',
  },
  botonDesactivado: {
    background: '#2d333b',
    color: '#8b949e',
    cursor: 'not-allowed',
  },
  spinner: {
    marginTop: '0.8rem',
    color: '#79c0ff',
    fontSize: '0.9rem',
  },
  error: {
    marginTop: '1rem',
    padding: '0.8rem',
    background: '#3d1a1a',
    border: '1px solid #f85149',
    borderRadius: '6px',
    color: '#ff7b72',
  },
  resultado: {
    marginTop: '1.2rem',
  },
  infoRow: {
    display: 'flex',
    gap: '0.5rem',
    marginBottom: '0.2rem',
    fontSize: '0.9rem',
    color: '#c9d1d9',
  },
  conteos: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.3rem',
  },
  filaConteo: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.6rem',
    fontSize: '0.85rem',
  },
  estado: {
    width: '60px',
    color: '#e3b341',
    fontWeight: 'bold',
  },
  barraContenedor: {
    flex: 1,
    height: '14px',
    background: '#21262d',
    borderRadius: '4px',
    overflow: 'hidden',
  },
  barra: {
    height: '100%',
    background: '#388bfd',
    borderRadius: '4px',
    transition: 'width 0.4s ease',
  },
  conteoNum: {
    width: '50px',
    textAlign: 'right',
    color: '#8b949e',
  },
  detalles: {
    marginTop: '1rem',
  },
  summary: {
    cursor: 'pointer',
    color: '#8b949e',
    fontSize: '0.85rem',
  },
  pre: {
    background: '#161b22',
    padding: '0.8rem',
    borderRadius: '6px',
    fontSize: '0.75rem',
    overflowX: 'auto',
    color: '#c9d1d9',
    marginTop: '0.4rem',
  },
};

export default QuantumTrafficLight;
