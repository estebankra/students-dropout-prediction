export default [
  {
    path: '/supervisor/students',
    name: 'SupervisorStudents',
    component: () => import('@/views/supervisor/Students.vue'),
    meta: { requiresAuth: true }
  }
]
