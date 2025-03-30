import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/lib/api'
import type { AxiosError } from 'axios'
import { useRouter } from 'vue-router'
import { useProfileStore } from '@/stores/profile'

interface User {
  id: string
  email: string
  name: string
  created_at: string
  updated_at: string
}

interface LoginPayload {
  username: string
  password: string
}

interface RegisterPayload {
  name: string
  email: string
  password: string
}

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()
  const token = ref<string | null>(localStorage.getItem('token'))
  const user = ref<User | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Computed property to check if the user is authenticated
  const isAuthenticated = computed(() => !!token.value)

  // Initialize auth state
  function init() {
    const storedToken = localStorage.getItem('token')
    if (storedToken) {
      token.value = storedToken
      fetchUserData()
    }
  }

  // Login function
  async function login(credentials: LoginPayload): Promise<boolean> {
    loading.value = true
    error.value = null

    try {
      // Convert credentials to form data for OAuth2 password flow
      const formData = new URLSearchParams()
      formData.append('username', credentials.username)
      formData.append('password', credentials.password)

      const response = await api.post('/auth/login', formData.toString(), {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      })

      const { access_token } = response.data

      if (access_token) {
        // Store token in localStorage and state
        localStorage.setItem('token', access_token)
        token.value = access_token

        // Fetch user data
        await fetchUserData()
        return true
      }

      error.value = 'Invalid response from server'
      return false
    } catch (err) {
      const axiosError = err as AxiosError<{ detail: string }>
      error.value = axiosError.response?.data?.detail || 'An error occurred during login'
      console.error('Login error:', err)
      return false
    } finally {
      loading.value = false
    }
  }

  // Register function
  async function register(userData: RegisterPayload): Promise<boolean> {
    loading.value = true
    error.value = null

    try {
      await api.post('/auth/register', userData)
      return true
    } catch (err) {
      const axiosError = err as AxiosError<{ detail: string }>
      error.value = axiosError.response?.data?.detail || 'An error occurred during registration'
      console.error('Registration error:', err)
      return false
    } finally {
      loading.value = false
    }
  }

  // Fetch user data
  async function fetchUserData(): Promise<void> {
    if (!token.value) return

    loading.value = true
    error.value = null

    try {
      const response = await api.get('/auth/me')
      user.value = response.data
    } catch (err) {
      console.error('Error fetching user data:', err)
      const axiosError = err as AxiosError<{ detail: string }>
      error.value = axiosError.response?.data?.detail || 'Failed to fetch user data'
      // Only logout if token is invalid (401)
      if (axiosError.response?.status === 401) {
        logout(false) // Pass false to prevent redirect
      }
    } finally {
      loading.value = false
    }
  }

  // Logout function
  function logout(redirect: boolean = true): void {
    token.value = null
    user.value = null
    localStorage.removeItem('token')

    // Reset profile store
    const profileStore = useProfileStore()
    profileStore.resetProfile()

    // Redirect to login page if requested
    if (redirect && router) {
      router.push('/login')
    }
  }

  // Call init to set up auth state
  init()

  return {
    token,
    user,
    loading,
    error,
    isAuthenticated,
    login,
    register,
    fetchUserData,
    logout,
  }
})
