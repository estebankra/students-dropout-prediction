export default [
  {
    path: '/students',
    name: 'StudentsRegistration',
    component: () => import('@/views/students/Registration.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/students/new',
    name: 'StudentsNewRegistration',
    component: () => import('@/views/students/NewRegistration.vue'),
    meta: { requiresAuth: false }
  }
]
