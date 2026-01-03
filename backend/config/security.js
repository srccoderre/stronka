require('dotenv').config();

module.exports = {
  jwt: {
    secret: process.env.JWT_SECRET || 'your-secret-key-change-in-production',
    refreshSecret: process.env.JWT_REFRESH_SECRET || 'your-refresh-secret-change-in-production',
    accessExpiry: process.env.JWT_ACCESS_EXPIRY || '15m',
    refreshExpiry: process.env.JWT_REFRESH_EXPIRY || '7d',
  },
  bcrypt: {
    rounds: parseInt(process.env.BCRYPT_ROUNDS) || 12,
  },
  cors: {
    origins: process.env.ALLOWED_ORIGINS ? process.env.ALLOWED_ORIGINS.split(',') : ['http://localhost:3000'],
    credentials: true,
  },
  rateLimit: {
    windowMs: parseInt(process.env.RATE_LIMIT_WINDOW_MS) || 15 * 60 * 1000, // 15 minutes
    maxRequests: parseInt(process.env.RATE_LIMIT_MAX_REQUESTS) || 100,
  },
};
