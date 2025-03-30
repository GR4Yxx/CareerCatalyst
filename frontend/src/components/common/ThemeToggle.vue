<template>
  <DropdownMenu>
    <DropdownMenuTrigger asChild>
      <Button
        variant="outline"
        size="icon"
        class="w-[52px] h-[52px] rounded-lg border-[0.5px] border-gray-600/25 hover:border-gray-600/40 p-0"
      >
        <Sun v-if="currentTheme === 'light'" class="h-4 w-4" />
        <Moon v-if="currentTheme === 'dark'" class="h-4 w-4" />
        <Monitor v-if="currentTheme === 'system'" class="h-4 w-4" />
        <span class="sr-only">Toggle theme</span>
      </Button>
    </DropdownMenuTrigger>
    <DropdownMenuContent align="end" class="min-w-[120px]">
      <DropdownMenuItem @click="themeStore.setTheme('light')" class="cursor-pointer">
        <Sun class="mr-2 h-4 w-4" />
        Light
      </DropdownMenuItem>
      <DropdownMenuItem @click="themeStore.setTheme('dark')" class="cursor-pointer">
        <Moon class="mr-2 h-4 w-4" />
        Dark
      </DropdownMenuItem>
      <DropdownMenuItem @click="themeStore.setTheme('system')" class="cursor-pointer">
        <Monitor class="mr-2 h-4 w-4" />
        System
      </DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>
</template>

<script setup lang="ts">
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
} from '@/components/ui/dropdown-menu'
import { Button } from '@/components/ui/button'
import { Sun, Moon, Monitor } from 'lucide-vue-next'
import { useThemeStore } from '@/stores/theme'
import { computed } from 'vue'

const themeStore = useThemeStore()
const currentTheme = computed(() => themeStore.theme)
</script>
