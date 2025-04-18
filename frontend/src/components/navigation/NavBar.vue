<template>
  <header
    class="sticky top-0 z-50 w-full border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60"
  >
    <div class="flex h-16 items-center justify-between w-full">
      <!-- Logo -->
      <div class="flex items-center ml-4">
        <RouterLink to="/" class="flex items-center space-x-2">
          <div class="p-1.5 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg shadow-md">
            <Rocket class="h-6 w-6 text-white" />
          </div>
          <span
            class="text-xl font-bold bg-gradient-to-r from-blue-500 to-purple-600 bg-clip-text text-transparent"
          >
            Career Catalyst
          </span>
        </RouterLink>
      </div>

      <!-- Right Actions -->
      <div class="flex items-center space-x-2 mr-4">
        <!-- Theme Toggle (Dropdown) -->
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="icon" class="h-9 w-9">
              <Sun v-if="currentTheme === 'light'" class="h-5 w-5" />
              <Moon v-if="currentTheme === 'dark'" class="h-5 w-5" />
              <Monitor v-if="currentTheme === 'system'" class="h-5 w-5" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
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

        <!-- User Profile -->
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="icon" class="relative h-9 w-9 rounded-full ml-1">
              <Avatar class="h-8 w-8 ring-1 ring-border">
                <AvatarFallback class="bg-muted text-muted-foreground">
                  {{ getUserInitials }}
                </AvatarFallback>
              </Avatar>
              <span
                class="absolute bottom-0 right-0 h-2.5 w-2.5 rounded-full bg-green-500 border border-background"
              ></span>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent class="w-64" align="end">
            <div class="p-3 border-b border-border">
              <div class="flex items-center gap-3">
                <Avatar class="h-10 w-10 ring-1 ring-border">
                  <AvatarFallback class="bg-muted text-muted-foreground">
                    {{ getUserInitials }}
                  </AvatarFallback>
                </Avatar>
                <div class="flex flex-col space-y-0.5">
                  <p class="text-sm font-medium leading-none">
                    {{ auth.user?.name }}
                  </p>
                  <p class="text-xs leading-none text-muted-foreground">{{ auth.user?.email }}</p>
                  <div class="flex items-center mt-1">
                    <div class="h-2 w-2 rounded-full bg-green-500 mr-1.5"></div>
                    <span class="text-xs text-green-500">Online</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="p-2">
              <h3 class="text-xs font-medium text-muted-foreground px-2 pb-1.5">Account</h3>
              <RouterLink to="/dashboard/profile">
                <DropdownMenuItem class="cursor-pointer">
                  <User class="mr-2 h-4 w-4" />
                  <span>Profile</span>
                </DropdownMenuItem>
              </RouterLink>
              <RouterLink to="/dashboard/settings">
                <DropdownMenuItem class="cursor-pointer">
                  <Settings class="mr-2 h-4 w-4" />
                  <span>Settings</span>
                </DropdownMenuItem>
              </RouterLink>
              <RouterLink to="/dashboard/resumes">
                <DropdownMenuItem class="cursor-pointer">
                  <FileText class="mr-2 h-4 w-4" />
                  <span>My Resumes</span>
                </DropdownMenuItem>
              </RouterLink>
            </div>

            <div class="p-2 border-t border-border">
              <h3 class="text-xs font-medium text-muted-foreground px-2 pb-1.5">Career</h3>
              <RouterLink to="/dashboard/saved-jobs">
                <DropdownMenuItem class="cursor-pointer">
                  <Briefcase class="mr-2 h-4 w-4" />
                  <span>Saved Jobs</span>
                </DropdownMenuItem>
              </RouterLink>
              <RouterLink to="/dashboard/applications">
                <DropdownMenuItem class="cursor-pointer">
                  <ClipboardCheck class="mr-2 h-4 w-4" />
                  <span>Applications</span>
                </DropdownMenuItem>
              </RouterLink>
              <RouterLink to="/dashboard/notifications">
                <DropdownMenuItem class="cursor-pointer">
                  <Bell class="mr-2 h-4 w-4" />
                  <span>Notifications</span>
                  <Badge variant="default" class="ml-auto h-5 bg-primary text-primary-foreground"
                    >3</Badge
                  >
                </DropdownMenuItem>
              </RouterLink>
            </div>

            <div class="p-2 border-t border-border">
              <DropdownMenuItem
                @click="handleLogout"
                class="cursor-pointer text-destructive focus:text-destructive"
              >
                <LogOut class="mr-2 h-4 w-4" />
                <span>Log out</span>
              </DropdownMenuItem>
            </div>
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
import { Badge } from '@/components/ui/badge'
import { Avatar, AvatarImage, AvatarFallback } from '@/components/ui/avatar'
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
} from '@/components/ui/dropdown-menu'
import {
  Sun,
  Moon,
  Monitor,
  LogOut,
  Rocket,
  User,
  Settings,
  FileText,
  Briefcase,
  ClipboardCheck,
  Bell,
} from 'lucide-vue-next'

const auth = useAuthStore()
const themeStore = useThemeStore()
const router = useRouter()
const { toast } = useToast()

const currentTheme = computed(() => themeStore.theme)

// Get user initials for avatar fallback
const getUserInitials = computed(() => {
  if (!auth.user) return 'U'

  if (auth.user.name) {
    const nameParts = auth.user.name.split(' ')
    if (nameParts.length > 1) {
      return `${nameParts[0][0]}${nameParts[1][0]}`.toUpperCase()
    }
    return nameParts[0][0].toUpperCase()
  }

  if (auth.user.email) {
    return auth.user.email[0].toUpperCase()
  }

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
