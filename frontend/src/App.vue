<script setup lang="ts">
import { RouterView } from 'vue-router'
import { useThemeStore } from '@/stores/theme'
import { useAuthStore } from '@/stores/auth'
import { Toaster } from '@/components/ui/toast'
import { ref, onMounted } from 'vue'
import { Loader2 } from 'lucide-vue-next'

const themeStore = useThemeStore()
const auth = useAuthStore()
const isInitialized = ref(true)

onMounted(() => {
  themeStore.updateTheme()
})
</script>

<template>
  <div :class="{ dark: themeStore.theme === 'dark' }">
    <main class="min-h-screen bg-background text-foreground">
      <Toaster />
      <RouterView />
    </main>
  </div>
</template>
