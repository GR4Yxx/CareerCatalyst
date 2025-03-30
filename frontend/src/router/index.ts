// router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { h } from 'vue'

// Simple NotFound component
const NotFound = h('div', { class: 'flex flex-col items-center justify-center min-h-screen' }, [
  h('h1', { class: 'text-6xl font-bold mb-4' }, '404'),
  h('p', { class: 'text-xl mb-6' }, 'Page not found'),
  h('a', { class: 'text-blue-500 hover:underline', href: '/' }, 'Go home'),
])

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/dashboard',
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/auth/LoginView.vue'),
      meta: { requiresGuest: true },
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/auth/RegisterView.vue'),
      meta: { requiresGuest: true },
    },
    {
      path: '/dashboard',
      component: () => import('../layouts/MainLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'dashboard',
          component: () => import('../views/dashboard/DashboardView.vue'),
        },
        {
          path: 'profile',
          name: 'profile',
          component: () => import('../views/profile/ProfileView.vue'),
        },
        {
          path: 'settings',
          name: 'settings',
          component: () => import('../views/profile/SettingsView.vue'),
        },
        {
          path: 'resumes',
          name: 'resumes',
          component: () => import('../views/profile/ResumesView.vue'),
        },
        {
          path: 'saved-jobs',
          name: 'saved-jobs',
          component: () => import('../views/profile/SavedJobsView.vue'),
        },
        {
          path: 'applications',
          name: 'applications',
          component: () => import('../views/profile/ApplicationsView.vue'),
        },
        {
          path: 'notifications',
          name: 'notifications',
          component: () => import('../views/profile/NotificationsView.vue'),
        },
        {
          path: 'job-finder',
          name: 'job-finder',
          component: () => import('../views/dashboard/JobFinderView.vue'),
        },
        {
          path: 'ats-intelligence',
          name: 'ats-intelligence',
          component: () => import('../views/dashboard/AtsIntelligenceView.vue'),
        },
        {
          path: 'career-path',
          name: 'career-path',
          component: () => import('../views/dashboard/CareerPathView.vue'),
        },
        {
          path: 'skills',
          name: 'skills',
          component: () => import('../views/dashboard/SkillsView.vue'),
        },
      ],
    },
    // Wildcard route for 404
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: { render: () => NotFound },
    },
  ],
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const isAuthenticated = authStore.isAuthenticated

  // Routes that require authentication
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
    return
  }

  // Routes that should not be accessible when logged in (like login, register)
  if (to.meta.requiresGuest && isAuthenticated) {
    next({ name: 'dashboard' })
    return
  }

  next()
})

export default router
