const Investment = require('../models/Investment');
const { isValidDate, isValidMonth, isValidAmount, isValidInvestmentType } = require('../utils/validators');

// Get all investments
exports.getAll = async (req, res, next) => {
  try {
    const userId = req.user.userId;
    const { type, month, startDate, endDate } = req.query;

    const filters = {};
    if (type) filters.type = type;
    if (month !== undefined) filters.month = parseInt(month);
    if (startDate) filters.startDate = startDate;
    if (endDate) filters.endDate = endDate;

    const investments = await Investment.findByUserId(userId, filters);
    res.json({ investments });
  } catch (error) {
    next(error);
  }
};

// Get single investment
exports.getOne = async (req, res, next) => {
  try {
    const { id } = req.params;
    const userId = req.user.userId;

    const investment = await Investment.findById(id, userId);
    
    if (!investment) {
      return res.status(404).json({ error: 'Investment not found' });
    }

    res.json({ investment });
  } catch (error) {
    next(error);
  }
};

// Create new investment
exports.create = async (req, res, next) => {
  try {
    const userId = req.user.userId;
    const { date, type, amount, price, total, notes, month } = req.body;

    // Validation
    if (!date || !type) {
      return res.status(400).json({ error: 'Date and type are required' });
    }

    if (!isValidDate(date)) {
      return res.status(400).json({ error: 'Invalid date format' });
    }

    if (!isValidInvestmentType(type)) {
      return res.status(400).json({ error: 'Invalid investment type' });
    }

    if (month !== undefined && !isValidMonth(month)) {
      return res.status(400).json({ error: 'Invalid month (0-11)' });
    }

    if (amount && !isValidAmount(amount)) {
      return res.status(400).json({ error: 'Invalid amount' });
    }

    if (price && !isValidAmount(price)) {
      return res.status(400).json({ error: 'Invalid price' });
    }

    if (total && !isValidAmount(total)) {
      return res.status(400).json({ error: 'Invalid total' });
    }

    const investment = await Investment.create(userId, {
      date,
      type,
      amount,
      price,
      total,
      notes,
      month: month !== undefined ? month : new Date(date).getMonth(),
    });

    res.status(201).json({ 
      message: 'Investment created successfully',
      investment 
    });
  } catch (error) {
    next(error);
  }
};

// Update investment
exports.update = async (req, res, next) => {
  try {
    const { id } = req.params;
    const userId = req.user.userId;
    const updates = req.body;

    // Validate updates
    if (updates.date && !isValidDate(updates.date)) {
      return res.status(400).json({ error: 'Invalid date format' });
    }

    if (updates.type && !isValidInvestmentType(updates.type)) {
      return res.status(400).json({ error: 'Invalid investment type' });
    }

    if (updates.month !== undefined && !isValidMonth(updates.month)) {
      return res.status(400).json({ error: 'Invalid month (0-11)' });
    }

    if (updates.amount && !isValidAmount(updates.amount)) {
      return res.status(400).json({ error: 'Invalid amount' });
    }

    if (updates.price && !isValidAmount(updates.price)) {
      return res.status(400).json({ error: 'Invalid price' });
    }

    if (updates.total && !isValidAmount(updates.total)) {
      return res.status(400).json({ error: 'Invalid total' });
    }

    const investment = await Investment.update(id, userId, updates);
    
    if (!investment) {
      return res.status(404).json({ error: 'Investment not found' });
    }

    res.json({ 
      message: 'Investment updated successfully',
      investment 
    });
  } catch (error) {
    next(error);
  }
};

// Delete investment
exports.delete = async (req, res, next) => {
  try {
    const { id } = req.params;
    const userId = req.user.userId;

    const investment = await Investment.delete(id, userId);
    
    if (!investment) {
      return res.status(404).json({ error: 'Investment not found' });
    }

    res.json({ 
      message: 'Investment deleted successfully',
      investment 
    });
  } catch (error) {
    next(error);
  }
};

// Get monthly statistics
exports.getMonthlyStats = async (req, res, next) => {
  try {
    const userId = req.user.userId;
    const { year, month } = req.params;

    if (!isValidMonth(month)) {
      return res.status(400).json({ error: 'Invalid month (0-11)' });
    }

    const stats = await Investment.getMonthlyStats(userId, parseInt(year), parseInt(month));
    const total = await Investment.getTotalForMonth(userId, parseInt(year), parseInt(month));
    
    res.json({ stats, total: total.total_investments });
  } catch (error) {
    next(error);
  }
};
