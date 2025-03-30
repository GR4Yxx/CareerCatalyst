// router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/dashboard',
    },
    {
      path: '/login',
      component: () => import('@/views/auth/LoginView.vue'),
    },
    // Main routes
    {
      path: '/dashboard',
      component: () => import('@/layouts/MainLayout.vue'),
      children: [
        {
          path: '',
          component: () => import('@/views/dashboard/DashboardView.vue'),
        },
        {
          path: 'skills',
          component: () => import('@/views/dashboard/SkillsView.vue'),
        },
        {
          path: 'job-finder',
          component: () => import('@/views/dashboard/JobFinderView.vue'),
        },
        {
          path: 'ats-intelligence',
          component: () => import('@/views/dashboard/AtsIntelligenceView.vue'),
        },
        {
          path: 'career-path',
          component: () => import('@/views/dashboard/CareerPathView.vue'),
        },
        // User profile menu routes
        {
          path: 'profile',
          component: () => import('@/views/profile/ProfileView.vue'),
        },
        {
          path: 'settings',
          component: () => import('@/views/profile/SettingsView.vue'),
        },
        {
          path: 'resumes',
          component: () => import('@/views/profile/ResumesView.vue'),
        },
        {
          path: 'saved-jobs',
          component: () => import('@/views/profile/SavedJobsView.vue'),
        },
        {
          path: 'applications',
          component: () => import('@/views/profile/ApplicationsView.vue'),
        },
        {
          path: 'notifications',
          component: () => import('@/views/profile/NotificationsView.vue'),
        },
      ],
    },
    // Catch all route for 404
    {
      path: '/:pathMatch(.*)*',
      redirect: '/',
    },
  ],
})

export default router
