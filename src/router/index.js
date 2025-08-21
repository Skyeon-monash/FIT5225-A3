// src/router/index.js

import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import LoginView from '../views/LoginView.vue'
import { useAuthStore } from '@/stores/auth' // 导入 hook 本身没有问题

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
      component: LoginView,
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true },
    },
    // 可以在这里加一个 404 页面
    // { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFoundView }
  ],
})

// 全局前置守卫
router.beforeEach((to, from, next) => {
  // ✅ 正确的做法：在守卫函数内部获取 store 实例
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    // 如果目标路由需要认证且用户未登录，则重定向到登录页
    next({ name: 'login' })
  } else {
    // 否则，正常放行
    next()
  }
})

export default router
