// /src/views/dashboard/DashboardView.vue
<template>
  <div class="user-dashboard">
    <h1 class="text-2xl font-bold mb-6 flex items-center">
      <LayoutDashboard class="h-7 w-7 mr-3 text-primary" />
      Dashboard
    </h1>

    <!-- Dashboard Overview Section -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
      <DashboardCard title="Welcome" :count="1">
        <User class="h-8 w-8" />
      </DashboardCard>
    </div>

    <!-- Welcome Section -->
    <div class="mb-8">
      <div class="p-6 bg-card rounded-lg border shadow-sm">
        <h2 class="text-xl font-semibold mb-4">Welcome to Your Dashboard</h2>
        <p class="mb-4">
          This is a simplified dashboard with only the login and dashboard functionality.
        </p>
        <p>You can customize this dashboard according to your needs.</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { LayoutDashboard, User } from 'lucide-vue-next'
import DashboardCard from '@/components/dashboard/DashboardCard.vue'
</script>
