const express = require('express');
const router = express.Router();
const investmentsController = require('../controllers/investmentsController');
const { authenticateToken } = require('../middleware/auth');

// All routes are protected
router.use(authenticateToken);

// Routes
router.get('/', investmentsController.getAll);
router.get('/stats/:year/:month', investmentsController.getMonthlyStats);
router.get('/:id', investmentsController.getOne);
router.post('/', investmentsController.create);
router.put('/:id', investmentsController.update);
router.delete('/:id', investmentsController.delete);

module.exports = router;
