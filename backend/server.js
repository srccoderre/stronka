require('dotenv').config();
const express = require('express');
const helmet = require('helmet');
const cors = require('cors');
const cookieParser = require('cookie-parser');
const hpp = require('hpp');
const securityConfig = require('./config/security');
const { apiLimiter } = require('./middleware/rateLimiter');
const { errorHandler, notFoundHandler, logger } = require('./middleware/errorHandler');

// Import routes
const authRoutes = require('./routes/auth');
const dailyEntriesRoutes = require('./routes/dailyEntries');
const investmentsRoutes = require('./routes/investments');
const goalsRoutes = require('./routes/goals');

// Initialize Express app
const app = express();
const PORT = process.env.PORT || 4000;

// Security middleware
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https:"],
    },
  },
  crossOriginEmbedderPolicy: false,
}));

// CORS configuration
app.use(cors({
  origin: securityConfig.cors.origins,
  credentials: securityConfig.cors.credentials,
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
}));

// Body parser middleware
app.use(express.json({ limit: '10kb' }));
app.use(express.urlencoded({ extended: true, limit: '10kb' }));

// Cookie parser
app.use(cookieParser());

// Prevent parameter pollution
app.use(hpp());

// Rate limiting
app.use('/api/', apiLimiter);

// Logging middleware
app.use((req, res, next) => {
  logger.info(`${req.method} ${req.path} - ${req.ip}`);
  next();
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// API routes
app.use('/api/auth', authRoutes);
app.use('/api/daily-entries', dailyEntriesRoutes);
app.use('/api/investments', investmentsRoutes);
app.use('/api/goals', goalsRoutes);

// Serve static files (frontend)
app.use(express.static('frontend'));

// 404 handler
app.use(notFoundHandler);

// Global error handler
app.use(errorHandler);

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
  console.log(`📝 Environment: ${process.env.NODE_ENV || 'development'}`);
  console.log(`🔒 CORS enabled for: ${securityConfig.cors.origins.join(', ')}`);
});

// Handle unhandled promise rejections
process.on('unhandledRejection', (err) => {
  logger.error('Unhandled Rejection:', err);
  console.error('💥 UNHANDLED REJECTION! Shutting down...');
  process.exit(1);
});

// Handle uncaught exceptions
process.on('uncaughtException', (err) => {
  logger.error('Uncaught Exception:', err);
  console.error('💥 UNCAUGHT EXCEPTION! Shutting down...');
  process.exit(1);
});

module.exports = app;
