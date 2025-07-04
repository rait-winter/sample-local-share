// video.ts
// 视频相关API封装，提供视频上传、列表、下载、预览、删除、最大数量设置等方法
// 用于前端与后端视频API交互

import apiClient from './config';

export interface VideoInfo {
  name: string;
  size: number;
  modified: number;
}

/**
 * 上传视频
 * @param file 视频文件对象
 * @returns Promise<AxiosResponse>
 */
export function uploadVideo(file: File) {
  const formData = new FormData();
  formData.append('file', file);
  return apiClient.post('/api/video/upload', formData);
}

/**
 * 获取视频列表
 * @returns Promise<AxiosResponse<{videos: any[]}>>
 */
export function listVideos() {
  return apiClient.get<{videos: VideoInfo[]}>('/api/video/list');
}

/**
 * 获取视频下载链接
 * @param name 视频文件名
 * @returns 下载URL
 */
export function downloadVideo(name: string) {
  return `/api/video/download/${encodeURIComponent(name)}`;
}

/**
 * 获取视频预览链接
 * @param name 视频文件名
 * @returns 预览URL
 */
export function previewVideo(name: string) {
  return `/api/video/preview/${encodeURIComponent(name)}`;
}

/**
 * 删除视频
 * @param name 视频文件名
 * @returns Promise<AxiosResponse>
 */
export function deleteVideo(name: string) {
  return apiClient.delete(`/api/video/delete/${encodeURIComponent(name)}`);
} 