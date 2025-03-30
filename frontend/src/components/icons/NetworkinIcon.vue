<template>
  <img :src="isDark ? '@/assets/icon-dark.svg' : '@/assets/icon-light.svg'" alt="Networkin Icon" />
</template>

<script setup lang="ts">
import { useThemeStore } from '@/stores/theme'
const { isDark } = useThemeStore()
</script>
