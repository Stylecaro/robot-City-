// MIT License - Copyright (c) 2026 Ciudad Robot Team
/**
 * QuantumTrafficLight
 * ====================
 * Componente React de demostración del semáforo cuántico.
 * Llama al endpoint POST /api/quantum/run-circuit y muestra el resultado
 * con un spinner mientras espera la respuesta.
 */

import React, { useState, useCallback } from 'react';

const API_URL = '/api/quantum/run-circuit';

const DEFAULT_PARAMS = {
  circuit_name: 'traffic_light',
  theta: 0.8,
  phi: 0.2,
  n_qubits: 3,
  shots: 1024,
};

/**
 * Determina el color del semáforo según los conteos de medición.
 * El qubit 0 codifica el estado del semáforo (0=rojo, 1=verde).
 *
 * @param {Object} conteos - Mapa bitstring → conteos
 * @returns {'green'|'red'|'yellow'} Color del semáforo
 */
function calcularColorSemaforo(conteos) {
  if (!conteos || Object.keys(conteos).length === 0) return 'yellow';
  let totalVerde = 0;
  let totalTotal = 0;
  for (const [bits, count] of Object.entries(conteos)) {
    totalTotal += count;
    if (bits[bits.length - 1] === '1') {
      totalVerde += count;
    }
  }
  if (totalTotal === 0) return 'yellow';
  const probVerde = totalVerde / totalTotal;
  if (probVerde > 0.55) return 'green';
  if (probVerde < 0.45) return 'red';
  return 'yellow';
}

/** Componente de semáforo visual */
function Semaforo({ color }) {
  const colores = ['red', 'yellow', 'green'];
  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 8,
        background: '#222',
        borderRadius: 12,
        padding: '16px 20px',
        width: 80,
        margin: '0 auto',
      }}
    >
      {colores.map((c) => (
        <div
          key={c}
          style={{
            width: 40,
            height: 40,
            borderRadius: '50%',
            background: color === c ? c : '#444',
            boxShadow: color === c ? `0 0 16px ${c}` : 'none',
            transition: 'all 0.3s ease',
          }}
        />
      ))}
    </div>
  );
}

/** Spinner de carga */
function Spinner() {
  return (
    <div
      style={{
        width: 36,
        height: 36,
        border: '4px solid #e0e0e0',
        borderTop: '4px solid #7c3aed',
        borderRadius: '50%',
        animation: 'spin 0.8s linear infinite',
        margin: '16px auto',
      }}
    />
  );
}

/**
 * Componente principal QuantumTrafficLight.
 * Permite ajustar parámetros y ejecutar el circuito cuántico de semáforo.
 */
export default function QuantumTrafficLight() {
  const [params, setParams] = useState(DEFAULT_PARAMS);
  const [resultado, setResultado] = useState(null);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState(null);

  const ejecutarCircuito = useCallback(async () => {
    setCargando(true);
    setError(null);
    setResultado(null);

    try {
      const respuesta = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(params),
        signal: AbortSignal.timeout(35000),
      });

      const json = await respuesta.json();

      if (!respuesta.ok || !json.success) {
        throw new Error(json.message || json.error || `HTTP ${respuesta.status}`);
      }

      setResultado(json.data);
    } catch (err) {
      setError(err.name === 'TimeoutError'
        ? 'Tiempo de espera agotado (>35s). El servidor puede estar ocupado.'
        : err.message);
    } finally {
      setCargando(false);
    }
  }, [params]);

  const colorSemaforo = resultado
    ? calcularColorSemaforo(resultado?.resultado?.conteos)
    : null;

  const handleParamChange = (key, value) => {
    setParams((prev) => ({
      ...prev,
      [key]: isNaN(value) || value === '' ? value : Number(value),
    }));
  };

  return (
    <div
      style={{
        fontFamily: 'system-ui, sans-serif',
        maxWidth: 520,
        margin: '32px auto',
        padding: 24,
        borderRadius: 16,
        background: '#f8f4ff',
        border: '1px solid #ddd6fe',
        boxShadow: '0 4px 24px rgba(124,58,237,0.08)',
      }}
    >
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>

      <h2 style={{ textAlign: 'center', color: '#5b21b6', marginBottom: 4 }}>
        ⚛️ Semáforo Cuántico
      </h2>
      <p style={{ textAlign: 'center', color: '#6b7280', marginBottom: 24, fontSize: 14 }}>
        Circuito cuántico de control de tráfico — quantum-core
      </p>

      {/* Controles de parámetros */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginBottom: 20 }}>
        {[
          { key: 'theta', label: 'θ (densidad tráfico)', min: 0, max: 3.14, step: 0.1 },
          { key: 'phi', label: 'φ (fase emergencia)', min: 0, max: 3.14, step: 0.1 },
          { key: 'n_qubits', label: 'Qubits', min: 2, max: 8, step: 1 },
          { key: 'shots', label: 'Disparos', min: 128, max: 4096, step: 128 },
        ].map(({ key, label, min, max, step }) => (
          <label key={key} style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
            <span style={{ fontSize: 13, color: '#374151', fontWeight: 500 }}>{label}</span>
            <input
              type="number"
              min={min}
              max={max}
              step={step}
              value={params[key]}
              onChange={(e) => handleParamChange(key, e.target.value)}
              disabled={cargando}
              style={{
                padding: '6px 10px',
                borderRadius: 8,
                border: '1px solid #c4b5fd',
                fontSize: 14,
                background: '#fff',
              }}
            />
          </label>
        ))}
      </div>

      {/* Botón ejecutar */}
      <button
        onClick={ejecutarCircuito}
        disabled={cargando}
        style={{
          width: '100%',
          padding: '12px 0',
          background: cargando ? '#a78bfa' : '#7c3aed',
          color: '#fff',
          border: 'none',
          borderRadius: 10,
          fontSize: 16,
          fontWeight: 600,
          cursor: cargando ? 'not-allowed' : 'pointer',
          transition: 'background 0.2s',
          marginBottom: 20,
        }}
      >
        {cargando ? '⏳ Ejecutando circuito...' : '▶ Ejecutar Circuito Cuántico'}
      </button>

      {/* Spinner */}
      {cargando && <Spinner />}

      {/* Error */}
      {error && (
        <div
          style={{
            padding: 12,
            background: '#fee2e2',
            border: '1px solid #fca5a5',
            borderRadius: 8,
            color: '#dc2626',
            fontSize: 14,
            marginBottom: 16,
          }}
        >
          ❌ <strong>Error:</strong> {error}
        </div>
      )}

      {/* Resultado */}
      {resultado && (
        <div>
          <div style={{ display: 'flex', gap: 24, alignItems: 'center', marginBottom: 20 }}>
            <Semaforo color={colorSemaforo} />
            <div>
              <p style={{ margin: 0, fontWeight: 600, color: '#1f2937' }}>
                Estado:{' '}
                <span
                  style={{
                    color: colorSemaforo === 'green' ? '#16a34a' : colorSemaforo === 'red' ? '#dc2626' : '#d97706',
                    textTransform: 'uppercase',
                  }}
                >
                  {colorSemaforo === 'green' ? 'Verde (Paso)' : colorSemaforo === 'red' ? 'Rojo (Stop)' : 'Amarillo (Precaución)'}
                </span>
              </p>
              <p style={{ margin: '4px 0 0', fontSize: 13, color: '#6b7280' }}>
                Circuito: <code>{resultado.circuito?.nombre}</code> · {resultado.circuito?.n_qubits} qubits · {resultado.circuito?.n_puertas} puertas
              </p>
              <p style={{ margin: '2px 0 0', fontSize: 13, color: '#6b7280' }}>
                Backend: <code>{resultado.resultado?.backend}</code> · {resultado.resultado?.shots} shots
              </p>
            </div>
          </div>

          <details style={{ background: '#fff', borderRadius: 8, padding: 12, border: '1px solid #e5e7eb' }}>
            <summary style={{ cursor: 'pointer', fontWeight: 600, color: '#5b21b6', fontSize: 14 }}>
              📊 Ver conteos de medición ({Object.keys(resultado.resultado?.conteos || {}).length} estados)
            </summary>
            <div style={{ marginTop: 10, overflowX: 'auto' }}>
              <table style={{ width: '100%', fontSize: 13, borderCollapse: 'collapse' }}>
                <thead>
                  <tr style={{ background: '#f3f4f6' }}>
                    <th style={{ padding: '4px 8px', textAlign: 'left' }}>Estado (bits)</th>
                    <th style={{ padding: '4px 8px', textAlign: 'right' }}>Conteos</th>
                    <th style={{ padding: '4px 8px', textAlign: 'right' }}>Probabilidad</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(resultado.resultado?.conteos || {})
                    .sort(([, a], [, b]) => b - a)
                    .slice(0, 10)
                    .map(([bits, count]) => (
                      <tr key={bits} style={{ borderTop: '1px solid #f3f4f6' }}>
                        <td style={{ padding: '4px 8px', fontFamily: 'monospace' }}>{bits}</td>
                        <td style={{ padding: '4px 8px', textAlign: 'right' }}>{count}</td>
                        <td style={{ padding: '4px 8px', textAlign: 'right' }}>
                          {((count / resultado.resultado.shots) * 100).toFixed(1)}%
                        </td>
                      </tr>
                    ))}
                </tbody>
              </table>
            </div>
          </details>
        </div>
      )}
    </div>
  );
}
