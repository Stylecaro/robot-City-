/**
 * Servicio de logging para el backend
 */

const winston = require('winston');
const path = require('path');

// Configuración de niveles de log personalizados
const customLevels = {
  levels: {
    error: 0,
    warn: 1,
    info: 2,
    http: 3,
    debug: 4
  },
  colors: {
    error: 'red',
    warn: 'yellow',
    info: 'green',
    http: 'magenta',
    debug: 'blue'
  }
};

// Agregar colores personalizados
winston.addColors(customLevels.colors);

// Formato personalizado para logs
const logFormat = winston.format.combine(
  winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
  winston.format.errors({ stack: true }),
  winston.format.colorize({ all: true }),
  winston.format.printf(({ timestamp, level, message, stack }) => {
    let logMessage = `${timestamp} [${level}]: ${message}`;
    if (stack) {
      logMessage += `\n${stack}`;
    }
    return logMessage;
  })
);

// Formato para archivos (sin colores)
const fileFormat = winston.format.combine(
  winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
  winston.format.errors({ stack: true }),
  winston.format.json()
);

// Crear directorio de logs si no existe
const logsDir = path.join(__dirname, '..', 'logs');
require('fs').mkdirSync(logsDir, { recursive: true });

// Configuración del logger
const logger = winston.createLogger({
  levels: customLevels.levels,
  level: process.env.LOG_LEVEL || 'info',
  transports: [
    // Console transport
    new winston.transports.Console({
      format: logFormat,
      handleExceptions: true,
      handleRejections: true
    }),
    
    // Archivo para todos los logs
    new winston.transports.File({
      filename: path.join(logsDir, 'app.log'),
      format: fileFormat,
      maxsize: 5242880, // 5MB
      maxFiles: 5,
      handleExceptions: true,
      handleRejections: true
    }),
    
    // Archivo solo para errores
    new winston.transports.File({
      filename: path.join(logsDir, 'error.log'),
      level: 'error',
      format: fileFormat,
      maxsize: 5242880, // 5MB
      maxFiles: 5,
      handleExceptions: true,
      handleRejections: true
    }),
    
    // Archivo para logs HTTP
    new winston.transports.File({
      filename: path.join(logsDir, 'access.log'),
      level: 'http',
      format: fileFormat,
      maxsize: 5242880, // 5MB
      maxFiles: 10
    })
  ],
  
  // Configuración de excepciones
  exceptionHandlers: [
    new winston.transports.File({
      filename: path.join(logsDir, 'exceptions.log'),
      format: fileFormat
    })
  ],
  
  // Configuración de promesas rechazadas
  rejectionHandlers: [
    new winston.transports.File({
      filename: path.join(logsDir, 'rejections.log'),
      format: fileFormat
    })
  ],
  
  exitOnError: false
});

// Funciones helper para logging específico
logger.httpLog = (req, res, responseTime) => {
  const logData = {
    method: req.method,
    url: req.url,
    statusCode: res.statusCode,
    responseTime: `${responseTime}ms`,
    userAgent: req.get('User-Agent') || 'Unknown',
    ip: req.ip || req.connection.remoteAddress,
    timestamp: new Date().toISOString()
  };
  
  logger.http('HTTP Request', logData);
};

logger.robotActivity = (robotId, action, details = {}) => {
  logger.info(`Robot Activity - ${robotId}: ${action}`, {
    robotId,
    action,
    details,
    category: 'robot_activity'
  });
};

logger.avatarActivity = (avatarId, action, details = {}) => {
  logger.info(`Avatar Activity - ${avatarId}: ${action}`, {
    avatarId,
    action,
    details,
    category: 'avatar_activity'
  });
};

logger.aiActivity = (taskType, details = {}) => {
  logger.info(`AI Activity - ${taskType}`, {
    taskType,
    details,
    category: 'ai_activity'
  });
};

logger.cityEvent = (eventType, details = {}) => {
  logger.info(`City Event - ${eventType}`, {
    eventType,
    details,
    category: 'city_event'
  });
};

logger.security = (event, details = {}) => {
  logger.warn(`Security Event - ${event}`, {
    event,
    details,
    category: 'security'
  });
};

logger.performance = (metric, value, details = {}) => {
  logger.info(`Performance Metric - ${metric}: ${value}`, {
    metric,
    value,
    details,
    category: 'performance'
  });
};

logger.systemHealth = (component, status, details = {}) => {
  const level = status === 'healthy' ? 'info' : 'warn';
  logger[level](`System Health - ${component}: ${status}`, {
    component,
    status,
    details,
    category: 'system_health'
  });
};

// Middleware para capturar y loggear errores no manejados
logger.errorHandler = (error, context = {}) => {
  logger.error('Unhandled Error', {
    error: {
      message: error.message,
      stack: error.stack,
      name: error.name
    },
    context,
    timestamp: new Date().toISOString()
  });
};

// Función para logging de eventos de WebSocket
logger.websocketEvent = (event, socketId, data = {}) => {
  logger.debug(`WebSocket Event - ${event}`, {
    event,
    socketId,
    data,
    category: 'websocket'
  });
};

// Función para logging de base de datos
logger.databaseQuery = (query, duration, success = true) => {
  const level = success ? 'debug' : 'warn';
  logger[level](`Database Query - ${success ? 'SUCCESS' : 'FAILED'}`, {
    query: query.substring(0, 100) + (query.length > 100 ? '...' : ''),
    duration: `${duration}ms`,
    success,
    category: 'database'
  });
};

// Función para logging de métricas de ciudad
logger.cityMetrics = (metrics) => {
  logger.info('City Metrics Update', {
    metrics,
    category: 'city_metrics',
    timestamp: new Date().toISOString()
  });
};

// Función para logging de autenticación
logger.auth = (action, userId, details = {}) => {
  logger.info(`Authentication - ${action}`, {
    action,
    userId,
    details,
    category: 'authentication',
    timestamp: new Date().toISOString()
  });
};

// Configuración de nivel de log en desarrollo
if (process.env.NODE_ENV === 'development') {
  logger.level = 'debug';
  logger.debug('Logger configurado para desarrollo');
}

// Configuración de nivel de log en producción
if (process.env.NODE_ENV === 'production') {
  logger.level = 'info';
  
  // En producción, agregar transport para servicios externos (opcional)
  // logger.add(new winston.transports.Http({
  //   host: 'log-server',
  //   port: 80,
  //   path: '/logs'
  // }));
}

// Función para obtener estadísticas de logs
logger.getStats = () => {
  const stats = {
    level: logger.level,
    transports: logger.transports.length,
    timestamp: new Date().toISOString()
  };
  
  logger.info('Logger statistics requested', stats);
  return stats;
};

// Función para cambiar nivel de log dinámicamente
logger.setLevel = (level) => {
  if (customLevels.levels.hasOwnProperty(level)) {
    logger.level = level;
    logger.info(`Log level changed to: ${level}`);
    return true;
  } else {
    logger.warn(`Invalid log level attempted: ${level}`);
    return false;
  }
};

// Función para limpiar logs antiguos (se puede llamar periódicamente)
logger.cleanup = () => {
  logger.info('Log cleanup initiated');
  // La limpieza se maneja automáticamente por las opciones maxFiles y maxsize
  // Esta función está disponible para limpieza manual si se necesita
};

module.exports = logger;