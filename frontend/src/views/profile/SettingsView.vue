<template>
  <div class="settings-view">
    <h1 class="text-2xl font-bold mb-6 flex items-center">
      <Settings class="h-7 w-7 mr-3 text-primary" />
      Settings
    </h1>

    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <!-- Sidebar Navigation -->
      <div class="md:col-span-1">
        <div class="p-4 bg-card rounded-lg border shadow-sm">
          <nav class="space-y-1">
            <button
              v-for="(section, index) in settingSections"
              :key="index"
              class="w-full flex items-center px-3 py-2 text-sm rounded-md"
              :class="
                activeSection === index ? 'bg-primary text-primary-foreground' : 'hover:bg-accent'
              "
              @click="activeSection = index"
            >
              <component :is="section.icon" class="h-4 w-4 mr-2" />
              {{ section.name }}
            </button>
          </nav>
        </div>
      </div>

      <!-- Main Content -->
      <div class="md:col-span-3">
        <div class="p-6 bg-card rounded-lg border shadow-sm">
          <h2 class="text-xl font-semibold mb-6">
            {{ settingSections[activeSection].name }}
          </h2>

          <!-- Appearance Settings -->
          <div v-if="activeSection === 0" class="space-y-6">
            <div class="space-y-3">
              <h3 class="text-lg font-medium">Theme</h3>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                <Button
                  variant="outline"
                  class="justify-start"
                  :class="{ 'border-primary': themeStore.theme === 'light' }"
                  @click="themeStore.setTheme('light')"
                >
                  <Sun class="h-4 w-4 mr-2" />
                  Light
                </Button>
                <Button
                  variant="outline"
                  class="justify-start"
                  :class="{ 'border-primary': themeStore.theme === 'dark' }"
                  @click="themeStore.setTheme('dark')"
                >
                  <Moon class="h-4 w-4 mr-2" />
                  Dark
                </Button>
                <Button
                  variant="outline"
                  class="justify-start"
                  :class="{ 'border-primary': themeStore.theme === 'system' }"
                  @click="themeStore.setTheme('system')"
                >
                  <Monitor class="h-4 w-4 mr-2" />
                  System
                </Button>
              </div>
            </div>

            <Separator />

            <div class="space-y-3">
              <h3 class="text-lg font-medium">Font Size</h3>
              <div class="flex items-center space-x-3">
                <span class="text-sm">A</span>
                <Slider
                  :min="12"
                  :max="20"
                  :step="1"
                  :model-value="[fontSize]"
                  @update:model-value="(value) => (fontSize = value[0])"
                />
                <span class="text-base">A</span>
              </div>
              <p class="text-sm text-muted-foreground">
                Adjust the font size for better readability.
              </p>
            </div>
          </div>

          <!-- Notification Settings -->
          <div v-if="activeSection === 1" class="space-y-6">
            <div class="space-y-3">
              <h3 class="text-lg font-medium">Email Notifications</h3>
              <div class="space-y-2">
                <div class="flex items-center justify-between">
                  <div>
                    <label class="font-medium">Job Matches</label>
                    <p class="text-sm text-muted-foreground">
                      Get notified when new jobs match your profile
                    </p>
                  </div>
                  <Switch :model-value="true" />
                </div>
                <div class="flex items-center justify-between">
                  <div>
                    <label class="font-medium">Application Updates</label>
                    <p class="text-sm text-muted-foreground">
                      Get notified about your job application status
                    </p>
                  </div>
                  <Switch :model-value="true" />
                </div>
                <div class="flex items-center justify-between">
                  <div>
                    <label class="font-medium">Career Insights</label>
                    <p class="text-sm text-muted-foreground">Receive career tips and insights</p>
                  </div>
                  <Switch :model-value="false" />
                </div>
              </div>
            </div>

            <Separator />

            <div class="space-y-3">
              <h3 class="text-lg font-medium">Push Notifications</h3>
              <div class="space-y-2">
                <div class="flex items-center justify-between">
                  <div>
                    <label class="font-medium">Browser Notifications</label>
                    <p class="text-sm text-muted-foreground">
                      Allow browser notifications for important updates
                    </p>
                  </div>
                  <Switch :model-value="false" />
                </div>
              </div>
            </div>
          </div>

          <!-- Account Settings -->
          <div v-if="activeSection === 2" class="space-y-6">
            <div class="space-y-3">
              <h3 class="text-lg font-medium">Account Information</h3>
              <div class="space-y-4">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div class="space-y-2">
                    <label for="email" class="block text-sm font-medium">Email</label>
                    <Input
                      id="email"
                      :value="auth.user?.primary_email || 'john.doe@example.com'"
                      disabled
                    />
                  </div>
                  <div class="space-y-2">
                    <label for="username" class="block text-sm font-medium">Username</label>
                    <Input id="username" :value="auth.user?.username || 'johndoe'" />
                  </div>
                </div>
                <Button>Update Information</Button>
              </div>
            </div>

            <Separator />

            <div class="space-y-3">
              <h3 class="text-lg font-medium">Password</h3>
              <div class="space-y-4">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div class="space-y-2">
                    <label for="current-password" class="block text-sm font-medium"
                      >Current Password</label
                    >
                    <Input id="current-password" type="password" placeholder="••••••••" />
                  </div>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div class="space-y-2">
                    <label for="new-password" class="block text-sm font-medium">New Password</label>
                    <Input id="new-password" type="password" placeholder="••••••••" />
                  </div>
                  <div class="space-y-2">
                    <label for="confirm-password" class="block text-sm font-medium"
                      >Confirm Password</label
                    >
                    <Input id="confirm-password" type="password" placeholder="••••••••" />
                  </div>
                </div>
                <Button>Change Password</Button>
              </div>
            </div>

            <Separator />

            <div class="space-y-3">
              <h3 class="text-lg font-medium">Danger Zone</h3>
              <div
                class="p-4 border border-red-200 bg-red-50 dark:bg-red-950/20 dark:border-red-900 rounded-md"
              >
                <h4 class="font-medium text-red-700 dark:text-red-400">Delete Account</h4>
                <p class="text-sm text-red-600 dark:text-red-300 mb-4">
                  Once you delete your account, there is no going back. Please be certain.
                </p>
                <Button variant="destructive">Delete Account</Button>
              </div>
            </div>
          </div>

          <!-- Privacy Settings -->
          <div v-if="activeSection === 3" class="space-y-6">
            <div class="space-y-3">
              <h3 class="text-lg font-medium">Profile Privacy</h3>
              <div class="space-y-2">
                <div class="flex items-center justify-between">
                  <div>
                    <label class="font-medium">Public Profile</label>
                    <p class="text-sm text-muted-foreground">
                      Make your profile visible to recruiters and employers
                    </p>
                  </div>
                  <Switch :model-value="true" />
                </div>
                <div class="flex items-center justify-between">
                  <div>
                    <label class="font-medium">Show Skills</label>
                    <p class="text-sm text-muted-foreground">
                      Display your skills on your public profile
                    </p>
                  </div>
                  <Switch :model-value="true" />
                </div>
              </div>
            </div>

            <Separator />

            <div class="space-y-3">
              <h3 class="text-lg font-medium">Data Usage</h3>
              <div class="space-y-2">
                <div class="flex items-center justify-between">
                  <div>
                    <label class="font-medium">Personalized Recommendations</label>
                    <p class="text-sm text-muted-foreground">
                      Allow us to use your data for personalized job recommendations
                    </p>
                  </div>
                  <Switch :model-value="true" />
                </div>
                <div class="flex items-center justify-between">
                  <div>
                    <label class="font-medium">Analytics Cookies</label>
                    <p class="text-sm text-muted-foreground">
                      Allow us to use cookies to improve your experience
                    </p>
                  </div>
                  <Switch :model-value="false" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'
import { Settings, Palette, Bell, User, ShieldCheck, Sun, Moon, Monitor } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Switch } from '@/components/ui/switch'
import { Separator } from '@/components/ui/separator'
import { Slider } from '@/components/ui/slider'

const auth = useAuthStore()
const themeStore = useThemeStore()
const activeSection = ref(0)
const fontSize = ref(16)

const settingSections = [
  { name: 'Appearance', icon: Palette },
  { name: 'Notifications', icon: Bell },
  { name: 'Account', icon: User },
  { name: 'Privacy', icon: ShieldCheck },
]
</script>
