import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/register',
    component: () => import('@/views/Register.vue')
  },
  {
    path: '/',
    component: () => import('@/views/StudentInfo.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 异步路由守卫，等待 Pinia 状态更新
router.beforeEach((to, from) => {
  // 从 localStorage 实时读取 token，避开 Pinia 状态延迟
  const userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}');
  // 需要认证且无 token → 跳登录；否则放行
  if (to.meta.requiresAuth && !userInfo?.token) {
    return '/login';
  }
  // 2. 其他情况 → 正常放行
  return true
})

export default router