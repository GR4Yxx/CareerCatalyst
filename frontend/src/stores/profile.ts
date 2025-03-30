import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/lib/api'
import type { AxiosError } from 'axios'

interface Education {
  id?: string
  institution: string
  degree: string
  field_of_study: string
  start_date: string
  end_date?: string
  current?: boolean
  description?: string
}

interface WorkExperience {
  id?: string
  company: string
  position: string
  start_date: string
  end_date?: string
  current?: boolean
  description?: string
  skills?: string[]
}

interface Skill {
  id?: string
  name: string
  level: 'beginner' | 'intermediate' | 'advanced' | 'expert'
  category?: string
}

interface Profile {
  id?: string
  user_id: string
  headline?: string
  summary?: string
  location?: string
  education: Education[]
  experience: WorkExperience[]
  skills: Skill[]
  avatar_url?: string
  resume_url?: string
}

export const useProfileStore = defineStore('profile', () => {
  const profile = ref<Profile | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Computed property to check if user has a profile
  const hasProfile = computed(() => !!profile.value)

  // Get user profile
  async function fetchProfile(): Promise<boolean> {
    loading.value = true
    error.value = null

    try {
      const response = await api.get('/user/profile')
      profile.value = response.data
      return true
    } catch (err) {
      const axiosError = err as AxiosError<{ detail: string }>
      error.value = axiosError.response?.data?.detail || 'Failed to fetch user profile'
      console.error('Profile fetch error:', err)
      return false
    } finally {
      loading.value = false
    }
  }

  // Create or update user profile
  async function updateProfile(profileData: Partial<Profile>): Promise<boolean> {
    loading.value = true
    error.value = null

    try {
      let response

      if (profile.value?.id) {
        // Update existing profile
        response = await api.put('/user/profile', profileData)
      } else {
        // Create new profile
        response = await api.post('/user/profile', profileData)
      }

      profile.value = response.data
      return true
    } catch (err) {
      const axiosError = err as AxiosError<{ detail: string }>
      error.value = axiosError.response?.data?.detail || 'Failed to update profile'
      console.error('Profile update error:', err)
      return false
    } finally {
      loading.value = false
    }
  }

  // Add education entry
  async function addEducation(educationData: Education): Promise<boolean> {
    loading.value = true
    error.value = null

    try {
      const response = await api.post('/user/education', educationData)

      if (!profile.value) await fetchProfile()
      else if (profile.value.education) {
        profile.value.education.push(response.data)
      }

      return true
    } catch (err) {
      const axiosError = err as AxiosError<{ detail: string }>
      error.value = axiosError.response?.data?.detail || 'Failed to add education'
      console.error('Add education error:', err)
      return false
    } finally {
      loading.value = false
    }
  }

  // Update education entry
  async function updateEducation(id: string, educationData: Education): Promise<boolean> {
    loading.value = true
    error.value = null

    try {
      const response = await api.put(`/user/education/${id}`, educationData)

      if (profile.value?.education) {
        const index = profile.value.education.findIndex((e) => e.id === id)
        if (index !== -1) {
          profile.value.education[index] = response.data
        }
      }

      return true
    } catch (err) {
      const axiosError = err as AxiosError<{ detail: string }>
      error.value = axiosError.response?.data?.detail || 'Failed to update education'
      console.error('Update education error:', err)
      return false
    } finally {
      loading.value = false
    }
  }

  // Delete education entry
  async function deleteEducation(id: string): Promise<boolean> {
    loading.value = true
    error.value = null

    try {
      await api.delete(`/user/education/${id}`)

      if (profile.value?.education) {
        profile.value.education = profile.value.education.filter((e) => e.id !== id)
      }

      return true
    } catch (err) {
      const axiosError = err as AxiosError<{ detail: string }>
      error.value = axiosError.response?.data?.detail || 'Failed to delete education'
      console.error('Delete education error:', err)
      return false
    } finally {
      loading.value = false
    }
  }

  // Add work experience
  async function addExperience(experienceData: WorkExperience): Promise<boolean> {
    loading.value = true
    error.value = null

    try {
      const response = await api.post('/user/experience', experienceData)

      if (!profile.value) await fetchProfile()
      else if (profile.value.experience) {
        profile.value.experience.push(response.data)
      }

      return true
    } catch (err) {
      const axiosError = err as AxiosError<{ detail: string }>
      error.value = axiosError.response?.data?.detail || 'Failed to add experience'
      console.error('Add experience error:', err)
      return false
    } finally {
      loading.value = false
    }
  }

  // Update work experience
  async function updateExperience(id: string, experienceData: WorkExperience): Promise<boolean> {
    loading.value = true
    error.value = null

    try {
      const response = await api.put(`/user/experience/${id}`, experienceData)

      if (profile.value?.experience) {
        const index = profile.value.experience.findIndex((e) => e.id === id)
        if (index !== -1) {
          profile.value.experience[index] = response.data
        }
      }

      return true
    } catch (err) {
      const axiosError = err as AxiosError<{ detail: string }>
      error.value = axiosError.response?.data?.detail || 'Failed to update experience'
      console.error('Update experience error:', err)
      return false
    } finally {
      loading.value = false
    }
  }

  // Delete work experience
  async function deleteExperience(id: string): Promise<boolean> {
    loading.value = true
    error.value = null

    try {
      await api.delete(`/user/experience/${id}`)

      if (profile.value?.experience) {
        profile.value.experience = profile.value.experience.filter((e) => e.id !== id)
      }

      return true
    } catch (err) {
      const axiosError = err as AxiosError<{ detail: string }>
      error.value = axiosError.response?.data?.detail || 'Failed to delete experience'
      console.error('Delete experience error:', err)
      return false
    } finally {
      loading.value = false
    }
  }

  // Add skill
  async function addSkill(skillData: Skill): Promise<boolean> {
    loading.value = true
    error.value = null

    try {
      const response = await api.post('/user/skill', skillData)

      if (!profile.value) await fetchProfile()
      else if (profile.value.skills) {
        profile.value.skills.push(response.data)
      }

      return true
    } catch (err) {
      const axiosError = err as AxiosError<{ detail: string }>
      error.value = axiosError.response?.data?.detail || 'Failed to add skill'
      console.error('Add skill error:', err)
      return false
    } finally {
      loading.value = false
    }
  }

  // Update skill
  async function updateSkill(id: string, skillData: Skill): Promise<boolean> {
    loading.value = true
    error.value = null

    try {
      const response = await api.put(`/user/skill/${id}`, skillData)

      if (profile.value?.skills) {
        const index = profile.value.skills.findIndex((s) => s.id === id)
        if (index !== -1) {
          profile.value.skills[index] = response.data
        }
      }

      return true
    } catch (err) {
      const axiosError = err as AxiosError<{ detail: string }>
      error.value = axiosError.response?.data?.detail || 'Failed to update skill'
      console.error('Update skill error:', err)
      return false
    } finally {
      loading.value = false
    }
  }

  // Delete skill
  async function deleteSkill(id: string): Promise<boolean> {
    loading.value = true
    error.value = null

    try {
      await api.delete(`/user/skill/${id}`)

      if (profile.value?.skills) {
        profile.value.skills = profile.value.skills.filter((s) => s.id !== id)
      }

      return true
    } catch (err) {
      const axiosError = err as AxiosError<{ detail: string }>
      error.value = axiosError.response?.data?.detail || 'Failed to delete skill'
      console.error('Delete skill error:', err)
      return false
    } finally {
      loading.value = false
    }
  }

  // Upload profile avatar
  async function uploadAvatar(file: File): Promise<boolean> {
    loading.value = true
    error.value = null

    try {
      const formData = new FormData()
      formData.append('avatar', file)

      const response = await api.post('/user/avatar', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      if (profile.value) {
        profile.value.avatar_url = response.data.avatar_url
      }

      return true
    } catch (err) {
      const axiosError = err as AxiosError<{ detail: string }>
      error.value = axiosError.response?.data?.detail || 'Failed to upload avatar'
      console.error('Avatar upload error:', err)
      return false
    } finally {
      loading.value = false
    }
  }

  // Upload resume
  async function uploadResume(file: File): Promise<boolean> {
    loading.value = true
    error.value = null

    try {
      const formData = new FormData()
      formData.append('resume', file)

      const response = await api.post('/user/resume', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      if (profile.value) {
        profile.value.resume_url = response.data.resume_url
      }

      return true
    } catch (err) {
      const axiosError = err as AxiosError<{ detail: string }>
      error.value = axiosError.response?.data?.detail || 'Failed to upload resume'
      console.error('Resume upload error:', err)
      return false
    } finally {
      loading.value = false
    }
  }

  // Reset profile state (used for logout)
  function resetProfile(): void {
    profile.value = null
    loading.value = false
    error.value = null
  }

  return {
    profile,
    loading,
    error,
    hasProfile,
    fetchProfile,
    updateProfile,
    addEducation,
    updateEducation,
    deleteEducation,
    addExperience,
    updateExperience,
    deleteExperience,
    addSkill,
    updateSkill,
    deleteSkill,
    uploadAvatar,
    uploadResume,
    resetProfile,
  }
})
