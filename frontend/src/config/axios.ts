// src/config/axios.ts
import axios from 'axios'

// The frontend is running on port 3000 but the API should be accessed through nginx on port 80
const baseURL = import.meta.env.VITE_API_URL || 'http://localhost'

export const api = axios.create({
  baseURL, // The API routes are already prefixed with /api in our Nginx config or .env
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
  },
  withCredentials: true,
})

export const csrf = axios.create({
  baseURL, // CSRF requests go to root
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
  },
  withCredentials: true,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 419) {
      await api.get('/sanctum/csrf-cookie')
      return api(error.config)
    }

    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }

    return Promise.reject(error)
  },
)

export default api
