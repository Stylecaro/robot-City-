/**
 * Rutas para el módulo cuántico de Ciudad Robot.
 *
 * Expone un endpoint que invoca el script Python de demostración del semáforo
 * cuántico mediante child_process y devuelve la salida JSON al cliente.
 *
 * Endpoint disponible:
 *   POST /api/quantum/run-circuit
 *
 * Cuerpo esperado:
 *   { "circuit_name": "traffic_light", "params": {} }
 *
 * Respuesta exitosa:
 *   { "success": true, "circuit_name": "traffic_light", "resultado": { ... } }
 *
 * Nota: El script Python se ejecuta en un proceso separado. Asegúrese de que
 * Python 3 y numpy estén instalados (ver quantum-core/requirements.txt).
 */

// MIT License — Copyright (c) 2026 Ciudad Robot Team

'use strict';

const express = require('express');
const { spawn } = require('child_process');
const path = require('path');
const router = express.Router();

/** Circuitos soportados y sus scripts de demostración correspondientes. */
const CIRCUITOS_SOPORTADOS = {
  traffic_light: path.join(
    __dirname,
    '../../quantum-core/examples/quantum_traffic_light_demo.py'
  )
};

/**
 * POST /api/quantum/run-circuit
 *
 * Ejecuta un circuito cuántico simulado llamando al script Python correspondiente.
 *
 * Body (JSON):
 *   - circuit_name {string} — Nombre del circuito a ejecutar.
 *     Valores válidos: "traffic_light"
 *   - params {object} — Parámetros adicionales (ignorados en la versión actual).
 *
 * Respuestas:
 *   200 — Ejecución exitosa con resultado JSON del circuito.
 *   400 — Parámetros inválidos o circuit_name no soportado.
 *   500 — Error interno al ejecutar el script Python.
 *   503 — Timeout: el script tardó más de 30 segundos.
 */
router.post('/run-circuit', (req, res) => {
  const { circuit_name, params } = req.body || {};

  // Validación de entrada
  if (!circuit_name || typeof circuit_name !== 'string') {
    return res.status(400).json({
      success: false,
      error: 'Parámetro inválido',
      message: 'El campo "circuit_name" es obligatorio y debe ser una cadena de texto.'
    });
  }

  const circuitNameSanitizado = circuit_name.trim().toLowerCase();

  if (!Object.prototype.hasOwnProperty.call(CIRCUITOS_SOPORTADOS, circuitNameSanitizado)) {
    return res.status(400).json({
      success: false,
      error: 'Circuito no soportado',
      message: `El circuito "${circuit_name}" no está disponible. Circuitos válidos: ${Object.keys(CIRCUITOS_SOPORTADOS).join(', ')}`
    });
  }

  const scriptPath = CIRCUITOS_SOPORTADOS[circuitNameSanitizado];

  let stdout = '';
  let stderr = '';
  let respondido = false;

  // Invocar el script Python en un proceso separado
  const proceso = spawn('python3', [scriptPath], {
    timeout: 30000,
    env: { ...process.env }
  });

  proceso.stdout.on('data', (data) => {
    stdout += data.toString();
  });

  proceso.stderr.on('data', (data) => {
    stderr += data.toString();
  });

  // Timeout de seguridad (30 segundos)
  const timer = setTimeout(() => {
    if (!respondido) {
      respondido = true;
      proceso.kill('SIGTERM');
      return res.status(503).json({
        success: false,
        error: 'Timeout',
        message: 'El script cuántico tardó demasiado en responder (límite: 30s).'
      });
    }
  }, 30000);

  proceso.on('close', (code) => {
    clearTimeout(timer);
    if (respondido) return;
    respondido = true;

    if (code !== 0) {
      return res.status(500).json({
        success: false,
        error: 'Error en script Python',
        message: `El script terminó con código ${code}.`,
        stderr: stderr.slice(0, 500) // limitar tamaño del mensaje de error
      });
    }

    // Extraer el JSON de la salida (última aparición de un bloque JSON)
    let resultado = null;
    const lineas = stdout.split('\n').filter(Boolean);
    for (let i = lineas.length - 1; i >= 0; i--) {
      const linea = lineas[i].trim();
      if (linea.startsWith('{')) {
        try {
          resultado = JSON.parse(linea);
          break;
        } catch (_) {
          // Intentar con el bloque multilínea restante
        }
      }
    }

    // Si no encontramos JSON en línea individual, buscar bloque multilínea
    if (!resultado) {
      const inicioJson = stdout.indexOf('{');
      if (inicioJson !== -1) {
        try {
          resultado = JSON.parse(stdout.slice(inicioJson));
        } catch (_) {
          resultado = { salida_raw: stdout.slice(0, 1000) };
        }
      } else {
        resultado = { salida_raw: stdout.slice(0, 1000) };
      }
    }

    return res.status(200).json({
      success: true,
      circuit_name: circuitNameSanitizado,
      resultado
    });
  });

  proceso.on('error', (err) => {
    clearTimeout(timer);
    if (respondido) return;
    respondido = true;

    return res.status(500).json({
      success: false,
      error: 'Error al iniciar proceso Python',
      message: err.message
    });
  });
});

module.exports = router;
