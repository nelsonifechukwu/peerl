/**
 * API Base URL Configuration
 * 
 * Development: Uses Vite proxy (/api → http://localhost:8000/api)
 * Production: Uses environment variable VITE_API_URL
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

export default API_BASE_URL;