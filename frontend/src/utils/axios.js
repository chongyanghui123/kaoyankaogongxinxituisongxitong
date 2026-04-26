import axios from 'axios'

// 创建 axios 实例
const service = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000
})

// 响应拦截器
service.interceptors.response.use(
  response => {
    return response
  },
  error => {
    // 阻止 axios 默认的控制台错误输出
    return Promise.reject(error)
  }
)

export default service