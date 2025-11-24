import axios from "axios";

const API_BASE_URL = "http://localhost:8000/";

export const apiClient = axios.create({
    baseURL: API_BASE_URL,
});

// Add authorization header automatically if token exists
apiClient.interceptors.request.use((config) => {
    const token = localStorage.getItem("access_token");

    if (token) {
        // Ensure headers exists and treat it as a flexible bag of values
        if (!config.headers) {
            config.headers = {} as any;
        }

        (config.headers as any).Authorization = `Bearer ${token}`;
    }

    return config;
});

export default apiClient;