// API Client for Mój Portfel 2026
const API_URL = window.location.hostname === 'localhost' 
  ? 'http://localhost:4000/api' 
  : '/api';

class API {
  // Generic request method
  static async request(endpoint, options = {}) {
    const token = localStorage.getItem('accessToken');
    
    const config = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
        ...options.headers,
      },
      credentials: 'include', // Include cookies for refresh token
    };
    
    try {
      const response = await fetch(`${API_URL}${endpoint}`, config);
      
      // Token expired - try to refresh
      if (response.status === 401 && endpoint !== '/auth/refresh' && endpoint !== '/auth/login') {
        const refreshed = await this.refreshToken();
        if (refreshed) {
          // Retry the original request with new token
          return this.request(endpoint, options);
        } else {
          // Refresh failed - redirect to login
          this.logout();
          window.location.href = '/login.html';
          throw new Error('Session expired. Please login again.');
        }
      }
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error || 'Request failed');
      }
      
      return data;
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }
  
  // Refresh access token
  static async refreshToken() {
    try {
      const response = await fetch(`${API_URL}/auth/refresh`, {
        method: 'POST',
        credentials: 'include',
      });
      
      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('accessToken', data.accessToken);
        return true;
      }
      
      return false;
    } catch (error) {
      console.error('Token refresh failed:', error);
      return false;
    }
  }
  
  // Logout
  static async logout() {
    try {
      await fetch(`${API_URL}/auth/logout`, {
        method: 'POST',
        credentials: 'include',
      });
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('accessToken');
      localStorage.removeItem('userEmail');
    }
  }
  
  // GET request
  static async get(endpoint) {
    return this.request(endpoint, { method: 'GET' });
  }
  
  // POST request
  static async post(endpoint, data) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
  
  // PUT request
  static async put(endpoint, data) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }
  
  // DELETE request
  static async delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' });
  }
  
  // Auth endpoints
  static async login(email, password) {
    const data = await this.post('/auth/login', { email, password });
    localStorage.setItem('accessToken', data.accessToken);
    localStorage.setItem('userEmail', data.user.email);
    return data;
  }
  
  static async register(email, password) {
    const data = await this.post('/auth/register', { email, password });
    localStorage.setItem('accessToken', data.accessToken);
    localStorage.setItem('userEmail', data.user.email);
    return data;
  }
  
  static async getMe() {
    return this.get('/auth/me');
  }
  
  // Daily entries endpoints
  static async getDailyEntries(filters = {}) {
    const params = new URLSearchParams(filters);
    return this.get(`/daily-entries?${params}`);
  }
  
  static async getDailyEntry(id) {
    return this.get(`/daily-entries/${id}`);
  }
  
  static async createDailyEntry(data) {
    return this.post('/daily-entries', data);
  }
  
  static async updateDailyEntry(id, data) {
    return this.put(`/daily-entries/${id}`, data);
  }
  
  static async deleteDailyEntry(id) {
    return this.delete(`/daily-entries/${id}`);
  }
  
  static async getDailyStats(year, month) {
    return this.get(`/daily-entries/stats/${year}/${month}`);
  }
  
  // Investments endpoints
  static async getInvestments(filters = {}) {
    const params = new URLSearchParams(filters);
    return this.get(`/investments?${params}`);
  }
  
  static async getInvestment(id) {
    return this.get(`/investments/${id}`);
  }
  
  static async createInvestment(data) {
    return this.post('/investments', data);
  }
  
  static async updateInvestment(id, data) {
    return this.put(`/investments/${id}`, data);
  }
  
  static async deleteInvestment(id) {
    return this.delete(`/investments/${id}`);
  }
  
  static async getInvestmentStats(year, month) {
    return this.get(`/investments/stats/${year}/${month}`);
  }
  
  // Goals endpoints
  static async getGoals(filters = {}) {
    const params = new URLSearchParams(filters);
    return this.get(`/goals?${params}`);
  }
  
  static async getMonthGoals(year, month) {
    return this.get(`/goals/${year}/${month}`);
  }
  
  static async saveGoals(data) {
    return this.post('/goals', data);
  }
  
  static async updateGoals(id, data) {
    return this.put(`/goals/${id}`, data);
  }
  
  static async deleteGoals(id) {
    return this.delete(`/goals/${id}`);
  }
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
  module.exports = API;
}
