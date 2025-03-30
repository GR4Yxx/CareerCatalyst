<template>
  <div class="resumes-view">
    <h1 class="text-2xl font-bold mb-6 flex items-center">
      <FileText class="h-7 w-7 mr-3 text-primary" />
      My Resumes
    </h1>

    <div v-if="loading" class="flex justify-center py-12">
      <div
        class="animate-spin h-10 w-10 border-4 border-primary border-t-transparent rounded-full"
      ></div>
    </div>

    <div
      v-else-if="error"
      class="bg-red-100 dark:bg-red-900/30 border border-red-400 text-red-700 dark:text-red-400 px-4 py-3 rounded mb-6"
    >
      <p>{{ error }}</p>
      <button
        @click="fetchResumes"
        class="mt-2 text-sm underline hover:text-red-800 dark:hover:text-red-300"
      >
        Try again
      </button>
    </div>

    <div v-else class="grid grid-cols-1 gap-6">
      <!-- Upload Section -->
      <div class="p-6 bg-card rounded-lg border shadow-sm">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl font-semibold">Upload Resume</h2>
        </div>

        <div
          class="border-2 border-dashed border-slate-300 dark:border-slate-700 rounded-lg p-8 text-center"
          @dragover.prevent="onDragOver"
          @dragleave.prevent="onDragLeave"
          @drop.prevent="onFileDrop"
          :class="{ 'border-primary bg-primary/5': dragover }"
        >
          <div class="mx-auto flex flex-col items-center justify-center">
            <Upload class="h-10 w-10 text-muted-foreground mb-4" />
            <h3 class="font-medium mb-1">Drag & drop your resume</h3>
            <p class="text-sm text-muted-foreground mb-4">
              Support for PDF, DOCX, or TXT file formats
            </p>
            <Button @click="triggerFileInput">
              <Plus class="h-4 w-4 mr-2" />
              Select File
            </Button>
            <input
              type="file"
              ref="fileInput"
              class="hidden"
              accept=".pdf,.docx,.doc,.txt"
              @change="onFileSelected"
            />
          </div>
        </div>

        <div v-if="uploadProgress > 0 && uploadProgress < 100" class="mt-4">
          <div class="flex justify-between text-sm mb-1">
            <span>Uploading...</span>
            <span>{{ uploadProgress }}%</span>
          </div>
          <div class="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2">
            <div class="bg-primary h-2 rounded-full" :style="{ width: `${uploadProgress}%` }"></div>
          </div>
        </div>
      </div>

      <!-- Master Resume Section -->
      <div v-if="masterResume" class="p-6 bg-card rounded-lg border shadow-sm">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl font-semibold">Master Resume</h2>
        </div>

        <div class="border rounded-lg p-4 hover:border-primary transition-colors">
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <div class="p-2 bg-blue-100 dark:bg-blue-900 rounded-lg mr-4">
                <FileText class="h-6 w-6 text-blue-600 dark:text-blue-400" />
              </div>
              <div>
                <h3 class="font-medium">{{ masterResume.original_filename }}</h3>
                <div class="flex items-center text-xs text-muted-foreground mt-1">
                  <span
                    >{{ getFileTypeDisplay(masterResume.file_type) }} •
                    {{ formatFileSize(masterResume.file_size) }}</span
                  >
                  <Circle class="h-1 w-1 mx-2 fill-current" />
                  <span>Uploaded {{ formatDate(masterResume.created_at) }}</span>
                  <Badge class="ml-2" variant="success">Primary</Badge>
                </div>
              </div>
            </div>
            <div class="flex items-center space-x-1">
              <Button @click="previewResume(masterResume._id)" variant="ghost" size="icon">
                <Eye class="h-4 w-4" />
              </Button>
              <Button
                @click="downloadResumeFile(masterResume._id, masterResume.original_filename)"
                variant="ghost"
                size="icon"
              >
                <Download class="h-4 w-4" />
              </Button>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" size="icon">
                    <MoreVertical class="h-4 w-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <DropdownMenuItem
                    @click="deleteResumeFile(masterResume._id)"
                    class="text-red-600"
                  >
                    <Trash class="h-4 w-4 mr-2" />
                    Delete
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </div>

          <div v-if="masterResume.parsed_content?.score" class="mt-4 space-y-1">
            <div class="flex justify-between text-sm">
              <span>ATS Score</span>
              <span class="font-medium"
                >{{ Math.round(masterResume.parsed_content.score) }}/100</span
              >
            </div>
            <div class="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-1.5">
              <div
                class="h-1.5 rounded-full"
                :class="getScoreColorClass(masterResume.parsed_content.score)"
                :style="{
                  width: `${Math.min(100, Math.round(masterResume.parsed_content.score))}%`,
                }"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Resume Versions Section - Only show if we have versions -->
      <div
        v-if="
          resumeWithVersions &&
          resumeWithVersions.versions &&
          resumeWithVersions.versions.length > 0
        "
        class="p-6 bg-card rounded-lg border shadow-sm"
      >
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl font-semibold">Resume Versions</h2>
        </div>

        <div class="space-y-4">
          <div
            v-for="version in resumeWithVersions.versions"
            :key="version._id"
            class="border rounded-lg p-4 hover:border-primary transition-colors"
          >
            <div class="flex items-center justify-between">
              <div class="flex items-center">
                <div class="p-2 bg-green-100 dark:bg-green-900 rounded-lg mr-4">
                  <FileText class="h-6 w-6 text-green-600 dark:text-green-400" />
                </div>
                <div>
                  <h3 class="font-medium">{{ version.version_name }}</h3>
                  <div class="flex items-center text-xs text-muted-foreground mt-1">
                    <span>Optimized for Job ID: {{ version.job_id }}</span>
                    <Circle class="h-1 w-1 mx-2 fill-current" />
                    <span>Created {{ formatDate(version.created_at) }}</span>
                  </div>
                </div>
              </div>
              <div class="flex items-center space-x-1">
                <Button variant="ghost" size="icon">
                  <Eye class="h-4 w-4" />
                </Button>
                <Button variant="ghost" size="icon">
                  <Download class="h-4 w-4" />
                </Button>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="icon">
                      <MoreVertical class="h-4 w-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem>
                      <FileEdit class="h-4 w-4 mr-2" />
                      Rename
                    </DropdownMenuItem>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem class="text-red-600">
                      <Trash class="h-4 w-4 mr-2" />
                      Delete
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>
            </div>

            <div class="mt-4 space-y-1">
              <div class="flex justify-between text-sm">
                <span>Optimization Score</span>
                <span class="font-medium">{{ Math.round(version.optimization_score) }}/100</span>
              </div>
              <div class="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-1.5">
                <div
                  class="h-1.5 rounded-full"
                  :class="getScoreColorClass(version.optimization_score)"
                  :style="{ width: `${Math.min(100, Math.round(version.optimization_score))}%` }"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- No Resume Message -->
      <div v-if="!masterResume" class="p-6 bg-card rounded-lg border shadow-sm text-center">
        <FileX class="h-12 w-12 text-muted-foreground mx-auto mb-3" />
        <h3 class="text-lg font-medium mb-2">No Resume Found</h3>
        <p class="text-muted-foreground mb-4">
          Upload your resume to get started with resume optimization and job matching.
        </p>
      </div>

      <!-- Resume Stats - Only show if we have a master resume -->
      <div
        v-if="masterResume && masterResume.parsed_content"
        class="p-6 bg-card rounded-lg border shadow-sm"
      >
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl font-semibold">Resume Analytics</h2>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="p-4 border rounded-lg">
            <h3 class="text-lg font-medium mb-2">Top Skills</h3>
            <div
              v-if="
                masterResume.parsed_content.skills && masterResume.parsed_content.skills.length > 0
              "
              class="space-y-1.5"
            >
              <div
                v-for="(skill, i) in masterResume.parsed_content.skills.slice(0, 5)"
                :key="i"
                class="flex justify-between text-sm"
              >
                <span>{{ skill.name }}</span>
                <span class="font-medium">{{ skill.level || 'Mentioned' }}</span>
              </div>
            </div>
            <div v-else class="text-sm text-muted-foreground">No skills detected</div>
          </div>

          <div class="p-4 border rounded-lg">
            <h3 class="text-lg font-medium mb-2">Skills Gaps</h3>
            <div
              v-if="
                masterResume.parsed_content.skillGaps &&
                masterResume.parsed_content.skillGaps.length > 0
              "
              class="space-y-1.5"
            >
              <div
                v-for="(skill, i) in masterResume.parsed_content.skillGaps.slice(0, 5)"
                :key="i"
                class="flex justify-between text-sm"
              >
                <span>{{ skill }}</span>
                <span class="text-amber-500">Missing</span>
              </div>
            </div>
            <div v-else class="text-sm text-muted-foreground">No skill gaps detected</div>
          </div>

          <div class="p-4 border rounded-lg">
            <h3 class="text-lg font-medium mb-2">Improvement Tips</h3>
            <div
              v-if="
                masterResume.parsed_content.improvementTips &&
                masterResume.parsed_content.improvementTips.length > 0
              "
            >
              <ul class="space-y-1.5 text-sm">
                <li
                  v-for="(tip, i) in masterResume.parsed_content.improvementTips.slice(0, 5)"
                  :key="i"
                  class="flex items-start"
                >
                  <ArrowRight class="h-4 w-4 mr-1 mt-0.5 text-blue-500" />
                  <span>{{ tip }}</span>
                </li>
              </ul>
            </div>
            <div v-else class="text-sm text-muted-foreground">No improvement tips available</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import {
  FileText,
  Upload,
  Plus,
  Eye,
  Download,
  MoreVertical,
  FileEdit,
  Check,
  Trash,
  Circle,
  ArrowRight,
  FileX,
} from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { useResumeStore } from '@/stores/resume'
import { AxiosError } from 'axios'

const resumeStore = useResumeStore()

const fileInput = ref<HTMLInputElement | null>(null)
const dragover = ref(false)
const uploadProgress = ref(0)

const loading = computed(() => resumeStore.loading)
const error = computed(() => resumeStore.error)
const masterResume = computed(() => resumeStore.masterResume)
const resumeWithVersions = computed(() => resumeStore.currentResumeWithVersions)

// Fetch resumes on component mount
onMounted(async () => {
  await fetchResumes()
})

async function fetchResumes() {
  await resumeStore.fetchAllResumes()

  // If we have a master resume, fetch its versions
  if (resumeStore.masterResume) {
    await resumeStore.fetchResumeWithVersions(resumeStore.masterResume._id)
  }
}

function onFileSelected(event: Event) {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    uploadFile(target.files[0])
  }
}

function onFileDrop(event: DragEvent) {
  event.preventDefault()
  dragover.value = false

  if (!event.dataTransfer) return

  const files = event.dataTransfer.files
  if (files && files.length > 0) {
    uploadFile(files[0])
  }
}

async function uploadFile(file: File) {
  // Validate file type
  const allowedTypes = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'text/plain',
  ]

  const fileType = file.type

  if (!allowedTypes.includes(fileType)) {
    alert('Invalid file type. Only PDF, DOCX and TXT files are allowed.')
    return
  }

  // Reset any previous errors
  resumeStore.error = null

  // Simulate upload progress
  uploadProgress.value = 0
  const interval = setInterval(() => {
    uploadProgress.value += 5
    if (uploadProgress.value >= 95) {
      clearInterval(interval)
    }
  }, 100)

  try {
    const newResume = await resumeStore.uploadResume(file)
    uploadProgress.value = 100

    if (!newResume) {
      // If resumeStore.uploadResume returns null, there was an error
      clearInterval(interval)
      uploadProgress.value = 0
      alert('Failed to upload resume. Please try again.')
      return
    }

    // Display success message
    alert('Resume uploaded successfully!')

    // Fetch versions if the upload was successful
    if (resumeStore.masterResume) {
      await resumeStore.fetchResumeWithVersions(resumeStore.masterResume._id)
    }

    setTimeout(() => {
      uploadProgress.value = 0
    }, 1000)
  } catch (err: unknown) {
    clearInterval(interval)
    uploadProgress.value = 0

    // Log the error to the console for debugging
    console.error('Upload failed:', err)

    let errorMessage = 'Failed to upload resume. Please try again later.'

    // Extract more specific error message if available
    if (err instanceof AxiosError && err.response?.data?.detail) {
      errorMessage = `Upload failed: ${err.response.data.detail}`
    } else if (err instanceof Error) {
      errorMessage = `Upload failed: ${err.message}`
    }

    alert(errorMessage)
  }
}

async function downloadResumeFile(resumeId: string, filename: string) {
  try {
    const blob = await resumeStore.downloadResume(resumeId)
    if (blob) {
      // Create a URL for the blob
      const url = window.URL.createObjectURL(blob)

      // Create a temporary anchor element and trigger download
      const a = document.createElement('a')
      a.href = url
      a.download = filename
      document.body.appendChild(a)
      a.click()

      // Clean up
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    }
  } catch (err) {
    console.error('Download failed:', err)
  }
}

async function deleteResumeFile(resumeId: string) {
  if (confirm('Are you sure you want to delete this resume?')) {
    await resumeStore.deleteResume(resumeId)
  }
}

function previewResume(resumeId: string) {
  // To be implemented - could open a modal or navigate to a preview page
  console.log('Preview resume:', resumeId)
  // For now, download the file
  if (masterResume.value) {
    downloadResumeFile(resumeId, masterResume.value.original_filename)
  }
}

// Helper functions
function formatDate(dateString: string): string {
  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))

  if (diffDays === 0) {
    return 'Today'
  } else if (diffDays === 1) {
    return 'Yesterday'
  } else if (diffDays < 7) {
    return `${diffDays} days ago`
  } else if (diffDays < 30) {
    const weeks = Math.floor(diffDays / 7)
    return `${weeks} ${weeks === 1 ? 'week' : 'weeks'} ago`
  } else if (diffDays < 365) {
    const months = Math.floor(diffDays / 30)
    return `${months} ${months === 1 ? 'month' : 'months'} ago`
  } else {
    const years = Math.floor(diffDays / 365)
    return `${years} ${years === 1 ? 'year' : 'years'} ago`
  }
}

function formatFileSize(bytes?: number): string {
  if (!bytes) return 'Unknown size'

  const kb = bytes / 1024
  if (kb < 1024) {
    return `${Math.round(kb)}KB`
  } else {
    const mb = kb / 1024
    return `${mb.toFixed(1)}MB`
  }
}

function getFileTypeDisplay(fileType: string): string {
  switch (fileType) {
    case 'application/pdf':
      return 'PDF'
    case 'application/msword':
    case 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
      return 'DOCX'
    case 'text/plain':
      return 'TXT'
    default:
      return fileType.split('/')[1].toUpperCase()
  }
}

function getScoreColorClass(score: number): string {
  if (score >= 80) {
    return 'bg-green-500'
  } else if (score >= 60) {
    return 'bg-blue-500'
  } else if (score >= 40) {
    return 'bg-amber-500'
  } else {
    return 'bg-red-500'
  }
}

function triggerFileInput() {
  if (fileInput.value) {
    fileInput.value.click()
  }
}

function onDragOver(event: DragEvent) {
  event.preventDefault()
  dragover.value = true
}

function onDragLeave(event: DragEvent) {
  event.preventDefault()
  dragover.value = false
}
</script>
