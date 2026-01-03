const db = require('../config/db');

class MonthlyGoal {
  // Create or update monthly goals
  static async upsert(userId, year, month, goals) {
    const { income_goal = 20000, gold_goal = 10, investments_goal = 5100, silver_goal = 500 } = goals;
    
    const query = `
      INSERT INTO monthly_goals (user_id, year, month, income_goal, gold_goal, investments_goal, silver_goal)
      VALUES ($1, $2, $3, $4, $5, $6, $7)
      ON CONFLICT (user_id, year, month)
      DO UPDATE SET
        income_goal = EXCLUDED.income_goal,
        gold_goal = EXCLUDED.gold_goal,
        investments_goal = EXCLUDED.investments_goal,
        silver_goal = EXCLUDED.silver_goal,
        updated_at = NOW()
      RETURNING *
    `;
    
    const result = await db.query(query, [userId, year, month, income_goal, gold_goal, investments_goal, silver_goal]);
    return result.rows[0];
  }

  // Get goals for a specific month
  static async findByMonth(userId, year, month) {
    const query = `
      SELECT * FROM monthly_goals 
      WHERE user_id = $1 AND year = $2 AND month = $3
    `;
    
    const result = await db.query(query, [userId, year, month]);
    return result.rows[0];
  }

  // Get all goals for a user
  static async findByUserId(userId, year = null) {
    let query = 'SELECT * FROM monthly_goals WHERE user_id = $1';
    const params = [userId];

    if (year !== null) {
      query += ' AND year = $2';
      params.push(year);
    }

    query += ' ORDER BY year DESC, month DESC';

    const result = await db.query(query, params);
    return result.rows;
  }

  // Update goals
  static async update(id, userId, updates) {
    const allowedFields = ['income_goal', 'gold_goal', 'investments_goal', 'silver_goal'];
    const fields = Object.keys(updates).filter(key => allowedFields.includes(key));
    
    if (fields.length === 0) {
      return null;
    }

    const setClause = fields.map((field, index) => `${field} = $${index + 3}`).join(', ');
    const values = fields.map(field => updates[field]);
    
    const query = `
      UPDATE monthly_goals 
      SET ${setClause}, updated_at = NOW()
      WHERE id = $1 AND user_id = $2
      RETURNING *
    `;
    
    const result = await db.query(query, [id, userId, ...values]);
    return result.rows[0];
  }

  // Delete goals
  static async delete(id, userId) {
    const query = 'DELETE FROM monthly_goals WHERE id = $1 AND user_id = $2 RETURNING *';
    const result = await db.query(query, [id, userId]);
    return result.rows[0];
  }

  // Get or create default goals for a month
  static async getOrCreateDefault(userId, year, month) {
    let goals = await this.findByMonth(userId, year, month);
    
    if (!goals) {
      goals = await this.upsert(userId, year, month, {});
    }
    
    return goals;
  }
}

module.exports = MonthlyGoal;
