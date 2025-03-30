import { api as axios } from '@/config/axios'
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
      const response = await axios.get('/resumes/user/current')
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
    const response = await axios.get('/resumes/user')
    return response.data
  }

  /**
   * Get the current resume for a profile
   */
  async getCurrentResume(profileId: string): Promise<Resume | null> {
    try {
      const response = await axios.get(`/resumes/profile/${profileId}/current`)
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
    const response = await axios.get(`/resumes/profile/${profileId}`)
    return response.data
  }

  /**
   * Get a resume with all its versions
   */
  async getResumeWithVersions(resumeId: string): Promise<ResumeWithVersions> {
    const response = await axios.get(`/resumes/${resumeId}`)
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

    const response = await axios.post('/resumes/upload', formData, {
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
    await axios.delete(`/resumes/${resumeId}`)
  }

  /**
   * Download a resume file
   */
  async downloadResume(resumeId: string): Promise<Blob> {
    const response = await axios.get(`/resumes/${resumeId}/download`, {
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
    const response = await axios.post(`/resumes/${resumeId}/versions`, {
      job_id: jobId,
      optimized_content: optimizedContent,
      version_name: versionName,
    })

    return response.data
  }
}

export const resumeService = new ResumeService()
export type { Resume, ResumeVersion, ResumeWithVersions }
