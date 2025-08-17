export default [
  {
    path: '/admin/models',
    name: 'AdminModels',
    component: () => import('@/views/admin/Models.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/users',
    name: 'AdminUsers',
    component: () => import('@/views/admin/Users.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/faculties',
    name: 'AdminFaculties',
    component: () => import('@/views/admin/Faculties.vue'),
    meta: { requiresAuth: true }
  }
]
