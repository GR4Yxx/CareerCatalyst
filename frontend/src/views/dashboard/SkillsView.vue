<template>
  <div class="skills-view">
    <h1 class="text-2xl font-bold mb-6 flex items-center">
      <Sparkles class="h-7 w-7 mr-3 text-primary" />
      Skills Intelligence
    </h1>

    <div v-if="loading" class="flex justify-center my-8">
      <div class="animate-spin h-8 w-8 text-primary">
        <Loader2 />
      </div>
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
                v-if="!userSkills || userSkills.skills.length === 0"
                @click="analyzeResume"
                :disabled="analyzing"
              >
                {{ analyzing ? 'Analyzing...' : 'Analyze Skills' }}
              </Button>
              <Button
                v-if="userSkills && userSkills.skills.length > 0"
                @click="analyzeResume"
                variant="outline"
                :disabled="analyzing"
              >
                {{ analyzing ? 'Analyzing...' : 'Re-analyze Skills' }}
              </Button>
            </div>
          </div>
        </div>
      </div>

      <!-- Skills Display Section -->
      <div v-if="userSkills && userSkills.skills.length > 0">
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
        v-else-if="currentResume && (!userSkills || userSkills.skills.length === 0)"
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
import axios from 'axios'

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
const userSkills = ref<UserSkill | null>(null)

const technicalSkills = computed(() => {
  if (!userSkills.value) return []
  return userSkills.value.skills
    .filter((skill) => skill.category === 'technical')
    .sort((a, b) => b.confidence - a.confidence)
})

const softSkills = computed(() => {
  if (!userSkills.value) return []
  return userSkills.value.skills
    .filter((skill) => skill.category === 'soft')
    .sort((a, b) => b.confidence - a.confidence)
})

const domainSkills = computed(() => {
  if (!userSkills.value) return []
  return userSkills.value.skills
    .filter((skill) => skill.category === 'domain')
    .sort((a, b) => b.confidence - a.confidence)
})

const certifications = computed(() => {
  if (!userSkills.value) return []
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
  try {
    const response = await axios.get('/api/resumes/user/current')
    currentResume.value = response.data
  } catch (error: any) {
    if (error.response?.status !== 404) {
      console.error('Error fetching current resume:', error)
      toast({
        title: 'Error',
        description: 'Failed to fetch current resume',
        variant: 'destructive',
      })
    }
  }
}

const fetchUserSkills = async () => {
  if (!currentResume.value) return

  try {
    const response = await axios.get(`/api/skills/resume/${currentResume.value.id}`)
    userSkills.value = response.data
  } catch (error: any) {
    if (error.response?.status !== 404) {
      console.error('Error fetching skills:', error)
      toast({
        title: 'Error',
        description: 'Failed to fetch skills',
        variant: 'destructive',
      })
    }
  }
}

const analyzeResume = async () => {
  if (!currentResume.value) return

  analyzing.value = true

  try {
    const response = await axios.post(`/api/skills/analyze/${currentResume.value.id}`)
    userSkills.value = response.data

    toast({
      title: 'Success',
      description: 'Resume skills analyzed successfully',
      variant: 'default',
    })
  } catch (error) {
    console.error('Error analyzing skills:', error)
    toast({
      title: 'Error',
      description: 'Failed to analyze resume skills',
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
    await fetchCurrentResume()
    if (currentResume.value) {
      await fetchUserSkills()
    }
  } finally {
    loading.value = false
  }
})
</script>
