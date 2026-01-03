const express = require('express');
const router = express.Router();
const authController = require('../controllers/authController');
const { authenticateToken } = require('../middleware/auth');
const { authLimiter, registerLimiter } = require('../middleware/rateLimiter');

// Public routes with rate limiting
router.post('/register', registerLimiter, authController.register);
router.post('/login', authLimiter, authController.login);
router.post('/refresh', authController.refresh);
router.post('/logout', authController.logout);

// Protected routes
router.get('/me', authenticateToken, authController.me);

module.exports = router;
