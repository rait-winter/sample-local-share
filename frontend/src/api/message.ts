// message.ts
// 消息相关API封装，提供发送消息、获取当前消息、获取历史消息等方法
// 用于前端与后端消息API交互

import apiClient from './config';

export interface MessageHistory {
  text: string;
  timestamp: string;
}

/**
 * 发送新消息
 * @param text 消息内容
 * @returns Promise<AxiosResponse>
 */
export function sendMessage(text: string) {
  return apiClient.post('/api/message/', { text });
}

/**
 * 获取当前最新消息
 * @returns Promise<AxiosResponse<{text: string}>>
 */
export function getMessage() {
  return apiClient.get<{text: string}>('/api/message/');
}

/**
 * 获取历史消息记录
 * @returns Promise<AxiosResponse<{history: any[]}>>
 */
export function getMessageHistory() {
  return apiClient.get<{history: MessageHistory[]}>('/api/message/history');
} 