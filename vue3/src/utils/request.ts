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
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

// 响应拦截器
request.interceptors.response.use(
    response => {
        return response.data;
    },
    error => {
        return Promise.reject(error);
    }
);

export default request;