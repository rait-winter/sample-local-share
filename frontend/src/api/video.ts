import axios from 'axios';

export interface VideoInfo {
  name: string;
  size: number;
  modified: number;
}

export function uploadVideo(file: File) {
  const formData = new FormData();
  formData.append('file', file);
  return axios.post('/api/video/upload', formData);
}

export function listVideos() {
  return axios.get<{videos: VideoInfo[]}>('/api/video/list');
}

export function downloadVideo(filename: string) {
  return `/api/video/download/${encodeURIComponent(filename)}`;
}

export function previewVideo(filename: string) {
  return `/api/video/preview/${encodeURIComponent(filename)}`;
}

export function deleteVideo(filename: string) {
  return axios.delete(`/api/video/delete/${encodeURIComponent(filename)}`);
} 