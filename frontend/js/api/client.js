// API Client Base
const API_BASE_URL = '/api/v1';

class APIClient {
    constructor() {
        this.baseURL = API_BASE_URL;
        this.accessToken = localStorage.getItem('accessToken');
        this.refreshToken = localStorage.getItem('refreshToken');
    }

    setTokens(accessToken, refreshToken) {
        this.accessToken = accessToken;
        this.refreshToken = refreshToken;
        localStorage.setItem('accessToken', accessToken);
        localStorage.setItem('refreshToken', refreshToken);
    }

    clearTokens() {
        this.accessToken = null;
        this.refreshToken = null;
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers,
        };

        if (this.accessToken) {
            headers['Authorization'] = `Bearer ${this.accessToken}`;
        }

        const config = {
            ...options,
            headers,
        };

        if (options.body && typeof options.body !== 'string') {
            config.body = JSON.stringify(options.body);
        }

        try {
            const response = await fetch(url, config);
            
            if (response.status === 401 && this.refreshToken) {
                // Try to refresh token
                const refreshed = await this.refreshAccessToken();
                if (refreshed) {
                    // Retry original request
                    headers['Authorization'] = `Bearer ${this.accessToken}`;
                    const retryResponse = await fetch(url, config);
                    return await this.handleResponse(retryResponse);
                }
            }

            return await this.handleResponse(response);
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    async handleResponse(response) {
        const data = await response.json().catch(() => ({}));
        
        if (!response.ok) {
            throw new Error(data.detail || `HTTP error! status: ${response.status}`);
        }
        
        return data;
    }

    async refreshAccessToken() {
        try {
            const response = await fetch(`${this.baseURL}/auth/refresh`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ refresh_token: this.refreshToken }),
            });

            if (response.ok) {
                const data = await response.json();
                this.setTokens(data.access_token, data.refresh_token);
                return true;
            }
        } catch (error) {
            console.error('Token refresh failed:', error);
        }
        
        this.clearTokens();
        return false;
    }

    get(endpoint, options = {}) {
        return this.request(endpoint, { ...options, method: 'GET' });
    }

    post(endpoint, data, options = {}) {
        return this.request(endpoint, { ...options, method: 'POST', body: data });
    }

    patch(endpoint, data, options = {}) {
        return this.request(endpoint, { ...options, method: 'PATCH', body: data });
    }

    put(endpoint, data, options = {}) {
        return this.request(endpoint, { ...options, method: 'PUT', body: data });
    }

    delete(endpoint, options = {}) {
        return this.request(endpoint, { ...options, method: 'DELETE' });
    }
}

// Export singleton instance
const apiClient = new APIClient();
export default apiClient;
