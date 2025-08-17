import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import Home from '@/views/Home.vue'

import authRoutes from './auth'
import adminRoutes from './admin'
import supervisorRoutes from './supervisor'
import studentsRoutes from './students'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
      meta: { requiresAuth: true }
    },
    ...authRoutes,
    ...adminRoutes,
    ...supervisorRoutes,
    ...studentsRoutes
  ],
  scrollBehavior() {
    return { top: 0, behavior: 'auto' }
  }
})

router.beforeEach(async (to, _, next) => {
  const userStore = useUserStore()

  if (userStore.isAuthenticated) {
    next()
    return
  }

  if (to.matched.some((record) => record.meta.requiresAuth)) {
    await userStore.fetchCurrentUser()
    if (userStore.isAuthenticated) {
      next()
    } else {
      next('/sign-in')
    }
  } else {
    next()
  }
})

export default router
