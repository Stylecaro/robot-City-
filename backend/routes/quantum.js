// MIT License - Copyright (c) 2026 Ciudad Robot Team
/**
 * Ruta Express para el módulo quantum-core
 * ==========================================
 * Expone el endpoint POST /api/quantum/run-circuit que ejecuta el script
 * Python quantum_traffic_light_demo.py mediante child_process.spawn,
 * envía los parámetros por stdin en JSON y devuelve el resultado parseado.
 *
 * Uso:
 *   Montar en server.js:
 *     const quantumRouter = require('./routes/quantum');
 *     app.use('/api/quantum', quantumRouter);
 *
 *   Probar con curl:
 *     curl -X POST http://localhost:8000/api/quantum/run-circuit \
 *       -H 'Content-Type: application/json' \
 *       -d '{"circuit_name":"traffic_light","theta":0.8}'
 */

'use strict';

const express = require('express');
const { spawn } = require('child_process');
const path = require('path');

const router = express.Router();

/** Tiempo máximo de espera para el script Python (milisegundos) */
const PYTHON_TIMEOUT_MS = 30000;

/** Ruta al script de demostración, relativa a la raíz del repositorio */
const DEMO_SCRIPT_PATH = path.join(
  __dirname,
  '../../quantum-core/examples/quantum_traffic_light_demo.py'
);

/**
 * POST /api/quantum/run-circuit
 *
 * Ejecuta el circuito cuántico de semáforo con los parámetros recibidos.
 *
 * Body (JSON):
 *   {
 *     "circuit_name": "traffic_light",  // nombre del circuito (opcional)
 *     "theta": 0.8,                     // ángulo de rotación RY (opcional)
 *     "phi": 0.2,                       // ángulo de fase RZ (opcional)
 *     "n_qubits": 3,                    // número de qubits (opcional)
 *     "shots": 1024                     // disparos del simulador (opcional)
 *   }
 *
 * Respuesta exitosa (200):
 *   {
 *     "success": true,
 *     "data": { ... }  // resultado JSON del script Python
 *   }
 *
 * Errores:
 *   400 - Body inválido o script devuelve JSON malformado
 *   504 - Timeout superado (> 30s)
 *   500 - Error interno del script Python
 */
router.post('/run-circuit', (req, res) => {
  const params = req.body || {};

  // Construir argumentos para el script Python
  const pythonArgs = [DEMO_SCRIPT_PATH];

  if (params.shots !== undefined) {
    pythonArgs.push('--shots', String(Number(params.shots)));
  }

  // Preparar el payload de stdin (parámetros del circuito sin "shots")
  const circuitParams = {};
  const circuitParamKeys = ['circuit_name', 'theta', 'phi', 'n_qubits'];
  for (const key of circuitParamKeys) {
    if (params[key] !== undefined) {
      circuitParams[key] = params[key];
    }
  }

  let stdinPayload;
  try {
    stdinPayload = JSON.stringify(circuitParams);
  } catch (err) {
    return res.status(400).json({
      success: false,
      error: 'Parámetros inválidos',
      message: err.message,
    });
  }

  // Lanzar proceso Python
  let pythonProcess;
  try {
    pythonProcess = spawn('python', pythonArgs, {
      stdio: ['pipe', 'pipe', 'pipe'],
    });
  } catch (spawnErr) {
    return res.status(500).json({
      success: false,
      error: 'No se pudo iniciar el intérprete Python',
      message: spawnErr.message,
    });
  }

  let stdout = '';
  let stderr = '';
  let timedOut = false;

  // Configurar timeout
  const timer = setTimeout(() => {
    timedOut = true;
    pythonProcess.kill('SIGTERM');
  }, PYTHON_TIMEOUT_MS);

  // Capturar stdout y stderr
  pythonProcess.stdout.on('data', (chunk) => {
    stdout += chunk.toString();
  });

  pythonProcess.stderr.on('data', (chunk) => {
    stderr += chunk.toString();
  });

  // Enviar parámetros por stdin y cerrar
  pythonProcess.stdin.write(stdinPayload);
  pythonProcess.stdin.end();

  // Manejar finalización del proceso
  pythonProcess.on('close', (code) => {
    clearTimeout(timer);

    if (timedOut) {
      return res.status(504).json({
        success: false,
        error: 'Timeout',
        message: `El script Python no respondió en ${PYTHON_TIMEOUT_MS / 1000}s`,
      });
    }

    if (code !== 0) {
      return res.status(500).json({
        success: false,
        error: 'Error en el script Python',
        message: stderr.trim() || `El proceso terminó con código ${code}`,
        exit_code: code,
      });
    }

    // Parsear la salida JSON del script
    try {
      const data = JSON.parse(stdout.trim());
      return res.status(200).json({
        success: true,
        data,
      });
    } catch (parseErr) {
      return res.status(400).json({
        success: false,
        error: 'Respuesta JSON inválida del script Python',
        message: parseErr.message,
        raw_output: stdout.slice(0, 500),
      });
    }
  });

  // Manejar errores del proceso
  pythonProcess.on('error', (err) => {
    clearTimeout(timer);
    if (!res.headersSent) {
      res.status(500).json({
        success: false,
        error: 'Error al ejecutar el script Python',
        message: err.message,
      });
    }
  });
});

module.exports = router;
