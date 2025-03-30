// router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: () => {
        const auth = useAuthStore()
        if (!auth.isAuthenticated) return '/login'
        return '/dashboard'
      },
    },
    {
      path: '/login',
      component: () => import('@/views/auth/LoginView.vue'),
      meta: { requiresGuest: true },
    },
    // Regular user routes
    {
      path: '/dashboard',
      component: () => import('@/layouts/UserLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          component: () => import('@/views/dashboard/DashboardView.vue'),
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

// Navigation guard
router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore()

  // Check if token exists in localStorage but user is not authenticated in store
  if (!auth.isAuthenticated && localStorage.getItem('token')) {
    await auth.checkAuth()
  }

  // Redirect to login if route requires authentication and user is not authenticated
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    next('/login')
    return
  }

  // Redirect to dashboard if route requires guest and user is authenticated
  if (to.meta.requiresGuest && auth.isAuthenticated) {
    next('/dashboard')
    return
  }

  next()
})

export default router
