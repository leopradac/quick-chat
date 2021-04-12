
const routes = [
  {
    path: '/auth',
    component: () => import('layouts/cleanLayout.vue'),
    children: [
      { path: '', name: 'auth', meta: { requiresUnlogged: true }, component: () => import('pages/auth.vue') }
    ]
  },
  {
    meta: { requiresAuth: true },
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', name: 'chat', component: () => import('pages/Index.vue') }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '*',
    component: () => import('pages/Error404.vue')
  }
]

export default routes
