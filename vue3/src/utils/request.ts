// src/api/request.ts 或 src/utils/request.ts
import axios from 'axios';

// 创建 axios 实例
const request = axios.create({
    baseURL: 'http://localhost:9090/api/v1',  // 后端地址
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    }
});

// 请求拦截器
request.interceptors.request.use(
    config => {
        console.log('请求:', config.url);
        return config;
    },
    error => {
        console.error('请求错误:', error);
        return Promise.reject(error);
    }
);

// 响应拦截器
request.interceptors.response.use(
    response => {
        console.log('响应:', response.data);
        return response.data;
    },
    error => {
        console.error('响应错误:', error);
        return Promise.reject(error);
    }
);

export default request;