import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { resumeService, type Resume, type ResumeWithVersions } from '@/services/resumeService'

export const useResumeStore = defineStore('resume', () => {
  const masterResume = ref<Resume | null>(null)
  const allResumes = ref<Resume[]>([])
  const currentResumeWithVersions = ref<ResumeWithVersions | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const hasResume = computed(() => !!masterResume.value)

  /**
   * Fetch the current master resume for the user
   */
  async function fetchMasterResume() {
    loading.value = true
    error.value = null

    try {
      masterResume.value = await resumeService.getCurrentUserResume()
      return masterResume.value
    } catch (err) {
      error.value = 'Failed to load master resume'
      console.error(err)
      return null
    } finally {
      loading.value = false
    }
  }

  /**
   * Fetch all resumes for the user
   */
  async function fetchAllResumes() {
    loading.value = true
    error.value = null

    try {
      allResumes.value = await resumeService.getUserResumes()
      // Set the master resume as the current one
      if (Array.isArray(allResumes.value) && allResumes.value.length > 0) {
        masterResume.value = allResumes.value.find((resume) => resume.is_current) || null
      } else {
        masterResume.value = null
        allResumes.value = []
      }
      return allResumes.value
    } catch (err) {
      error.value = 'Failed to load resumes'
      console.error(err)
      allResumes.value = []
      masterResume.value = null
      return []
    } finally {
      loading.value = false
    }
  }

  /**
   * Fetch a specific resume with all its versions
   */
  async function fetchResumeWithVersions(resumeId: string) {
    loading.value = true
    error.value = null

    try {
      currentResumeWithVersions.value = await resumeService.getResumeWithVersions(resumeId)
      return currentResumeWithVersions.value
    } catch (err) {
      error.value = 'Failed to load resume with versions'
      console.error(err)
      return null
    } finally {
      loading.value = false
    }
  }

  /**
   * Upload a new resume (this becomes the master resume)
   */
  async function uploadResume(file: File, profileId?: string) {
    loading.value = true
    error.value = null

    try {
      const newResume = await resumeService.uploadResume(file, profileId)
      masterResume.value = newResume

      // Update the allResumes array with the new resume
      await fetchAllResumes()

      return newResume
    } catch (err) {
      error.value = 'Failed to upload resume'
      console.error(err)
      return null
    } finally {
      loading.value = false
    }
  }

  /**
   * Delete a resume
   */
  async function deleteResume(resumeId: string) {
    loading.value = true
    error.value = null

    try {
      await resumeService.deleteResume(resumeId)

      // If we deleted the master resume, set it to null
      if (masterResume.value && masterResume.value._id === resumeId) {
        masterResume.value = null
      }

      // Update the allResumes array
      await fetchAllResumes()

      return true
    } catch (err) {
      error.value = 'Failed to delete resume'
      console.error(err)
      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * Download a resume file
   */
  async function downloadResume(resumeId: string) {
    loading.value = true
    error.value = null

    try {
      const blob = await resumeService.downloadResume(resumeId)
      return blob
    } catch (err) {
      error.value = 'Failed to download resume'
      console.error(err)
      return null
    } finally {
      loading.value = false
    }
  }

  /**
   * Create an optimized version of a resume for a specific job
   */
  async function createResumeVersion(
    resumeId: string,
    jobId: string,
    optimizedContent: Record<string, any>,
    versionName?: string,
  ) {
    loading.value = true
    error.value = null

    try {
      const version = await resumeService.createResumeVersion(
        resumeId,
        jobId,
        optimizedContent,
        versionName,
      )

      // Refresh the current resume with versions
      if (currentResumeWithVersions.value && currentResumeWithVersions.value._id === resumeId) {
        await fetchResumeWithVersions(resumeId)
      }

      return version
    } catch (err) {
      error.value = 'Failed to create resume version'
      console.error(err)
      return null
    } finally {
      loading.value = false
    }
  }

  /**
   * Reset the store state
   */
  function resetResumes() {
    masterResume.value = null
    allResumes.value = []
    currentResumeWithVersions.value = null
    error.value = null
  }

  return {
    masterResume,
    allResumes,
    currentResumeWithVersions,
    loading,
    error,
    hasResume,
    fetchMasterResume,
    fetchAllResumes,
    fetchResumeWithVersions,
    uploadResume,
    deleteResume,
    downloadResume,
    createResumeVersion,
    resetResumes,
  }
})
