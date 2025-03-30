<script setup lang="ts">
import { RouterView } from 'vue-router'
import { useThemeStore } from '@/stores/theme'
import { useAuthStore } from '@/stores/auth'
import { Toaster } from '@/components/ui/toast'
import { ref, onMounted } from 'vue'
import { Loader2 } from 'lucide-vue-next'

const themeStore = useThemeStore()
const auth = useAuthStore()
const isInitialized = ref(false)

onMounted(async () => {
  themeStore.updateTheme()

  if (localStorage.getItem('token')) {
    await auth.checkAuth()
  }
  isInitialized.value = true
})
</script>

<template>
  <div :class="{ dark: themeStore.theme === 'dark' }">
    <main class="min-h-screen bg-background text-foreground">
      <Toaster />
      <RouterView v-if="isInitialized" />
      <div v-else class="min-h-screen flex items-center justify-center">
        <Loader2 class="h-8 w-8 animate-spin" />
      </div>
    </main>
  </div>
</template>
