const MonthlyGoal = require('../models/MonthlyGoal');
const { isValidMonth, isValidYear, isValidAmount } = require('../utils/validators');

// Get goals for a specific month
exports.getMonthGoals = async (req, res, next) => {
  try {
    const userId = req.user.userId;
    const { year, month } = req.params;

    if (!isValidYear(year)) {
      return res.status(400).json({ error: 'Invalid year' });
    }

    if (!isValidMonth(month)) {
      return res.status(400).json({ error: 'Invalid month (0-11)' });
    }

    const goals = await MonthlyGoal.getOrCreateDefault(userId, parseInt(year), parseInt(month));
    res.json({ goals });
  } catch (error) {
    next(error);
  }
};

// Get all goals for a user
exports.getAll = async (req, res, next) => {
  try {
    const userId = req.user.userId;
    const { year } = req.query;

    const goals = await MonthlyGoal.findByUserId(userId, year ? parseInt(year) : null);
    res.json({ goals });
  } catch (error) {
    next(error);
  }
};

// Create or update goals
exports.upsert = async (req, res, next) => {
  try {
    const userId = req.user.userId;
    const { year, month, income_goal, gold_goal, investments_goal, silver_goal } = req.body;

    // Validation
    if (year === undefined || month === undefined) {
      return res.status(400).json({ error: 'Year and month are required' });
    }

    if (!isValidYear(year)) {
      return res.status(400).json({ error: 'Invalid year' });
    }

    if (!isValidMonth(month)) {
      return res.status(400).json({ error: 'Invalid month (0-11)' });
    }

    const goalData = {};
    if (income_goal !== undefined) {
      if (!isValidAmount(income_goal)) {
        return res.status(400).json({ error: 'Invalid income goal' });
      }
      goalData.income_goal = income_goal;
    }

    if (gold_goal !== undefined) {
      if (!isValidAmount(gold_goal)) {
        return res.status(400).json({ error: 'Invalid gold goal' });
      }
      goalData.gold_goal = gold_goal;
    }

    if (investments_goal !== undefined) {
      if (!isValidAmount(investments_goal)) {
        return res.status(400).json({ error: 'Invalid investments goal' });
      }
      goalData.investments_goal = investments_goal;
    }

    if (silver_goal !== undefined) {
      if (!isValidAmount(silver_goal)) {
        return res.status(400).json({ error: 'Invalid silver goal' });
      }
      goalData.silver_goal = silver_goal;
    }

    const goals = await MonthlyGoal.upsert(userId, parseInt(year), parseInt(month), goalData);

    res.status(200).json({ 
      message: 'Goals saved successfully',
      goals 
    });
  } catch (error) {
    next(error);
  }
};

// Update existing goals
exports.update = async (req, res, next) => {
  try {
    const { id } = req.params;
    const userId = req.user.userId;
    const updates = req.body;

    // Validate updates
    if (updates.income_goal !== undefined && !isValidAmount(updates.income_goal)) {
      return res.status(400).json({ error: 'Invalid income goal' });
    }

    if (updates.gold_goal !== undefined && !isValidAmount(updates.gold_goal)) {
      return res.status(400).json({ error: 'Invalid gold goal' });
    }

    if (updates.investments_goal !== undefined && !isValidAmount(updates.investments_goal)) {
      return res.status(400).json({ error: 'Invalid investments goal' });
    }

    if (updates.silver_goal !== undefined && !isValidAmount(updates.silver_goal)) {
      return res.status(400).json({ error: 'Invalid silver goal' });
    }

    const goals = await MonthlyGoal.update(id, userId, updates);
    
    if (!goals) {
      return res.status(404).json({ error: 'Goals not found' });
    }

    res.json({ 
      message: 'Goals updated successfully',
      goals 
    });
  } catch (error) {
    next(error);
  }
};

// Delete goals
exports.delete = async (req, res, next) => {
  try {
    const { id } = req.params;
    const userId = req.user.userId;

    const goals = await MonthlyGoal.delete(id, userId);
    
    if (!goals) {
      return res.status(404).json({ error: 'Goals not found' });
    }

    res.json({ 
      message: 'Goals deleted successfully',
      goals 
    });
  } catch (error) {
    next(error);
  }
};
