const db = require('../config/db');
const bcrypt = require('bcrypt');
const securityConfig = require('../config/security');

class User {
  // Create a new user
  static async create(email, password) {
    const hashedPassword = await bcrypt.hash(password, securityConfig.bcrypt.rounds);
    
    const query = `
      INSERT INTO users (email, password_hash)
      VALUES ($1, $2)
      RETURNING id, email, created_at, is_active
    `;
    
    const result = await db.query(query, [email, hashedPassword]);
    return result.rows[0];
  }

  // Find user by email
  static async findByEmail(email) {
    const query = 'SELECT * FROM users WHERE email = $1';
    const result = await db.query(query, [email]);
    return result.rows[0];
  }

  // Find user by ID
  static async findById(id) {
    const query = 'SELECT id, email, created_at, updated_at, last_login, is_active FROM users WHERE id = $1';
    const result = await db.query(query, [id]);
    return result.rows[0];
  }

  // Verify password
  static async verifyPassword(plainPassword, hashedPassword) {
    return await bcrypt.compare(plainPassword, hashedPassword);
  }

  // Update last login
  static async updateLastLogin(userId) {
    const query = 'UPDATE users SET last_login = NOW() WHERE id = $1';
    await db.query(query, [userId]);
  }

  // Update user
  static async update(userId, updates) {
    const allowedFields = ['email'];
    const fields = Object.keys(updates).filter(key => allowedFields.includes(key));
    
    if (fields.length === 0) {
      return null;
    }

    const setClause = fields.map((field, index) => `${field} = $${index + 2}`).join(', ');
    const values = fields.map(field => updates[field]);
    
    const query = `
      UPDATE users 
      SET ${setClause}, updated_at = NOW()
      WHERE id = $1
      RETURNING id, email, updated_at
    `;
    
    const result = await db.query(query, [userId, ...values]);
    return result.rows[0];
  }

  // Deactivate user
  static async deactivate(userId) {
    const query = 'UPDATE users SET is_active = FALSE WHERE id = $1';
    await db.query(query, [userId]);
  }
}

module.exports = User;
