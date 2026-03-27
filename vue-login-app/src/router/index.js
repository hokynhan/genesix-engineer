import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import { supabase } from '../supabase'

const routes = [
  { path: '/', component: Login, alias: '/login' },
  { path: '/dashboard', component: Dashboard, meta: { requiresAuth: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const { data: { user } } = await supabase.auth.getUser()
  
  if (to.meta.requiresAuth && !user) {
    next('/login')
  } else if (to.path === '/login' && user) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
