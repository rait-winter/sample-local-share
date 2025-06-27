<template>
  <div>
    <h2>视频管理</h2>
    <div class="upload-section">
      <input type="file" @change="onFileChange" accept="video/*" ref="videoInput" />
      <button @click="upload" class="btn" :disabled="!fileObj">上传</button>
      <button @click="clearFile" class="btn btn-secondary" :disabled="!fileObj">清除</button>
    </div>
    
    <div v-if="uploading" class="upload-status">
      正在上传...
    </div>
    
    <h3 style="margin-top:16px;">视频列表</h3>
    <div v-if="videos.length === 0" class="empty-state">
      暂无视频
    </div>
    <div v-else class="video-list">
      <div v-for="video in videos" :key="video.name" class="video-item">
        <div class="video-info">
          <div class="video-name">{{ video.name }}</div>
          <div class="video-meta">
            {{ formatFileSize(video.size) }} | {{ formatDate(video.modified) }}
          </div>
        </div>
        <div class="video-actions">
          <button @click="preview(video.name)" class="btn btn-small">预览</button>
          <a :href="downloadUrl(video.name)" download class="btn btn-small">下载</a>
          <button @click="deleteVideoHandler(video.name)" class="btn btn-small btn-danger">删除</button>
        </div>
      </div>
    </div>
    
    <div v-if="previewUrl" class="preview-section">
      <h4>视频预览</h4>
      <button @click="closePreview" class="btn btn-small">关闭预览</button>
      <video :src="previewUrl" controls class="video-player"></video>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { uploadVideo, listVideos, downloadVideo, previewVideo, deleteVideo, type VideoInfo } from '../api/video'

const videos = ref<VideoInfo[]>([])
const fileObj = ref<File | null>(null)
const videoInput = ref<HTMLInputElement>()
const previewUrl = ref('')
const uploading = ref(false)
let pollInterval: number | null = null

function onFileChange(e: Event) {
  const target = e.target as HTMLInputElement
  fileObj.value = target.files ? target.files[0] : null
}

function clearFile() {
  fileObj.value = null
  if (videoInput.value) {
    videoInput.value.value = ''
  }
}

async function upload() {
  if (!fileObj.value) return
  
  uploading.value = true
  try {
    await uploadVideo(fileObj.value)
    clearFile()
    await load()
  } catch (error: any) {
    alert('上传失败: ' + (error.response?.data?.error || error.message))
  } finally {
    uploading.value = false
  }
}

async function load() {
  try {
    const res = await listVideos()
    videos.value = res.data.videos
  } catch (error: any) {
    console.error('加载视频列表失败:', error)
  }
}

function downloadUrl(name: string) {
  return downloadVideo(name)
}

function preview(name: string) {
  previewUrl.value = previewVideo(name)
}

function closePreview() {
  previewUrl.value = ''
}

async function deleteVideoHandler(filename: string) {
  if (!confirm(`确定要删除视频 "${filename}" 吗？`)) {
    return
  }
  
  try {
    await deleteVideo(filename)
    await load()
  } catch (error: any) {
    alert('删除失败: ' + (error.response?.data?.error || error.message))
  }
}

function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

function formatDate(timestamp: number): string {
  return new Date(timestamp * 1000).toLocaleString('zh-CN')
}

// 开始自动轮询
function startPolling() {
  pollInterval = window.setInterval(() => {
    load()
  }, 10000) // 每10秒刷新一次
}

// 停止自动轮询
function stopPolling() {
  if (pollInterval) {
    clearInterval(pollInterval)
    pollInterval = null
  }
}

onMounted(() => {
  load()
  startPolling()
})

onUnmounted(() => {
  stopPolling()
})
</script>

<style scoped>
.upload-section {
  display: flex;
  gap: 8px;
  align-items: center;
  margin-bottom: 16px;
}

.upload-status {
  color: #2563eb;
  font-style: italic;
  margin-bottom: 16px;
}

.empty-state {
  text-align: center;
  color: #666;
  padding: 32px;
  background: #f9fafb;
  border-radius: 8px;
}

.video-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.video-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: #f9fafb;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.video-info {
  flex: 1;
}

.video-name {
  font-weight: 500;
  margin-bottom: 4px;
}

.video-meta {
  font-size: 12px;
  color: #666;
}

.video-actions {
  display: flex;
  gap: 4px;
}

.preview-section {
  margin-top: 16px;
  padding: 16px;
  background: #f9fafb;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.video-player {
  width: 100%;
  max-width: 640px;
  margin-top: 12px;
  border-radius: 8px;
}

.btn {
  background: #2563eb;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 6px 16px;
  cursor: pointer;
  font-size: 14px;
}

.btn:hover {
  background: #1746a2;
}

.btn:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.btn-secondary {
  background: #6b7280;
}

.btn-secondary:hover {
  background: #4b5563;
}

.btn-small {
  padding: 4px 8px;
  font-size: 12px;
}

.btn-danger {
  background: #dc2626;
}

.btn-danger:hover {
  background: #b91c1c;
}
</style> 