import axios from 'axios';

export interface FileInfo {
  name: string;
  size: number;
  modified: number;
}

export function uploadFile(file: File) {
  const formData = new FormData();
  formData.append('file', file);
  return axios.post('/api/file/upload', formData);
}

export function listFiles() {
  return axios.get<{files: FileInfo[]}>('/api/file/list');
}

export function downloadFile(filename: string) {
  return `/api/file/download/${encodeURIComponent(filename)}`;
}

export function previewFile(filename: string) {
  return `/api/file/preview/${encodeURIComponent(filename)}`;
}

export function deleteFile(filename: string) {
  return axios.delete(`/api/file/delete/${encodeURIComponent(filename)}`);
} 