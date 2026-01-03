const jwt = require('jsonwebtoken');
const User = require('../models/User');
const db = require('../config/db');
const securityConfig = require('../config/security');
const { isValidEmail, isStrongPassword } = require('../utils/validators');

// Generate access token
const generateAccessToken = (userId, email) => {
  return jwt.sign(
    { userId, email },
    securityConfig.jwt.secret,
    { expiresIn: securityConfig.jwt.accessExpiry }
  );
};

// Generate refresh token
const generateRefreshToken = (userId, email) => {
  return jwt.sign(
    { userId, email },
    securityConfig.jwt.refreshSecret,
    { expiresIn: securityConfig.jwt.refreshExpiry }
  );
};

// Store refresh token in database
const storeRefreshToken = async (userId, token) => {
  const expiresAt = new Date();
  expiresAt.setDate(expiresAt.getDate() + 7); // 7 days

  const query = `
    INSERT INTO refresh_tokens (user_id, token, expires_at)
    VALUES ($1, $2, $3)
  `;
  
  await db.query(query, [userId, token, expiresAt]);
};

// Remove refresh token
const removeRefreshToken = async (token) => {
  const query = 'DELETE FROM refresh_tokens WHERE token = $1';
  await db.query(query, [token]);
};

// Register new user
exports.register = async (req, res, next) => {
  try {
    const { email, password } = req.body;

    // Validation
    if (!email || !password) {
      return res.status(400).json({ error: 'Email and password are required' });
    }

    if (!isValidEmail(email)) {
      return res.status(400).json({ error: 'Invalid email format' });
    }

    if (!isStrongPassword(password)) {
      return res.status(400).json({ 
        error: 'Password must be at least 8 characters with uppercase, lowercase, and number' 
      });
    }

    // Check if user exists
    const existingUser = await User.findByEmail(email);
    if (existingUser) {
      return res.status(409).json({ error: 'User already exists' });
    }

    // Create user
    const user = await User.create(email, password);

    // Generate tokens
    const accessToken = generateAccessToken(user.id, user.email);
    const refreshToken = generateRefreshToken(user.id, user.email);

    // Store refresh token
    await storeRefreshToken(user.id, refreshToken);

    // Set refresh token as HTTP-only cookie
    res.cookie('refreshToken', refreshToken, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict',
      maxAge: 7 * 24 * 60 * 60 * 1000, // 7 days
    });

    res.status(201).json({
      message: 'User registered successfully',
      user: {
        id: user.id,
        email: user.email,
      },
      accessToken,
    });
  } catch (error) {
    next(error);
  }
};

// Login user
exports.login = async (req, res, next) => {
  try {
    const { email, password } = req.body;

    // Validation
    if (!email || !password) {
      return res.status(400).json({ error: 'Email and password are required' });
    }

    // Find user
    const user = await User.findByEmail(email);
    if (!user) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    // Verify password
    const isValidPassword = await User.verifyPassword(password, user.password_hash);
    if (!isValidPassword) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    // Check if user is active
    if (!user.is_active) {
      return res.status(403).json({ error: 'Account is deactivated' });
    }

    // Update last login
    await User.updateLastLogin(user.id);

    // Generate tokens
    const accessToken = generateAccessToken(user.id, user.email);
    const refreshToken = generateRefreshToken(user.id, user.email);

    // Store refresh token
    await storeRefreshToken(user.id, refreshToken);

    // Set refresh token as HTTP-only cookie
    res.cookie('refreshToken', refreshToken, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict',
      maxAge: 7 * 24 * 60 * 60 * 1000,
    });

    res.json({
      message: 'Login successful',
      user: {
        id: user.id,
        email: user.email,
      },
      accessToken,
    });
  } catch (error) {
    next(error);
  }
};

// Refresh access token
exports.refresh = async (req, res, next) => {
  try {
    const { refreshToken } = req.cookies;

    if (!refreshToken) {
      return res.status(401).json({ error: 'Refresh token required' });
    }

    // Verify refresh token
    jwt.verify(refreshToken, securityConfig.jwt.refreshSecret, async (err, decoded) => {
      if (err) {
        return res.status(403).json({ error: 'Invalid refresh token' });
      }

      // Check if token exists in database
      const query = 'SELECT * FROM refresh_tokens WHERE token = $1 AND expires_at > NOW()';
      const result = await db.query(query, [refreshToken]);

      if (result.rows.length === 0) {
        return res.status(403).json({ error: 'Refresh token expired or invalid' });
      }

      // Generate new access token
      const accessToken = generateAccessToken(decoded.userId, decoded.email);

      res.json({ accessToken });
    });
  } catch (error) {
    next(error);
  }
};

// Logout user
exports.logout = async (req, res, next) => {
  try {
    const { refreshToken } = req.cookies;

    if (refreshToken) {
      await removeRefreshToken(refreshToken);
    }

    res.clearCookie('refreshToken');
    res.json({ message: 'Logout successful' });
  } catch (error) {
    next(error);
  }
};

// Get current user
exports.me = async (req, res, next) => {
  try {
    const user = await User.findById(req.user.userId);
    
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    res.json({ user });
  } catch (error) {
    next(error);
  }
};
