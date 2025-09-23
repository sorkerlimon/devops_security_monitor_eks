import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API endpoints
export const authAPI = {
  login: (credentials) => api.post('/auth/login-json', credentials),
  me: () => api.get('/auth/me'),
};

export const usersAPI = {
  register: (userData) => api.post('/users/register', userData),
  getUsers: () => api.get('/users/'),
  getUser: (id) => api.get(`/users/${id}`),
  updateUser: (id, userData) => api.put(`/users/${id}`, userData),
  deleteUser: (id) => api.delete(`/users/${id}`),
};

export const networkAPI = {
  getReports: (params) => api.get('/network', { params }),
  getReport: (id) => api.get(`/network/${id}`),
  getStats: (days = 30) => api.get('/network/stats/summary', { params: { days } }),
  deleteReport: (id) => api.delete(`/network/${id}`),
};

export const malwareAPI = {
  getReports: (params) => api.get('/malware', { params }),
  getReport: (id) => api.get(`/malware/${id}`),
  getStats: (days = 30) => api.get('/malware/stats/summary', { params: { days } }),
  getRecentActivity: (limit = 10) => api.get('/malware/recent/activity', { params: { limit } }),
  deleteReport: (id) => api.delete(`/malware/${id}`),
};

export const webAPI = {
  getReports: (params) => api.get('/web', { params }),
  getReport: (id) => api.get(`/web/${id}`),
  getStats: (days = 30) => api.get('/web/stats/summary', { params: { days } }),
  getRecentActivity: (limit = 10) => api.get('/web/recent/activity', { params: { limit } }),
  getTopDomains: (limit = 20, days = 30) => api.get('/web/domains/top', { params: { limit, days } }),
  blockDomain: (domain) => api.post('/web/block-domain', { domain }),
  whitelistDomain: (domain) => api.post('/web/whitelist-domain', { domain }),
  deleteReport: (id) => api.delete(`/web/${id}`),
};