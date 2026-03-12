/**
 * Middleware de autenticación y autorización
 */

const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');
const rateLimit = require('express-rate-limit');
const logger = require('./logger');

// Configuración
const JWT_SECRET = process.env.JWT_SECRET || 'ciudad-robot-secret-key-development';
const JWT_EXPIRES_IN = process.env.JWT_EXPIRES_IN || '24h';
const REFRESH_TOKEN_EXPIRES_IN = process.env.REFRESH_TOKEN_EXPIRES_IN || '7d';

// Simulación de base de datos de usuarios (en producción sería BD real)
let users = [
  {
    id: 'user-001',
    username: 'admin',
    email: 'admin@ciudadrobot.com',
    password: '$2a$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', // password
    role: 'admin',
    permissions: ['create', 'read', 'update', 'delete', 'manage'],
    created_at: new Date().toISOString(),
    last_login: null,
    active: true
  },
  {
    id: 'user-002',
    username: 'developer',
    email: 'dev@ciudadrobot.com',
    password: '$2a$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', // password
    role: 'developer',
    permissions: ['create', 'read', 'update', 'manage_robots', 'manage_ai'],
    created_at: new Date().toISOString(),
    last_login: null,
    active: true
  },
  {
    id: 'user-003',
    username: 'observer',
    email: 'observer@ciudadrobot.com',
    password: '$2a$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', // password
    role: 'observer',
    permissions: ['read'],
    created_at: new Date().toISOString(),
    last_login: null,
    active: true
  }
];

let refreshTokens = []; // En producción sería BD o Redis

// Rate limiting para diferentes endpoints
const authRateLimit = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutos
  max: 5, // máximo 5 intentos de login por IP
  message: {
    success: false,
    error: 'Demasiados intentos de autenticación',
    message: 'Intenta nuevamente en 15 minutos'
  },
  standardHeaders: true,
  legacyHeaders: false,
  handler: (req, res) => {
    logger.security('Rate limit exceeded for authentication', {
      ip: req.ip,
      userAgent: req.get('User-Agent')
    });
    res.status(429).json({
      success: false,
      error: 'Demasiados intentos de autenticación',
      message: 'Intenta nuevamente en 15 minutos'
    });
  }
});

const apiRateLimit = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutos
  max: 1000, // máximo 1000 requests por IP
  message: {
    success: false,
    error: 'Límite de requests excedido',
    message: 'Intenta nuevamente en 15 minutos'
  },
  standardHeaders: true,
  legacyHeaders: false
});

// Funciones de utilidad
const generateTokens = (user) => {
  const payload = {
    userId: user.id,
    username: user.username,
    role: user.role,
    permissions: user.permissions
  };
  
  const accessToken = jwt.sign(payload, JWT_SECRET, { 
    expiresIn: JWT_EXPIRES_IN,
    issuer: 'ciudad-robot-api',
    audience: 'ciudad-robot-app'
  });
  
  const refreshToken = jwt.sign(
    { userId: user.id, type: 'refresh' }, 
    JWT_SECRET, 
    { 
      expiresIn: REFRESH_TOKEN_EXPIRES_IN,
      issuer: 'ciudad-robot-api',
      audience: 'ciudad-robot-app'
    }
  );
  
  return { accessToken, refreshToken };
};

const hashPassword = async (password) => {
  return await bcrypt.hash(password, 12);
};

const comparePassword = async (password, hash) => {
  return await bcrypt.compare(password, hash);
};

const findUserByUsername = (username) => {
  return users.find(user => user.username === username && user.active);
};

const findUserByEmail = (email) => {
  return users.find(user => user.email === email && user.active);
};

const findUserById = (id) => {
  return users.find(user => user.id === id && user.active);
};

// Middleware de autenticación
const authenticate = (req, res, next) => {
  try {
    const authHeader = req.headers.authorization;
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({
        success: false,
        error: 'Token de acceso requerido',
        message: 'Proporciona un token válido en el header Authorization'
      });
    }
    
    const token = authHeader.substring(7); // Remover 'Bearer '
    
    const decoded = jwt.verify(token, JWT_SECRET, {
      issuer: 'ciudad-robot-api',
      audience: 'ciudad-robot-app'
    });
    
    const user = findUserById(decoded.userId);
    
    if (!user) {
      return res.status(401).json({
        success: false,
        error: 'Usuario no encontrado',
        message: 'El usuario asociado al token no existe'
      });
    }
    
    req.user = {
      id: user.id,
      username: user.username,
      role: user.role,
      permissions: user.permissions
    };
    
    logger.auth('Token authenticated', user.id, {
      username: user.username,
      role: user.role
    });
    
    next();
  } catch (error) {
    if (error.name === 'JsonWebTokenError') {
      return res.status(401).json({
        success: false,
        error: 'Token inválido',
        message: 'El token proporcionado no es válido'
      });
    } else if (error.name === 'TokenExpiredError') {
      return res.status(401).json({
        success: false,
        error: 'Token expirado',
        message: 'El token ha expirado, usa el refresh token'
      });
    } else {
      logger.error('Error en autenticación:', error);
      return res.status(500).json({
        success: false,
        error: 'Error de autenticación',
        message: 'Error interno del servidor'
      });
    }
  }
};

// Middleware de autorización
const authorize = (requiredPermissions = []) => {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({
        success: false,
        error: 'Usuario no autenticado'
      });
    }
    
    const userPermissions = req.user.permissions || [];
    
    // Los administradores tienen todos los permisos
    if (req.user.role === 'admin') {
      return next();
    }
    
    // Verificar si el usuario tiene los permisos requeridos
    const hasPermission = requiredPermissions.every(permission => 
      userPermissions.includes(permission)
    );
    
    if (!hasPermission) {
      logger.security('Authorization failed', {
        userId: req.user.id,
        required: requiredPermissions,
        user_permissions: userPermissions
      });
      
      return res.status(403).json({
        success: false,
        error: 'Permisos insuficientes',
        message: 'No tienes permisos para realizar esta acción',
        required: requiredPermissions
      });
    }
    
    next();
  };
};

// Middleware opcional de autenticación (para endpoints públicos con funcionalidad extra para usuarios autenticados)
const optionalAuth = (req, res, next) => {
  try {
    const authHeader = req.headers.authorization;
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return next(); // Continuar sin autenticación
    }
    
    const token = authHeader.substring(7);
    
    const decoded = jwt.verify(token, JWT_SECRET, {
      issuer: 'ciudad-robot-api',
      audience: 'ciudad-robot-app'
    });
    
    const user = findUserById(decoded.userId);
    
    if (user) {
      req.user = {
        id: user.id,
        username: user.username,
        role: user.role,
        permissions: user.permissions
      };
    }
    
    next();
  } catch (error) {
    // En autenticación opcional, ignorar errores de token
    next();
  }
};

// Funciones de autenticación
const login = async (username, password) => {
  try {
    const user = findUserByUsername(username) || findUserByEmail(username);
    
    if (!user) {
      logger.security('Login attempt with invalid username', { username });
      throw new Error('Credenciales inválidas');
    }
    
    const isValidPassword = await comparePassword(password, user.password);
    
    if (!isValidPassword) {
      logger.security('Login attempt with invalid password', { 
        userId: user.id,
        username: user.username 
      });
      throw new Error('Credenciales inválidas');
    }
    
    // Actualizar último login
    user.last_login = new Date().toISOString();
    
    const { accessToken, refreshToken } = generateTokens(user);
    
    // Almacenar refresh token
    refreshTokens.push({
      token: refreshToken,
      userId: user.id,
      created_at: new Date().toISOString()
    });
    
    logger.auth('User logged in', user.id, {
      username: user.username,
      role: user.role
    });
    
    return {
      user: {
        id: user.id,
        username: user.username,
        email: user.email,
        role: user.role,
        permissions: user.permissions
      },
      tokens: {
        accessToken,
        refreshToken,
        expiresIn: JWT_EXPIRES_IN
      }
    };
  } catch (error) {
    throw error;
  }
};

const refreshAccessToken = async (refreshToken) => {
  try {
    if (!refreshTokens.find(rt => rt.token === refreshToken)) {
      throw new Error('Refresh token inválido');
    }
    
    const decoded = jwt.verify(refreshToken, JWT_SECRET, {
      issuer: 'ciudad-robot-api',
      audience: 'ciudad-robot-app'
    });
    
    if (decoded.type !== 'refresh') {
      throw new Error('Token inválido');
    }
    
    const user = findUserById(decoded.userId);
    
    if (!user) {
      throw new Error('Usuario no encontrado');
    }
    
    const { accessToken, refreshToken: newRefreshToken } = generateTokens(user);
    
    // Remover refresh token anterior y agregar nuevo
    refreshTokens = refreshTokens.filter(rt => rt.token !== refreshToken);
    refreshTokens.push({
      token: newRefreshToken,
      userId: user.id,
      created_at: new Date().toISOString()
    });
    
    logger.auth('Token refreshed', user.id);
    
    return {
      accessToken,
      refreshToken: newRefreshToken,
      expiresIn: JWT_EXPIRES_IN
    };
  } catch (error) {
    throw error;
  }
};

const logout = (refreshToken) => {
  try {
    const tokenData = refreshTokens.find(rt => rt.token === refreshToken);
    
    if (tokenData) {
      refreshTokens = refreshTokens.filter(rt => rt.token !== refreshToken);
      logger.auth('User logged out', tokenData.userId);
      return true;
    }
    
    return false;
  } catch (error) {
    logger.error('Error in logout:', error);
    return false;
  }
};

const createUser = async (userData) => {
  try {
    // Verificar si el usuario ya existe
    if (findUserByUsername(userData.username) || findUserByEmail(userData.email)) {
      throw new Error('Usuario o email ya existe');
    }
    
    const hashedPassword = await hashPassword(userData.password);
    
    const newUser = {
      id: `user-${Date.now()}`,
      username: userData.username,
      email: userData.email,
      password: hashedPassword,
      role: userData.role || 'observer',
      permissions: userData.permissions || ['read'],
      created_at: new Date().toISOString(),
      last_login: null,
      active: true
    };
    
    users.push(newUser);
    
    logger.auth('User created', newUser.id, {
      username: newUser.username,
      role: newUser.role
    });
    
    return {
      id: newUser.id,
      username: newUser.username,
      email: newUser.email,
      role: newUser.role,
      permissions: newUser.permissions
    };
  } catch (error) {
    throw error;
  }
};

// Middleware para validar permisos específicos por recurso
const resourcePermission = (resource, action) => {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({
        success: false,
        error: 'Usuario no autenticado'
      });
    }
    
    const permissions = req.user.permissions || [];
    
    // Los administradores tienen acceso completo
    if (req.user.role === 'admin') {
      return next();
    }
    
    // Verificar permisos específicos por recurso
    const resourcePermissions = {
      robots: {
        create: ['create', 'manage_robots'],
        read: ['read'],
        update: ['update', 'manage_robots'],
        delete: ['delete', 'manage_robots']
      },
      avatars: {
        create: ['create'],
        read: ['read'],
        update: ['update'],
        delete: ['delete']
      },
      city: {
        create: ['manage'],
        read: ['read'],
        update: ['manage'],
        delete: ['manage']
      },
      ai: {
        create: ['manage_ai'],
        read: ['read'],
        update: ['manage_ai'],
        delete: ['manage_ai']
      },
      security: {
        create: ['create', 'manage'],
        read: ['read'],
        update: ['update', 'manage'],
        delete: ['delete', 'manage']
      }
    };
    
    const requiredPermissions = resourcePermissions[resource]?.[action] || [];
    const hasPermission = requiredPermissions.some(permission => 
      permissions.includes(permission)
    );
    
    if (!hasPermission) {
      logger.security('Resource permission denied', {
        userId: req.user.id,
        resource,
        action,
        required: requiredPermissions
      });
      
      return res.status(403).json({
        success: false,
        error: 'Permisos insuficientes',
        message: `No tienes permisos para ${action} en ${resource}`
      });
    }
    
    next();
  };
};

module.exports = {
  authenticate,
  authorize,
  optionalAuth,
  resourcePermission,
  authRateLimit,
  apiRateLimit,
  login,
  refreshAccessToken,
  logout,
  createUser,
  findUserById,
  findUserByUsername,
  generateTokens,
  hashPassword,
  comparePassword
};