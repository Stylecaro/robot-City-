/**
 * Rutas para gestión de robots
 */

const express = require('express');
const router = express.Router();
const { body, param, query, validationResult } = require('express-validator');
const logger = require('../utils/logger');

// Simulación de datos de robots (en producción sería BD)
let robots = [
  {
    id: 'robot-001',
    name: 'Constructor Alpha',
    type: 'construction',
    status: 'active',
    position: { x: 10, y: 0, z: 5 },
    energy: 85,
    task: 'Building structure A-1',
    capabilities: ['construction', 'heavy_lifting', 'precision_work'],
    created_at: new Date().toISOString()
  },
  {
    id: 'robot-002',
    name: 'Analyzer Beta',
    type: 'analysis',
    status: 'idle',
    position: { x: -5, y: 0, z: 10 },
    energy: 92,
    task: null,
    capabilities: ['data_analysis', 'pattern_recognition', 'monitoring'],
    created_at: new Date().toISOString()
  },
  {
    id: 'robot-003',
    name: 'Guardian Gamma',
    type: 'security',
    status: 'patrol',
    position: { x: 0, y: 0, z: -8 },
    energy: 78,
    task: 'Patrolling sector 3',
    capabilities: ['surveillance', 'threat_detection', 'emergency_response'],
    created_at: new Date().toISOString()
  }
];

// Middleware de validación
const validateRobot = [
  body('name').trim().isLength({ min: 1, max: 50 }).withMessage('Nombre requerido (1-50 caracteres)'),
  body('type').isIn(['construction', 'maintenance', 'security', 'transport', 'cleaning', 'analysis', 'communication', 'emergency'])
    .withMessage('Tipo de robot inválido'),
  body('position.x').isNumeric().withMessage('Posición X debe ser numérica'),
  body('position.y').isNumeric().withMessage('Posición Y debe ser numérica'),
  body('position.z').isNumeric().withMessage('Posición Z debe ser numérica')
];

const validateCommand = [
  body('type').isIn(['move', 'task', 'stop', 'charge']).withMessage('Tipo de comando inválido'),
  body('payload').isObject().withMessage('Payload debe ser un objeto')
];

// GET /api/robots - Obtener todos los robots
router.get('/', (req, res) => {
  try {
    const { type, status, limit = 50 } = req.query;
    
    let filteredRobots = robots;
    
    // Filtrar por tipo
    if (type) {
      filteredRobots = filteredRobots.filter(robot => robot.type === type);
    }
    
    // Filtrar por estado
    if (status) {
      filteredRobots = filteredRobots.filter(robot => robot.status === status);
    }
    
    // Limitar resultados
    filteredRobots = filteredRobots.slice(0, parseInt(limit));
    
    res.json({
      success: true,
      data: filteredRobots,
      total: filteredRobots.length,
      timestamp: new Date().toISOString()
    });
    
    logger.info(`Robots obtenidos: ${filteredRobots.length} robots`);
  } catch (error) {
    logger.error('Error obteniendo robots:', error);
    res.status(500).json({
      success: false,
      error: 'Error interno del servidor',
      message: error.message
    });
  }
});

// GET /api/robots/:id - Obtener robot específico
router.get('/:id', [
  param('id').trim().notEmpty().withMessage('ID de robot requerido')
], (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array()
      });
    }
    
    const robot = robots.find(r => r.id === req.params.id);
    
    if (!robot) {
      return res.status(404).json({
        success: false,
        error: 'Robot no encontrado',
        message: `Robot con ID ${req.params.id} no existe`
      });
    }
    
    res.json({
      success: true,
      data: robot,
      timestamp: new Date().toISOString()
    });
    
    logger.info(`Robot obtenido: ${robot.name} (${robot.id})`);
  } catch (error) {
    logger.error('Error obteniendo robot:', error);
    res.status(500).json({
      success: false,
      error: 'Error interno del servidor',
      message: error.message
    });
  }
});

// POST /api/robots - Crear nuevo robot
router.post('/', validateRobot, (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array()
      });
    }
    
    const newRobot = {
      id: `robot-${Date.now()}`,
      name: req.body.name,
      type: req.body.type,
      status: 'idle',
      position: req.body.position,
      energy: 100,
      task: null,
      capabilities: getCapabilitiesForType(req.body.type),
      created_at: new Date().toISOString(),
      ...req.body.customConfig // Configuración adicional
    };
    
    robots.push(newRobot);
    
    res.status(201).json({
      success: true,
      data: newRobot,
      message: 'Robot creado exitosamente',
      timestamp: new Date().toISOString()
    });
    
    logger.info(`Robot creado: ${newRobot.name} (${newRobot.id})`);
    
    // Emitir evento via WebSocket
    if (req.app.locals.io) {
      req.app.locals.io.emit('robot_created', newRobot);
    }
    
  } catch (error) {
    logger.error('Error creando robot:', error);
    res.status(500).json({
      success: false,
      error: 'Error interno del servidor',
      message: error.message
    });
  }
});

// PUT /api/robots/:id - Actualizar robot
router.put('/:id', [
  param('id').trim().notEmpty().withMessage('ID de robot requerido'),
  body('name').optional().trim().isLength({ min: 1, max: 50 }),
  body('position').optional().isObject(),
  body('status').optional().isIn(['active', 'idle', 'maintenance', 'charging', 'error', 'offline'])
], (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array()
      });
    }
    
    const robotIndex = robots.findIndex(r => r.id === req.params.id);
    
    if (robotIndex === -1) {
      return res.status(404).json({
        success: false,
        error: 'Robot no encontrado'
      });
    }
    
    // Actualizar campos proporcionados
    const updatedRobot = {
      ...robots[robotIndex],
      ...req.body,
      id: req.params.id, // Preservar ID
      updated_at: new Date().toISOString()
    };
    
    robots[robotIndex] = updatedRobot;
    
    res.json({
      success: true,
      data: updatedRobot,
      message: 'Robot actualizado exitosamente',
      timestamp: new Date().toISOString()
    });
    
    logger.info(`Robot actualizado: ${updatedRobot.name} (${updatedRobot.id})`);
    
    // Emitir evento via WebSocket
    if (req.app.locals.io) {
      req.app.locals.io.emit('robot_updated', updatedRobot);
    }
    
  } catch (error) {
    logger.error('Error actualizando robot:', error);
    res.status(500).json({
      success: false,
      error: 'Error interno del servidor',
      message: error.message
    });
  }
});

// POST /api/robots/:id/command - Enviar comando a robot
router.post('/:id/command', [
  param('id').trim().notEmpty().withMessage('ID de robot requerido'),
  ...validateCommand
], async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array()
      });
    }
    
    const robot = robots.find(r => r.id === req.params.id);
    
    if (!robot) {
      return res.status(404).json({
        success: false,
        error: 'Robot no encontrado'
      });
    }
    
    // Procesar comando
    const commandResult = await processRobotCommand(robot, req.body);
    
    res.json({
      success: true,
      data: commandResult,
      message: `Comando ${req.body.type} ejecutado`,
      timestamp: new Date().toISOString()
    });
    
    logger.info(`Comando enviado a robot ${robot.name}: ${req.body.type}`);
    
    // Emitir evento via WebSocket
    if (req.app.locals.io) {
      req.app.locals.io.emit('robot_command_executed', {
        robot_id: robot.id,
        command: req.body,
        result: commandResult
      });
    }
    
  } catch (error) {
    logger.error('Error ejecutando comando:', error);
    res.status(500).json({
      success: false,
      error: 'Error ejecutando comando',
      message: error.message
    });
  }
});

// DELETE /api/robots/:id - Eliminar robot
router.delete('/:id', [
  param('id').trim().notEmpty().withMessage('ID de robot requerido')
], (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array()
      });
    }
    
    const robotIndex = robots.findIndex(r => r.id === req.params.id);
    
    if (robotIndex === -1) {
      return res.status(404).json({
        success: false,
        error: 'Robot no encontrado'
      });
    }
    
    const deletedRobot = robots.splice(robotIndex, 1)[0];
    
    res.json({
      success: true,
      message: 'Robot eliminado exitosamente',
      data: { id: deletedRobot.id, name: deletedRobot.name },
      timestamp: new Date().toISOString()
    });
    
    logger.info(`Robot eliminado: ${deletedRobot.name} (${deletedRobot.id})`);
    
    // Emitir evento via WebSocket
    if (req.app.locals.io) {
      req.app.locals.io.emit('robot_deleted', { id: deletedRobot.id });
    }
    
  } catch (error) {
    logger.error('Error eliminando robot:', error);
    res.status(500).json({
      success: false,
      error: 'Error interno del servidor',
      message: error.message
    });
  }
});

// GET /api/robots/stats/summary - Estadísticas de robots
router.get('/stats/summary', (req, res) => {
  try {
    const stats = {
      total: robots.length,
      by_type: {},
      by_status: {},
      average_energy: 0,
      active_tasks: 0
    };
    
    robots.forEach(robot => {
      // Contar por tipo
      stats.by_type[robot.type] = (stats.by_type[robot.type] || 0) + 1;
      
      // Contar por estado
      stats.by_status[robot.status] = (stats.by_status[robot.status] || 0) + 1;
      
      // Sumar energía
      stats.average_energy += robot.energy;
      
      // Contar tareas activas
      if (robot.task) {
        stats.active_tasks++;
      }
    });
    
    // Calcular promedio de energía
    stats.average_energy = robots.length > 0 ? 
      Math.round(stats.average_energy / robots.length) : 0;
    
    res.json({
      success: true,
      data: stats,
      timestamp: new Date().toISOString()
    });
    
  } catch (error) {
    logger.error('Error obteniendo estadísticas:', error);
    res.status(500).json({
      success: false,
      error: 'Error interno del servidor',
      message: error.message
    });
  }
});

// Funciones auxiliares
function getCapabilitiesForType(type) {
  const capabilitiesByType = {
    construction: ['construction', 'heavy_lifting', 'precision_work'],
    maintenance: ['maintenance', 'diagnostics', 'repair'],
    security: ['surveillance', 'threat_detection', 'emergency_response'],
    transport: ['transportation', 'logistics', 'route_optimization'],
    cleaning: ['cleaning', 'waste_management', 'sanitation'],
    analysis: ['data_analysis', 'pattern_recognition', 'monitoring'],
    communication: ['communication', 'networking', 'data_relay'],
    emergency: ['emergency_response', 'rescue_operations', 'medical_assistance']
  };
  
  return capabilitiesByType[type] || ['basic_operations'];
}

async function processRobotCommand(robot, command) {
  // Simular procesamiento de comando
  const { type, payload } = command;
  
  switch (type) {
    case 'move':
      robot.position = payload.target || robot.position;
      robot.status = 'active';
      return {
        success: true,
        action: 'movement',
        new_position: robot.position,
        estimated_duration: 5000 // 5 segundos
      };
      
    case 'task':
      robot.task = payload.task_description || 'Nueva tarea asignada';
      robot.status = 'active';
      return {
        success: true,
        action: 'task_assignment',
        task: robot.task,
        estimated_completion: new Date(Date.now() + 60000).toISOString()
      };
      
    case 'stop':
      robot.task = null;
      robot.status = 'idle';
      return {
        success: true,
        action: 'stop',
        message: 'Robot detenido exitosamente'
      };
      
    case 'charge':
      robot.status = 'charging';
      return {
        success: true,
        action: 'charging',
        message: 'Iniciando proceso de carga',
        estimated_completion: new Date(Date.now() + 30000).toISOString()
      };
      
    default:
      throw new Error(`Comando no soportado: ${type}`);
  }
}

module.exports = router;