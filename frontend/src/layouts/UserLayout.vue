<template>
  <div class="min-h-screen flex flex-col">
    <Navbar />
    <div class="flex-1 flex">
      <Sheet v-model:open="mobileMenuOpen" side="left">
        <SheetContent class="w-[240px] sm:w-[300px]" side="left">
          <div class="py-4">
            <h2 class="text-lg font-semibold px-4 mb-2">Dashboard</h2>
            <nav>
              <Separator />
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

      <aside class="hidden md:block w-[240px] border-r border-border h-[calc(100vh-64px)]">
        <div class="py-4">
          <h2 class="text-lg font-semibold px-4 mb-2">Dashboard</h2>
          <nav>
            <Separator />
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

      <main class="flex-1 p-6 overflow-auto">
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
import { LayoutDashboard, Menu } from 'lucide-vue-next'
import { Sheet, SheetContent } from '@/components/ui/sheet'
import { Separator } from '@/components/ui/separator'
import { Button } from '@/components/ui/button'

const route = useRoute()
const mobileMenuOpen = ref(false)

const menuItems = [{ label: 'Dashboard', path: '/dashboard', icon: LayoutDashboard }]

const isActive = (path: string) => {
  return route.path === path || route.path.startsWith(`${path}/`)
}
</script>
