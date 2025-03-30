import { ref } from 'vue'

type Theme = 'dark' | 'light' | 'system'

export function useTheme() {
  const theme = ref<Theme>('system')

  const setTheme = (newTheme: Theme) => {
    theme.value = newTheme

    // Apply theme to document
    if (newTheme === 'system') {
      const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches
        ? 'dark'
        : 'light'
      document.documentElement.classList.toggle('dark', systemTheme === 'dark')
    } else {
      document.documentElement.classList.toggle('dark', newTheme === 'dark')
    }

    // Store theme preference
    localStorage.setItem('theme', newTheme)
  }

  // Initialize theme from stored preference
  const storedTheme = localStorage.getItem('theme') as Theme | null
  if (storedTheme) {
    setTheme(storedTheme)
  } else {
    setTheme('system')
  }

  // Watch for system theme changes
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    if (theme.value === 'system') {
      document.documentElement.classList.toggle('dark', e.matches)
    }
  })

  return {
    theme,
    setTheme,
  }
}
