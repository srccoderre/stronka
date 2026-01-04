// Auth API
import apiClient from './client.js';

export const authAPI = {
    async register(userData) {
        return await apiClient.post('/auth/register', userData);
    },

    async login(credentials) {
        const data = await apiClient.post('/auth/login', credentials);
        if (data.access_token) {
            apiClient.setTokens(data.access_token, data.refresh_token);
        }
        return data;
    },

    async logout() {
        await apiClient.post('/auth/logout');
        apiClient.clearTokens();
    },

    async getMe() {
        return await apiClient.get('/auth/me');
    },

    async refresh(refreshToken) {
        return await apiClient.post('/auth/refresh', { refresh_token: refreshToken });
    }
};
