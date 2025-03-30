<template>
  <div class="skills-view">
    <h1 class="text-2xl font-bold mb-6 flex items-center">
      <Sparkles class="h-7 w-7 mr-3 text-primary" />
      Skills Intelligence
    </h1>

    <!-- Main loading indicator -->
    <div v-if="loading" class="flex flex-col items-center justify-center my-8 space-y-4">
      <div class="animate-spin h-8 w-8 text-primary">
        <Loader2 />
      </div>
      <p class="text-muted-foreground">Loading your skills data...</p>
    </div>

    <div v-else>
      <!-- Resume Upload and Analysis Section -->
      <div class="mb-8">
        <div class="p-6 bg-card rounded-lg border shadow-sm">
          <h2 class="text-xl font-semibold mb-4">Skills Extraction and Analysis</h2>
          <p class="mb-4">
            Extract, categorize, and contextualize skills from your resume. Understand how your
            skills align with job market demands.
          </p>

          <div v-if="!currentResume">
            <p class="mb-4">
              Upload your resume to get started with a comprehensive analysis of your skillset.
            </p>
            <Button @click="navigateToResumes" class="mt-2">Upload Resume</Button>
          </div>

          <div v-else>
            <p class="mb-4">
              Current resume: <span class="font-medium">{{ currentResume.original_filename }}</span>
            </p>

            <div class="flex gap-4 mt-4">
              <Button
                v-if="!userSkills || !userSkills.skills || userSkills.skills.length === 0"
                @click="analyzeResume"
                :disabled="analyzing"
                class="relative"
              >
                <div v-if="analyzing" class="flex items-center">
                  <Loader2 class="h-4 w-4 mr-2 animate-spin" />
                  <span>Analyzing...</span>
                </div>
                <span v-else>Analyze Skills</span>
              </Button>
              <Button
                v-if="userSkills && userSkills.skills && userSkills.skills.length > 0"
                @click="analyzeResume"
                variant="outline"
                :disabled="analyzing"
                class="relative"
              >
                <div v-if="analyzing" class="flex items-center">
                  <Loader2 class="h-4 w-4 mr-2 animate-spin" />
                  <span>Analyzing...</span>
                </div>
                <span v-else>Re-analyze Skills</span>
              </Button>
            </div>
          </div>
        </div>
      </div>

      <!-- Analysis in progress indicator -->
      <div v-if="analyzing" class="my-6 p-4 bg-muted rounded-lg border flex items-center">
        <Loader2 class="h-5 w-5 mr-3 animate-spin text-primary" />
        <div>
          <p class="font-medium">AI Analysis in Progress</p>
          <p class="text-sm text-muted-foreground">
            Our AI is analyzing your resume. This may take up to a minute...
          </p>
        </div>
      </div>

      <!-- Skills Display Section -->
      <div v-if="userSkills && userSkills.skills && userSkills.skills.length > 0">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Technical Skills -->
          <div class="p-6 bg-card rounded-lg border shadow-sm">
            <h3 class="text-lg font-semibold mb-3">Technical Skills</h3>
            <p class="text-sm text-muted-foreground mb-4">
              Your technical competencies and hard skills
            </p>
            <div v-if="technicalSkills.length > 0" class="flex flex-wrap gap-2">
              <Badge
                v-for="skill in technicalSkills"
                :key="skill.name"
                :class="getConfidenceClass(skill.confidence)"
              >
                {{ skill.name }}
              </Badge>
            </div>
            <p v-else class="text-sm text-muted-foreground">No technical skills identified</p>
          </div>

          <!-- Soft Skills -->
          <div class="p-6 bg-card rounded-lg border shadow-sm">
            <h3 class="text-lg font-semibold mb-3">Soft Skills</h3>
            <p class="text-sm text-muted-foreground mb-4">
              Your interpersonal and transferable skills
            </p>
            <div v-if="softSkills.length > 0" class="flex flex-wrap gap-2">
              <Badge
                v-for="skill in softSkills"
                :key="skill.name"
                variant="outline"
                :class="getConfidenceClass(skill.confidence)"
              >
                {{ skill.name }}
              </Badge>
            </div>
            <p v-else class="text-sm text-muted-foreground">No soft skills identified</p>
          </div>
        </div>

        <!-- Domain Knowledge -->
        <div class="mt-6 p-6 bg-card rounded-lg border shadow-sm">
          <h3 class="text-lg font-semibold mb-3">Domain Knowledge</h3>
          <p class="text-sm text-muted-foreground mb-4">
            Your industry-specific expertise and knowledge areas
          </p>
          <div v-if="domainSkills.length > 0" class="flex flex-wrap gap-2">
            <Badge
              v-for="skill in domainSkills"
              :key="skill.name"
              variant="secondary"
              :class="getConfidenceClass(skill.confidence)"
            >
              {{ skill.name }}
            </Badge>
          </div>
          <p v-else class="text-sm text-muted-foreground">No domain knowledge identified</p>
        </div>

        <!-- Certifications -->
        <div class="mt-6 p-6 bg-card rounded-lg border shadow-sm">
          <h3 class="text-lg font-semibold mb-3">Certifications</h3>
          <p class="text-sm text-muted-foreground mb-4">
            Your professional certifications and qualifications
          </p>
          <div v-if="certifications.length > 0" class="flex flex-wrap gap-2">
            <Badge
              v-for="cert in certifications"
              :key="cert.name"
              variant="destructive"
              :class="getConfidenceClass(cert.confidence)"
            >
              {{ cert.name }}
            </Badge>
          </div>
          <p v-else class="text-sm text-muted-foreground">No certifications identified</p>
        </div>
      </div>

      <!-- No Skills Yet Message -->
      <div
        v-else-if="
          currentResume && (!userSkills || !userSkills.skills || userSkills.skills.length === 0)
        "
        class="p-6 bg-card rounded-lg border shadow-sm mt-6"
      >
        <h3 class="text-lg font-semibold mb-3">No Skills Analyzed Yet</h3>
        <p class="text-sm text-muted-foreground mb-4">
          Click the "Analyze Skills" button to extract skills from your resume.
        </p>
      </div>

      <!-- No Resume Message -->
      <div v-else-if="!currentResume" class="p-6 bg-card rounded-lg border shadow-sm mt-6">
        <h3 class="text-lg font-semibold mb-3">No Resume Uploaded</h3>
        <p class="text-sm text-muted-foreground mb-4">
          Please upload a resume to analyze your skills.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Sparkles, Loader2 } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/components/ui/toast/use-toast'
import api from '@/lib/api'

interface Skill {
  id?: string
  name: string
  category: 'technical' | 'soft' | 'domain' | 'certification'
  confidence: number
  level?: string
  description?: string
}

interface UserSkill {
  id?: string
  user_id?: string
  profile_id?: string
  resume_id: string
  skills: Skill[]
  created_at: string
  updated_at: string
}

interface Resume {
  id: string
  original_filename: string
  file_type: string
  created_at: string
  is_current: boolean
}

const router = useRouter()
const authStore = useAuthStore()
const { toast } = useToast()

const loading = ref(true)
const analyzing = ref(false)
const currentResume = ref<Resume | null>(null)
const currentResumeLoading = ref(false)
const userSkills = ref<UserSkill | null>(null)
const userSkillsLoading = ref(false)
const error = ref<string | null>(null)

const technicalSkills = computed(() => {
  if (!userSkills.value || !userSkills.value.skills) return []
  return userSkills.value.skills
    .filter((skill) => skill.category === 'technical')
    .sort((a, b) => b.confidence - a.confidence)
})

const softSkills = computed(() => {
  if (!userSkills.value || !userSkills.value.skills) return []
  return userSkills.value.skills
    .filter((skill) => skill.category === 'soft')
    .sort((a, b) => b.confidence - a.confidence)
})

const domainSkills = computed(() => {
  if (!userSkills.value || !userSkills.value.skills) return []
  return userSkills.value.skills
    .filter((skill) => skill.category === 'domain')
    .sort((a, b) => b.confidence - a.confidence)
})

const certifications = computed(() => {
  if (!userSkills.value || !userSkills.value.skills) return []
  return userSkills.value.skills
    .filter((skill) => skill.category === 'certification')
    .sort((a, b) => b.confidence - a.confidence)
})

// Confidence level styling
const getConfidenceClass = (confidence: number) => {
  if (confidence >= 0.9) return 'border-green-400'
  if (confidence >= 0.7) return 'border-yellow-400'
  return 'border-gray-400'
}

const fetchCurrentResume = async () => {
  currentResumeLoading.value = true

  try {
    console.log('Fetching current resume...')
    const response = await api.get('/resumes/user/current')
    console.log('Current resume raw response:', response.data)

    if (response.data) {
      // Handle various ID formats
      if (response.data.id) {
        currentResume.value = response.data
        console.log('Current resume set with ID:', currentResume.value.id)
        return true
      } else if (response.data._id) {
        // Handle MongoDB ObjectId format
        currentResume.value = {
          ...response.data,
          id: response.data._id,
        }
        console.log('Current resume ID fixed from _id:', currentResume.value.id)
        return true
      } else if (response.data.file_id) {
        // Handle case where we have file_id instead
        currentResume.value = {
          ...response.data,
          id: response.data.file_id,
        }
        console.log('Current resume ID fixed from file_id:', currentResume.value.id)
        return true
      } else {
        console.warn('Resume found but has no valid ID')
        return false
      }
    } else {
      console.warn('No current resume found')
      return false
    }
  } catch (err) {
    console.error('Error fetching current resume:', err)
    return false
  } finally {
    currentResumeLoading.value = false
  }
}

const fetchUserSkills = async () => {
  if (!currentResume.value || !currentResume.value.id) {
    console.warn('Cannot fetch skills: no valid resume ID')
    return false
  }

  userSkillsLoading.value = true

  try {
    console.log(`Fetching skills for resume ID: ${currentResume.value.id}`)
    const response = await api.get(`/skills/resume/${currentResume.value.id}`)
    console.log('Skills response:', response.data)
    userSkills.value = response.data
    return true
  } catch (error) {
    if (error.response?.status !== 404) {
      console.error('Error fetching skills:', error)
      toast({
        title: 'Error',
        description: 'Failed to fetch skills',
        variant: 'destructive',
      })
    }
    return false
  } finally {
    userSkillsLoading.value = false
  }
}

const analyzeResume = async () => {
  if (!currentResume.value || !currentResume.value.id) {
    console.warn('Cannot analyze resume: no valid resume ID')
    toast({
      title: 'Error',
      description: 'No resume available for analysis',
      variant: 'destructive',
    })
    return
  }

  analyzing.value = true
  error.value = null

  try {
    console.log(`Analyzing resume with ID: ${currentResume.value.id}`)
    const response = await api.post(`/skills/analyze/${currentResume.value.id}`)
    console.log('Analysis response:', response.data)
    userSkills.value = response.data

    toast({
      title: 'Success',
      description: 'Resume skills analyzed successfully',
      variant: 'default',
    })
  } catch (error) {
    console.error('Error analyzing skills:', error)
    error.value = error.response?.data?.detail || 'Failed to analyze resume skills'
    toast({
      title: 'Error',
      description: error.value,
      variant: 'destructive',
    })
  } finally {
    analyzing.value = false
  }
}

const navigateToResumes = () => {
  router.push('/dashboard/resumes')
}

onMounted(async () => {
  loading.value = true
  try {
    const resumeLoaded = await fetchCurrentResume()
    if (resumeLoaded && currentResume.value) {
      await fetchUserSkills()
    }
  } catch (err) {
    console.error('Error during component initialization:', err)
    error.value = 'Failed to load skill data'
    toast({
      title: 'Error',
      description: 'Failed to load skill data',
      variant: 'destructive',
    })
  } finally {
    loading.value = false
  }
})
</script>
