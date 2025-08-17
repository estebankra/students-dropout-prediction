export default [
  {
    path: '/sign-in',
    name: 'SignIn',
    component: () => import('@/views/SignIn.vue'),
    meta: { requiresAuth: false }
  }
]
