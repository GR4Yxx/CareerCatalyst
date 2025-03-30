<template>
  <div class="h-screen flex flex-col overflow-hidden">
    <Navbar class="flex-shrink-0" />
    <div class="flex-1 flex overflow-hidden">
      <Sheet v-model:open="mobileMenuOpen" side="left">
        <SheetContent class="w-[240px] sm:w-[300px]" side="left">
          <div class="py-4">
            <nav>
              <div class="space-y-1 mt-2">
                <RouterLink
                  v-for="item in menuItems"
                  :key="item.path"
                  :to="item.path"
                  class="flex items-center px-4 py-2 rounded-md hover:bg-accent"
                  :class="{ 'bg-accent': isActive(item.path) }"
                  @click="mobileMenuOpen = false"
                >
                  <component :is="item.icon" class="h-5 w-5 mr-3" />
                  <span>{{ item.label }}</span>
                </RouterLink>
              </div>
            </nav>
          </div>
        </SheetContent>
      </Sheet>

      <aside class="hidden md:block w-[240px] border-r border-border flex-shrink-0">
        <div class="py-4">
          <nav>
            <div class="space-y-1 mt-2">
              <RouterLink
                v-for="item in menuItems"
                :key="item.path"
                :to="item.path"
                class="flex items-center px-4 py-2 rounded-md hover:bg-accent"
                :class="{ 'bg-accent': isActive(item.path) }"
              >
                <component :is="item.icon" class="h-5 w-5 mr-3" />
                <span>{{ item.label }}</span>
              </RouterLink>
            </div>
          </nav>
        </div>
      </aside>

      <main class="flex-1 p-6 overflow-y-auto">
        <div class="md:hidden mb-4">
          <Button variant="outline" size="sm" @click="mobileMenuOpen = true">
            <Menu class="h-5 w-5 mr-2" />
            Menu
          </Button>
        </div>
        <RouterView v-slot="{ Component }">
          <component :is="Component" />
        </RouterView>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, RouterView, useRoute } from 'vue-router'
import Navbar from '@/components/navigation/NavBar.vue'
import { LayoutDashboard, Menu, Sparkles, Briefcase, FileSearch, Map } from 'lucide-vue-next'
import { Sheet, SheetContent } from '@/components/ui/sheet'
import { Separator } from '@/components/ui/separator'
import { Button } from '@/components/ui/button'

const route = useRoute()
const mobileMenuOpen = ref(false)

const menuItems = [
  { label: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
  { label: 'Skills Intelligence', path: '/dashboard/skills', icon: Sparkles },
  { label: 'Job Finder', path: '/dashboard/job-finder', icon: Briefcase },
  { label: 'ATS Intelligence', path: '/dashboard/ats-intelligence', icon: FileSearch },
  { label: 'Career Path', path: '/dashboard/career-path', icon: Map },
]

const isActive = (path: string) => {
  // For the dashboard path, only highlight if it's an exact match
  if (path === '/dashboard') {
    return route.path === '/dashboard'
  }

  // For other paths, check if the route starts with the path
  return route.path.startsWith(path)
}
</script>
