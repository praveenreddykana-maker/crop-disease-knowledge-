// API configuration and axios instance
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000,
  headers: { 'Content-Type': 'application/json' },
});

// Attach admin token if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('adminToken');
  if (token) {
    config.headers['x-admin-token'] = token;
  }
  return config;
});

// Chat API
export const chatAPI = {
  sendMessage: (question, conversationId = null) =>
    api.post('/api/chat/', { question, conversation_id: conversationId }),

  getHistory: () => api.get('/api/chat/history'),

  searchHistory: (query) => api.get('/api/chat/history/search', { params: { q: query } }),

  getConversation: (id) => api.get(`/api/chat/history/${id}`),

  deleteConversation: (id) => api.delete(`/api/chat/history/${id}`),

  clearAllHistory: () => api.delete('/api/chat/history'),
};

// Crops API
export const cropsAPI = {
  getCrops: () => api.get('/api/crops/'),
  getCropDiseases: (crop) => api.get(`/api/crops/${crop}/diseases`),
};

// Documents API
export const documentsAPI = {
  uploadDocument: (file, adminToken) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/api/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        'x-admin-token': adminToken,
      },
    });
  },

  getDocuments: (adminToken) =>
    api.get('/api/documents/', { headers: { 'x-admin-token': adminToken } }),

  deleteDocument: (id, adminToken) =>
    api.delete(`/api/documents/${id}`, { headers: { 'x-admin-token': adminToken } }),

  getStats: (adminToken) =>
    api.get('/api/documents/stats/knowledge-base', {
      headers: { 'x-admin-token': adminToken },
    }),
};

// Admin API
export const adminAPI = {
  login: (password) => api.post('/api/admin/login', { password }),
  health: () => api.get('/api/admin/health'),
};

export default api;

