/**
 * MIT License - Usar misma licencia que el repositorio
 *
 * Rutas cuánticas para quantum-core.
 *
 * Endpoint disponible:
 *   POST /api/quantum/run-circuit
 *     - Valida el cuerpo JSON (circuit_name string, params object opcional).
 *     - Ejecuta el script Python quantum-core/examples/quantum_traffic_light_demo.py
 *       mediante child_process.exec y devuelve el resultado JSON al cliente.
 *
 * Seguridad:
 *   - Los parámetros nunca se concatenan directamente en el comando shell.
 *   - Se usa una lista blanca de circuit_name permitidos.
 *   - Tiempo de espera máximo: 30 segundos.
 *
 * Para cambiar "python" por "python3":
 *   Modificar la variable PYTHON_CMD a "python3".
 */

'use strict';

const express = require('express');
const router = express.Router();
const { execFile } = require('child_process');
const path = require('path');
const rateLimit = require('express-rate-limit');

// Limite de velocidad: máximo 20 peticiones por minuto por IP.
// Esto protege el endpoint que ejecuta un proceso Python del sistema.
const quantumLimiter = rateLimit({
  windowMs: 60 * 1000, // 1 minuto
  max: 20,
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: 'Demasiadas peticiones al endpoint cuántico. Intenta de nuevo en 1 minuto.' },
});

// Comando Python a usar. Cambiar a 'python3' si es necesario.
const PYTHON_CMD = process.env.PYTHON_CMD || 'python';

// Timeout en milisegundos para la ejecución del script Python
const EXEC_TIMEOUT_MS = 30000;

// Lista blanca de circuitos permitidos
const ALLOWED_CIRCUITS = ['traffic_light'];

// Ruta absoluta al script de demo
const DEMO_SCRIPT = path.resolve(
  __dirname,
  '../../quantum-core/examples/quantum_traffic_light_demo.py'
);

/**
 * POST /api/quantum/run-circuit
 *
 * Cuerpo esperado:
 * {
 *   "circuit_name": "traffic_light",  // string requerido
 *   "params": { "qubits": 3 }         // object opcional
 * }
 *
 * Respuesta exitosa (200):
 * { "counts": {...}, "probabilities": {...}, "shots": 1024, "backend": "local_simulator", ... }
 *
 * Errores:
 * 400 - Payload inválido o circuit_name no permitido
 * 500 - Error al ejecutar el script Python
 */
router.post('/run-circuit', quantumLimiter, (req, res) => {
  const { circuit_name, params } = req.body;

  // Validar que circuit_name sea un string no vacío
  if (!circuit_name || typeof circuit_name !== 'string' || circuit_name.trim() === '') {
    return res.status(400).json({
      error: 'El campo "circuit_name" es requerido y debe ser un string no vacío.',
    });
  }

  // Validar contra lista blanca para prevenir inyección
  const sanitizedCircuit = circuit_name.trim().toLowerCase();
  if (!ALLOWED_CIRCUITS.includes(sanitizedCircuit)) {
    return res.status(400).json({
      error: `Circuito "${sanitizedCircuit}" no permitido. Circuitos disponibles: ${ALLOWED_CIRCUITS.join(', ')}.`,
    });
  }

  // Validar que params sea un objeto si se provee
  if (params !== undefined && (typeof params !== 'object' || Array.isArray(params) || params === null)) {
    return res.status(400).json({
      error: 'El campo "params" debe ser un objeto JSON.',
    });
  }

  // Extraer parámetros seguros (solo qubits y shots, validados como enteros)
  const qubits = params && Number.isInteger(params.qubits) ? params.qubits : 3;
  const shots = params && Number.isInteger(params.shots) ? params.shots : 1024;

  // Validar rangos
  if (qubits < 1 || qubits > 16) {
    return res.status(400).json({ error: 'qubits debe estar entre 1 y 16.' });
  }
  if (shots < 1 || shots > 100000) {
    return res.status(400).json({ error: 'shots debe estar entre 1 y 100000.' });
  }

  // Construir argumentos como array (sin concatenación de strings del usuario)
  // execFile evita la interpretación del shell, previniendo inyección de comandos
  const args = [DEMO_SCRIPT, '--qubits', String(qubits), '--shots', String(shots)];

  execFile(
    PYTHON_CMD,
    args,
    { timeout: EXEC_TIMEOUT_MS, maxBuffer: 1024 * 1024 },
    (error, stdout, stderr) => {
      if (error) {
        console.error('[quantum] Error ejecutando script Python:', stderr || error.message);
        return res.status(500).json({
          error: 'Error al ejecutar el circuito cuántico.',
          detail: stderr ? stderr.trim() : error.message,
        });
      }

      let resultado;
      try {
        resultado = JSON.parse(stdout);
      } catch (parseError) {
        console.error('[quantum] Error parseando JSON de stdout:', stdout);
        return res.status(500).json({
          error: 'El script Python no devolvió JSON válido.',
          detail: stdout.trim(),
        });
      }

      return res.status(200).json(resultado);
    }
  );
});

module.exports = router;
