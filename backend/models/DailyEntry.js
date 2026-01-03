const db = require('../config/db');

class DailyEntry {
  // Create a new daily entry
  static async create(userId, data) {
    const { date, income = 0, expense = 0, category = null, notes = null, month } = data;
    
    const query = `
      INSERT INTO daily_entries (user_id, date, income, expense, category, notes, month)
      VALUES ($1, $2, $3, $4, $5, $6, $7)
      RETURNING *
    `;
    
    const result = await db.query(query, [userId, date, income, expense, category, notes, month]);
    return result.rows[0];
  }

  // Get all entries for a user
  static async findByUserId(userId, filters = {}) {
    let query = 'SELECT * FROM daily_entries WHERE user_id = $1';
    const params = [userId];
    let paramIndex = 2;

    if (filters.month !== undefined) {
      query += ` AND month = $${paramIndex}`;
      params.push(filters.month);
      paramIndex++;
    }

    if (filters.startDate) {
      query += ` AND date >= $${paramIndex}`;
      params.push(filters.startDate);
      paramIndex++;
    }

    if (filters.endDate) {
      query += ` AND date <= $${paramIndex}`;
      params.push(filters.endDate);
      paramIndex++;
    }

    query += ' ORDER BY date DESC';

    const result = await db.query(query, params);
    return result.rows;
  }

  // Get a single entry by ID
  static async findById(id, userId) {
    const query = 'SELECT * FROM daily_entries WHERE id = $1 AND user_id = $2';
    const result = await db.query(query, [id, userId]);
    return result.rows[0];
  }

  // Update an entry
  static async update(id, userId, updates) {
    const allowedFields = ['date', 'income', 'expense', 'category', 'notes', 'month'];
    const fields = Object.keys(updates).filter(key => allowedFields.includes(key));
    
    if (fields.length === 0) {
      return null;
    }

    const setClause = fields.map((field, index) => `${field} = $${index + 3}`).join(', ');
    const values = fields.map(field => updates[field]);
    
    const query = `
      UPDATE daily_entries 
      SET ${setClause}, updated_at = NOW()
      WHERE id = $1 AND user_id = $2
      RETURNING *
    `;
    
    const result = await db.query(query, [id, userId, ...values]);
    return result.rows[0];
  }

  // Delete an entry
  static async delete(id, userId) {
    const query = 'DELETE FROM daily_entries WHERE id = $1 AND user_id = $2 RETURNING *';
    const result = await db.query(query, [id, userId]);
    return result.rows[0];
  }

  // Get monthly statistics
  static async getMonthlyStats(userId, year, month) {
    const query = `
      SELECT 
        COALESCE(SUM(income), 0) as total_income,
        COALESCE(SUM(expense), 0) as total_expense,
        COALESCE(SUM(balance), 0) as total_balance,
        COUNT(*) as entry_count
      FROM daily_entries
      WHERE user_id = $1 AND month = $2 AND EXTRACT(YEAR FROM date) = $3
    `;
    
    const result = await db.query(query, [userId, month, year]);
    return result.rows[0];
  }
}

module.exports = DailyEntry;
