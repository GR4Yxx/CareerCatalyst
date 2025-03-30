<template>
  <div class="ats-intelligence-view">
    <h1 class="text-2xl font-bold mb-6 flex items-center">
      <FileSearch class="h-7 w-7 mr-3 text-primary" />
      ATS Intelligence
    </h1>

    <div v-if="isLoading" class="flex justify-center my-12">
      <Loader2 class="h-8 w-8 text-primary animate-spin" />
      <span class="ml-3">Processing your resume...</span>
    </div>

    <div v-else-if="error" class="p-6 bg-card rounded-lg border shadow-sm text-center my-8">
      <XCircle class="h-12 w-12 mx-auto text-destructive mb-3" />
      <h3 class="text-lg font-medium mb-2">Error Loading Resume</h3>
      <p class="text-sm text-muted-foreground mb-4">{{ error }}</p>
      <Button @click="loadUserResume">Try Again</Button>
    </div>

    <div v-else>
      <!-- Job Details Card (shown only when a job is selected) -->
      <div v-if="selectedJob" class="mb-8">
        <div class="p-6 bg-card rounded-lg border shadow-sm">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-xl font-semibold">{{ selectedJob.job.title }}</h2>
            <Badge :class="getMatchScoreClass(selectedJob.match_score)">
              {{ Math.round(selectedJob.match_score * 100) }}% Match
            </Badge>
          </div>
          <p class="text-sm mb-2"><strong>Company:</strong> {{ selectedJob.job.company }}</p>
          <p class="text-sm mb-2"><strong>Location:</strong> {{ selectedJob.job.location }}</p>
          <div class="mt-4 mb-2">
            <strong class="text-sm">Job Description:</strong>
            <p class="text-sm mt-1 whitespace-pre-line">{{ selectedJob.job.job_description }}</p>
          </div>
          <div
            v-if="selectedJob.matching_skills && selectedJob.matching_skills.length > 0"
            class="mt-4"
          >
            <p class="text-sm font-medium mb-2">Your Matching Skills:</p>
            <div class="flex flex-wrap gap-2 mb-4">
              <Badge
                variant="secondary"
                class="bg-green-500 hover:bg-green-600"
                v-for="skill in selectedJob.matching_skills"
                :key="skill"
              >
                {{ skill }}
              </Badge>
            </div>
          </div>
          <div
            v-if="selectedJob.missing_skills && selectedJob.missing_skills.length > 0"
            class="mt-4"
          >
            <p class="text-sm font-medium mb-2">Skills to Develop:</p>
            <div class="flex flex-wrap gap-2 mb-4">
              <Badge variant="outline" v-for="skill in selectedJob.missing_skills" :key="skill">
                {{ skill }}
              </Badge>
            </div>
          </div>
        </div>
      </div>

      <!-- Resume Optimization Card -->
      <div class="mb-8">
        <div class="p-6 bg-card rounded-lg border shadow-sm">
          <h2 class="text-xl font-semibold mb-4">Resume Optimization</h2>
          <p class="mb-4">
            Tailor your resume to increase visibility with Applicant Tracking Systems. Our ATS
            intelligence system helps you optimize your resume for each job application.
          </p>

          <div v-if="!selectedJob" class="flex items-center space-x-4 mt-4">
            <Input
              v-model="jobDescription"
              placeholder="Paste job description..."
              class="max-w-md"
            />
            <Button @click="analyzeResume" :disabled="!jobDescription.trim()">Analyze</Button>
          </div>

          <div v-else class="flex items-center space-x-4 mt-4">
            <Button @click="generateLatexResume" :disabled="!userResume || isGeneratingResume">
              <Loader2 v-if="isGeneratingResume" class="h-4 w-4 mr-2 animate-spin" />
              <FileText v-else class="h-4 w-4 mr-2" />
              Generate Optimized Resume
            </Button>
          </div>
        </div>
      </div>

      <!-- Resume Preview (shown when LaTeX is generated) -->
      <div v-if="latexCode" class="grid grid-cols-1 gap-6">
        <div class="p-6 bg-card rounded-lg border shadow-sm">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-semibold">Generated Resume</h3>
            <div class="flex items-center space-x-2">
              <Button @click="downloadPdf" size="sm" variant="outline">
                <Download class="h-4 w-4 mr-2" />
                Download PDF
              </Button>
              <Button @click="copyLatex" size="sm" variant="outline">
                <Copy class="h-4 w-4 mr-2" />
                Copy LaTeX
              </Button>
            </div>
          </div>
          <div class="bg-muted p-4 rounded-md overflow-auto max-h-96">
            <pre class="text-xs"><code>{{ latexCode }}</code></pre>
          </div>
        </div>
      </div>

      <!-- ATS Analysis Grid (Always visible) -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="p-6 bg-card rounded-lg border shadow-sm">
          <h3 class="text-lg font-semibold mb-3">ATS Compatibility Score</h3>
          <div class="flex items-center mb-4">
            <div
              class="w-16 h-16 rounded-full bg-blue-500 flex items-center justify-center text-white font-bold text-2xl"
            >
              {{ atsScore }}%
            </div>
            <div class="ml-4">
              <p class="text-sm text-muted-foreground">
                {{ getAtsScoreMessage(atsScore) }}
              </p>
            </div>
          </div>
          <h4 class="font-medium mb-2">Suggested Improvements:</h4>
          <ul class="space-y-2 text-sm">
            <li v-for="(suggestion, index) in atsSuggestions" :key="index" class="flex items-start">
              <AlertCircle
                v-if="suggestion.type === 'warning'"
                class="h-4 w-4 mr-2 text-red-500 mt-0.5"
              />
              <CheckCircle2 v-else class="h-4 w-4 mr-2 text-green-500 mt-0.5" />
              <span>{{ suggestion.message }}</span>
            </li>
          </ul>
        </div>

        <div class="p-6 bg-card rounded-lg border shadow-sm">
          <h3 class="text-lg font-semibold mb-3">Keyword Analysis</h3>
          <p class="text-sm text-muted-foreground mb-4">
            Keywords found in the job description vs. your resume
          </p>
          <div class="space-y-3">
            <div v-for="(keyword, index) in keywordAnalysis" :key="index">
              <div class="flex justify-between text-sm mb-1">
                <span>{{ keyword.name }}</span>
                <span :class="keyword.found ? 'text-green-500' : 'text-red-500'">
                  {{ keyword.found ? 'Found' : 'Missing' }}
                </span>
              </div>
              <div class="w-full bg-slate-200 rounded-full h-2">
                <div
                  :class="keyword.found ? 'bg-green-500' : 'bg-red-500'"
                  class="h-2 rounded-full"
                  :style="`width: ${keyword.found ? '100%' : '0%'}`"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import {
  FileSearch,
  AlertCircle,
  CheckCircle2,
  Loader2,
  XCircle,
  Download,
  Copy,
  FileText,
} from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { useRouter } from 'vue-router'
import { useToast } from '@/components/ui/toast/use-toast'
import type { JobMatch } from '@/services/jobService'
import { resumeService } from '@/services/resumeService'
import type { Resume } from '@/services/resumeService'
import { atsService } from '@/services/atsService'

// State
const router = useRouter()
const { toast } = useToast()
const isLoading = ref(false)
const error = ref<string | null>(null)
const selectedJob = ref<JobMatch | null>(null)
const userResume = ref<Resume | null>(null)
const jobDescription = ref('')
const latexCode = ref('')
const isGeneratingResume = ref(false)
const atsScore = ref(72)
const atsSuggestions = ref([
  {
    type: 'warning',
    message: 'Add more specific technical skills relevant to the job description',
  },
  { type: 'warning', message: 'Use more industry standard terminology in your experience section' },
  { type: 'success', message: 'Your resume format is ATS-friendly' },
])
const keywordAnalysis = ref([
  { name: 'Vue.js', found: true },
  { name: 'TypeScript', found: true },
  { name: 'CI/CD Experience', found: false },
  { name: 'Agile Development', found: true },
])

// Load job from localStorage if available
onMounted(async () => {
  try {
    const jobData = localStorage.getItem('selectedJob')
    if (jobData) {
      selectedJob.value = JSON.parse(jobData)

      // Update job description input
      if (selectedJob.value?.job.job_description) {
        jobDescription.value = selectedJob.value.job.job_description
      }
    }

    // Load user's resume
    await loadUserResume()

    // Analyze resume if we have a job description
    if (selectedJob.value) {
      analyzeResume()
    }
  } catch (err) {
    console.error('Error initializing ATS Intelligence:', err)
    error.value = 'Failed to load job details'
  }
})

// Load the user's current resume
async function loadUserResume() {
  isLoading.value = true
  error.value = null

  try {
    // Fetch resume for the specified email or current user if not specified
    userResume.value = await resumeService.getCurrentUserResume()

    if (!userResume.value) {
      error.value = 'No resume found. Please upload a resume in your profile.'
    }
  } catch (err) {
    console.error('Error loading resume:', err)
    error.value = 'Failed to load resume data'
  } finally {
    isLoading.value = false
  }
}

// Analyze the resume against the job description
async function analyzeResume() {
  if (!jobDescription.value.trim() && !selectedJob.value?.job.job_description) {
    toast({
      title: 'Missing Information',
      description: 'Please provide a job description to analyze',
      variant: 'destructive',
    })
    return
  }

  if (!userResume.value) {
    toast({
      title: 'Missing Resume',
      description: 'Please upload a resume in your profile',
      variant: 'destructive',
    })
    return
  }

  isLoading.value = true

  try {
    const desc = selectedJob.value?.job.job_description || jobDescription.value
    const result = await atsService.analyzeResume(userResume.value._id, desc)

    // Update state with analysis results
    atsScore.value = result.score
    atsSuggestions.value = result.suggestions
    keywordAnalysis.value = result.keywordAnalysis
  } catch (err) {
    console.error('Error analyzing resume:', err)
    toast({
      title: 'Analysis Failed',
      description: 'Failed to analyze your resume against the job description',
      variant: 'destructive',
    })
  } finally {
    isLoading.value = false
  }
}

// Generate LaTeX resume from user resume and job details
async function generateLatexResume() {
  if (!userResume.value) {
    toast({
      title: 'Missing Resume',
      description: 'Please upload a resume in your profile',
      variant: 'destructive',
    })
    return
  }

  isGeneratingResume.value = true

  try {
    // Get job description and requirements
    const jobDesc = selectedJob.value?.job.job_description || jobDescription.value
    const requiredSkills = selectedJob.value?.missing_skills || []

    // Generate optimized resume
    const result = await atsService.generateOptimizedResume(
      userResume.value._id,
      jobDesc,
      requiredSkills,
    )

    latexCode.value = result.latexCode

    toast({
      title: 'Resume Generated',
      description: 'Your optimized LaTeX resume has been generated',
    })
  } catch (err) {
    console.error('Error generating LaTeX resume:', err)
    toast({
      title: 'Generation Failed',
      description: 'Failed to generate optimized resume',
      variant: 'destructive',
    })
  } finally {
    isGeneratingResume.value = false
  }
}

// Copy LaTeX code to clipboard
function copyLatex() {
  if (!latexCode.value) return

  navigator.clipboard
    .writeText(latexCode.value)
    .then(() => {
      toast({
        title: 'Copied to Clipboard',
        description: 'LaTeX code copied to clipboard',
      })
    })
    .catch((err) => {
      console.error('Failed to copy:', err)
      toast({
        title: 'Copy Failed',
        description: 'Failed to copy LaTeX code',
        variant: 'destructive',
      })
    })
}

// Download PDF version of the resume
async function downloadPdf() {
  if (!latexCode.value) return

  try {
    isLoading.value = true

    // Convert LaTeX to PDF
    const blob = await atsService.convertLatexToPdf(latexCode.value)

    // Create a URL for the blob
    const url = window.URL.createObjectURL(blob)

    // Create a temporary anchor element and trigger download
    const a = document.createElement('a')
    a.href = url
    a.download = 'optimized_resume.pdf'
    document.body.appendChild(a)
    a.click()

    // Clean up
    window.URL.revokeObjectURL(url)
    document.body.removeChild(a)

    toast({
      title: 'PDF Downloaded',
      description: 'Your optimized resume has been downloaded as a PDF',
    })
  } catch (err) {
    console.error('Error downloading PDF:', err)
    toast({
      title: 'Download Failed',
      description: 'Failed to download PDF',
      variant: 'destructive',
    })
  } finally {
    isLoading.value = false
  }
}

// Helper: Get ATS score message
function getAtsScoreMessage(score: number): string {
  if (score >= 90) return 'Your resume is highly optimized for ATS'
  if (score >= 70) return 'Your resume is somewhat optimized for ATS'
  if (score >= 50) return 'Your resume needs improvement for ATS compatibility'
  return 'Your resume is not well optimized for ATS'
}

// Helper: Get match score class
function getMatchScoreClass(score: number) {
  if (score >= 0.9) return 'bg-emerald-500'
  if (score >= 0.7) return 'bg-green-500'
  if (score >= 0.5) return 'bg-amber-500'
  return 'bg-red-500'
}
</script>
