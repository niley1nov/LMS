// src/redux/apiService.js
// Optional: Centralized Axios instance
import axios from 'axios';

export const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'https://localhost:8000/api/v1';

const apiService = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true, // Send cookies with every request
});

// You can add interceptors here if needed (e.g., for error handling)
apiService.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle global errors or re-throw
    // console.error("API Error:", error.response || error.message);
    return Promise.reject(error);
  }
);

export default apiService;