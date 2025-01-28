import axios from "axios";
import nuxtStorage from "nuxt-storage";

const apiClient = axios.create({
  baseURL: "http://localhost:5432",
  timeout: 10000,
});

apiClient.interceptors.request.use((config) => {
  const token = nuxtStorage.localStorage.getData("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default apiClient;
