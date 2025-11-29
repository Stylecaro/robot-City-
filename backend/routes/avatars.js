/**
 * Rutas para gestión de avatares
 */

const express = require('express');
const router = express.Router();
const { body, param, query, validationResult } = require('express-validator');
const logger = require('../utils/logger');

// Simulación de datos de avatares (en producción sería BD)
let avatars = [
  {
    id: 'avatar-001',
    user_id: 'user-001',
    name: 'Alex',
    type: 'professional',
    appearance: {
      model: 'humanoid_v2',
      skin_color: '#FDB5A6',
      hair_color: '#8B4513',
      eye_color: '#4682B4',
      height: 1.75,
      clothing: 'business_suit'
    },
    personality: {
      traits: {
        openness: 0.7,
        conscientiousness: 0.8,
        extraversion: 0.6,
        agreeableness: 0.7,
        neuroticism: 0.3
      },
      communication_style: 'formal',
      interaction_preferences: ['problem_solving', 'leadership', 'collaboration']
    },
    skills: ['project_management', 'data_analysis', 'strategic_planning'],
    position: { x: 0, y: 0, z: 0 },
    status: 'active',
    energy: 95,
    mood: 'confident',
    created_at: new Date().toISOString()
  },
  {
    id: 'avatar-002',
    user_id: 'user-002',
    name: 'Sam',
    type: 'creative',
    appearance: {
      model: 'humanoid_v1',
      skin_color: '#D2B48C',
      hair_color: '#FF6347',
      eye_color: '#32CD32',
      height: 1.68,
      clothing: 'casual_creative'
    },
    personality: {
      traits: {
        openness: 0.9,
        conscientiousness: 0.5,
        extraversion: 0.8,
        agreeableness: 0.6,
        neuroticism: 0.4
      },
      communication_style: 'informal',
      interaction_preferences: ['creativity', 'brainstorming', 'artistic_expression']
    },
    skills: ['digital_art', 'music_composition', '3d_modeling'],
    position: { x: 5, y: 0, z: 3 },
    status: 'creating',
    energy: 88,
    mood: 'inspired',
    created_at: new Date().toISOString()
  }
];

// Middleware de validación
const validateAvatar = [
  body('name').trim().isLength({ min: 1, max: 30 }).withMessage('Nombre requerido (1-30 caracteres)'),
  body('type').isIn(['professional', 'creative', 'social', 'explorer', 'guardian'])
    .withMessage('Tipo de avatar inválido'),
  body('appearance').isObject().withMessage('Configuración de apariencia requerida'),
  body('appearance.model').isIn(['humanoid_v1', 'humanoid_v2', 'android_v1', 'custom'])
    .withMessage('Modelo de apariencia inválido')
];

const validatePersonality = [
  body('personality.traits.openness').isFloat({ min: 0, max: 1 })
    .withMessage('Apertura debe ser entre 0 y 1'),
  body('personality.traits.conscientiousness').isFloat({ min: 0, max: 1 })
    .withMessage('Responsabilidad debe ser entre 0 y 1'),
  body('personality.traits.extraversion').isFloat({ min: 0, max: 1 })
    .withMessage('Extraversión debe ser entre 0 y 1'),
  body('personality.traits.agreeableness').isFloat({ min: 0, max: 1 })
    .withMessage('Amabilidad debe ser entre 0 y 1'),
  body('personality.traits.neuroticism').isFloat({ min: 0, max: 1 })
    .withMessage('Neuroticismo debe ser entre 0 y 1')
];

const validateAction = [
  body('type').isIn(['move', 'interact', 'emote', 'speak', 'task'])
    .withMessage('Tipo de acción inválido'),
  body('data').isObject().withMessage('Datos de acción requeridos')
];

// GET /api/avatars - Obtener todos los avatares
router.get('/', (req, res) => {
  try {
    const { user_id, type, status, limit = 50 } = req.query;
    
    let filteredAvatars = avatars;
    
    // Filtrar por usuario
    if (user_id) {
      filteredAvatars = filteredAvatars.filter(avatar => avatar.user_id === user_id);
    }
    
    // Filtrar por tipo
    if (type) {
      filteredAvatars = filteredAvatars.filter(avatar => avatar.type === type);
    }
    
    // Filtrar por estado
    if (status) {
      filteredAvatars = filteredAvatars.filter(avatar => avatar.status === status);
    }
    
    // Limitar resultados
    filteredAvatars = filteredAvatars.slice(0, parseInt(limit));
    
    res.json({
      success: true,
      data: filteredAvatars,
      total: filteredAvatars.length,
      timestamp: new Date().toISOString()
    });
    
    logger.info(`Avatares obtenidos: ${filteredAvatars.length} avatares`);
  } catch (error) {
    logger.error('Error obteniendo avatares:', error);
    res.status(500).json({
      success: false,
      error: 'Error interno del servidor',
      message: error.message
    });
  }
});

// GET /api/avatars/:id - Obtener avatar específico
router.get('/:id', [
  param('id').trim().notEmpty().withMessage('ID de avatar requerido')
], (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array()
      });
    }
    
    const avatar = avatars.find(a => a.id === req.params.id);
    
    if (!avatar) {
      return res.status(404).json({
        success: false,
        error: 'Avatar no encontrado',
        message: `Avatar con ID ${req.params.id} no existe`
      });
    }
    
    res.json({
      success: true,
      data: avatar,
      timestamp: new Date().toISOString()
    });
    
    logger.info(`Avatar obtenido: ${avatar.name} (${avatar.id})`);
  } catch (error) {
    logger.error('Error obteniendo avatar:', error);
    res.status(500).json({
      success: false,
      error: 'Error interno del servidor',
      message: error.message
    });
  }
});

// POST /api/avatars - Crear nuevo avatar
router.post('/', [...validateAvatar, ...validatePersonality], (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array()
      });
    }
    
    const newAvatar = {
      id: `avatar-${Date.now()}`,
      user_id: req.body.user_id || `user-${Date.now()}`,
      name: req.body.name,
      type: req.body.type,
      appearance: {
        model: req.body.appearance.model,
        skin_color: req.body.appearance.skin_color || '#FDB5A6',
        hair_color: req.body.appearance.hair_color || '#8B4513',
        eye_color: req.body.appearance.eye_color || '#4682B4',
        height: req.body.appearance.height || 1.70,
        clothing: req.body.appearance.clothing || 'casual'
      },
      personality: req.body.personality,
      skills: getSkillsForType(req.body.type),
      position: req.body.position || { x: 0, y: 0, z: 0 },
      status: 'active',
      energy: 100,
      mood: 'neutral',
      created_at: new Date().toISOString(),
      learning_data: {
        interactions: 0,
        preferences: {},
        adaptations: []
      }
    };
    
    avatars.push(newAvatar);
    
    res.status(201).json({
      success: true,
      data: newAvatar,
      message: 'Avatar creado exitosamente',
      timestamp: new Date().toISOString()
    });
    
    logger.info(`Avatar creado: ${newAvatar.name} (${newAvatar.id})`);
    
    // Emitir evento via WebSocket
    if (req.app.locals.io) {
      req.app.locals.io.emit('avatar_created', newAvatar);
    }
    
  } catch (error) {
    logger.error('Error creando avatar:', error);
    res.status(500).json({
      success: false,
      error: 'Error interno del servidor',
      message: error.message
    });
  }
});

// PUT /api/avatars/:id - Actualizar avatar
router.put('/:id', [
  param('id').trim().notEmpty().withMessage('ID de avatar requerido'),
  body('name').optional().trim().isLength({ min: 1, max: 30 }),
  body('appearance').optional().isObject(),
  body('personality').optional().isObject(),
  body('position').optional().isObject()
], (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array()
      });
    }
    
    const avatarIndex = avatars.findIndex(a => a.id === req.params.id);
    
    if (avatarIndex === -1) {
      return res.status(404).json({
        success: false,
        error: 'Avatar no encontrado'
      });
    }
    
    // Actualizar campos proporcionados (merge profundo para objetos anidados)
    const updatedAvatar = {
      ...avatars[avatarIndex],
      ...req.body,
      id: req.params.id, // Preservar ID
      appearance: { ...avatars[avatarIndex].appearance, ...req.body.appearance },
      personality: { 
        ...avatars[avatarIndex].personality, 
        ...req.body.personality,
        traits: { ...avatars[avatarIndex].personality.traits, ...req.body.personality?.traits }
      },
      updated_at: new Date().toISOString()
    };
    
    avatars[avatarIndex] = updatedAvatar;
    
    res.json({
      success: true,
      data: updatedAvatar,
      message: 'Avatar actualizado exitosamente',
      timestamp: new Date().toISOString()
    });
    
    logger.info(`Avatar actualizado: ${updatedAvatar.name} (${updatedAvatar.id})`);
    
    // Emitir evento via WebSocket
    if (req.app.locals.io) {
      req.app.locals.io.emit('avatar_updated', updatedAvatar);
    }
    
  } catch (error) {
    logger.error('Error actualizando avatar:', error);
    res.status(500).json({
      success: false,
      error: 'Error interno del servidor',
      message: error.message
    });
  }
});

// POST /api/avatars/:id/action - Ejecutar acción de avatar
router.post('/:id/action', [
  param('id').trim().notEmpty().withMessage('ID de avatar requerido'),
  ...validateAction
], async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array()
      });
    }
    
    const avatar = avatars.find(a => a.id === req.params.id);
    
    if (!avatar) {
      return res.status(404).json({
        success: false,
        error: 'Avatar no encontrado'
      });
    }
    
    // Procesar acción
    const actionResult = await processAvatarAction(avatar, req.body);
    
    res.json({
      success: true,
      data: actionResult,
      message: `Acción ${req.body.type} ejecutada`,
      timestamp: new Date().toISOString()
    });
    
    logger.info(`Acción ejecutada por avatar ${avatar.name}: ${req.body.type}`);
    
    // Emitir evento via WebSocket
    if (req.app.locals.io) {
      req.app.locals.io.emit('avatar_action_executed', {
        avatar_id: avatar.id,
        action: req.body,
        result: actionResult
      });
    }
    
  } catch (error) {
    logger.error('Error ejecutando acción:', error);
    res.status(500).json({
      success: false,
      error: 'Error ejecutando acción',
      message: error.message
    });
  }
});

// POST /api/avatars/:id/interact - Interactuar con avatar
router.post('/:id/interact', [
  param('id').trim().notEmpty().withMessage('ID de avatar requerido'),
  body('type').isIn(['conversation', 'question', 'command', 'social'])
    .withMessage('Tipo de interacción inválido'),
  body('content').trim().notEmpty().withMessage('Contenido de interacción requerido')
], async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array()
      });
    }
    
    const avatar = avatars.find(a => a.id === req.params.id);
    
    if (!avatar) {
      return res.status(404).json({
        success: false,
        error: 'Avatar no encontrado'
      });
    }
    
    // Generar respuesta basada en personalidad
    const response = await generateAvatarResponse(avatar, req.body);
    
    // Actualizar datos de aprendizaje
    avatar.learning_data.interactions += 1;
    avatar.updated_at = new Date().toISOString();
    
    res.json({
      success: true,
      data: {
        response: response,
        avatar_state: {
          mood: avatar.mood,
          energy: avatar.energy,
          interactions: avatar.learning_data.interactions
        }
      },
      timestamp: new Date().toISOString()
    });
    
    logger.info(`Interacción con avatar ${avatar.name}: ${req.body.type}`);
    
    // Emitir evento via WebSocket
    if (req.app.locals.io) {
      req.app.locals.io.emit('avatar_interaction', {
        avatar_id: avatar.id,
        interaction: req.body,
        response: response
      });
    }
    
  } catch (error) {
    logger.error('Error en interacción:', error);
    res.status(500).json({
      success: false,
      error: 'Error en interacción',
      message: error.message
    });
  }
});

// DELETE /api/avatars/:id - Eliminar avatar
router.delete('/:id', [
  param('id').trim().notEmpty().withMessage('ID de avatar requerido')
], (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array()
      });
    }
    
    const avatarIndex = avatars.findIndex(a => a.id === req.params.id);
    
    if (avatarIndex === -1) {
      return res.status(404).json({
        success: false,
        error: 'Avatar no encontrado'
      });
    }
    
    const deletedAvatar = avatars.splice(avatarIndex, 1)[0];
    
    res.json({
      success: true,
      message: 'Avatar eliminado exitosamente',
      data: { id: deletedAvatar.id, name: deletedAvatar.name },
      timestamp: new Date().toISOString()
    });
    
    logger.info(`Avatar eliminado: ${deletedAvatar.name} (${deletedAvatar.id})`);
    
    // Emitir evento via WebSocket
    if (req.app.locals.io) {
      req.app.locals.io.emit('avatar_deleted', { id: deletedAvatar.id });
    }
    
  } catch (error) {
    logger.error('Error eliminando avatar:', error);
    res.status(500).json({
      success: false,
      error: 'Error interno del servidor',
      message: error.message
    });
  }
});

// GET /api/avatars/stats/summary - Estadísticas de avatares
router.get('/stats/summary', (req, res) => {
  try {
    const stats = {
      total: avatars.length,
      by_type: {},
      by_status: {},
      average_energy: 0,
      total_interactions: 0,
      mood_distribution: {}
    };
    
    avatars.forEach(avatar => {
      // Contar por tipo
      stats.by_type[avatar.type] = (stats.by_type[avatar.type] || 0) + 1;
      
      // Contar por estado
      stats.by_status[avatar.status] = (stats.by_status[avatar.status] || 0) + 1;
      
      // Sumar energía
      stats.average_energy += avatar.energy;
      
      // Sumar interacciones
      stats.total_interactions += avatar.learning_data?.interactions || 0;
      
      // Contar distribución de ánimos
      stats.mood_distribution[avatar.mood] = (stats.mood_distribution[avatar.mood] || 0) + 1;
    });
    
    // Calcular promedio de energía
    stats.average_energy = avatars.length > 0 ? 
      Math.round(stats.average_energy / avatars.length) : 0;
    
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
function getSkillsForType(type) {
  const skillsByType = {
    professional: ['project_management', 'data_analysis', 'strategic_planning', 'leadership'],
    creative: ['digital_art', 'music_composition', '3d_modeling', 'creative_writing'],
    social: ['communication', 'community_building', 'conflict_resolution', 'networking'],
    explorer: ['research', 'discovery', 'adventure_planning', 'navigation'],
    guardian: ['protection', 'security_analysis', 'emergency_response', 'monitoring']
  };
  
  return skillsByType[type] || ['basic_interaction'];
}

async function processAvatarAction(avatar, action) {
  const { type, data } = action;
  
  switch (type) {
    case 'move':
      avatar.position = data.target || avatar.position;
      avatar.energy = Math.max(0, avatar.energy - 2);
      return {
        success: true,
        action: 'movement',
        new_position: avatar.position,
        energy_consumed: 2
      };
      
    case 'interact':
      avatar.energy = Math.max(0, avatar.energy - 1);
      return {
        success: true,
        action: 'interaction',
        target: data.target,
        interaction_type: data.interaction_type || 'friendly'
      };
      
    case 'emote':
      avatar.mood = data.emotion || avatar.mood;
      return {
        success: true,
        action: 'emotion',
        emotion: data.emotion,
        intensity: data.intensity || 0.5
      };
      
    case 'speak':
      avatar.energy = Math.max(0, avatar.energy - 1);
      return {
        success: true,
        action: 'speech',
        message: data.message,
        tone: data.tone || 'neutral'
      };
      
    case 'task':
      avatar.status = 'busy';
      avatar.energy = Math.max(0, avatar.energy - 5);
      return {
        success: true,
        action: 'task_execution',
        task: data.task_description,
        estimated_duration: data.duration || 30000
      };
      
    default:
      throw new Error(`Acción no soportada: ${type}`);
  }
}

async function generateAvatarResponse(avatar, interaction) {
  const { type, content } = interaction;
  const personality = avatar.personality;
  
  // Generar respuesta basada en personalidad y tipo de interacción
  let responseTemplate = '';
  
  if (personality.traits.extraversion > 0.7) {
    responseTemplate = personality.communication_style === 'formal' ? 
      'Excelente pregunta. ' : '¡Qué interesante! ';
  } else {
    responseTemplate = personality.communication_style === 'formal' ? 
      'Entiendo. ' : 'Hmm, ';
  }
  
  switch (type) {
    case 'conversation':
      if (personality.traits.openness > 0.6) {
        return responseTemplate + `Me gusta explorar nuevas ideas. Sobre "${content}", creo que podríamos considerar diferentes perspectivas.`;
      } else {
        return responseTemplate + `Respecto a "${content}", prefiero mantener un enfoque práctico y probado.`;
      }
      
    case 'question':
      if (personality.traits.conscientiousness > 0.7) {
        return responseTemplate + `Permíteme analizar tu pregunta sobre "${content}" de manera detallada...`;
      } else {
        return responseTemplate + `Sobre "${content}", mi primera impresión es...`;
      }
      
    case 'command':
      if (personality.traits.agreeableness > 0.6) {
        return responseTemplate + `Por supuesto, estaré encantado de ayudar con "${content}".`;
      } else {
        return responseTemplate + `Evaluaré si puedo asistir con "${content}".`;
      }
      
    case 'social':
      if (personality.traits.extraversion > 0.5) {
        return responseTemplate + `¡Me alegra que quieras compartir sobre "${content}"! Cuéntame más.`;
      } else {
        return responseTemplate + `Aprecio que compartas "${content}" conmigo.`;
      }
      
    default:
      return responseTemplate + `Interesante punto sobre "${content}".`;
  }
}

module.exports = router;