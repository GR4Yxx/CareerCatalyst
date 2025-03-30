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
    user: {
      id: 1,
      username: 'testuser',
      primary_email: 'test@example.com',
      password: '',
      role: 'regular',
      is_active: true,
      two_factor_enabled: false,
      created_at: new Date(),
      updated_at: new Date(),
    },
    token: 'dummy-token',
    isAuthenticated: true,
  }),

  getters: {
    currentUser: (state) => state.user,
    isLoggedIn: (state) => true,
  },

  actions: {
    async login(credentials: LoginCredentials) {
      // Simply return success without making any API calls
      return { user: this.user, token: this.token }
    },

    async logout() {
      // Do nothing - keep the user logged in
      return true
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
      // Simply return success without making any API calls
      return { success: true }
    },

    clearAuth() {
      // Do nothing - keep the user logged in
    },

    async checkAuth() {
      // Always return true
      return true
    },

    async refreshUserData() {
      // Do nothing - keep using the mock user data
      return true
    },
  },
})
