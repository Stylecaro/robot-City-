/**
 * Rutas PQC (Post-Quantum Cryptography) — Ciudad Robot
 * =====================================================
 * Endpoints REST para gestión de criptografía post-cuántica:
 *  - Generación de key bundles (ML-KEM + ML-DSA + SLH-DSA)
 *  - Firma y verificación de transacciones
 *  - Establecimiento de canales seguros
 *  - Estado de seguridad del sistema PQC
 */

'use strict';

const express = require('express');
const { spawn } = require('child_process');
const path = require('path');
const rateLimit = require('express-rate-limit');

const router = express.Router();

const PYTHON_CMD = process.env.PYTHON_CMD || 'python';
const PYTHON_TIMEOUT_MS = 15000;

const pqcRateLimiter = rateLimit({
  windowMs: 60 * 1000,
  max: 30,
  standardHeaders: true,
  legacyHeaders: false,
  message: {
    success: false,
    error: 'Demasiadas solicitudes PQC',
  },
});

router.use(pqcRateLimiter);

/**
 * Ejecuta un comando PQC en Python y devuelve el resultado JSON.
 */
function runPQCCommand(command, params) {
  return new Promise((resolve, reject) => {
    const scriptPath = path.join(__dirname, '../../quantum-blockchain/pqc_bridge.py');
    const child = spawn(PYTHON_CMD, [scriptPath], {
      timeout: PYTHON_TIMEOUT_MS,
      env: { ...process.env, PYTHONIOENCODING: 'utf-8' },
    });

    const input = JSON.stringify({ command, ...params });
    let stdout = '';
    let stderr = '';

    child.stdout.on('data', (data) => { stdout += data.toString(); });
    child.stderr.on('data', (data) => { stderr += data.toString(); });

    child.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(stderr || `PQC script exit code ${code}`));
        return;
      }
      try {
        resolve(JSON.parse(stdout));
      } catch {
        reject(new Error('Invalid JSON from PQC script'));
      }
    });

    child.on('error', (err) => reject(err));
    child.stdin.write(input);
    child.stdin.end();
  });
}

/**
 * GET /api/pqc/status
 * Estado del sistema de seguridad PQC.
 */
router.get('/status', async (req, res) => {
  try {
    const result = await runPQCCommand('status', {});
    res.json({ success: true, ...result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

/**
 * POST /api/pqc/keygen
 * Genera un key bundle PQC para una entidad.
 * Body: { "entity_id": "robot-001" }
 */
router.post('/keygen', async (req, res) => {
  const { entity_id } = req.body;
  if (!entity_id || typeof entity_id !== 'string') {
    return res.status(400).json({ success: false, error: 'entity_id requerido' });
  }
  try {
    const result = await runPQCCommand('keygen', { entity_id });
    res.json({ success: true, ...result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

/**
 * POST /api/pqc/sign
 * Firma datos con ML-DSA.
 * Body: { "signer_id": "robot-001", "data": "transaction payload" }
 */
router.post('/sign', async (req, res) => {
  const { signer_id, data } = req.body;
  if (!signer_id || !data) {
    return res.status(400).json({ success: false, error: 'signer_id y data requeridos' });
  }
  try {
    const result = await runPQCCommand('sign', { signer_id, data });
    res.json({ success: true, ...result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

/**
 * POST /api/pqc/verify
 * Verifica una firma PQC.
 * Body: { "signer_id": "robot-001", "data": "...", "signature": {...} }
 */
router.post('/verify', async (req, res) => {
  const { signer_id, data, signature } = req.body;
  if (!signer_id || !data || !signature) {
    return res.status(400).json({ success: false, error: 'signer_id, data y signature requeridos' });
  }
  try {
    const result = await runPQCCommand('verify', { signer_id, data, signature });
    res.json({ success: true, ...result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

/**
 * POST /api/pqc/secure-channel
 * Establece canal seguro post-cuántico entre dos entidades.
 * Body: { "initiator_id": "robot-001", "responder_id": "robot-002" }
 */
router.post('/secure-channel', async (req, res) => {
  const { initiator_id, responder_id } = req.body;
  if (!initiator_id || !responder_id) {
    return res.status(400).json({ success: false, error: 'initiator_id y responder_id requeridos' });
  }
  try {
    const result = await runPQCCommand('secure_channel', { initiator_id, responder_id });
    res.json({ success: true, ...result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

/**
 * GET /api/pqc/audit-log
 * Devuelve el audit log PQC.
 */
router.get('/audit-log', async (req, res) => {
  try {
    const result = await runPQCCommand('audit_log', {});
    res.json({ success: true, ...result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

module.exports = router;
