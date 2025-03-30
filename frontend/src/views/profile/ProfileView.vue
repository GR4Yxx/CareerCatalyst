<template>
  <div class="profile-view">
    <h1 class="text-2xl font-bold mb-6 flex items-center">
      <User class="h-7 w-7 mr-3 text-primary" />
      Profile
    </h1>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <!-- Profile Information -->
      <div class="md:col-span-2 space-y-6">
        <div class="p-6 bg-card rounded-lg border shadow-sm">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-xl font-semibold">Personal Information</h2>
            <Button variant="outline" size="sm">
              <Pencil class="h-4 w-4 mr-2" />
              Edit
            </Button>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="text-sm font-medium text-muted-foreground">First Name</label>
              <p class="mt-1">{{ auth.user?.first_name || 'John' }}</p>
            </div>
            <div>
              <label class="text-sm font-medium text-muted-foreground">Last Name</label>
              <p class="mt-1">{{ auth.user?.last_name || 'Doe' }}</p>
            </div>
            <div>
              <label class="text-sm font-medium text-muted-foreground">Username</label>
              <p class="mt-1">{{ auth.user?.username || 'johndoe' }}</p>
            </div>
            <div>
              <label class="text-sm font-medium text-muted-foreground">Email</label>
              <p class="mt-1">{{ auth.user?.primary_email || 'john.doe@example.com' }}</p>
            </div>
            <div>
              <label class="text-sm font-medium text-muted-foreground">Phone</label>
              <p class="mt-1">{{ auth.user?.phone || '+1 123-456-7890' }}</p>
            </div>
            <div>
              <label class="text-sm font-medium text-muted-foreground">Role</label>
              <p class="mt-1 capitalize">{{ auth.user?.role || 'regular' }}</p>
            </div>
          </div>
        </div>

        <div class="p-6 bg-card rounded-lg border shadow-sm">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-xl font-semibold">Professional Information</h2>
            <Button variant="outline" size="sm">
              <Pencil class="h-4 w-4 mr-2" />
              Edit
            </Button>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="text-sm font-medium text-muted-foreground">Current Position</label>
              <p class="mt-1">Frontend Developer</p>
            </div>
            <div>
              <label class="text-sm font-medium text-muted-foreground">Company</label>
              <p class="mt-1">{{ auth.user?.company_name || 'Tech Solutions Inc.' }}</p>
            </div>
            <div class="md:col-span-2">
              <label class="text-sm font-medium text-muted-foreground">Bio</label>
              <p class="mt-1">
                {{
                  auth.user?.bio ||
                  'Passionate frontend developer with 5+ years of experience building modern, responsive web applications using Vue.js, TypeScript, and related technologies.'
                }}
              </p>
            </div>
          </div>
        </div>

        <div class="p-6 bg-card rounded-lg border shadow-sm">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-xl font-semibold">Account Security</h2>
            <Button variant="outline" size="sm">
              <Pencil class="h-4 w-4 mr-2" />
              Edit
            </Button>
          </div>

          <div class="space-y-4">
            <div>
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="font-medium">Password</h3>
                  <p class="text-sm text-muted-foreground">Last updated 2 months ago</p>
                </div>
                <Button variant="ghost" size="sm">Change Password</Button>
              </div>
            </div>
            <Separator />
            <div>
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="font-medium">Two-Factor Authentication</h3>
                  <p class="text-sm text-muted-foreground">
                    {{ auth.user?.two_factor_enabled ? 'Enabled' : 'Not enabled' }}
                  </p>
                </div>
                <Button variant="ghost" size="sm">Setup 2FA</Button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Sidebar -->
      <div class="space-y-6">
        <div class="p-6 bg-card rounded-lg border shadow-sm">
          <div class="flex flex-col items-center">
            <Avatar class="h-24 w-24 mb-4">
              <AvatarImage
                :src="auth.user?.avatar_path || ''"
                :alt="auth.user?.username || 'User'"
              />
              <AvatarFallback class="text-2xl">{{ getUserInitials }}</AvatarFallback>
            </Avatar>
            <h2 class="text-xl font-semibold">
              {{ auth.user?.first_name }} {{ auth.user?.last_name }}
            </h2>
            <p class="text-sm text-muted-foreground mb-4">{{ auth.user?.username }}</p>
            <Button class="w-full">
              <Upload class="h-4 w-4 mr-2" />
              Change Avatar
            </Button>
          </div>
        </div>

        <div class="p-6 bg-card rounded-lg border shadow-sm">
          <h3 class="font-semibold mb-4">Account Status</h3>
          <div class="space-y-2">
            <div class="flex justify-between items-center">
              <span class="text-sm">Member Since</span>
              <span class="text-sm font-medium">Jan 2023</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-sm">Last Login</span>
              <span class="text-sm font-medium">Today</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-sm">Email Verified</span>
              <Badge variant="success">Verified</Badge>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-sm">Subscription</span>
              <Badge>Free</Badge>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { User, Pencil, Upload } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Avatar, AvatarImage, AvatarFallback } from '@/components/ui/avatar'
import { Separator } from '@/components/ui/separator'
import { Badge } from '@/components/ui/badge'

const auth = useAuthStore()

// Get user initials for avatar fallback
const getUserInitials = computed(() => {
  if (!auth.user) return 'JD'

  const first = auth.user.first_name?.[0] || ''
  const last = auth.user.last_name?.[0] || ''

  if (first && last) return `${first}${last}`
  if (first) return first
  if (auth.user.username) return auth.user.username[0].toUpperCase()
  return 'U'
})
</script>
