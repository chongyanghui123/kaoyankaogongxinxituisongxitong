<template>
  <div class="login">
    <div class="login-container">
      <h2 class="title">双赛道情报通 - 登录</h2>
      <el-form :model="loginForm" :rules="rules" ref="loginFormRef" label-width="80px">
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="loginForm.email" placeholder="请输入邮箱" prefix-icon="Message" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="loginForm.password" type="password" placeholder="请输入密码" prefix-icon="Lock" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="login" :loading="loading" style="width: 100%">登录</el-button>
        </el-form-item>

      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from '../utils/axios'

const router = useRouter()
const loginFormRef = ref(null)
const loading = ref(false)

const loginForm = reactive({
  email: '',
  password: ''
})

const rules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ]
}

const login = async () => {
  if (!loginFormRef.value) return
  
  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        // 调用真实登录API
        console.log('发送登录请求:', {
          username: loginForm.email,
          password: loginForm.password
        })
        console.log('发送请求前的表单数据:', loginForm)
        const requestData = {
          username: loginForm.email,
          password: loginForm.password
        }
        console.log('发送请求前的请求数据:', requestData)
        const response = await axios.post('/api/v1/auth/login', requestData, {
          headers: {
            'Content-Type': 'application/json'
          },
          timeout: 10000
        })
        console.log('登录响应:', response)
        
        // 检查登录是否成功
        if (response.data && response.data.success) {
          const { access_token, user_id, username, email, is_admin } = response.data.data
          
          // 存储token和用户信息
          localStorage.setItem('token', access_token)
          localStorage.setItem('userInfo', JSON.stringify({
            id: user_id,
            username: username,
            email: email,
            is_admin: is_admin
          }))
          
          // 登录成功后根据用户类型处理
          ElMessage.success('登录成功')
          // 所有用户都跳转到首页，添加短暂延迟让用户看到成功提示
          setTimeout(() => {
            if (is_admin) {
              router.push('/admin')
            } else {
              router.push('/')
            }
            loading.value = false
          }, 1000)
        } else {
          // 登录失败，显示错误信息
          ElMessage.error(response.data?.message || '登录失败')
        }
      } catch (error) {
        // 处理后端返回的错误
        console.error('完整的错误信息:', error)
        if (error.response) {
          console.error('响应状态:', error.response.status)
          console.error('响应数据:', error.response.data)
          ElMessage.error(error.response.data.message || '登录失败')
        } else if (error.request) {
          console.error('请求信息:', error.request)
          ElMessage.error('请求失败，请检查网络连接')
        } else {
          console.error('请求配置错误:', error.message)
          ElMessage.error('登录失败，请检查网络连接或服务器状态')
        }
        loading.value = false
      }
    }
  })
}

const navigateTo = (path) => {
  router.push(path)
}
</script>

<style scoped>
.login {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f7fa;
}

.login-container {
  width: 400px;
  padding: 40px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.title {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
  font-size: 24px;
  font-weight: bold;
}

.login-footer {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.login-footer span {
  margin-right: 10px;
  color: #666;
}
</style>
