// 配置API - 获取应用配置信息
import { apiClient } from './client'

export interface AppConfig {
  app_name: string
  company_name: string
  version: string
  description: string
  share_url: string
  frontend_url: string
}

/**
 * 获取应用配置信息
 */
export const getAppConfig = async (): Promise<AppConfig> => {
  try {
    const response = await apiClient.get('/api/config')
    return response.data
  } catch (error) {
    console.error('获取应用配置失败:', error)
    // 返回默认配置
    return {
      app_name: '内网文件共享工具',
      company_name: '内部共享系统',
      version: '1.0.0',
      description: '便捷的内网文件、视频和消息共享工具',
      share_url: window.location.origin.replace(':5173', ':5000'),
      frontend_url: window.location.origin
    }
  }
}

/**
 * 获取本机IP地址
 */
export const getLocalIP = (): string => {
  const url = window.location.hostname
  return url === 'localhost' ? '127.0.0.1' : url
}

/**
 * 获取共享URL
 */
export const getShareURL = (): string => {
  const ip = getLocalIP()
  return `http://${ip}:5000`
}

/**
 * 获取前端URL
 */
export const getFrontendURL = (): string => {
  const ip = getLocalIP()
  return `http://${ip}:5173`
} 