/**
 * Servidor principal para Ciudad Robot Backend
 * API REST con WebSockets para comunicación en tiempo real
 */

const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const compression = require('compression');
const rateLimit = require('express-rate-limit');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

const tryRequireLocal = (relativePath, fallbackFactory, logger) => {
  const absolutePath = path.join(__dirname, relativePath);
  const exists = fs.existsSync(absolutePath) || fs.existsSync(`${absolutePath}.js`);

  if (exists) {
    return require(relativePath);
  }

  if (logger) {
    logger.warn(`Modulo opcional no encontrado: ${relativePath}. Se usara fallback.`);
  }
  return fallbackFactory();
};

const createUnavailableRoute = (name) => {
  const router = express.Router();
  router.use((req, res) => {
    res.status(503).json({
      success: false,
      error: 'Modulo no disponible',
      message: `La ruta ${name} no esta habilitada en esta instalacion.`
    });
  });
  return router;
};

class FallbackAIService {
  async initialize() {}
  async processRequest() {
    throw new Error('AIService no disponible');
  }
  getStatus() {
    return 'unavailable';
  }
  async getRequestsPerMinute() {
    return 0;
  }
  async getAverageResponseTime() {
    return 0;
  }
}

class FallbackSocketService {
  constructor() {
    this.connectionCount = 0;
  }
  async initialize() {}
  handleConnection() {
    this.connectionCount += 1;
  }
  handleDisconnection() {
    this.connectionCount = Math.max(0, this.connectionCount - 1);
  }
  handleJoinCity() {}
  handleRobotCommand() {}
  handleAvatarAction() {}
  handleCityInteraction() {}
  getConnectionCount() {
    return this.connectionCount;
  }
}

class FallbackDatabaseService {
  async connect() {}
  async disconnect() {}
}

// Importar rutas
const robotRoutes = require('./routes/robots');
const avatarRoutes = require('./routes/avatars');
const cityRoutes = require('./routes/city');
const aiRoutes = require('./routes/ai');
const authRoutes = require('./routes/auth');
const logger = require('./utils/logger');
const userRoutes = tryRequireLocal('./routes/users', () => createUnavailableRoute('users'), logger);
const analyticsRoutes = tryRequireLocal('./routes/analytics', () => createUnavailableRoute('analytics'), logger);
const quantumRoutes = tryRequireLocal('./routes/quantum', () => createUnavailableRoute('quantum'), logger);

// Importar middleware
const errorHandler = tryRequireLocal('./middleware/errorHandler', () => {
  return (error, req, res, next) => {
    logger.error('Error no manejado:', error);
    res.status(500).json({
      success: false,
      error: 'Error interno del servidor',
      message: error?.message || 'Unexpected error'
    });
  };
}, logger);

// Importar servicios
const AIService = tryRequireLocal('./services/aiService', () => FallbackAIService, logger);
const SocketService = tryRequireLocal('./services/socketService', () => FallbackSocketService, logger);
const DatabaseService = tryRequireLocal('./services/databaseService', () => FallbackDatabaseService, logger);

class CiudadRobotServer {
  constructor() {
    this.app = express();
    this.server = http.createServer(this.app);
    this.io = socketIo(this.server, {
      cors: {
        origin: process.env.FRONTEND_URL || "http://localhost:3000",
        methods: ["GET", "POST"]
      }
    });
    
    this.port = process.env.PORT || 8000;
    this.aiService = new AIService();
    this.socketService = new SocketService(this.io);
    this.databaseService = new DatabaseService();
    
    this.setupMiddleware();
    this.setupRoutes();
    this.setupSocketHandlers();
    this.setupErrorHandling();
  }

  setupMiddleware() {
    // Seguridad
    this.app.use(helmet());
    
    // CORS
    this.app.use(cors({
      origin: process.env.FRONTEND_URL || "http://localhost:3000",
      credentials: true
    }));
    
    // Compresión
    this.app.use(compression());
    
    // Rate limiting
    const limiter = rateLimit({
      windowMs: 15 * 60 * 1000, // 15 minutos
      max: 100, // límite de 100 requests por ventana
      message: 'Demasiadas solicitudes desde esta IP'
    });
    this.app.use(limiter);
    
    // Logging
    this.app.use(morgan('combined', { 
      stream: { write: message => logger.info(message.trim()) }
    }));
    
    // Body parsing
    this.app.use(express.json({ limit: '10mb' }));
    this.app.use(express.urlencoded({ extended: true, limit: '10mb' }));
    
    // Archivos estáticos
    this.app.use('/uploads', express.static('uploads'));
  }

  setupRoutes() {
    // Ruta de salud del sistema
    this.app.get('/health', (req, res) => {
      res.json({
        status: 'OK',
        timestamp: new Date().toISOString(),
        uptime: process.uptime(),
        version: process.env.npm_package_version || '1.0.0',
        environment: process.env.NODE_ENV || 'development'
      });
    });

    // API Routes
    this.app.use('/api/robots', robotRoutes);
    this.app.use('/api/avatars', avatarRoutes);
    this.app.use('/api/city', cityRoutes);
    this.app.use('/api/ai', aiRoutes);
    this.app.use('/api/auth', authRoutes);
    this.app.use('/api/users', userRoutes);
    this.app.use('/api/analytics', analyticsRoutes);
    this.app.use('/api/security', require('./routes/security'));
    this.app.use('/api/quantum', quantumRoutes);

    // Documentación de la API
    this.app.get('/api', (req, res) => {
      res.json({
        name: 'Ciudad Robot API',
        version: '1.0.0',
        description: 'API REST para gestión de ciudad robot virtual con IA avanzada',
        endpoints: {
          '/api/robots': 'Gestión de robots virtuales',
          '/api/avatars': 'Sistema de avatares personalizados',
          '/api/city': 'Optimización y métricas de ciudad',
          '/api/ai': 'Interacción con sistema de IA',
          '/api/users': 'Gestión de usuarios',
          '/api/analytics': 'Análisis y estadísticas',
          '/api/security': 'Sistema de seguridad con humanoides IA',
          '/api/quantum': 'Módulo cuántico — circuitos y simulación',
          '/health': 'Estado del sistema',
          '/ws': 'WebSocket para tiempo real'
        },
        documentation: '/api/docs'
      });
    });

    // Ruta 404 (Express 5: usar middleware sin patron wildcard)
    this.app.use((req, res) => {
      res.status(404).json({
        error: 'Endpoint no encontrado',
        message: `La ruta ${req.originalUrl} no existe`,
        availableEndpoints: '/api'
      });
    });
  }

  setupSocketHandlers() {
    this.io.on('connection', (socket) => {
      logger.info(`Cliente conectado: ${socket.id}`);
      
      // Registrar cliente en el servicio de sockets
      this.socketService.handleConnection(socket);
      
      // Eventos principales
      socket.on('join_city', (data) => {
        this.socketService.handleJoinCity(socket, data);
      });
      
      socket.on('robot_command', (data) => {
        this.socketService.handleRobotCommand(socket, data);
      });
      
      socket.on('avatar_action', (data) => {
        this.socketService.handleAvatarAction(socket, data);
      });
      
      socket.on('ai_request', async (data) => {
        try {
          const result = await this.aiService.processRequest(data);
          socket.emit('ai_response', result);
        } catch (error) {
          socket.emit('ai_error', { error: error.message });
        }
      });
      
      socket.on('city_interaction', (data) => {
        this.socketService.handleCityInteraction(socket, data);
      });
      
      socket.on('disconnect', (reason) => {
        logger.info(`Cliente desconectado: ${socket.id}, razón: ${reason}`);
        this.socketService.handleDisconnection(socket);
      });
      
      // Enviar estado inicial del sistema
      socket.emit('system_status', this.getSystemStatus());
    });
  }

  setupErrorHandling() {
    // Middleware de manejo de errores
    this.app.use(errorHandler);
    
    // Manejo de errores no capturados
    process.on('uncaughtException', (error) => {
      logger.error('Uncaught Exception:', error);
      process.exit(1);
    });
    
    process.on('unhandledRejection', (reason, promise) => {
      logger.error('Unhandled Rejection at:', promise, 'reason:', reason);
      process.exit(1);
    });
  }

  getSystemStatus() {
    return {
      server: 'online',
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
      memory: {
        used: Math.round((process.memoryUsage().heapUsed / 1024 / 1024) * 100) / 100,
        total: Math.round((process.memoryUsage().heapTotal / 1024 / 1024) * 100) / 100
      },
      connections: this.socketService.getConnectionCount(),
      ai_status: this.aiService.getStatus()
    };
  }

  async start() {
    try {
      // Conectar a la base de datos
      await this.databaseService.connect();
      
      // Inicializar servicios
      await this.aiService.initialize();
      await this.socketService.initialize();
      
      // Iniciar servidor
      this.server.listen(this.port, () => {
        logger.info(`🤖 Ciudad Robot Server iniciado en puerto ${this.port}`);
        logger.info(`📡 WebSocket disponible en ws://localhost:${this.port}`);
        logger.info(`🌐 API disponible en http://localhost:${this.port}/api`);
        logger.info(`💚 Health check en http://localhost:${this.port}/health`);
        
        if (process.env.NODE_ENV === 'development') {
          logger.info(`🔧 Modo desarrollo activado`);
        }
      });
      
      // Configurar broadcasting de estado del sistema
      this.startSystemBroadcast();
      
    } catch (error) {
      logger.error('Error iniciando servidor:', error);
      process.exit(1);
    }
  }

  startSystemBroadcast() {
    // Enviar estado del sistema cada 5 segundos
    setInterval(() => {
      const status = this.getSystemStatus();
      this.io.emit('system_status_update', status);
    }, 5000);
    
    // Estadísticas cada 30 segundos
    setInterval(async () => {
      try {
        const analytics = await this.getSystemAnalytics();
        this.io.emit('system_analytics', analytics);
      } catch (error) {
        logger.error('Error obteniendo analytics:', error);
      }
    }, 30000);
  }

  async getSystemAnalytics() {
    // Obtener estadísticas del sistema
    return {
      timestamp: new Date().toISOString(),
      robots: {
        total: await this.getRobotCount(),
        active: await this.getActiveRobotCount()
      },
      avatars: {
        total: await this.getAvatarCount(),
        online: await this.getOnlineAvatarCount()
      },
      city: {
        efficiency: await this.getCityEfficiency(),
        optimization_score: await this.getOptimizationScore()
      },
      ai: {
        requests_per_minute: await this.aiService.getRequestsPerMinute(),
        average_response_time: await this.aiService.getAverageResponseTime()
      }
    };
  }

  // Métodos auxiliares para analytics
  async getRobotCount() {
    // Implementar conteo de robots desde BD o servicio
    return 0;
  }

  async getActiveRobotCount() {
    return 0;
  }

  async getAvatarCount() {
    return 0;
  }

  async getOnlineAvatarCount() {
    return 0;
  }

  async getCityEfficiency() {
    return 0.85; // 85% de eficiencia simulada
  }

  async getOptimizationScore() {
    return 0.92; // 92% de score de optimización simulado
  }

  async shutdown() {
    logger.info('Cerrando servidor...');
    
    // Cerrar conexiones de base de datos
    await this.databaseService.disconnect();
    
    // Cerrar servidor
    this.server.close(() => {
      logger.info('Servidor cerrado correctamente');
      process.exit(0);
    });
  }
}

// Crear y iniciar servidor
const server = new CiudadRobotServer();

// Manejo de señales de cierre
process.on('SIGTERM', () => server.shutdown());
process.on('SIGINT', () => server.shutdown());

// Iniciar servidor
server.start().catch(error => {
  logger.error('Error fatal:', error);
  process.exit(1);
});

module.exports = CiudadRobotServer;