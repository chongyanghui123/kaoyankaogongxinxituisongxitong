import axios from 'axios'

const service = axios.create({
  baseURL: '/',
  timeout: 10000
})

service.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

service.interceptors.response.use(
  response => {
    console.log('axios响应:', response.config.url, response.status, response.data)
    return response.data
  },
  error => {
    console.error('响应错误:', error)
    return Promise.reject(error)
  }
)

export default service