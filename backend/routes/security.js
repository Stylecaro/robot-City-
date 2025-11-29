"""
Rutas API para el Sistema de Seguridad con Humanoides IA
Integración con el backend principal
"""

const express = require('express');
const router = express.Router();
const { body, param, query, validationResult } = require('express-validator');
const { authenticate, authorize, resourcePermission } = require('../utils/auth');
const logger = require('../utils/logger');
const axios = require('axios');

// Configuración del sistema de seguridad
const SECURITY_SYSTEM_URL = process.env.SECURITY_SYSTEM_URL || 'http://localhost:5001';
const SECURITY_TIMEOUT = 30000;

// Simulación de datos de seguridad (en producción vendría del sistema Python)
let securityData = {
  alert_level: 'GREEN',
  total_humanoids: 0,
  active_humanoids: 0,
  active_incidents: 0,
  security_zones: 0,
  system_metrics: {
    total_threats_detected: 0,
    total_threats_neutralized: 0,
    average_response_time: 0.0,
    coverage_percentage: 0.0,
    false_positive_rate: 0.0
  },
  humanoids: {},
  zones: {},
  recent_incidents: []
};

// Middleware de validación
const validateThreatReport = [
  body('type').isIn(['intrusion_physical', 'cyber_attack', 'hostile_entity', 'system_malfunction', 'natural_disaster'])
    .withMessage('Tipo de amenaza inválido'),
  body('location').isObject().withMessage('Ubicación requerida'),
  body('location.x').isNumeric().withMessage('Coordenada X debe ser numérica'),
  body('location.y').isNumeric().withMessage('Coordenada Y debe ser numérica'),
  body('location.z').isNumeric().withMessage('Coordenada Z debe ser numérica'),
  body('severity').isIn(['LOW', 'MEDIUM', 'HIGH', 'CRITICAL', 'IMMINENT'])
    .withMessage('Severidad inválida'),
  body('description').trim().isLength({ min: 10, max: 500 })
    .withMessage('Descripción debe tener entre 10 y 500 caracteres')
];

const validateHumanoidDeployment = [
  body('type').isIn(['guardian', 'sentinel', 'interceptor', 'scout', 'commander', 'medic', 'cyber_defender', 'heavy_guardian'])
    .withMessage('Tipo de humanoide inválido'),
  body('position').isObject().withMessage('Posición requerida'),
  body('position.x').isNumeric().withMessage('Coordenada X debe ser numérica'),
  body('position.y').isNumeric().withMessage('Coordenada Y debe ser numérica'),
  body('position.z').isNumeric().withMessage('Coordenada Z debe ser numérica'),
  body('zone_id').optional().isString().withMessage('ID de zona debe ser texto')
];

const validateSecurityZone = [
  body('name').trim().isLength({ min: 3, max: 50 }).withMessage('Nombre debe tener entre 3 y 50 caracteres'),
  body('type').isIn(['public', 'restricted', 'high_security', 'critical_infrastructure', 'residential', 'industrial'])
    .withMessage('Tipo de zona inválido'),
  body('boundaries').isArray({ min: 3 }).withMessage('Se requieren al menos 3 puntos para definir la zona'),
  body('security_level').isInt({ min: 1, max: 10 }).withMessage('Nivel de seguridad debe ser entre 1 y 10')
];

// GET /api/security - Obtener estado general del sistema de seguridad
router.get('/', authenticate, authorize(['read']), async (req, res) => {
  try {
    // Intentar obtener datos del sistema de seguridad Python
    try {
      const response = await axios.get(`${SECURITY_SYSTEM_URL}/api/status`, {
        timeout: SECURITY_TIMEOUT
      });
      securityData = response.data;
    } catch (systemError) {
      logger.warn('Sistema de seguridad no disponible, usando datos simulados');
      updateSimulatedSecurityData();
    }
    
    res.json({
      success: true,
      data: securityData,
      timestamp: new Date().toISOString()
    });
    
    logger.info('Estado del sistema de seguridad obtenido');
    
  } catch (error) {
    logger.error('Error obteniendo estado de seguridad:', error);
    res.status(500).json({
      success: false,
      error: 'Error interno del servidor',
      message: error.message
    });
  }
});

// GET /api/security/humanoids - Obtener información de humanoides
router.get('/humanoids', authenticate, authorize(['read']), (req, res) => {
  try {
    const { type, status, zone_id } = req.query;
    
    let humanoids = Object.values(securityData.humanoids || {});
    
    // Filtrar por tipo
    if (type) {
      humanoids = humanoids.filter(h => h.type === type);
    }
    
    // Filtrar por estado
    if (status) {
      humanoids = humanoids.filter(h => h.status === status);
    }
    
    // Filtrar por zona
    if (zone_id) {
      humanoids = humanoids.filter(h => h.assigned_zone === zone_id);
    }
    
    res.json({
      success: true,
      data: humanoids,
      total: humanoids.length,
      filters_applied: { type, status, zone_id },
      timestamp: new Date().toISOString()
    });
    
    logger.info(`Humanoides obtenidos: ${humanoids.length} unidades`);
    
  } catch (error) {
    logger.error('Error obteniendo humanoides:', error);
    res.status(500).json({
      success: false,
      error: 'Error interno del servidor',
      message: error.message
    });
  }
});

// GET /api/security/humanoids/:id - Obtener humanoide específico
router.get('/humanoids/:id', [
  authenticate,
  authorize(['read']),
  param('id').trim().notEmpty().withMessage('ID de humanoide requerido')
], (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array()
      });
    }
    
    const humanoid = securityData.humanoids[req.params.id];
    
    if (!humanoid) {
      return res.status(404).json({
        success: false,
        error: 'Humanoide no encontrado',
        message: `Humanoide con ID ${req.params.id} no existe`
      });
    }
    
    res.json({
      success: true,
      data: humanoid,
      timestamp: new Date().toISOString()
    });
    
    logger.info(`Humanoide obtenido: ${humanoid.id}`);
    
  } catch (error) {
    logger.error('Error obteniendo humanoide:', error);
    res.status(500).json({
      success: false,
      error: 'Error interno del servidor',
      message: error.message
    });
  }
});

// POST /api/security/humanoids - Desplegar nuevo humanoide
router.post('/humanoids', [
  authenticate,
  resourcePermission('security', 'create'),
  ...validateHumanoidDeployment
], async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array()
      });
    }
    
    const deploymentData = {
      type: req.body.type,
      position: req.body.position,
      zone_id: req.body.zone_id,
      priority: req.body.priority || 'normal',
      special_config: req.body.special_config || {}
    };
    
    try {
      // Intentar desplegar en el sistema real
      const response = await axios.post(`${SECURITY_SYSTEM_URL}/api/deploy`, deploymentData, {
        timeout: SECURITY_TIMEOUT
      });
      
      const newHumanoid = response.data;
      
      res.status(201).json({
        success: true,
        data: newHumanoid,
        message: 'Humanoide desplegado exitosamente',
        timestamp: new Date().toISOString()
      });
      
      logger.info(`Humanoide desplegado: ${newHumanoid.id} (${newHumanoid.type})`);
      
    } catch (systemError) {
      // Simular despliegue si el sistema no está disponible
      logger.warn('Sistema de seguridad no disponible, simulando despliegue');
      
      const simulatedHumanoid = createSimulatedHumanoid(deploymentData);
      securityData.humanoids[simulatedHumanoid.id] = simulatedHumanoid;
      securityData.total_humanoids++;
      securityData.active_humanoids++;
      
      res.status(201).json({
        success: true,
        data: simulatedHumanoid,
        message: 'Humanoide desplegado exitosamente (simulado)',
        simulated: true,
        timestamp: new Date().toISOString()
      });
      
      logger.info(`Humanoide simulado desplegado: ${simulatedHumanoid.id}`);
    }
    
    // Emitir evento via WebSocket
    if (req.app.locals.io) {
      req.app.locals.io.emit('humanoid_deployed', {
        humanoid: req.body,
        timestamp: new Date().toISOString()
      });
    }
    
  } catch (error) {
    logger.error('Error desplegando humanoide:', error);
    res.status(500).json({
      success: false,
      error: 'Error desplegando humanoide',
      message: error.message
    });
  }
});

// POST /api/security/humanoids/:id/command - Enviar comando a humanoide
router.post('/humanoids/:id/command', [
  authenticate,
  resourcePermission('security', 'update'),
  param('id').trim().notEmpty().withMessage('ID de humanoide requerido'),
  body('command').isIn(['patrol', 'investigate', 'respond', 'return_base', 'emergency_stop', 'recharge'])
    .withMessage('Comando inválido'),
  body('parameters').optional().isObject().withMessage('Parámetros deben ser un objeto')
], async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array()
      });
    }
    
    const { command, parameters = {} } = req.body;
    const humanoidId = req.params.id;
    
    // Verificar que el humanoide existe
    if (!securityData.humanoids[humanoidId]) {
      return res.status(404).json({
        success: false,
        error: 'Humanoide no encontrado'
      });
    }
    
    try {
      // Enviar comando al sistema real
      const response = await axios.post(
        `${SECURITY_SYSTEM_URL}/api/humanoids/${humanoidId}/command`,
        { command, parameters },
        { timeout: SECURITY_TIMEOUT }
      );
      
      const commandResult = response.data;
      
      res.json({
        success: true,
        data: commandResult,
        message: `Comando ${command} enviado exitosamente`,
        timestamp: new Date().toISOString()
      });
      
    } catch (systemError) {
      // Simular ejecución de comando
      logger.warn('Sistema de seguridad no disponible, simulando comando');
      
      const simulatedResult = simulateHumanoidCommand(humanoidId, command, parameters);
      
      res.json({
        success: true,
        data: simulatedResult,
        message: `Comando ${command} ejecutado (simulado)`,
        simulated: true,
        timestamp: new Date().toISOString()
      });
    }
    
    logger.info(`Comando ${command} enviado a humanoide ${humanoidId}`);
    
    // Emitir evento via WebSocket
    if (req.app.locals.io) {
      req.app.locals.io.emit('humanoid_command_executed', {
        humanoid_id: humanoidId,
        command,
        parameters,
        timestamp: new Date().toISOString()
      });
    }
    
  } catch (error) {
    logger.error('Error enviando comando:', error);
    res.status(500).json({
      success: false,
      error: 'Error enviando comando',
      message: error.message
    });
  }
});

// POST /api/security/threats/report - Reportar amenaza
router.post('/threats/report', [
  authenticate,
  authorize(['create']),
  ...validateThreatReport
], async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array()
      });
    }
    
    const threatData = {
      type: req.body.type,
      location: req.body.location,
      severity: req.body.severity,
      description: req.body.description,
      reporter: req.user.username,
      evidence: req.body.evidence || {},
      immediate_response: req.body.immediate_response || false
    };
    
    try {
      // Reportar al sistema de seguridad real
      const response = await axios.post(`${SECURITY_SYSTEM_URL}/api/threats/report`, threatData, {
        timeout: SECURITY_TIMEOUT
      });
      
      const threatResponse = response.data;
      
      res.status(201).json({
        success: true,
        data: threatResponse,
        message: 'Amenaza reportada y procesada',
        timestamp: new Date().toISOString()
      });
      
    } catch (systemError) {
      // Simular procesamiento de amenaza
      logger.warn('Sistema de seguridad no disponible, simulando reporte de amenaza');
      
      const simulatedResponse = simulateThreatReport(threatData);
      
      res.status(201).json({
        success: true,
        data: simulatedResponse,
        message: 'Amenaza reportada (procesamiento simulado)',
        simulated: true,
        timestamp: new Date().toISOString()
      });
    }
    
    logger.security('Amenaza reportada', {
      type: threatData.type,
      severity: threatData.severity,
      location: threatData.location,
      reporter: threatData.reporter
    });
    
    // Emitir alerta via WebSocket
    if (req.app.locals.io) {
      req.app.locals.io.emit('threat_reported', {
        threat: threatData,
        timestamp: new Date().toISOString()
      });
    }
    
  } catch (error) {
    logger.error('Error reportando amenaza:', error);
    res.status(500).json({
      success: false,
      error: 'Error reportando amenaza',
      message: error.message
    });
  }
});

// GET /api/security/zones - Obtener zonas de seguridad
router.get('/zones', authenticate, authorize(['read']), (req, res) => {
  try {
    const { type, security_level } = req.query;
    
    let zones = Object.values(securityData.zones || {});
    
    // Filtrar por tipo
    if (type) {
      zones = zones.filter(z => z.type === type);
    }
    
    // Filtrar por nivel de seguridad
    if (security_level) {
      const level = parseInt(security_level);
      zones = zones.filter(z => z.security_level >= level);
    }
    
    res.json({
      success: true,
      data: zones,
      total: zones.length,
      timestamp: new Date().toISOString()
    });
    
    logger.info(`Zonas de seguridad obtenidas: ${zones.length} zonas`);
    
  } catch (error) {
    logger.error('Error obteniendo zonas:', error);
    res.status(500).json({
      success: false,
      error: 'Error interno del servidor',
      message: error.message
    });
  }
});

// POST /api/security/zones - Crear zona de seguridad
router.post('/zones', [
  authenticate,
  resourcePermission('security', 'create'),
  ...validateSecurityZone
], async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array()
      });
    }
    
    const zoneData = {
      name: req.body.name,
      type: req.body.type,
      boundaries: req.body.boundaries,
      security_level: req.body.security_level,
      access_permissions: req.body.access_permissions || [],
      patrol_frequency: req.body.patrol_frequency || 15.0,
      special_protocols: req.body.special_protocols || []
    };
    
    try {
      // Crear zona en el sistema real
      const response = await axios.post(`${SECURITY_SYSTEM_URL}/api/zones`, zoneData, {
        timeout: SECURITY_TIMEOUT
      });
      
      const newZone = response.data;
      
      res.status(201).json({
        success: true,
        data: newZone,
        message: 'Zona de seguridad creada exitosamente',
        timestamp: new Date().toISOString()
      });
      
    } catch (systemError) {
      // Simular creación de zona
      const simulatedZone = createSimulatedZone(zoneData);
      securityData.zones[simulatedZone.zone_id] = simulatedZone;
      securityData.security_zones++;
      
      res.status(201).json({
        success: true,
        data: simulatedZone,
        message: 'Zona de seguridad creada (simulada)',
        simulated: true,
        timestamp: new Date().toISOString()
      });
    }
    
    logger.info(`Zona de seguridad creada: ${zoneData.name}`);
    
    // Emitir evento via WebSocket
    if (req.app.locals.io) {
      req.app.locals.io.emit('security_zone_created', {
        zone: zoneData,
        timestamp: new Date().toISOString()
      });
    }
    
  } catch (error) {
    logger.error('Error creando zona:', error);
    res.status(500).json({
      success: false,
      error: 'Error creando zona',
      message: error.message
    });
  }
});

// GET /api/security/incidents - Obtener incidentes de seguridad
router.get('/incidents', authenticate, authorize(['read']), (req, res) => {
  try {
    const { status, severity, limit = 50 } = req.query;
    
    let incidents = securityData.recent_incidents || [];
    
    // Filtrar por estado
    if (status) {
      incidents = incidents.filter(i => i.status === status);
    }
    
    // Filtrar por severidad
    if (severity) {
      incidents = incidents.filter(i => i.severity === severity);
    }
    
    // Limitar resultados
    incidents = incidents.slice(0, parseInt(limit));
    
    res.json({
      success: true,
      data: incidents,
      total: incidents.length,
      timestamp: new Date().toISOString()
    });
    
    logger.info(`Incidentes obtenidos: ${incidents.length} incidentes`);
    
  } catch (error) {
    logger.error('Error obteniendo incidentes:', error);
    res.status(500).json({
      success: false,
      error: 'Error interno del servidor',
      message: error.message
    });
  }
});

// POST /api/security/alert-level - Cambiar nivel de alerta
router.post('/alert-level', [
  authenticate,
  resourcePermission('security', 'update'),
  body('level').isIn(['GREEN', 'YELLOW', 'ORANGE', 'RED', 'BLACK'])
    .withMessage('Nivel de alerta inválido'),
  body('reason').trim().isLength({ min: 10 }).withMessage('Razón requerida')
], async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array()
      });
    }
    
    const { level, reason } = req.body;
    
    try {
      // Cambiar nivel en el sistema real
      const response = await axios.post(`${SECURITY_SYSTEM_URL}/api/alert-level`, {
        level,
        reason,
        changed_by: req.user.username
      }, {
        timeout: SECURITY_TIMEOUT
      });
      
      const alertResult = response.data;
      
      res.json({
        success: true,
        data: alertResult,
        message: `Nivel de alerta cambiado a ${level}`,
        timestamp: new Date().toISOString()
      });
      
    } catch (systemError) {
      // Simular cambio de nivel
      const previousLevel = securityData.alert_level;
      securityData.alert_level = level;
      
      const simulatedResult = {
        previous_level: previousLevel,
        new_level: level,
        reason: reason,
        changed_by: req.user.username,
        protocols_activated: getAlertProtocols(level)
      };
      
      res.json({
        success: true,
        data: simulatedResult,
        message: `Nivel de alerta cambiado a ${level} (simulado)`,
        simulated: true,
        timestamp: new Date().toISOString()
      });
    }
    
    logger.security('Nivel de alerta cambiado', {
      new_level: level,
      reason,
      changed_by: req.user.username
    });
    
    // Emitir alerta crítica via WebSocket
    if (req.app.locals.io) {
      req.app.locals.io.emit('alert_level_changed', {
        level,
        reason,
        changed_by: req.user.username,
        timestamp: new Date().toISOString()
      });
    }
    
  } catch (error) {
    logger.error('Error cambiando nivel de alerta:', error);
    res.status(500).json({
      success: false,
      error: 'Error cambiando nivel de alerta',
      message: error.message
    });
  }
});

// GET /api/security/metrics - Obtener métricas del sistema
router.get('/metrics', authenticate, authorize(['read']), (req, res) => {
  try {
    const metrics = {
      ...securityData.system_metrics,
      current_alert_level: securityData.alert_level,
      humanoid_distribution: calculateHumanoidDistribution(),
      zone_coverage: calculateZoneCoverage(),
      threat_statistics: calculateThreatStatistics(),
      performance_indicators: calculatePerformanceIndicators(),
      system_health: calculateSystemHealth()
    };
    
    res.json({
      success: true,
      data: metrics,
      timestamp: new Date().toISOString()
    });
    
    logger.info('Métricas de seguridad obtenidas');
    
  } catch (error) {
    logger.error('Error obteniendo métricas:', error);
    res.status(500).json({
      success: false,
      error: 'Error interno del servidor',
      message: error.message
    });
  }
});

// Funciones auxiliares
function updateSimulatedSecurityData() {
  // Simular actualizaciones en tiempo real
  securityData.system_metrics.total_threats_detected += Math.floor(Math.random() * 3);
  securityData.system_metrics.total_threats_neutralized += Math.floor(Math.random() * 2);
  securityData.system_metrics.average_response_time = Math.random() * 30 + 15; // 15-45 segundos
  securityData.system_metrics.coverage_percentage = Math.random() * 20 + 80; // 80-100%
  securityData.system_metrics.false_positive_rate = Math.random() * 0.1; // 0-10%
}

function createSimulatedHumanoid(deploymentData) {
  const humanoidId = `SIM-${Date.now()}`;
  
  return {
    id: humanoidId,
    type: deploymentData.type,
    position: deploymentData.position,
    status: 'active',
    energy: 100,
    armor: 100,
    shields: 100,
    assigned_zone: deploymentData.zone_id,
    current_protocol: 'patrol',
    deployed_at: new Date().toISOString(),
    performance_metrics: {
      threats_neutralized: 0,
      response_time_avg: 0,
      success_rate: 1.0,
      uptime_percentage: 100
    }
  };
}

function simulateHumanoidCommand(humanoidId, command, parameters) {
  const humanoid = securityData.humanoids[humanoidId];
  
  const results = {
    patrol: {
      success: true,
      action: 'patrol_started',
      estimated_duration: 30 * 60, // 30 minutos
      route_points: 8
    },
    investigate: {
      success: true,
      action: 'investigation_started',
      target_location: parameters.location || humanoid.position,
      estimated_completion: 10 * 60 // 10 minutos
    },
    respond: {
      success: true,
      action: 'emergency_response',
      threat_id: parameters.threat_id,
      eta: 2 * 60 // 2 minutos
    },
    return_base: {
      success: true,
      action: 'returning_to_base',
      base_location: { x: 0, y: 0, z: 0 },
      eta: 5 * 60 // 5 minutos
    },
    emergency_stop: {
      success: true,
      action: 'emergency_stop_activated',
      previous_action: humanoid.current_protocol,
      stopped_at: new Date().toISOString()
    },
    recharge: {
      success: true,
      action: 'recharge_initiated',
      current_energy: humanoid.energy,
      estimated_recharge_time: (100 - humanoid.energy) * 60 // 1 min por %
    }
  };
  
  return results[command] || { success: false, error: 'Comando no reconocido' };
}

function simulateThreatReport(threatData) {
  const threatId = `THR-${Date.now()}`;
  
  return {
    threat_id: threatId,
    status: 'processing',
    priority: getThreatPriority(threatData.severity),
    assigned_humanoids: [],
    estimated_response_time: getThreatResponseTime(threatData.severity),
    confidence_level: Math.random() * 0.3 + 0.7, // 70-100%
    risk_assessment: getThreatRiskAssessment(threatData.type, threatData.severity),
    recommended_actions: getThreatRecommendations(threatData.type, threatData.severity)
  };
}

function createSimulatedZone(zoneData) {
  const zoneId = `ZONE-SIM-${Date.now()}`;
  
  return {
    zone_id: zoneId,
    name: zoneData.name,
    type: zoneData.type,
    boundaries: zoneData.boundaries,
    security_level: zoneData.security_level,
    assigned_humanoids: [],
    access_permissions: zoneData.access_permissions,
    patrol_frequency: zoneData.patrol_frequency,
    active: true,
    created_at: new Date().toISOString(),
    threat_history: [],
    current_status: 'secure'
  };
}

function getAlertProtocols(level) {
  const protocols = {
    'GREEN': ['normal_operations'],
    'YELLOW': ['increased_vigilance', 'enhanced_patrols'],
    'ORANGE': ['heightened_security', 'additional_humanoids', 'restricted_access'],
    'RED': ['emergency_protocols', 'full_deployment', 'lockdown_procedures'],
    'BLACK': ['maximum_alert', 'total_lockdown', 'emergency_response', 'civilian_evacuation']
  };
  
  return protocols[level] || protocols['GREEN'];
}

function calculateHumanoidDistribution() {
  const distribution = {};
  Object.values(securityData.humanoids || {}).forEach(humanoid => {
    distribution[humanoid.type] = (distribution[humanoid.type] || 0) + 1;
  });
  return distribution;
}

function calculateZoneCoverage() {
  const zones = Object.values(securityData.zones || {});
  return zones.map(zone => ({
    zone_id: zone.zone_id,
    name: zone.name,
    assigned_humanoids: zone.assigned_humanoids?.length || 0,
    coverage_percentage: Math.min(100, (zone.assigned_humanoids?.length || 0) * 25)
  }));
}

function calculateThreatStatistics() {
  return {
    last_24h: Math.floor(Math.random() * 10),
    last_week: Math.floor(Math.random() * 50),
    by_type: {
      intrusion_physical: Math.floor(Math.random() * 15),
      cyber_attack: Math.floor(Math.random() * 8),
      hostile_entity: Math.floor(Math.random() * 5),
      system_malfunction: Math.floor(Math.random() * 12),
      natural_disaster: Math.floor(Math.random() * 3)
    }
  };
}

function calculatePerformanceIndicators() {
  return {
    response_time_trend: 'improving',
    neutralization_rate: Math.random() * 0.1 + 0.9, // 90-100%
    false_alarm_rate: Math.random() * 0.05, // 0-5%
    system_availability: Math.random() * 0.02 + 0.98, // 98-100%
    humanoid_efficiency: Math.random() * 0.15 + 0.85 // 85-100%
  };
}

function calculateSystemHealth() {
  return {
    overall_status: securityData.alert_level === 'GREEN' ? 'healthy' : 'alert',
    subsystems: {
      humanoid_network: 'operational',
      sensor_array: 'operational',
      communication: 'operational',
      ai_systems: 'operational',
      power_grid: 'optimal'
    },
    uptime_percentage: Math.random() * 2 + 98 // 98-100%
  };
}

function getThreatPriority(severity) {
  const priorities = {
    'LOW': 'low',
    'MEDIUM': 'medium',
    'HIGH': 'high',
    'CRITICAL': 'critical',
    'IMMINENT': 'emergency'
  };
  return priorities[severity] || 'medium';
}

function getThreatResponseTime(severity) {
  const times = {
    'LOW': 300, // 5 minutos
    'MEDIUM': 180, // 3 minutos
    'HIGH': 60, // 1 minuto
    'CRITICAL': 30, // 30 segundos
    'IMMINENT': 10 // 10 segundos
  };
  return times[severity] || 180;
}

function getThreatRiskAssessment(type, severity) {
  return {
    containment_difficulty: Math.random() * 0.6 + 0.2,
    potential_damage: Math.random() * 0.8 + 0.1,
    escalation_probability: Math.random() * 0.4 + 0.1,
    resource_requirements: Math.random() * 0.7 + 0.3
  };
}

function getThreatRecommendations(type, severity) {
  const recommendations = {
    'intrusion_physical': ['Deploy guardian humanoids', 'Secure perimeter', 'Verify identity'],
    'cyber_attack': ['Activate cyber defender', 'Isolate affected systems', 'Trace attack source'],
    'hostile_entity': ['Deploy interceptors', 'Evacuate civilians', 'Neutralize threat'],
    'system_malfunction': ['Dispatch maintenance team', 'Isolate failed system', 'Activate backup'],
    'natural_disaster': ['Initiate evacuation', 'Deploy rescue teams', 'Secure critical systems']
  };
  
  return recommendations[type] || ['Assess situation', 'Deploy appropriate response'];
}

module.exports = router;