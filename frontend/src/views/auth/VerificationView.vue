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

    <!-- Verification Card -->
    <div class="flex-1 flex items-center justify-center p-8 relative z-10">
      <div class="w-full max-w-[500px] space-y-8 animate-fade-in">
        <div class="text-center">
          <h2 class="text-3xl font-bold tracking-tight text-white mb-2">Verify your email</h2>
          <p class="text-base text-indigo-200/80">Check your inbox for a verification code</p>
        </div>

        <div
          class="bg-slate-900/80 backdrop-blur-sm border border-indigo-800/20 p-8 rounded-2xl shadow-xl"
        >
          <form v-if="!verified" @submit.prevent="verifyEmail" class="space-y-6">
            <div class="space-y-4">
              <Label for="verification_code" class="text-base text-indigo-200"
                >Verification Code</Label
              >
              <Input
                id="verification_code"
                v-model="code"
                type="text"
                placeholder="Enter the 6-digit code"
                class="h-12 bg-slate-800/70 border-indigo-700/30 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all"
                :disabled="isLoading"
                required
              />
            </div>

            <Button
              type="submit"
              class="w-full h-12 text-base bg-indigo-600 hover:bg-indigo-700 text-white transition-all duration-300"
              :class="{ 'opacity-90 hover:bg-indigo-600': isLoading }"
              :disabled="isLoading"
            >
              <Loader2 v-if="isLoading" class="mr-2 h-5 w-5 animate-spin" />
              {{ isLoading ? 'Verifying...' : 'Verify Email' }}
            </Button>

            <div class="flex justify-between items-center pt-4">
              <Button
                type="button"
                variant="link"
                class="text-indigo-400 hover:text-indigo-300 transition-colors p-0 h-auto"
                @click="resendCode"
                :disabled="isResending || countdown > 0"
              >
                {{ countdown > 0 ? `Resend in ${countdown}s` : 'Resend code' }}
              </Button>

              <RouterLink
                to="/login"
                class="text-sm font-medium text-indigo-400 hover:text-indigo-300 transition-colors"
              >
                Back to login
              </RouterLink>
            </div>
          </form>

          <div v-else class="text-center space-y-6">
            <div class="flex justify-center">
              <div class="bg-indigo-900/40 p-4 rounded-full">
                <CheckCircle class="h-16 w-16 text-indigo-400" />
              </div>
            </div>
            <div>
              <h3 class="text-xl font-semibold text-white">Email verified!</h3>
              <p class="mt-2 text-indigo-200/80">Your account has been successfully verified.</p>
            </div>
            <Button
              class="w-full h-12 text-base bg-indigo-600 hover:bg-indigo-700 text-white transition-all duration-300"
              @click="router.push('/login')"
            >
              Continue to login
            </Button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useToast } from '@/components/ui/toast'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Loader2, CheckCircle } from 'lucide-vue-next'
import api from '@/config/axios'

const router = useRouter()
const { toast } = useToast()
const code = ref('')
const isLoading = ref(false)
const isResending = ref(false)
const verified = ref(false)
const countdown = ref(0)
let countdownTimer: number | null = null

// Get email from query params or localStorage
const email = ref(localStorage.getItem('verification_email') || '')

async function verifyEmail() {
  if (!code.value || code.value.length !== 6) {
    toast({
      variant: 'destructive',
      title: 'Invalid Code',
      description: 'Please enter a valid 6-digit verification code',
    })
    return
  }

  isLoading.value = true
  try {
    await api.post('/verify-email', {
      email: email.value,
      code: code.value,
    })

    verified.value = true
    toast({
      title: 'Success',
      description: 'Your email has been verified! You can now log in to your account.',
    })

    // Clear the stored email
    localStorage.removeItem('verification_email')
  } catch (error: any) {
    const errorMessage =
      error.response?.data?.message || 'Failed to verify email. Please try again.'

    toast({
      variant: 'destructive',
      title: 'Verification Failed',
      description: errorMessage,
    })
  } finally {
    isLoading.value = false
  }
}

async function resendCode() {
  if (countdown.value > 0) return

  isResending.value = true
  try {
    await api.post('/resend-verification', {
      email: email.value,
    })

    toast({
      title: 'Code Sent',
      description: 'A new verification code has been sent to your email.',
    })

    // Start countdown
    countdown.value = 60
    startCountdown()
  } catch (error: any) {
    const errorMessage =
      error.response?.data?.message || 'Failed to resend verification code. Please try again.'

    toast({
      variant: 'destructive',
      title: 'Failed to Resend',
      description: errorMessage,
    })
  } finally {
    isResending.value = false
  }
}

function startCountdown() {
  countdownTimer = window.setInterval(() => {
    if (countdown.value > 0) {
      countdown.value--
    } else if (countdownTimer) {
      clearInterval(countdownTimer)
    }
  }, 1000)
}

onMounted(() => {
  // Check if email is provided in query params
  const urlParams = new URLSearchParams(window.location.search)
  const emailParam = urlParams.get('email')

  if (emailParam) {
    email.value = emailParam
    localStorage.setItem('verification_email', emailParam)
  }

  // Redirect if no email is available
  if (!email.value) {
    toast({
      variant: 'destructive',
      title: 'Error',
      description: 'No email address provided for verification.',
    })
    router.push('/login')
  }
})

onUnmounted(() => {
  if (countdownTimer) {
    clearInterval(countdownTimer)
  }
})
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.8s ease-out forwards;
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
