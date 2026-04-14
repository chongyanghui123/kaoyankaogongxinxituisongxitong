import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/admin'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: {
      title: '登录'
    }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('../views/Admin.vue'),
    meta: {
      title: '管理后台',
      requiresAuth: true,
      requiresAdmin: true
    }
  },

  {
    path: '/kaoyan-student-form',
    name: 'KaoyanStudentForm',
    component: () => import('../views/KaoyanStudentForm.vue'),
    meta: {
      title: '考研学生信息录入'
    }
  },
  {
    path: '/kaogong-student-form',
    name: 'KaogongStudentForm',
    component: () => import('../views/KaogongStudentForm.vue'),
    meta: {
      title: '考公学生信息录入'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  document.title = to.meta.title || '管理后台'
  
  // 检查登录状态
  const token = localStorage.getItem('token')
  
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.meta.requiresAdmin) {
    // 检查是否为管理员
    const userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}')
    if (!userInfo.is_admin) {
      next('/login')
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router
