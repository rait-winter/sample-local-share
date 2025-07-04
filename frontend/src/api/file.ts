// file.ts
// 文件相关API封装，提供文件上传、列表、下载、预览、删除、最大数量设置等方法
// 用于前端与后端文件API交互

import apiClient from './config';

export interface FileInfo {
  name: string;
  size: number;
  modified: number;
}

/**
 * 上传文件
 * @param file 文件对象
 * @returns Promise<AxiosResponse>
 */
export function uploadFile(file: File) {
  const formData = new FormData();
  formData.append('file', file);
  return apiClient.post('/api/file/upload', formData, {
    headers: {
      'Content-Type': undefined // 让axios自动设置multipart/form-data
    }
  });
}

/**
 * 获取文件列表
 * @returns Promise<AxiosResponse<{files: any[]}>>
 */
export function listFiles() {
  return apiClient.get<{files: FileInfo[]}>('/api/file/list');
}

/**
 * 获取文件下载链接
 * @param name 文件名
 * @returns 下载URL
 */
export function downloadFile(name: string) {
  return `/api/file/download/${encodeURIComponent(name)}`;
}

/**
 * 获取文件预览链接
 * @param name 文件名
 * @returns 预览URL
 */
export function previewFile(name: string) {
  return `/api/file/preview/${encodeURIComponent(name)}`;
}

/**
 * 删除文件
 * @param name 文件名
 * @returns Promise<AxiosResponse>
 */
export function deleteFile(name: string) {
  return apiClient.delete(`/api/file/delete/${encodeURIComponent(name)}`);
} 