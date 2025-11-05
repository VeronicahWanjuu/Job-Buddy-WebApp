/**
 * API Service for JobBuddy Frontend
 * 
 * This module provides all API communication functions with the backend.
 * It handles authentication tokens, error handling, and request/response formatting.
 */

import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api/v1';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Add response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear token and redirect to login
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

/**
 * Authentication API calls
 */
export const authAPI = {
  register: (email, password, name) =>
    api.post('/auth/register', { email, password, name }),
  
  login: (email, password) =>
    api.post('/auth/login', { email, password }),
  
  logout: () =>
    api.post('/auth/logout'),
  
  passwordRecovery: (email) =>
    api.post('/auth/password-recovery', { email }),
};

/**
 * Profile API calls
 */
export const profileAPI = {
  getProfile: () =>
    api.get('/profile'),
  
  updateProfile: (data) =>
    api.put('/profile', data),
  
  changePassword: (currentPassword, newPassword) =>
    api.put('/profile/password', { current_password: currentPassword, new_password: newPassword }),
  
  deleteAccount: () =>
    api.delete('/profile'),
};

/**
 * Onboarding API calls
 */
export const onboardingAPI = {
  createOnboarding: (data) =>
    api.post('/onboarding', data),
  
  getOnboarding: () =>
    api.get('/onboarding'),
};

/**
 * Companies API calls
 */
export const companiesAPI = {
  listCompanies: (params) =>
    api.get('/companies', { params }),
  
  createCompany: (data) =>
    api.post('/companies', data),
  
  getCompany: (id) =>
    api.get(`/companies/${id}`),
  
  updateCompany: (id, data) =>
    api.put(`/companies/${id}`, data),
  
  deleteCompany: (id) =>
    api.delete(`/companies/${id}`),
};

/**
 * Contacts API calls
 */
export const contactsAPI = {
  listContacts: (params) =>
    api.get('/contacts', { params }),
  
  createContact: (data) =>
    api.post('/contacts', data),
  
  discoverContacts: (data) =>
    api.post('/contacts/discover', data),
  
  updateContact: (id, data) =>
    api.put(`/contacts/${id}`, data),
  
  deleteContact: (id) =>
    api.delete(`/contacts/${id}`),
};

/**
 * Applications API calls
 */
export const applicationsAPI = {
  listApplications: (params) =>
    api.get('/applications', { params }),
  
  createApplication: (data) =>
    api.post('/applications', data),
  
  getApplication: (id) =>
    api.get(`/applications/${id}`),
  
  updateApplication: (id, data) =>
    api.put(`/applications/${id}`, data),
  
  deleteApplication: (id) =>
    api.delete(`/applications/${id}`),
  
  bulkUpload: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/applications/bulk-upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
};

/**
 * Goals API calls
 */
export const goalsAPI = {
  getCurrentGoal: () =>
    api.get('/goals/current'),
  
  setGoal: (data) =>
    api.post('/goals', data),
  
  getStreak: () =>
    api.get('/goals/streak'),
  
  getMicroQuests: () =>
    api.get('/goals/micro-quests'),
  
  completeMicroQuest: (questId) =>
    api.post(`/goals/micro-quests/${questId}/complete`),
};

/**
 * Notifications API calls
 */
export const notificationsAPI = {
  listNotifications: (params) =>
    api.get('/notifications', { params }),
  
  markAsRead: (id) =>
    api.put(`/notifications/${id}/read`),
  
  markAllAsRead: () =>
    api.put('/notifications/read-all'),
  
  deleteNotification: (id) =>
    api.delete(`/notifications/${id}`),
};

export default api;
