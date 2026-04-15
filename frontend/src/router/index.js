import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/kaoyan-student-form'
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
  },
  {
    path: '/payment',
    name: 'PaymentPage',
    component: () => import('../views/PaymentPage.vue'),
    meta: {
      title: '订单支付',
      requiresAuth: false,
      requiresAdmin: false
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from) => {
  // 设置页面标题
  document.title = to.meta.title || '管理后台'
  
  // 检查登录状态
  const token = localStorage.getItem('token')
  
  if (to.meta.requiresAuth && !token) {
    return '/login'
  } else if (to.meta.requiresAdmin) {
    // 检查是否为管理员
    try {
      const userInfoStr = localStorage.getItem('userInfo')
      const userInfo = userInfoStr && userInfoStr !== 'undefined' && userInfoStr !== 'null' 
        ? JSON.parse(userInfoStr) 
        : {}
      
      if (!userInfo.is_admin) {
        return '/login'
      }
    } catch (error) {
      console.error('解析用户信息失败:', error)
      return '/login'
    }
  }
})

export default router
