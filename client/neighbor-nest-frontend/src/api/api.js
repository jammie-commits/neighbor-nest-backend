import axios from 'axios';

const API_URL = 'http://localhost:5000'; //  backend URL

export const api = axios.create({
    baseURL: API_URL,
});

export const setAuthHeader = (token) => {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
};
