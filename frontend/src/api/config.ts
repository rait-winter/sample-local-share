// API配置文件，统一管理API基础URL和配置

// 判断是否为开发环境
const isDevelopment = import.meta.env.DEV;

// API基础URL配置
// 开发环境：使用Vite代理
// 生产环境：使用相对路径（与后端同域）
export const API_BASE_URL = isDevelopment ? '' : '';

import axios from 'axios';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use(
  (config) => config,
  (error) => Promise.reject(error)
);

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API请求错误:', error);
    return Promise.reject(error);
  }
);

export default apiClient; 