const jwt = require('jsonwebtoken');
const securityConfig = require('../config/security');

// Verify JWT access token
const authenticateToken = (req, res, next) => {
  try {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1]; // Bearer TOKEN

    if (!token) {
      return res.status(401).json({ error: 'Access token required' });
    }

    jwt.verify(token, securityConfig.jwt.secret, (err, user) => {
      if (err) {
        if (err.name === 'TokenExpiredError') {
          return res.status(401).json({ error: 'Token expired' });
        }
        return res.status(403).json({ error: 'Invalid token' });
      }

      req.user = user;
      next();
    });
  } catch (error) {
    res.status(500).json({ error: 'Authentication error' });
  }
};

// Optional authentication (doesn't fail if no token)
const optionalAuth = (req, res, next) => {
  try {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];

    if (!token) {
      return next();
    }

    jwt.verify(token, securityConfig.jwt.secret, (err, user) => {
      if (!err) {
        req.user = user;
      }
      next();
    });
  } catch (error) {
    next();
  }
};

// Check resource ownership
const checkOwnership = (resourceUserIdField = 'user_id') => {
  return (req, res, next) => {
    const resourceUserId = req.body[resourceUserIdField] || req.params[resourceUserIdField];
    
    if (req.user.userId !== resourceUserId && req.user.userId !== parseInt(resourceUserId)) {
      return res.status(403).json({ error: 'Access denied' });
    }
    
    next();
  };
};

module.exports = {
  authenticateToken,
  optionalAuth,
  checkOwnership,
};
