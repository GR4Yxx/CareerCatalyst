<template>
  <div class="job-finder-view">
    <h1 class="text-2xl font-bold mb-6 flex items-center">
      <Briefcase class="h-7 w-7 mr-3 text-primary" />
      Job Finder
    </h1>

    <div class="mb-8">
      <div class="p-6 bg-card rounded-lg border shadow-sm">
        <h2 class="text-xl font-semibold mb-4">Job Recommendations</h2>
        <p class="mb-4">
          Discover job opportunities matched to your skills and experience. Our recommendation
          engine takes into account both direct matches and adjacent skill sets.
        </p>
        <div class="flex items-center space-x-4 mt-4">
          <Input
            v-model="searchQuery"
            placeholder="Search jobs..."
            class="max-w-md"
            @keyup.enter="handleSearch"
          />
          <Button @click="handleSearch">Search</Button>
        </div>
      </div>
    </div>

    <!-- Loading state -->
    <div v-if="isLoading" class="flex justify-center my-12">
      <Loader2 class="h-8 w-8 text-primary animate-spin" />
      <span class="ml-3">Finding the best matches for your skills...</span>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="p-6 bg-card rounded-lg border shadow-sm text-center my-8">
      <XCircle class="h-12 w-12 mx-auto text-destructive mb-3" />
      <h3 class="text-lg font-medium mb-2">Error Loading Jobs</h3>
      <p class="text-sm text-muted-foreground mb-4">{{ error }}</p>
      <Button @click="loadJobRecommendations">Try Again</Button>
    </div>

    <!-- No results state -->
    <div
      v-else-if="jobMatches.length === 0"
      class="p-6 bg-card rounded-lg border shadow-sm text-center my-8"
    >
      <SearchX class="h-12 w-12 mx-auto text-muted-foreground mb-3" />
      <h3 class="text-lg font-medium mb-2">No Job Matches Found</h3>
      <p class="text-sm text-muted-foreground mb-4">
        Try broadening your search criteria or uploading an updated resume to match more
        opportunities.
      </p>
      <div class="flex justify-center space-x-4">
        <Button variant="outline" @click="loadJobRecommendations">Reset Search</Button>
        <RouterLink to="/profile/resumes">
          <Button>Upload Resume</Button>
        </RouterLink>
      </div>
    </div>

    <!-- Job matches list -->
    <div v-else class="space-y-4">
      <div class="mb-6 flex items-center justify-between">
        <h2 class="text-lg font-semibold">{{ jobMatches.length }} Matches Found</h2>
        <div class="flex items-center">
          <span class="text-sm mr-2">AI Enhanced Matching:</span>
          <Switch v-model="useGemini" @update:model-value="toggleGeminiMatching" class="mr-2" />
          <Sparkles v-if="useGemini" class="w-4 h-4 text-amber-400" />
        </div>
      </div>
      <TransitionGroup name="job-list">
        <div
          v-for="job in jobMatches"
          :key="job.job._id"
          class="p-6 bg-card rounded-lg border shadow-sm hover:shadow-md transition-shadow"
        >
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold">{{ job.job.title }}</h3>
            <Badge :class="getMatchScoreClass(job.match_score)">
              {{ Math.round(job.match_score * 100) }}% Match
            </Badge>
          </div>
          <p class="text-sm mb-2"><strong>Company:</strong> {{ job.job.company }}</p>
          <p class="text-sm mb-2"><strong>Location:</strong> {{ job.job.location }}</p>
          <p v-if="job.job.salary_range" class="text-sm mb-4">
            <strong>Salary:</strong> {{ job.job.salary_range }}
          </p>
          <p class="text-sm text-muted-foreground mb-4">
            {{ job.job.description_snippet || truncateText(job.job.job_description, 200) }}
          </p>

          <!-- AI Match Explanation -->
          <div v-if="job.match_explanation" class="mb-4 p-3 bg-muted rounded-md">
            <div class="flex items-start">
              <Sparkles class="w-4 h-4 text-amber-400 mr-2 mt-1" />
              <div>
                <p class="text-sm font-medium mb-1">Match Analysis:</p>
                <p class="text-sm">{{ job.match_explanation }}</p>
              </div>
            </div>
          </div>

          <!-- Matching skills section -->
          <div v-if="job.matching_skills && job.matching_skills.length > 0">
            <p class="text-sm font-medium mb-2">Your Matching Skills:</p>
            <div class="flex flex-wrap gap-2 mb-4">
              <Badge
                variant="secondary"
                class="bg-green-500 hover:bg-green-600"
                v-for="skill in job.matching_skills"
                :key="skill"
              >
                {{ skill }}
              </Badge>
            </div>
          </div>

          <!-- Missing skills section -->
          <div v-if="job.missing_skills && job.missing_skills.length > 0">
            <p class="text-sm font-medium mb-2">Skills to Develop:</p>
            <div class="flex flex-wrap gap-2 mb-4">
              <Badge variant="outline" v-for="skill in job.missing_skills" :key="skill">
                {{ skill }}
              </Badge>
            </div>
          </div>

          <div class="flex space-x-2 mt-4">
            <Button variant="outline" size="sm" @click="viewJobDetails(job.job._id)">
              View Details
            </Button>
            <Button
              size="sm"
              :href="job.job.url"
              target="_blank"
              rel="noopener noreferrer"
              component="a"
            >
              Apply Now
            </Button>
            <Button
              variant="ghost"
              size="sm"
              class="ml-auto"
              @click="saveJob(job.job._id)"
              :disabled="savedJobs.has(job.job._id)"
            >
              <Bookmark v-if="savedJobs.has(job.job._id)" class="h-4 w-4 mr-2 text-primary" />
              <BookmarkPlus v-else class="h-4 w-4 mr-2" />
              {{ savedJobs.has(job.job._id) ? 'Saved' : 'Save Job' }}
            </Button>
          </div>
        </div>
      </TransitionGroup>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import {
  Briefcase,
  Loader2,
  XCircle,
  SearchX,
  Bookmark,
  BookmarkPlus,
  Sparkles,
} from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Switch } from '@/components/ui/switch'
import { jobService, type JobMatch } from '@/services/jobService'

// State
const jobMatches = ref<JobMatch[]>([])
const isLoading = ref(false)
const error = ref<string | null>(null)
const searchQuery = ref('')
const savedJobs = ref<Set<string>>(new Set())
const useGemini = ref(true)
const router = useRouter()

// Load job recommendations
async function loadJobRecommendations() {
  isLoading.value = true
  error.value = null

  try {
    jobMatches.value = await jobService.getJobRecommendations(10, useGemini.value)
  } catch (err) {
    console.error('Failed to load job recommendations:', err)
    error.value = 'There was an error loading job recommendations. Please try again later.'
  } finally {
    isLoading.value = false
  }
}

// Toggle between Gemini and basic matching
async function toggleGeminiMatching() {
  await loadJobRecommendations()
}

// Truncate text helper
function truncateText(text: string | undefined, maxLength: number): string {
  if (!text) return ''
  return text.length > maxLength ? `${text.substring(0, maxLength)}...` : text
}

// Search jobs
async function handleSearch() {
  if (!searchQuery.value.trim()) {
    // If search query is empty, reload recommendations
    return loadJobRecommendations()
  }

  isLoading.value = true
  error.value = null

  try {
    const jobs = await jobService.searchJobs({ query: searchQuery.value })
    // Convert search results to JobMatch format
    jobMatches.value = jobs.map((job) => ({
      job,
      match_score: 0.7, // Default match score for search results
      matching_skills: [],
      missing_skills: [],
    }))
  } catch (err) {
    console.error('Failed to search jobs:', err)
    error.value = 'There was an error searching for jobs. Please try again later.'
  } finally {
    isLoading.value = false
  }
}

// View job details
function viewJobDetails(jobId: string) {
  // Find the selected job
  const selectedJob = jobMatches.value.find((match) => match.job._id === jobId)

  if (selectedJob) {
    // Save selected job to localStorage for the ATS Intelligence page
    localStorage.setItem('selectedJob', JSON.stringify(selectedJob))

    // Navigate to ATS Intelligence page
    router.push('/dashboard/ats-intelligence')
  }
}

// Save a job
async function saveJob(jobId: string) {
  try {
    const success = await jobService.saveJob(jobId)
    if (success) {
      savedJobs.value.add(jobId)
    }
  } catch (err) {
    console.error('Failed to save job:', err)
  }
}

// Load saved jobs
async function loadSavedJobs() {
  try {
    const jobs = await jobService.getSavedJobs()
    savedJobs.value = new Set(jobs.map((job) => job._id))
  } catch (err) {
    console.error('Failed to load saved jobs:', err)
  }
}

// Get badge class based on match score
function getMatchScoreClass(score: number) {
  if (score >= 0.9) return 'bg-emerald-500'
  if (score >= 0.7) return 'bg-green-500'
  if (score >= 0.5) return 'bg-amber-500'
  return 'bg-red-500'
}

// Lifecycle hooks
onMounted(() => {
  loadJobRecommendations()
  loadSavedJobs()
})
</script>

<style scoped>
.job-list-enter-active,
.job-list-leave-active {
  transition: all 0.3s ease;
}
.job-list-enter-from,
.job-list-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style>
