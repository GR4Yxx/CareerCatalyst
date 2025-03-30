import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

type Theme = 'dark' | 'light' | 'system'

export const useThemeStore = defineStore('theme', () => {
  const theme = ref<Theme>((localStorage.getItem('theme') as Theme) || 'system')

  const isDark = computed(() => {
    const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    return theme.value === 'dark' || (theme.value === 'system' && systemDark)
  })

  const updateTheme = () => {
    const storedTheme = localStorage.getItem('theme') as Theme | null
    if (storedTheme) {
      theme.value = storedTheme
      document.documentElement.classList.toggle('dark', isDark.value)
    }
  }

  const setTheme = (newTheme: Theme) => {
    theme.value = newTheme
    localStorage.setItem('theme', newTheme)
    document.documentElement.classList.toggle('dark', isDark.value)
  }

  document.documentElement.classList.toggle('dark', isDark.value)

  return {
    theme,
    isDark,
    setTheme,
    updateTheme,
  }
})
