const express = require('express');
const router = express.Router();
const goalsController = require('../controllers/goalsController');
const { authenticateToken } = require('../middleware/auth');

// All routes are protected
router.use(authenticateToken);

// Routes
router.get('/', goalsController.getAll);
router.get('/:year/:month', goalsController.getMonthGoals);
router.post('/', goalsController.upsert);
router.put('/:id', goalsController.update);
router.delete('/:id', goalsController.delete);

module.exports = router;
