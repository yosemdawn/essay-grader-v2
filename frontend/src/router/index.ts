/**
 * Vue Router配置
 * 定义应用路由和权限守卫
 */
import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

// 路由配置
const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { title: '🔐 登录', requiresAuth: false }
  },
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    component: () => import('@/layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      // 管理员路由
      {
        path: '',
        name: 'Dashboard',
        component: () => import('@/views/admin/Dashboard.vue'),
        meta: { title: '📊 控制台', requiresAdmin: true }
      },
      {
        path: '/admin/grading',
        name: 'AdminGrading',
        component: () => import('@/views/admin/Grading.vue'),
        meta: { title: '✍️ 批阅处理', requiresAdmin: true }
      },
      {
        path: '/admin/students',
        name: 'AdminStudents',
        component: () => import('@/views/admin/Students.vue'),
        meta: { title: '👥 学生管理', requiresAdmin: true }
      },
      {
        path: '/admin/records',
        name: 'AdminRecords',
        component: () => import('@/views/admin/Records.vue'),
        meta: { title: '📝 批阅记录', requiresAdmin: true }
      },
      {
        path: '/admin/settings',
        name: 'AdminSettings',
        component: () => import('@/views/admin/Settings.vue'),
        meta: { title: 'AI配置', requiresAdmin: true }
      },
      // 学生路由
      {
        path: '/student/records',
        name: 'StudentRecords',
        component: () => import('@/views/student/MyRecords.vue'),
        meta: { title: '📚 我的批阅记录', requiresStudent: true }
      },
      {
        path: '/student/profile',
        name: 'StudentProfile',
        component: () => import('@/views/student/Profile.vue'),
        meta: { title: '👤 个人信息', requiresStudent: true }
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: { title: '404' }
  }
]

// 创建路由器实例
const router = createRouter({
  history: createWebHistory(),
  routes
})

// 全局前置守卫
router.beforeEach((to, _from, next) => {
  const userStore = useUserStore()
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const requiresAdmin = to.matched.some(record => record.meta.requiresAdmin)
  const requiresStudent = to.matched.some(record => record.meta.requiresStudent)

  // 设置页面标题
  document.title = (to.meta.title as string) || 'AI作文批阅系统'

  // 需要登录但未登录
  if (requiresAuth && !userStore.isLoggedIn) {
    ElMessage.warning('⚠️ 请先登录')
    next({ name: 'Login', query: { redirect: to.fullPath } })
    return
  }

  // 需要管理员权限但不是管理员
  if (requiresAdmin && !userStore.isAdmin) {
    ElMessage.error('⛔ 此功能仅限管理员使用')
    next({ name: 'StudentRecords' })
    return
  }

  // 需要学生权限但不是学生
  if (requiresStudent && !userStore.isStudent) {
    ElMessage.error('⛔ 此功能仅限学生使用')
    next({ name: 'Dashboard' })
    return
  }

  // 已登录用户访问登录页，重定向到主页
  if (to.name === 'Login' && userStore.isLoggedIn) {
    const redirectPath = userStore.isAdmin ? '/dashboard' : '/student/records'
    next(redirectPath)
    return
  }

  next()
})

export default router
