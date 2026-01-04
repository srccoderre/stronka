// API Module Exports
export { default as apiClient } from './client.js';
export { authAPI } from './auth.js';

// Entries API
import apiClient from './client.js';

export const entriesAPI = {
    async getAll(params = {}) {
        const query = new URLSearchParams(params).toString();
        return await apiClient.get(`/entries${query ? '?' + query : ''}`);
    },

    async getById(id) {
        return await apiClient.get(`/entries/${id}`);
    },

    async create(data) {
        return await apiClient.post('/entries', data);
    },

    async update(id, data) {
        return await apiClient.patch(`/entries/${id}`, data);
    },

    async delete(id) {
        return await apiClient.delete(`/entries/${id}`);
    }
};

// Investments API
export const investmentsAPI = {
    async getAll() {
        return await apiClient.get('/investments');
    },

    async getSummary() {
        return await apiClient.get('/investments/summary');
    },

    async getById(id) {
        return await apiClient.get(`/investments/${id}`);
    },

    async create(data) {
        return await apiClient.post('/investments', data);
    },

    async update(id, data) {
        return await apiClient.patch(`/investments/${id}`, data);
    },

    async delete(id) {
        return await apiClient.delete(`/investments/${id}`);
    }
};

// Goals API
export const goalsAPI = {
    async getMonthly(year, month) {
        return await apiClient.get(`/goals/monthly/${year}/${month}`);
    },

    async updateMonthly(year, month, data) {
        return await apiClient.put(`/goals/monthly/${year}/${month}`, data);
    },

    async getYearly(year) {
        return await apiClient.get(`/goals/yearly/${year}`);
    }
};

// Analytics API
export const analyticsAPI = {
    async getDashboard() {
        return await apiClient.get('/analytics/dashboard');
    },

    async getMonthly(year, month) {
        return await apiClient.get(`/analytics/monthly/${year}/${month}`);
    },

    async getAnnual(year) {
        return await apiClient.get(`/analytics/annual/${year}`);
    }
};

// Notifications API
export const notificationsAPI = {
    async getAll(unreadOnly = false, skip = 0, limit = 50) {
        const params = new URLSearchParams({ unread_only: unreadOnly, skip, limit });
        return await apiClient.get(`/notifications?${params}`);
    },

    async getUnreadCount() {
        return await apiClient.get('/notifications/unread/count');
    },

    async markAsRead(id) {
        return await apiClient.post(`/notifications/${id}/read`);
    },

    async markAllAsRead() {
        return await apiClient.post('/notifications/read-all');
    },

    async delete(id) {
        return await apiClient.delete(`/notifications/${id}`);
    }
};
