import api from '@/lib/api'
import { AxiosError } from 'axios'

interface Resume {
  _id: string
  profile_id?: string
  user_id?: string
  original_filename: string
  file_type: string
  file_id: string
  created_at: string
  is_current: boolean
  parsed_content?: Record<string, any>
  file_size?: number
}

interface ResumeVersion {
  _id: string
  resume_id: string
  job_id: string
  version_name: string
  optimization_score: number
  optimized_content: Record<string, any>
  created_at: string
}

interface ResumeWithVersions extends Resume {
  versions: ResumeVersion[]
}

class ResumeService {
  /**
   * Get the current resume for the logged-in user
   */
  async getCurrentUserResume(): Promise<Resume | null> {
    try {
      const response = await api.get('/resumes/user/current')
      return response.data
    } catch (error: unknown) {
      if (error instanceof AxiosError && error.response?.status === 404) {
        return null
      }
      throw error
    }
  }

  /**
   * Get all resumes for the logged-in user
   */
  async getUserResumes(): Promise<Resume[]> {
    try {
      console.log('Fetching user resumes...')
      const response = await api.get('/resumes/user', {
        headers: {
          // Ensure content-type is set correctly for GET request
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
      })
      console.log('User resumes fetch successful:', response.data)
      return response.data
    } catch (error: unknown) {
      // Enhanced error logging for debugging
      if (error instanceof AxiosError) {
        console.error('Error fetching user resumes:', {
          status: error.response?.status,
          statusText: error.response?.statusText,
          data: error.response?.data,
          headers: error.response?.headers,
          config: {
            url: error.config?.url,
            method: error.config?.method,
            headers: error.config?.headers,
          },
        })
      } else {
        console.error('Unknown error fetching resumes:', error)
      }
      // Return empty array instead of throwing to avoid breaking the UI
      return []
    }
  }

  /**
   * Get the current resume for a profile
   */
  async getCurrentResume(profileId: string): Promise<Resume | null> {
    try {
      const response = await api.get(`/resumes/profile/${profileId}/current`)
      return response.data
    } catch (error: unknown) {
      if (error instanceof AxiosError && error.response?.status === 404) {
        return null
      }
      throw error
    }
  }

  /**
   * Get all resumes for a profile
   */
  async getResumes(profileId: string): Promise<Resume[]> {
    const response = await api.get(`/resumes/profile/${profileId}`)
    return response.data
  }

  /**
   * Get the number of resumes for the current user
   */
  async getUserResumeCount(): Promise<number> {
    try {
      const response = await api.get('/resumes/user/count')
      return response.data
    } catch (error) {
      console.error('Error fetching resume count:', error)
      return 0
    }
  }

  /**
   * Get a resume with all its versions
   */
  async getResumeWithVersions(resumeId: string): Promise<ResumeWithVersions> {
    const response = await api.get(`/resumes/${resumeId}`)
    return response.data
  }

  /**
   * Upload a new resume
   */
  async uploadResume(file: File, profileId?: string): Promise<Resume> {
    const formData = new FormData()
    formData.append('file', file)

    if (profileId) {
      formData.append('profile_id', profileId)
    }

    const response = await api.post('/resumes/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    return response.data
  }

  /**
   * Delete a resume
   */
  async deleteResume(resumeId: string): Promise<void> {
    await api.delete(`/resumes/${resumeId}`)
  }

  /**
   * Download a resume file
   */
  async downloadResume(resumeId: string): Promise<Blob> {
    const response = await api.get(`/resumes/${resumeId}/download`, {
      responseType: 'blob',
    })
    return response.data
  }

  /**
   * Create an optimized version of a resume for a specific job
   */
  async createResumeVersion(
    resumeId: string,
    jobId: string,
    optimizedContent: Record<string, any>,
    versionName?: string,
  ): Promise<ResumeVersion> {
    const response = await api.post(`/resumes/${resumeId}/versions`, {
      job_id: jobId,
      optimized_content: optimizedContent,
      version_name: versionName,
    })

    return response.data
  }
}

export const resumeService = new ResumeService()
export type { Resume, ResumeVersion, ResumeWithVersions }
