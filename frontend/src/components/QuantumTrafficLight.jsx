/**
 * QuantumTrafficLight — Componente React para el semáforo cuántico.
 *
 * Permite ejecutar el circuito cuántico de semáforo desde la interfaz web
 * llamando al endpoint REST POST /api/quantum/run-circuit del backend.
 *
 * Uso:
 *   import QuantumTrafficLight from './components/QuantumTrafficLight';
 *   <QuantumTrafficLight />
 */

// MIT License — Copyright (c) 2026 Ciudad Robot Team

import { useState } from 'react';

/** URL base de la API. Sobreescribir con variable de entorno en producción. */
const API_BASE = import.meta.env?.VITE_API_URL || 'http://localhost:8000';

/**
 * Componente que muestra un botón para ejecutar el circuito cuántico de semáforo
 * y visualiza los resultados de la simulación.
 */
export default function QuantumTrafficLight() {
  const [cargando, setCargando] = useState(false);
  const [resultado, setResultado] = useState(null);
  const [error, setError] = useState(null);

  /** Llama al endpoint y actualiza el estado con la respuesta. */
  const ejecutarCircuito = async () => {
    setCargando(true);
    setError(null);
    setResultado(null);

    try {
      const respuesta = await fetch(`${API_BASE}/api/quantum/run-circuit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ circuit_name: 'traffic_light', params: {} })
      });

      const datos = await respuesta.json();

      if (!respuesta.ok || !datos.success) {
        throw new Error(datos.message || `Error ${respuesta.status}`);
      }

      setResultado(datos.resultado);
    } catch (err) {
      setError(err.message || 'Error desconocido al ejecutar el circuito.');
    } finally {
      setCargando(false);
    }
  };

  return (
    <div style={estilos.contenedor}>
      <h2 style={estilos.titulo}>⚛️ Semáforo Cuántico</h2>
      <p style={estilos.descripcion}>
        Ejecuta el circuito cuántico de semáforo simulado en el backend.
        Usa superposición de qubits para representar estados rojo, amarillo y verde.
      </p>

      <button
        onClick={ejecutarCircuito}
        disabled={cargando}
        style={{ ...estilos.boton, ...(cargando ? estilos.botonDeshabilitado : {}) }}
        aria-busy={cargando}
      >
        {cargando ? (
          <>
            <span style={estilos.spinner} aria-hidden="true">⏳</span>
            {' Ejecutando circuito…'}
          </>
        ) : (
          '▶ Ejecutar circuito cuántico'
        )}
      </button>

      {error && (
        <div style={estilos.error} role="alert">
          <strong>Error:</strong> {error}
        </div>
      )}

      {resultado && (
        <div style={estilos.resultado}>
          <h3 style={estilos.subtitulo}>
            ✅ Resultado — {resultado.circuito || 'Circuito'}
          </h3>

          <div style={estilos.filaInfo}>
            <span style={estilos.etiqueta}>Backend:</span>
            <span>{resultado.backend || 'LocalSimulator'}</span>
          </div>
          <div style={estilos.filaInfo}>
            <span style={estilos.etiqueta}>Shots:</span>
            <span>{resultado.shots}</span>
          </div>
          <div style={estilos.filaInfo}>
            <span style={estilos.etiqueta}>Qubits:</span>
            <span>{resultado.qubits}</span>
          </div>

          {resultado.probabilidades && (
            <>
              <h4 style={estilos.subtitulo2}>Probabilidades por estado</h4>
              {Object.entries(resultado.probabilidades).map(([estado, prob]) => (
                <div key={estado} style={estilos.barraFila}>
                  <span style={estilos.estadoLabel}>{estado}</span>
                  <div style={estilos.barraFondo}>
                    <div
                      style={{
                        ...estilos.barraRelleno,
                        width: `${Math.round(prob * 100)}%`,
                        backgroundColor: colorEstado(estado)
                      }}
                    />
                  </div>
                  <span style={estilos.probValor}>{(prob * 100).toFixed(1)}%</span>
                </div>
              ))}
            </>
          )}

          {resultado.conteos && (
            <>
              <h4 style={estilos.subtitulo2}>Conteos simulados</h4>
              <pre style={estilos.pre}>
                {JSON.stringify(resultado.conteos, null, 2)}
              </pre>
            </>
          )}
        </div>
      )}
    </div>
  );
}

/** Devuelve un color según el nombre del estado del semáforo. */
function colorEstado(estado) {
  if (estado.includes('rojo') || estado === '00') return '#e53e3e';
  if (estado.includes('amarillo') || estado === '01') return '#d69e2e';
  if (estado.includes('verde') || estado === '10') return '#38a169';
  return '#718096';
}

const estilos = {
  contenedor: {
    maxWidth: '600px',
    margin: '2rem auto',
    padding: '1.5rem',
    backgroundColor: '#1a202c',
    borderRadius: '12px',
    color: '#e2e8f0',
    fontFamily: 'system-ui, sans-serif',
    boxShadow: '0 4px 24px rgba(0,0,0,0.4)'
  },
  titulo: {
    fontSize: '1.5rem',
    fontWeight: 700,
    marginBottom: '0.5rem',
    color: '#90cdf4'
  },
  descripcion: {
    fontSize: '0.9rem',
    color: '#a0aec0',
    marginBottom: '1.5rem',
    lineHeight: 1.5
  },
  boton: {
    backgroundColor: '#3182ce',
    color: '#fff',
    border: 'none',
    padding: '0.75rem 1.5rem',
    borderRadius: '8px',
    fontSize: '1rem',
    fontWeight: 600,
    cursor: 'pointer',
    transition: 'background-color 0.2s',
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem'
  },
  botonDeshabilitado: {
    backgroundColor: '#4a5568',
    cursor: 'not-allowed'
  },
  spinner: {
    display: 'inline-block',
    animation: 'spin 1s linear infinite'
  },
  error: {
    marginTop: '1rem',
    padding: '0.75rem 1rem',
    backgroundColor: '#742a2a',
    borderRadius: '8px',
    color: '#fed7d7',
    fontSize: '0.9rem'
  },
  resultado: {
    marginTop: '1.5rem',
    padding: '1rem',
    backgroundColor: '#2d3748',
    borderRadius: '8px'
  },
  subtitulo: {
    fontSize: '1.1rem',
    fontWeight: 600,
    color: '#68d391',
    marginBottom: '0.75rem'
  },
  subtitulo2: {
    fontSize: '0.95rem',
    fontWeight: 600,
    color: '#90cdf4',
    marginTop: '1rem',
    marginBottom: '0.5rem'
  },
  filaInfo: {
    display: 'flex',
    gap: '0.5rem',
    marginBottom: '0.25rem',
    fontSize: '0.9rem'
  },
  etiqueta: {
    color: '#a0aec0',
    minWidth: '80px'
  },
  barraFila: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.75rem',
    marginBottom: '0.4rem',
    fontSize: '0.85rem'
  },
  estadoLabel: {
    minWidth: '130px',
    color: '#cbd5e0',
    fontSize: '0.8rem'
  },
  barraFondo: {
    flex: 1,
    backgroundColor: '#4a5568',
    borderRadius: '4px',
    height: '12px',
    overflow: 'hidden'
  },
  barraRelleno: {
    height: '100%',
    borderRadius: '4px',
    transition: 'width 0.5s ease'
  },
  probValor: {
    minWidth: '48px',
    textAlign: 'right',
    color: '#e2e8f0'
  },
  pre: {
    backgroundColor: '#1a202c',
    padding: '0.75rem',
    borderRadius: '6px',
    fontSize: '0.8rem',
    overflowX: 'auto',
    color: '#a0aec0'
  }
};
