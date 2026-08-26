import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:6000';

const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const fetchSearchResults = async (query) => {
    const startTime = performance.now();
    const response = await apiClient.post('/search', { query });
    const endTime = performance.now();
    const duration = ((endTime - startTime) / 1000).toFixed(3);

    return {
        results: response.data.results || [],
        duration,
    };
};
