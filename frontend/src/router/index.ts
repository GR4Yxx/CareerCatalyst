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
    // Regular user routes
    {
      path: '/dashboard',
      component: () => import('@/layouts/UserLayout.vue'),
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
