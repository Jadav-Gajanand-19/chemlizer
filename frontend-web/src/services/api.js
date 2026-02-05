import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Token ${token}`;
    }
    return config;
});

// API Service
const apiService = {
    // Authentication
    login: async (username, password) => {
        const response = await api.post('/auth/login/', { username, password });
        if (response.data.token) {
            localStorage.setItem('token', response.data.token);
            localStorage.setItem('username', response.data.username);
        }
        return response.data;
    },

    logout: () => {
        localStorage.removeItem('token');
        localStorage.removeItem('username');
    },

    isAuthenticated: () => {
        return !!localStorage.getItem('token');
    },

    getUsername: () => {
        return localStorage.getItem('username');
    },

    // CSV Upload
    uploadCSV: async (file) => {
        const formData = new FormData();
        formData.append('file', file);

        const response = await api.post('/upload/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    },

    // Get Equipment Data
    getData: async () => {
        const response = await api.get('/data/');
        return response.data;
    },

    // Get Summary Statistics
    getSummary: async () => {
        const response = await api.get('/summary/');
        return response.data;
    },

    // Get Upload History
    getHistory: async () => {
        const response = await api.get('/history/');
        return response.data;
    },

    // Download PDF Report
    downloadReport: async () => {
        const response = await api.get('/report/', {
            responseType: 'blob',
        });

        // Create download link
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `chemlizer_report_${Date.now()}.pdf`);
        document.body.appendChild(link);
        link.click();
        link.remove();

        return response.data;
    },
};

export default apiService;
