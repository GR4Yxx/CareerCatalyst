import { defineStore } from 'pinia'
import api, { csrf } from '@/config/axios'
import type { AxiosError } from 'axios'

interface User {
  id: number
  username: string
  first_name?: string
  last_name?: string
  primary_email: string
  email_verified_at?: Date
  password: string
  remember_token?: string
  avatar_path?: string
  phone?: string
  bio?: string
  role: 'regular' | 'organizer' | 'admin'
  company_name?: string
  company_logo_path?: string
  preferred_timezone?: string
  subscription_plan?: string
  subscription_ends_at?: Date
  last_login_at?: Date
  is_active: boolean
  two_factor_enabled: boolean
  two_factor_secret?: string
  created_at: Date
  updated_at: Date
  deleted_at?: Date
}

interface LoginCredentials {
  email: string
  password: string
  remember?: boolean
}

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    token: null,
    isAuthenticated: false,
  }),

  getters: {
    currentUser: (state) => state.user,
    isLoggedIn: (state) => state.isAuthenticated,
  },

  actions: {
    async login(credentials: LoginCredentials) {
      try {
        // Get CSRF cookie
        await csrf.get('/sanctum/csrf-cookie')

        // Attempt login
        const response = await api.post('/login', {
          email: credentials.email,
          password: credentials.password,
          remember: credentials.remember,
        })

        // Handle successful login
        const token = response.data.token
        if (token) {
          localStorage.setItem('token', token)
          this.token = token
        }

        // Update store state
        this.user = response.data.user
        this.isAuthenticated = true

        // Update last login if returned
        if (response.data.user?.last_login_at && this.user) {
          this.user.last_login_at = new Date(response.data.user.last_login_at)
        }

        return response.data
      } catch (error) {
        this.clearAuth()
        throw error
      }
    },

    async logout() {
      try {
        await api.post('/logout')
      } catch (error) {
        console.error('Logout error:', error)
      } finally {
        this.clearAuth()
      }
    },

    register: async (userData: {
      username: string
      first_name: string
      last_name: string
      primary_email: string
      password: string
      password_confirmation: string
      role: 'regular' | 'organizer' | 'admin'
    }) => {
      try {
        // Get CSRF cookie first, just like in login
        await csrf.get('/sanctum/csrf-cookie')

        const response = await api.post('/register', userData)
        return response.data
      } catch (error) {
        throw error
      }
    },

    clearAuth() {
      this.user = null
      this.token = null
      this.isAuthenticated = false
      localStorage.removeItem('token')
    },

    async checkAuth() {
      try {
        const token = localStorage.getItem('token')
        if (!token) return false

        const response = await api.get('/user')

        // Update store with user data
        this.user = response.data
        this.token = token
        this.isAuthenticated = true

        return true
      } catch (error) {
        console.error('Auth check failed:', error)
        this.clearAuth()
        return false
      }
    },

    async refreshUserData() {
      if (!this.isAuthenticated) return

      try {
        const response = await api.get('/user')
        this.user = response.data
      } catch (error) {
        console.error('Failed to refresh user data:', error)
        if ((error as AxiosError).response?.status === 401) {
          this.clearAuth()
        }
      }
    },
  },
})
