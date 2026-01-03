-- Mój Portfel 2026 - PostgreSQL Database Schema
-- Created: 2026-01-03

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop tables if exist (for clean install)
DROP TABLE IF EXISTS refresh_tokens CASCADE;
DROP TABLE IF EXISTS monthly_goals CASCADE;
DROP TABLE IF EXISTS investments CASCADE;
DROP TABLE IF EXISTS daily_entries CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- 1. Users Table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  last_login TIMESTAMP,
  is_active BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_users_email ON users(email);

-- 2. Daily Entries Table
CREATE TABLE daily_entries (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  income NUMERIC(10, 2) DEFAULT 0,
  expense NUMERIC(10, 2) DEFAULT 0,
  balance NUMERIC(10, 2) GENERATED ALWAYS AS (income - expense) STORED,
  category VARCHAR(100),
  notes TEXT,
  month INTEGER CHECK (month >= 0 AND month <= 11),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  CONSTRAINT unique_user_date UNIQUE(user_id, date)
);

CREATE INDEX idx_daily_entries_user_date ON daily_entries(user_id, date);
CREATE INDEX idx_daily_entries_month ON daily_entries(user_id, month);

-- 3. Investments Table
CREATE TABLE investments (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  type VARCHAR(50) CHECK (type IN ('gold', 'silver', 'stocks', 'bonds', 'crypto', 'etf', 'other')),
  amount NUMERIC(12, 4),
  price NUMERIC(10, 2),
  total NUMERIC(12, 2),
  notes TEXT,
  month INTEGER CHECK (month >= 0 AND month <= 11),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_investments_user_date ON investments(user_id, date);
CREATE INDEX idx_investments_type ON investments(user_id, type);

-- 4. Monthly Goals Table
CREATE TABLE monthly_goals (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  year INTEGER NOT NULL,
  month INTEGER CHECK (month >= 0 AND month <= 11),
  income_goal NUMERIC(10, 2) DEFAULT 20000,
  gold_goal NUMERIC(8, 2) DEFAULT 10,
  investments_goal NUMERIC(10, 2) DEFAULT 5100,
  silver_goal NUMERIC(10, 2) DEFAULT 500,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  CONSTRAINT unique_user_year_month UNIQUE(user_id, year, month)
);

CREATE INDEX idx_monthly_goals_user ON monthly_goals(user_id, year, month);

-- 5. Refresh Tokens Table (for JWT)
CREATE TABLE refresh_tokens (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  token VARCHAR(500) UNIQUE NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_refresh_tokens_user ON refresh_tokens(user_id);
CREATE INDEX idx_refresh_tokens_token ON refresh_tokens(token);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_daily_entries_updated_at BEFORE UPDATE ON daily_entries
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_investments_updated_at BEFORE UPDATE ON investments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_monthly_goals_updated_at BEFORE UPDATE ON monthly_goals
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert default monthly goals template (optional)
-- This can be used when a user first creates an account
-- INSERT INTO monthly_goals (user_id, year, month) VALUES (1, 2026, 0);
