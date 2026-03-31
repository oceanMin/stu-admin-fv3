import axios from 'axios';
import { ElMessage, ElMessageBox } from 'element-plus';

// 创建axios实例
const request = axios.create({
    baseURL: 'http://localhost:9090/api/v1', // 后端基础地址
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json;charset=utf-8'
    }
});

// 请求拦截器：添加token
request.interceptors.request.use(
    config => {
        // 给请求头加 token（如果需要）
        const token = localStorage.getItem('token')
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`
        }
        return config
    },
    error => Promise.reject(error)
)
// 响应拦截器：统一处理响应
request.interceptors.response.use(
    response => {
        // 直接返回后端的完整响应数据，不做任何覆盖/修改
        const res = response.data
        // 只做状态码判断，不修改数据结构
        if (res.code === 200) {
            return res // 原样返回，包含 token、username 等所有字段
        } else {
            ElMessage.error(res.message || '请求失败')
            return Promise.reject(res)
        }
    },
    error => {
        ElMessage.error(error.message || '网络错误')
        return Promise.reject(error)
    }
)
  

export default request;