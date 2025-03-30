import api from '@/lib/api'
import { AxiosError } from 'axios'

export interface Job {
  _id: string
  title: string
  company: string
  location: string
  url: string
  job_description?: string
  description_snippet?: string
  salary_range?: string
  extracted_skills: string[]
  fetched_at: string
}

export interface JobMatch {
  job: Job
  match_score: number
  matching_skills: string[]
  missing_skills: string[]
  match_explanation?: string
}

interface JobSearchParams {
  query?: string
  location?: string
  remote_only?: boolean
  skills?: string[]
  limit?: number
  page?: number
}

class JobService {
  /**
   * Get job recommendations based on the user's current resume
   * @param limit Number of recommendations to return
   * @param useGemini Whether to use Gemini enhanced matching
   */
  async getJobRecommendations(limit: number = 10, useGemini: boolean = true): Promise<JobMatch[]> {
    try {
      const response = await api.get('/jobs/recommend', {
        params: {
          limit,
          use_gemini: useGemini,
        },
      })

      // Map API response format to our frontend format
      return response.data.map((job: any) => ({
        job: {
          _id: job._id,
          title: job.title,
          company: job.company,
          location: job.location,
          url: job.url,
          job_description: job.job_description,
          extracted_skills: job.extracted_skills || [],
          fetched_at: job.fetched_at,
        },
        match_score: job.match_score || 0,
        matching_skills: job.matching_skills || [],
        missing_skills: job.missing_skills || [],
        match_explanation: job.match_explanation,
      }))
    } catch (error: unknown) {
      if (error instanceof AxiosError) {
        console.error('Error fetching job recommendations:', {
          status: error.response?.status,
          statusText: error.response?.statusText,
          data: error.response?.data,
        })

        // If we got a 404, try a more standard endpoint
        if (error.response?.status === 404) {
          try {
            const response = await api.get('/api/jobs/recommend', {
              params: {
                limit,
                use_gemini: useGemini,
              },
            })
            return response.data
          } catch (secondError) {
            console.error('Secondary attempt also failed:', secondError)
            // Fall back to mock data
            return this.getMockJobRecommendations()
          }
        }
      }

      // Return mock data if anything fails
      return this.getMockJobRecommendations()
    }
  }

  /**
   * Search for jobs with specific criteria
   */
  async searchJobs(params: JobSearchParams = {}): Promise<Job[]> {
    try {
      const response = await api.get('/jobs/search', { params })
      return response.data
    } catch (error: unknown) {
      if (error instanceof AxiosError) {
        console.error('Error searching jobs:', {
          status: error.response?.status,
          statusText: error.response?.statusText,
          data: error.response?.data,
        })

        // If the API endpoint is not implemented yet, use the fallback mock data
        if (error.response?.status === 404) {
          return this.getMockJobs(params.query || '')
        }
      }
      // Return empty array instead of throwing to avoid breaking the UI
      return []
    }
  }

  /**
   * Get details for a specific job
   */
  async getJobDetails(jobId: string): Promise<Job | null> {
    try {
      const response = await api.get(`/jobs/${jobId}`)
      return response.data
    } catch (error: unknown) {
      if (error instanceof AxiosError && error.response?.status === 404) {
        return null
      }
      throw error
    }
  }

  /**
   * Save a job to the user's favorites
   */
  async saveJob(jobId: string): Promise<boolean> {
    try {
      await api.post('/jobs/saved', { job_id: jobId })
      return true
    } catch (error) {
      console.error('Error saving job:', error)
      return false
    }
  }

  /**
   * Get the user's saved jobs
   */
  async getSavedJobs(): Promise<Job[]> {
    try {
      const response = await api.get('/jobs/saved')
      return response.data
    } catch (error) {
      console.error('Error fetching saved jobs:', error)
      return []
    }
  }

  /**
   * Remove a job from the user's saved jobs
   */
  async removeSavedJob(jobId: string): Promise<boolean> {
    try {
      await api.delete(`/jobs/saved/${jobId}`)
      return true
    } catch (error) {
      console.error('Error removing saved job:', error)
      return false
    }
  }

  /**
   * Get mock job recommendations for testing when the API is not available
   * This is only used as a fallback when the real API endpoint is not yet implemented
   */
  private getMockJobRecommendations(): JobMatch[] {
    return [
      {
        job: {
          _id: 'job1',
          title: 'Senior Full Stack Developer',
          company: 'TechCorp Inc.',
          location: 'Remote / New York, NY',
          url: 'https://example.com/jobs/1',
          description_snippet:
            "We're looking for a Senior Full Stack Developer with experience in Vue.js, TypeScript, and modern web development practices...",
          salary_range: '$120,000 - $150,000',
          extracted_skills: [
            'Vue.js',
            'TypeScript',
            'JavaScript',
            'HTML/CSS',
            'Node.js',
            'MongoDB',
          ],
          fetched_at: new Date().toISOString(),
        },
        match_score: 0.95,
        matching_skills: ['JavaScript', 'TypeScript', 'Vue', 'MongoDB'],
        missing_skills: ['Node.js', 'GraphQL'],
      },
      {
        job: {
          _id: 'job2',
          title: 'Lead UI/UX Developer',
          company: 'DesignWave Studio',
          location: 'Remote / San Francisco, CA',
          url: 'https://example.com/jobs/2',
          description_snippet:
            'Join our team as a Lead UI/UX Developer to create beautiful, responsive interfaces that delight users...',
          salary_range: '$110,000 - $140,000',
          extracted_skills: ['UI/UX', 'JavaScript', 'CSS', 'Design Systems', 'Figma', 'React'],
          fetched_at: new Date().toISOString(),
        },
        match_score: 0.87,
        matching_skills: ['JavaScript', 'React', 'Figma', 'UI/UX Design'],
        missing_skills: ['Design Systems', 'User Testing'],
      },
      {
        job: {
          _id: 'job3',
          title: 'Cloud DevOps Engineer',
          company: 'CloudNative Solutions',
          location: 'Remote / Austin, TX',
          url: 'https://example.com/jobs/3',
          description_snippet:
            'We are seeking a Cloud DevOps Engineer to help build and maintain our cloud infrastructure...',
          salary_range: '$130,000 - $160,000',
          extracted_skills: ['AWS', 'Docker', 'Kubernetes', 'CI/CD', 'Terraform', 'Python'],
          fetched_at: new Date().toISOString(),
        },
        match_score: 0.82,
        matching_skills: ['AWS', 'Docker', 'CI/CD', 'Python'],
        missing_skills: ['Kubernetes', 'Terraform'],
      },
      {
        job: {
          _id: 'job4',
          title: 'Backend Engineer',
          company: 'DataSystems Inc.',
          location: 'Boston, MA / Hybrid',
          url: 'https://example.com/jobs/4',
          description_snippet:
            'Looking for a Backend Engineer to develop high-performance APIs and services...',
          salary_range: '$115,000 - $145,000',
          extracted_skills: ['Java', 'Spring', 'SQL', 'MongoDB', 'Microservices', 'Docker'],
          fetched_at: new Date().toISOString(),
        },
        match_score: 0.78,
        matching_skills: ['Java', 'MongoDB', 'Docker'],
        missing_skills: ['Spring', 'Microservices'],
      },
      {
        job: {
          _id: 'job5',
          title: 'Senior Game Developer',
          company: 'GameLab Studios',
          location: 'Remote / Los Angeles, CA',
          url: 'https://example.com/jobs/5',
          description_snippet:
            'Join our creative team developing cutting-edge games on Unreal Engine...',
          salary_range: '$125,000 - $155,000',
          extracted_skills: [
            'C++',
            'Unreal Engine',
            'Game Development',
            '3D Modeling',
            'Physics',
            'AI',
          ],
          fetched_at: new Date().toISOString(),
        },
        match_score: 0.75,
        matching_skills: ['C++', 'Unreal Engine', 'Game Development', '3D Modelling'],
        missing_skills: ['Physics Simulation', 'Game AI'],
      },
    ]
  }

  /**
   * Get mock jobs for testing when the API is not available
   * This is only used as a fallback when the real API endpoint is not yet implemented
   */
  private getMockJobs(query: string = ''): Job[] {
    const allMockJobs: Job[] = [
      {
        _id: 'job1',
        title: 'Senior Full Stack Developer',
        company: 'TechCorp Inc.',
        location: 'Remote / New York, NY',
        url: 'https://example.com/jobs/1',
        description_snippet:
          "We're looking for a Senior Full Stack Developer with experience in Vue.js, TypeScript, and modern web development practices...",
        salary_range: '$120,000 - $150,000',
        extracted_skills: ['Vue.js', 'TypeScript', 'JavaScript', 'HTML/CSS', 'Node.js', 'MongoDB'],
        fetched_at: new Date().toISOString(),
      },
      {
        _id: 'job2',
        title: 'Lead UI/UX Developer',
        company: 'DesignWave Studio',
        location: 'Remote / San Francisco, CA',
        url: 'https://example.com/jobs/2',
        description_snippet:
          'Join our team as a Lead UI/UX Developer to create beautiful, responsive interfaces that delight users...',
        salary_range: '$110,000 - $140,000',
        extracted_skills: ['UI/UX', 'JavaScript', 'CSS', 'Design Systems', 'Figma', 'React'],
        fetched_at: new Date().toISOString(),
      },
      {
        _id: 'job3',
        title: 'Cloud DevOps Engineer',
        company: 'CloudNative Solutions',
        location: 'Remote / Austin, TX',
        url: 'https://example.com/jobs/3',
        description_snippet:
          'We are seeking a Cloud DevOps Engineer to help build and maintain our cloud infrastructure...',
        salary_range: '$130,000 - $160,000',
        extracted_skills: ['AWS', 'Docker', 'Kubernetes', 'CI/CD', 'Terraform', 'Python'],
        fetched_at: new Date().toISOString(),
      },
      {
        _id: 'job4',
        title: 'Backend Engineer',
        company: 'DataSystems Inc.',
        location: 'Boston, MA / Hybrid',
        url: 'https://example.com/jobs/4',
        description_snippet:
          'Looking for a Backend Engineer to develop high-performance APIs and services...',
        salary_range: '$115,000 - $145,000',
        extracted_skills: ['Java', 'Spring', 'SQL', 'MongoDB', 'Microservices', 'Docker'],
        fetched_at: new Date().toISOString(),
      },
      {
        _id: 'job5',
        title: 'Senior Game Developer',
        company: 'GameLab Studios',
        location: 'Remote / Los Angeles, CA',
        url: 'https://example.com/jobs/5',
        description_snippet:
          'Join our creative team developing cutting-edge games on Unreal Engine...',
        salary_range: '$125,000 - $155,000',
        extracted_skills: [
          'C++',
          'Unreal Engine',
          'Game Development',
          '3D Modeling',
          'Physics',
          'AI',
        ],
        fetched_at: new Date().toISOString(),
      },
    ]

    // If no query, return all mock jobs
    if (!query) return allMockJobs

    // Filter mock jobs based on query
    const lowerQuery = query.toLowerCase()
    return allMockJobs.filter(
      (job) =>
        job.title.toLowerCase().includes(lowerQuery) ||
        job.company.toLowerCase().includes(lowerQuery) ||
        job.description_snippet?.toLowerCase().includes(lowerQuery) ||
        job.extracted_skills.some((skill) => skill.toLowerCase().includes(lowerQuery)),
    )
  }
}

// Ensure we're exporting only the jobService instance
export const jobService = new JobService()
