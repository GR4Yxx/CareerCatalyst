<template>
  <div class="min-h-screen flex relative overflow-hidden bg-background">
    <!-- Background elements -->
    <div
      class="absolute inset-0 bg-gradient-to-br from-slate-950 via-indigo-950 to-slate-950 overflow-hidden"
    >
      <div class="absolute inset-0 opacity-20">
        <img
          src="https://images.unsplash.com/photo-1558494949-ef010cbdcc31?q=80&w=2034&auto=format&fit=crop"
          class="object-cover w-full h-full"
          alt=""
        />
      </div>
      <div
        class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500"
      ></div>
    </div>

    <!-- Left side - Branding -->
    <div class="hidden lg:flex lg:w-[580px] relative p-12 flex-col justify-between z-10">
      <!-- Title & Tagline -->
      <div class="animate-fade-in">
        <h1
          class="text-4xl font-bold tracking-tight text-white bg-gradient-to-r from-indigo-400 via-purple-300 to-pink-300 text-transparent bg-clip-text"
        >
          Networkin
        </h1>
        <p class="mt-2 text-lg text-indigo-200/80">Your Professional Networking Platform</p>
      </div>

      <FeatureList />

      <!-- Footer with Theme Toggle -->
      <div class="space-y-6 animate-fade-in-delay-2">
        <ThemeToggle />
        <p class="text-sm text-indigo-300/60">© 2025 Networkin. All rights reserved.</p>
      </div>
    </div>

    <!-- Right side - Registration wizard -->
    <div class="flex-1 flex items-center justify-center p-8 relative z-10">
      <div class="w-full max-w-[520px] space-y-6 animate-fade-in">
        <div class="text-center">
          <h2 class="text-3xl font-bold tracking-tight text-white mb-2">Create your account</h2>
          <p class="text-base text-indigo-200/80">Join our professional networking platform</p>
        </div>

        <!-- Progress stepper -->
        <RegistrationStepper :steps="steps" :current-step="currentStep" />

        <!-- Form container -->
        <div
          class="bg-slate-900/80 backdrop-blur-sm border border-indigo-800/20 p-8 rounded-2xl shadow-xl"
        >
          <!-- Dynamic step component -->
          <component
            :is="currentStepComponent"
            :form-data="formData"
            :social-profiles="socialProfiles"
            :is-loading="isLoading"
            @update:formData="updateFormData"
            @update:socialProfiles="updateSocialProfiles"
            @image-upload="handleImageUpload"
          />

          <!-- Navigation Buttons -->
          <div class="flex justify-between mt-8">
            <Button
              v-if="currentStep > 0"
              type="button"
              variant="outline"
              class="border-indigo-700/30 text-indigo-200 hover:bg-indigo-950/50 hover:text-indigo-100"
              :disabled="isLoading"
              @click="previousStep"
            >
              Back
            </Button>
            <div v-else></div>

            <Button
              type="button"
              class="bg-indigo-600 hover:bg-indigo-700 text-white"
              :class="{ 'opacity-90 hover:bg-indigo-600': isLoading }"
              :disabled="isLoading"
              @click="nextStep"
            >
              <Loader2 v-if="isLoading" class="mr-2 h-5 w-5 animate-spin" />
              {{ isLastStep ? 'Create Account' : 'Continue' }}
            </Button>
          </div>
        </div>

        <div class="text-center">
          <p class="text-indigo-200/80">
            Already have an account?
            <RouterLink
              to="/login"
              class="font-medium text-indigo-400 hover:text-indigo-300 ml-1 transition-colors"
            >
              Sign in
            </RouterLink>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useToast } from '@/components/ui/toast'
import { Button } from '@/components/ui/button'
import { Loader2 } from 'lucide-vue-next'
import ThemeToggle from '@/components/common/ThemeToggle.vue'
import FeatureList from '@/components/auth/FeatureList.vue'
import RegistrationStepper from '@/components/auth/RegistrationStepper.vue'
import BasicInfoStep from '@/components/auth/registration/BasicInfoStep.vue'
import SubscriptionStep from '@/components/auth/registration/SubscriptionStep.vue'
import ProfileSetupStep from '@/components/auth/registration/ProfileSetupStep.vue'
import FinalReviewStep from '@/components/auth/registration/FinalReviewStep.vue'
import api from '@/config/axios'
import type { AxiosError } from 'axios'

interface FormDataType {
  username: string
  first_name: string
  last_name: string
  primary_email: string
  password: string
  password_confirmation: string
  role: 'regular' | 'organizer' | 'admin'
  company_name: string
  subscription_plan: string
  avatar_path: string
  avatar_file: File | null
  bio: string
  job_title: string
  phone: string
  preferred_timezone: string
  profile_visibility: boolean
  privacy_agreed: boolean
  terms_agreed: boolean
  marketing_agreed: boolean
}

interface SocialProfileType {
  [key: string]: {
    social_type: string
    handle: string
    url: string
    visibility: boolean
  }
}

const router = useRouter()
const { toast } = useToast()
const isLoading = ref(false)
const previewImage = ref('')

// Step management
const steps = [
  { title: 'Account' },
  { title: 'Subscription' },
  { title: 'Profile' },
  { title: 'Review' },
]
const currentStep = ref(0)
const isLastStep = computed(() => currentStep.value === steps.length - 1)

// Dynamic component based on current step
const currentStepComponent = computed(() => {
  switch (currentStep.value) {
    case 0:
      return BasicInfoStep
    case 1:
      return SubscriptionStep
    case 2:
      return ProfileSetupStep
    case 3:
      return FinalReviewStep
    default:
      return BasicInfoStep
  }
})

// Form data
const formData = reactive({
  // Basic account info
  username: '',
  first_name: '',
  last_name: '',
  primary_email: '',
  password: '',
  password_confirmation: '',
  role: 'regular' as 'regular' | 'organizer' | 'admin',
  company_name: '',

  // Subscription
  subscription_plan: 'free',

  // Profile
  avatar_path: '',
  avatar_file: null as File | null,
  bio: '',
  job_title: '',
  phone: '',
  preferred_timezone: 'UTC',
  profile_visibility: true,

  // Terms
  privacy_agreed: false,
  terms_agreed: false,
  marketing_agreed: false,
})

// Social profiles
const socialProfiles = reactive({
  linkedin: { social_type: 'linkedin', handle: '', url: '', visibility: true },
  twitter: { social_type: 'twitter', handle: '', url: '', visibility: true },
  instagram: { social_type: 'instagram', handle: '', url: '', visibility: true },
})

// Load saved form data from localStorage if available
onMounted(() => {
  const savedData = localStorage.getItem('registration_form_data')
  if (savedData) {
    const parsedData = JSON.parse(savedData)
    Object.assign(formData, parsedData)
  }

  const savedStep = localStorage.getItem('registration_current_step')
  if (savedStep) {
    currentStep.value = parseInt(savedStep, 10)
  }

  const savedSocials = localStorage.getItem('registration_social_profiles')
  if (savedSocials) {
    const parsedSocials = JSON.parse(savedSocials)
    Object.assign(socialProfiles, parsedSocials)
  }
})

// Save form data to localStorage when updated
watch(
  [formData, currentStep, socialProfiles],
  () => {
    localStorage.setItem('registration_form_data', JSON.stringify(formData))
    localStorage.setItem('registration_current_step', currentStep.value.toString())
    localStorage.setItem('registration_social_profiles', JSON.stringify(socialProfiles))
  },
  { deep: true },
)

// Update methods for child components
function updateFormData(newData: Partial<FormDataType>) {
  Object.assign(formData, newData)
}

function updateSocialProfiles(newProfiles: Partial<SocialProfileType>) {
  Object.assign(socialProfiles, newProfiles)
}

// Image upload handling
function handleImageUpload(file: File | null) {
  if (!file) return

  // Validate file type
  if (!file.type.startsWith('image/')) {
    toast({
      variant: 'destructive',
      title: 'Invalid file type',
      description: 'Please upload an image file (JPG, PNG, etc.)',
    })
    return
  }

  // Create a preview URL
  previewImage.value = URL.createObjectURL(file)

  // Store the file reference
  formData.avatar_file = file as File
}

// Step navigation
function nextStep() {
  if (currentStep.value === 0) {
    if (!validateBasicInfo()) return
  } // Update this section in your nextStep function
  else if (currentStep.value === 3) {
    // This is the final step, process registration
    console.log('Final step, validating...')

    const finalStepValid = validateFinalStep()
    console.log('Final step validation:', finalStepValid)

    const registrationDataValid = validateRegistrationData()
    console.log('Registration data validation:', registrationDataValid)

    if (!finalStepValid || !registrationDataValid) {
      console.log('Validation failed, not proceeding')
      return
    }

    console.log('All validation passed, calling handleRegister()')
    handleRegister()
    return
  }

  // Move to next step
  if (currentStep.value < steps.length - 1) {
    currentStep.value++
  }
}

function previousStep() {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

// Validation
function validateBasicInfo() {
  // Username validation
  if (!formData.username || formData.username.length < 3) {
    toast({
      variant: 'destructive',
      title: 'Invalid Username',
      description: 'Username must be at least 3 characters long',
    })
    return false
  }

  // Email validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!formData.primary_email || !emailRegex.test(formData.primary_email)) {
    toast({
      variant: 'destructive',
      title: 'Invalid Email',
      description: 'Please enter a valid email address',
    })
    return false
  }

  // Password validation
  if (!formData.password || formData.password.length < 8) {
    toast({
      variant: 'destructive',
      title: 'Invalid Password',
      description: 'Password must be at least 8 characters long',
    })
    return false
  }

  // Password confirmation
  if (formData.password !== formData.password_confirmation) {
    toast({
      variant: 'destructive',
      title: 'Password Mismatch',
      description: 'Passwords do not match',
    })
    return false
  }

  // Company name (for organizers)
  if (formData.role === 'organizer' && !formData.company_name) {
    toast({
      variant: 'destructive',
      title: 'Company Name Required',
      description: 'Please enter your company name',
    })
    return false
  }

  return true
}

function validateFinalStep() {
  // Terms validation
  if (!formData.terms_agreed || !formData.privacy_agreed) {
    toast({
      variant: 'destructive',
      title: 'Terms Required',
      description: 'You must agree to the Terms of Service and Privacy Policy',
    })
    console.log('Terms not agreed to:', {
      terms: formData.terms_agreed,
      privacy: formData.privacy_agreed,
    })
    return false
  }

  return true
}

// In RegisterView.vue
async function handleRegister() {
  console.log('handleRegister function called')
  isLoading.value = true

  try {
    // Create form data for user registration
    const registrationData = new FormData()

    // Add all basic user fields
    for (const [key, value] of Object.entries(formData)) {
      // Skip fields not needed for API
      if (
        [
          'privacy_agreed',
          'terms_agreed',
          'marketing_agreed',
          'job_title', // We'll handle this specifically if needed
        ].includes(key)
      )
        continue

      // Handle file upload
      if (key === 'avatar_file' && value) {
        registrationData.append('avatar', value as Blob)
      } else if (value !== null && value !== undefined) {
        registrationData.append(key, String(value))
      }
    }

    // Add job title as display_name_suffix if provided
    if (formData.job_title) {
      registrationData.append('job_title', formData.job_title)
    }

    // Process social profiles - filter out empty ones
    const socialProfilesArray = Object.values(socialProfiles)
      .filter((social) => social.handle && social.handle.trim() !== '')
      .map((social) => ({
        social_type: social.social_type,
        social_handle: social.handle,
        social_url:
          social.url || `https://${social.social_type}.com/${social.handle.replace('@', '')}`,
        visibility: social.visibility,
      }))

    if (socialProfilesArray.length > 0) {
      registrationData.append('social_profiles', JSON.stringify(socialProfilesArray))
    }

    console.log('Sending registration data with social profiles:', {
      ...formData,
      password: '[REDACTED]',
      profile_visibility: formData.profile_visibility,
      social_profiles: socialProfilesArray,
    })

    // Send registration request
    const response = await api.post('/users', registrationData)

    // Success! Show message and redirect
    toast({
      title: 'Account Created',
      description: 'Your account has been successfully created! You can now log in.',
    })

    // Clear registration data from localStorage
    localStorage.removeItem('registration_form_data')
    localStorage.removeItem('registration_current_step')
    localStorage.removeItem('registration_social_profiles')

    // Redirect to login page
    router.push('/login')
  } catch (error) {
    // Error handling...
  } finally {
    isLoading.value = false
  }
}

function validateRegistrationData() {
  // Validate username
  if (!formData.username || formData.username.length < 3) {
    toast({
      variant: 'destructive',
      title: 'Invalid Username',
      description: 'Username must be at least 3 characters long',
    })
    return false
  }

  // Validate email
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!formData.primary_email || !emailRegex.test(formData.primary_email)) {
    toast({
      variant: 'destructive',
      title: 'Invalid Email',
      description: 'Please enter a valid email address',
    })
    return false
  }

  // Validate required fields based on your database schema
  if (!formData.first_name || !formData.last_name) {
    toast({
      variant: 'destructive',
      title: 'Missing Information',
      description: 'Please provide your first and last name',
    })
    return false
  }

  if (formData.role === 'organizer' && !formData.company_name) {
    toast({
      variant: 'destructive',
      title: 'Company Name Required',
      description: 'Please enter your company name for organizer accounts',
    })
    return false
  }

  return true
}
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.8s ease-out forwards;
}

.animate-fade-in-delay {
  animation: fadeIn 0.8s ease-out 0.3s forwards;
  opacity: 0;
}

.animate-fade-in-delay-2 {
  animation: fadeIn 0.8s ease-out 0.6s forwards;
  opacity: 0;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
