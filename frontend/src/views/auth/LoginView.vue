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
          CareerCatalyst
        </h1>
        <p class="mt-2 text-lg text-indigo-200/80">Accelerate Your Career Journey</p>
      </div>

      <!-- Feature List -->
      <div class="space-y-10 animate-fade-in-delay">
        <div class="flex items-start space-x-6 transition-all duration-300 hover:translate-x-1">
          <div
            class="p-3 rounded-xl bg-indigo-950/50 border border-indigo-700/20 shadow-lg shadow-indigo-900/20"
          >
            <FileText class="h-7 w-7 text-indigo-400" />
          </div>
          <div>
            <h3 class="text-lg font-medium text-white">Resume Optimization</h3>
            <p class="mt-1.5 text-indigo-200/70">Tailor your resume to specific job listings</p>
          </div>
        </div>

        <div class="flex items-start space-x-6 transition-all duration-300 hover:translate-x-1">
          <div
            class="p-3 rounded-xl bg-indigo-950/50 border border-indigo-700/20 shadow-lg shadow-indigo-900/20"
          >
            <SearchCheck class="h-7 w-7 text-indigo-400" />
          </div>
          <div>
            <h3 class="text-lg font-medium text-white">ATS Intelligence</h3>
            <p class="mt-1.5 text-indigo-200/70">Optimize for applicant tracking systems</p>
          </div>
        </div>

        <div class="flex items-start space-x-6 transition-all duration-300 hover:translate-x-1">
          <div
            class="p-3 rounded-xl bg-indigo-950/50 border border-indigo-700/20 shadow-lg shadow-indigo-900/20"
          >
            <GraduationCap class="h-7 w-7 text-indigo-400" />
          </div>
          <div>
            <h3 class="text-lg font-medium text-white">Career Growth</h3>
            <p class="mt-1.5 text-indigo-200/70">
              Get personalized career advice and skill recommendations
            </p>
          </div>
        </div>
      </div>

      <!-- Footer with Theme Toggle -->
      <div class="space-y-6 animate-fade-in-delay-2">
        <ThemeToggle />
        <p class="text-sm text-indigo-300/60">© 2024 CareerCatalyst. All rights reserved.</p>
      </div>
    </div>

    <!-- Right side - Login form -->
    <div class="flex-1 flex items-center justify-center p-8 relative z-10">
      <div class="w-full max-w-[420px] space-y-8 animate-fade-in">
        <div class="text-center">
          <h2 class="text-3xl font-bold tracking-tight text-white mb-2">Welcome back</h2>
          <p class="text-base text-indigo-200/80">Enter your credentials to continue</p>
        </div>

        <div
          class="bg-slate-900/80 backdrop-blur-sm border border-indigo-800/20 p-8 rounded-2xl shadow-xl"
        >
          <form @submit.prevent="handleLogin" class="space-y-6">
            <div class="space-y-4">
              <Label for="email" class="text-base text-indigo-200">Email</Label>
              <Input
                id="email"
                v-model="email"
                type="email"
                placeholder="name@example.com"
                class="h-12 bg-slate-800/70 border-indigo-700/30 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all"
                :disabled="isLoading"
                required
              />
            </div>

            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <Label for="password" class="text-base text-indigo-200">Password</Label>
                <RouterLink
                  to="/forgot-password"
                  class="text-sm font-medium text-indigo-400 hover:text-indigo-300 transition-colors"
                >
                  Forgot password?
                </RouterLink>
              </div>
              <Input
                id="password"
                v-model="password"
                type="password"
                class="h-12 bg-slate-800/70 border-indigo-700/30 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all"
                :disabled="isLoading"
                required
              />
            </div>

            <div class="flex items-center space-x-3">
              <Checkbox
                id="remember"
                v-model="rememberMe"
                class="border-indigo-700/30 data-[state=checked]:bg-indigo-600"
              />
              <Label for="remember" class="text-sm font-medium text-indigo-200">Remember me</Label>
            </div>

            <div
              v-if="errorMessage"
              class="p-3 bg-red-950/40 border border-red-800/30 rounded-md text-red-300 text-sm"
            >
              {{ errorMessage }}
            </div>

            <Button
              type="submit"
              class="w-full h-12 text-base bg-indigo-600 hover:bg-indigo-700 text-white transition-all duration-300"
              :class="{ 'opacity-90 hover:bg-indigo-600': isLoading }"
              :disabled="isLoading"
            >
              <Loader2 v-if="isLoading" class="mr-2 h-5 w-5 animate-spin" />
              {{ isLoading ? 'Signing in...' : 'Sign in' }}
            </Button>
          </form>
        </div>

        <div class="text-center">
          <p class="text-indigo-200/80">
            Don't have an account?
            <RouterLink
              to="/register"
              class="font-medium text-indigo-400 hover:text-indigo-300 ml-1 transition-colors"
            >
              Sign up
            </RouterLink>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter, RouterLink } from 'vue-router'
import { useToast } from '@/components/ui/toast'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Checkbox } from '@/components/ui/checkbox'
import { FileText, SearchCheck, GraduationCap, Loader2 } from 'lucide-vue-next'
import ThemeToggle from '@/components/common/ThemeToggle.vue'
import type { AxiosError } from 'axios'

const auth = useAuthStore()
const router = useRouter()
const { toast } = useToast()

const email = ref('')
const password = ref('')
const rememberMe = ref(false)
const isLoading = ref(false)
const errorMessage = ref('')

async function handleLogin() {
  if (!email.value || !password.value) {
    errorMessage.value = 'Please fill in all fields'
    toast({
      variant: 'destructive',
      title: 'Error',
      description: 'Please fill in all fields',
    })
    return
  }

  isLoading.value = true
  errorMessage.value = ''

  try {
    const success = await auth.login({
      username: email.value, // FastAPI expects username field
      password: password.value,
    })

    if (success) {
      // Redirect to dashboard after login
      router.push('/dashboard')
    } else {
      errorMessage.value = auth.error || 'Invalid email or password'
      toast({
        variant: 'destructive',
        title: 'Authentication Error',
        description: errorMessage.value,
      })
    }
  } catch (error) {
    const axiosError = error as AxiosError<{ detail: string }>
    errorMessage.value = axiosError.response?.data?.detail || 'Invalid email or password'

    toast({
      variant: 'destructive',
      title: 'Authentication Error',
      description: errorMessage.value,
    })

    console.error('Login error:', error)
  } finally {
    isLoading.value = false
  }
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
