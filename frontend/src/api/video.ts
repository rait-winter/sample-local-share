import axios from 'axios';

export function uploadVideo(file: File) {
  const formData = new FormData();
  formData.append('file', file);
  return axios.post('/api/video/upload', formData);
}

export function listVideos() {
  return axios.get('/api/video/list');
}

export function downloadVideo(filename: string) {
  return `/api/video/download/${encodeURIComponent(filename)}`;
}

export function previewVideo(filename: string) {
  return `/api/video/preview/${encodeURIComponent(filename)}`;
} 