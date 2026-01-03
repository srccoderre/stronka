// Input validators
const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

const isValidDate = (dateString) => {
  const date = new Date(dateString);
  return date instanceof Date && !isNaN(date);
};

const isValidMonth = (month) => {
  const m = parseInt(month);
  return !isNaN(m) && m >= 0 && m <= 11;
};

const isValidYear = (year) => {
  const y = parseInt(year);
  return !isNaN(y) && y >= 2000 && y <= 2100;
};

const isValidAmount = (amount) => {
  const a = parseFloat(amount);
  return !isNaN(a) && a >= 0;
};

const isValidInvestmentType = (type) => {
  const validTypes = ['gold', 'silver', 'stocks', 'bonds', 'crypto', 'etf', 'other'];
  return validTypes.includes(type);
};

const isStrongPassword = (password) => {
  // At least 8 characters, 1 uppercase, 1 lowercase, 1 number
  const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;
  return passwordRegex.test(password);
};

module.exports = {
  isValidEmail,
  isValidDate,
  isValidMonth,
  isValidYear,
  isValidAmount,
  isValidInvestmentType,
  isStrongPassword,
};
