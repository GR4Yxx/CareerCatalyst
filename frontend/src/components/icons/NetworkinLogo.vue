<template>
  <img :src="currentLogo" alt="Networkin Logo" :style="{ height: '32px', width: 'auto' }" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useThemeStore } from '@/stores/theme'

const themeStore = useThemeStore()

const currentLogo = computed(() =>
  themeStore.isDark ? '/src/assets/svgs/logo-dark.svg' : '/src/assets/svgs/logo-light.svg',
)
</script>
