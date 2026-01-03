const db = require('../config/db');

class Investment {
  // Create a new investment
  static async create(userId, data) {
    const { date, type, amount, price, total, notes = null, month } = data;
    
    const query = `
      INSERT INTO investments (user_id, date, type, amount, price, total, notes, month)
      VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
      RETURNING *
    `;
    
    const result = await db.query(query, [userId, date, type, amount, price, total, notes, month]);
    return result.rows[0];
  }

  // Get all investments for a user
  static async findByUserId(userId, filters = {}) {
    let query = 'SELECT * FROM investments WHERE user_id = $1';
    const params = [userId];
    let paramIndex = 2;

    if (filters.type) {
      query += ` AND type = $${paramIndex}`;
      params.push(filters.type);
      paramIndex++;
    }

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

  // Get a single investment by ID
  static async findById(id, userId) {
    const query = 'SELECT * FROM investments WHERE id = $1 AND user_id = $2';
    const result = await db.query(query, [id, userId]);
    return result.rows[0];
  }

  // Update an investment
  static async update(id, userId, updates) {
    const allowedFields = ['date', 'type', 'amount', 'price', 'total', 'notes', 'month'];
    const fields = Object.keys(updates).filter(key => allowedFields.includes(key));
    
    if (fields.length === 0) {
      return null;
    }

    const setClause = fields.map((field, index) => `${field} = $${index + 3}`).join(', ');
    const values = fields.map(field => updates[field]);
    
    const query = `
      UPDATE investments 
      SET ${setClause}, updated_at = NOW()
      WHERE id = $1 AND user_id = $2
      RETURNING *
    `;
    
    const result = await db.query(query, [id, userId, ...values]);
    return result.rows[0];
  }

  // Delete an investment
  static async delete(id, userId) {
    const query = 'DELETE FROM investments WHERE id = $1 AND user_id = $2 RETURNING *';
    const result = await db.query(query, [id, userId]);
    return result.rows[0];
  }

  // Get monthly statistics by type
  static async getMonthlyStats(userId, year, month) {
    const query = `
      SELECT 
        type,
        COALESCE(SUM(amount), 0) as total_amount,
        COALESCE(SUM(total), 0) as total_value,
        COUNT(*) as count
      FROM investments
      WHERE user_id = $1 AND month = $2 AND EXTRACT(YEAR FROM date) = $3
      GROUP BY type
      ORDER BY type
    `;
    
    const result = await db.query(query, [userId, month, year]);
    return result.rows;
  }

  // Get total investments for a month
  static async getTotalForMonth(userId, year, month) {
    const query = `
      SELECT 
        COALESCE(SUM(total), 0) as total_investments
      FROM investments
      WHERE user_id = $1 AND month = $2 AND EXTRACT(YEAR FROM date) = $3
    `;
    
    const result = await db.query(query, [userId, month, year]);
    return result.rows[0];
  }
}

module.exports = Investment;
