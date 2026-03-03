import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

// 🚫 BLOCK protected requests if no token
API.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");

    // Allow auth routes without token
    if (config.url.startsWith("/auth")) {
      return config;
    }

    // Block everything else if token missing
    if (!token) {
      return Promise.reject({
        response: { status: 401, message: "No token" },
      });
    }

    config.headers.Authorization = `Bearer ${token}`;
    return config;
  },
  (error) => Promise.reject(error)
);

export default API;
