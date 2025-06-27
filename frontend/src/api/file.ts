import axios from 'axios';

export function uploadFile(file: File) {
  const formData = new FormData();
  formData.append('file', file);
  return axios.post('/api/file/upload', formData);
}
export function listFiles() {
  return axios.get('/api/file/list');
}
export function downloadFile(filename: string) {
  return `/api/file/download/${encodeURIComponent(filename)}`;
}
export function previewFile(filename: string) {
  return `/api/file/preview/${encodeURIComponent(filename)}`;
} 