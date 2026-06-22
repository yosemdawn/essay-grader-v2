/**
 * Axios HTTP客户端封装
 * 统一处理请求和响应，自动添加token
 */
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'
import { ElMessage } from 'element-plus'

interface RequestClient {
  <T = any>(config: AxiosRequestConfig): Promise<T>
  get<T = any>(url: string, config?: AxiosRequestConfig): Promise<T>
  post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T>
  put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T>
  delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<T>
}

// 创建axios实例
const request: AxiosInstance = axios.create({
  baseURL: '/api',  // Vite代理会转发到 http://localhost:8000/api
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    // 从localStorage获取token
    const token = localStorage.getItem('access_token')
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response: AxiosResponse) => {
    return response.data
  },
  (error) => {
    // 处理HTTP错误
    if (error.response) {
      const { status, data } = error.response
      
      switch (status) {
        case 401:
          ElMessage.error('🔒 未登录或登录已过期，请重新登录')
          // 清除token并跳转到登录页
          localStorage.removeItem('access_token')
          localStorage.removeItem('user_info')
          window.location.href = '/login'
          break
        case 403:
          ElMessage.error('⛔ 权限不足，无法访问此资源')
          break
        case 404:
          ElMessage.error('❌ 请求的资源不存在')
          break
        case 422:
          ElMessage.error(data.message || '❌ 请求参数验证失败')
          break
        case 500:
          ElMessage.error('💥 服务器内部错误，请稍后重试')
          break
        default:
          ElMessage.error(data.message || `❌ 请求失败 (${status})`)
      }
    } else if (error.request) {
      ElMessage.error('🌐 网络错误，请检查网络连接')
    } else {
      ElMessage.error('❌ 请求配置错误')
    }
    
    return Promise.reject(error)
  }
)

export default request as unknown as RequestClient
