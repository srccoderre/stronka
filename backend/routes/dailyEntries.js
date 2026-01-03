const express = require('express');
const router = express.Router();
const dailyEntriesController = require('../controllers/dailyEntriesController');
const { authenticateToken } = require('../middleware/auth');

// All routes are protected
router.use(authenticateToken);

// Routes
router.get('/', dailyEntriesController.getAll);
router.get('/stats/:year/:month', dailyEntriesController.getMonthlyStats);
router.get('/:id', dailyEntriesController.getOne);
router.post('/', dailyEntriesController.create);
router.put('/:id', dailyEntriesController.update);
router.delete('/:id', dailyEntriesController.delete);

module.exports = router;
