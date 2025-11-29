/**
 * Rutas de autenticación
 */

const express = require('express');
const router = express.Router();
const { body, validationResult } = require('express-validator');
const { 
  login, 
  refreshAccessToken, 
  logout, 
  createUser,
  authRateLimit 
} = require('../utils/auth');
const logger = require('../utils/logger');

// Aplicar rate limiting a todas las rutas de auth
router.use(authRateLimit);

// Validadores
const loginValidation = [
  body('username').trim().isLength({ min: 3 }).withMessage('Username debe tener al menos 3 caracteres'),
  body('password').isLength({ min: 6 }).withMessage('Password debe tener al menos 6 caracteres')
];

const registerValidation = [
  body('username').trim().isLength({ min: 3, max: 30 }).withMessage('Username debe tener entre 3 y 30 caracteres'),
  body('email').isEmail().withMessage('Email inválido'),
  body('password').isLength({ min: 6 }).withMessage('Password debe tener al menos 6 caracteres'),
  body('role').optional().isIn(['admin', 'developer', 'observer']).withMessage('Rol inválido')
];

const refreshValidation = [
  body('refreshToken').notEmpty().withMessage('Refresh token requerido')
];

// POST /api/auth/login - Iniciar sesión
router.post('/login', loginValidation, async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array()
      });
    }
    
    const { username, password } = req.body;
    
    const result = await login(username, password);
    
    res.json({
      success: true,
      data: result,
      message: 'Login exitoso',
      timestamp: new Date().toISOString()
    });
    
    logger.auth('Login successful', result.user.id, {
      username: result.user.username,
      role: result.user.role,
      ip: req.ip
    });
    
  } catch (error) {
    logger.security('Login failed', {
      username: req.body.username,
      ip: req.ip,
      error: error.message
    });
    
    res.status(401).json({
      success: false,
      error: 'Error de autenticación',
      message: error.message
    });
  }
});

// POST /api/auth/register - Registrar nuevo usuario
router.post('/register', registerValidation, async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array()
      });
    }
    
    const userData = {
      username: req.body.username,
      email: req.body.email,
      password: req.body.password,
      role: req.body.role || 'observer'
    };
    
    const newUser = await createUser(userData);
    
    res.status(201).json({
      success: true,
      data: newUser,
      message: 'Usuario creado exitosamente',
      timestamp: new Date().toISOString()
    });
    
    logger.auth('User registered', newUser.id, {
      username: newUser.username,
      role: newUser.role,
      ip: req.ip
    });
    
  } catch (error) {
    logger.error('Registration failed:', error);
    
    res.status(400).json({
      success: false,
      error: 'Error en registro',
      message: error.message
    });
  }
});

// POST /api/auth/refresh - Renovar token de acceso
router.post('/refresh', refreshValidation, async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array()
      });
    }
    
    const { refreshToken } = req.body;
    
    const tokens = await refreshAccessToken(refreshToken);
    
    res.json({
      success: true,
      data: tokens,
      message: 'Token renovado exitosamente',
      timestamp: new Date().toISOString()
    });
    
    logger.auth('Token refreshed', null, {
      ip: req.ip
    });
    
  } catch (error) {
    logger.security('Token refresh failed', {
      ip: req.ip,
      error: error.message
    });
    
    res.status(401).json({
      success: false,
      error: 'Error renovando token',
      message: error.message
    });
  }
});

// POST /api/auth/logout - Cerrar sesión
router.post('/logout', [
  body('refreshToken').notEmpty().withMessage('Refresh token requerido')
], (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array()
      });
    }
    
    const { refreshToken } = req.body;
    
    const logoutSuccess = logout(refreshToken);
    
    if (logoutSuccess) {
      res.json({
        success: true,
        message: 'Logout exitoso',
        timestamp: new Date().toISOString()
      });
      
      logger.auth('User logged out', null, {
        ip: req.ip
      });
    } else {
      res.status(400).json({
        success: false,
        error: 'Error en logout',
        message: 'Refresh token inválido'
      });
    }
    
  } catch (error) {
    logger.error('Logout error:', error);
    
    res.status(500).json({
      success: false,
      error: 'Error interno del servidor',
      message: error.message
    });
  }
});

// GET /api/auth/profile - Obtener perfil del usuario (requiere autenticación)
router.get('/profile', require('../utils/auth').authenticate, (req, res) => {
  try {
    res.json({
      success: true,
      data: {
        id: req.user.id,
        username: req.user.username,
        role: req.user.role,
        permissions: req.user.permissions
      },
      timestamp: new Date().toISOString()
    });
    
    logger.auth('Profile accessed', req.user.id);
    
  } catch (error) {
    logger.error('Profile access error:', error);
    
    res.status(500).json({
      success: false,
      error: 'Error interno del servidor',
      message: error.message
    });
  }
});

// GET /api/auth/check - Verificar si el token es válido
router.get('/check', require('../utils/auth').authenticate, (req, res) => {
  try {
    res.json({
      success: true,
      data: {
        valid: true,
        user: {
          id: req.user.id,
          username: req.user.username,
          role: req.user.role,
          permissions: req.user.permissions
        }
      },
      timestamp: new Date().toISOString()
    });
    
  } catch (error) {
    res.status(401).json({
      success: false,
      data: {
        valid: false
      },
      error: 'Token inválido'
    });
  }
});

module.exports = router;