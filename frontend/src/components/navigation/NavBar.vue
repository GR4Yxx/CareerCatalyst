<template>
  <header
    class="sticky top-0 z-50 w-full border-b border-slate-800 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60"
  >
    <div class="flex h-16 items-center justify-between w-full">
      <!-- Logo -->
      <div class="flex items-center ml-4">
        <RouterLink to="/" class="flex items-center">
          <NetworkinLogo class="h-8 w-8" />
        </RouterLink>
      </div>

      <!-- Title -->
      <div class="flex-1 max-w-md mx-4">
        <h1 class="text-xl font-semibold">Dashboard</h1>
      </div>

      <!-- Right Actions -->
      <div class="flex items-center space-x-2 mr-4">
        <!-- Theme Toggle (Dropdown) -->
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="icon" class="h-9 w-9 text-slate-300">
              <Sun v-if="currentTheme === 'light'" class="h-5 w-5" />
              <Moon v-if="currentTheme === 'dark'" class="h-5 w-5" />
              <Monitor v-if="currentTheme === 'system'" class="h-5 w-5" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent class="bg-slate-900 border border-slate-700" align="end">
            <DropdownMenuItem
              @click="themeStore.setTheme('light')"
              class="text-slate-300 focus:bg-slate-800 focus:text-white cursor-pointer"
            >
              <Sun class="mr-2 h-4 w-4" />
              Light
            </DropdownMenuItem>
            <DropdownMenuItem
              @click="themeStore.setTheme('dark')"
              class="text-slate-300 focus:bg-slate-800 focus:text-white cursor-pointer"
            >
              <Moon class="mr-2 h-4 w-4" />
              Dark
            </DropdownMenuItem>
            <DropdownMenuItem
              @click="themeStore.setTheme('system')"
              class="text-slate-300 focus:bg-slate-800 focus:text-white cursor-pointer"
            >
              <Monitor class="mr-2 h-4 w-4" />
              System
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>

        <!-- User Profile -->
        <DropdownMenu v-if="auth.isAuthenticated">
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="icon" class="relative h-9 w-9 rounded-full ml-1">
              <Avatar class="h-8 w-8 ring-1 ring-slate-700">
                <AvatarImage
                  :src="auth.user?.avatar_path || ''"
                  :alt="auth.user?.username || 'User'"
                />
                <AvatarFallback class="bg-slate-800 text-slate-200">
                  {{ getUserInitials }}
                </AvatarFallback>
              </Avatar>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent class="w-56 bg-slate-900 border border-slate-700" align="end">
            <DropdownMenuLabel class="font-normal">
              <div class="flex flex-col space-y-1">
                <p class="text-sm font-medium leading-none text-slate-200">
                  {{ auth.user?.first_name }} {{ auth.user?.last_name }}
                </p>
                <p class="text-xs leading-none text-slate-400">{{ auth.user?.username }}</p>
              </div>
            </DropdownMenuLabel>
            <DropdownMenuSeparator class="bg-slate-700" />
            <DropdownMenuItem
              @click="handleLogout"
              class="text-red-400 focus:text-red-300 focus:bg-slate-800 cursor-pointer"
            >
              <LogOut class="mr-2 h-4 w-4" />
              <span>Log out</span>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useThemeStore } from '@/stores/theme'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/components/ui/toast'
import { Button } from '@/components/ui/button'
import { Avatar, AvatarImage, AvatarFallback } from '@/components/ui/avatar'
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
} from '@/components/ui/dropdown-menu'
import { Sun, Moon, Monitor, LogOut } from 'lucide-vue-next'
import NetworkinLogo from '@/components/icons/NetworkinLogo.vue'

const auth = useAuthStore()
const themeStore = useThemeStore()
const router = useRouter()
const { toast } = useToast()

const currentTheme = computed(() => themeStore.theme)

// Get user initials for avatar fallback
const getUserInitials = computed(() => {
  if (!auth.user) return 'U'

  const first = auth.user.first_name?.[0] || ''
  const last = auth.user.last_name?.[0] || ''

  if (first && last) return `${first}${last}`
  if (first) return first
  if (auth.user.username) return auth.user.username[0].toUpperCase()
  return 'U'
})

async function handleLogout() {
  try {
    await auth.logout()
    toast({
      title: 'Logged out',
      description: 'You have been successfully logged out.',
    })
    router.push('/login')
  } catch (error) {
    console.error('Logout error:', error)
    toast({
      variant: 'destructive',
      title: 'Error',
      description: 'Failed to log out. Please try again.',
    })
  }
}
</script>
