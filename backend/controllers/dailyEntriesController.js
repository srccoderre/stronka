const DailyEntry = require('../models/DailyEntry');
const { isValidDate, isValidMonth, isValidAmount } = require('../utils/validators');

// Get all daily entries
exports.getAll = async (req, res, next) => {
  try {
    const userId = req.user.userId;
    const { month, startDate, endDate } = req.query;

    const filters = {};
    if (month !== undefined) filters.month = parseInt(month);
    if (startDate) filters.startDate = startDate;
    if (endDate) filters.endDate = endDate;

    const entries = await DailyEntry.findByUserId(userId, filters);
    res.json({ entries });
  } catch (error) {
    next(error);
  }
};

// Get single entry
exports.getOne = async (req, res, next) => {
  try {
    const { id } = req.params;
    const userId = req.user.userId;

    const entry = await DailyEntry.findById(id, userId);
    
    if (!entry) {
      return res.status(404).json({ error: 'Entry not found' });
    }

    res.json({ entry });
  } catch (error) {
    next(error);
  }
};

// Create new entry
exports.create = async (req, res, next) => {
  try {
    const userId = req.user.userId;
    const { date, income, expense, category, notes, month } = req.body;

    // Validation
    if (!date) {
      return res.status(400).json({ error: 'Date is required' });
    }

    if (!isValidDate(date)) {
      return res.status(400).json({ error: 'Invalid date format' });
    }

    if (month !== undefined && !isValidMonth(month)) {
      return res.status(400).json({ error: 'Invalid month (0-11)' });
    }

    if (income && !isValidAmount(income)) {
      return res.status(400).json({ error: 'Invalid income amount' });
    }

    if (expense && !isValidAmount(expense)) {
      return res.status(400).json({ error: 'Invalid expense amount' });
    }

    const entry = await DailyEntry.create(userId, {
      date,
      income,
      expense,
      category,
      notes,
      month: month !== undefined ? month : new Date(date).getMonth(),
    });

    res.status(201).json({ 
      message: 'Entry created successfully',
      entry 
    });
  } catch (error) {
    if (error.constraint === 'unique_user_date') {
      return res.status(409).json({ error: 'Entry for this date already exists' });
    }
    next(error);
  }
};

// Update entry
exports.update = async (req, res, next) => {
  try {
    const { id } = req.params;
    const userId = req.user.userId;
    const updates = req.body;

    // Validate updates
    if (updates.date && !isValidDate(updates.date)) {
      return res.status(400).json({ error: 'Invalid date format' });
    }

    if (updates.month !== undefined && !isValidMonth(updates.month)) {
      return res.status(400).json({ error: 'Invalid month (0-11)' });
    }

    if (updates.income && !isValidAmount(updates.income)) {
      return res.status(400).json({ error: 'Invalid income amount' });
    }

    if (updates.expense && !isValidAmount(updates.expense)) {
      return res.status(400).json({ error: 'Invalid expense amount' });
    }

    const entry = await DailyEntry.update(id, userId, updates);
    
    if (!entry) {
      return res.status(404).json({ error: 'Entry not found' });
    }

    res.json({ 
      message: 'Entry updated successfully',
      entry 
    });
  } catch (error) {
    next(error);
  }
};

// Delete entry
exports.delete = async (req, res, next) => {
  try {
    const { id } = req.params;
    const userId = req.user.userId;

    const entry = await DailyEntry.delete(id, userId);
    
    if (!entry) {
      return res.status(404).json({ error: 'Entry not found' });
    }

    res.json({ 
      message: 'Entry deleted successfully',
      entry 
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

    const stats = await DailyEntry.getMonthlyStats(userId, parseInt(year), parseInt(month));
    res.json({ stats });
  } catch (error) {
    next(error);
  }
};
