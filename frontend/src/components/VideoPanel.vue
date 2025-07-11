<!--
VideoPanel.vue
视频管理区组件，负责视频上传、列表、预览、下载、删除、详情等功能。
props: 支持传入视频列表、分页等参数
emit: 支持操作反馈、刷新等事件
主要逻辑：视频上传、分页、操作按钮、详情弹窗
-->
<template>
  <div>
    <h2>视频管理</h2>
    <div class="upload-section">
      <input type="file" @change="onFileChange" accept="video/*" ref="videoInput" />
      <button @click="upload" class="btn" :disabled="!fileObj">上传</button>
      <button @click="clearFile" class="btn btn-secondary" :disabled="!fileObj">清除</button>
    </div>
    
    <div v-if="uploading" class="upload-status">
      <div>正在上传... {{ uploadProgress }}%</div>
      <div style="background:#eee;width:200px;height:8px;border-radius:4px;overflow:hidden;margin:4px 0;">
        <div :style="{width: uploadProgress + '%', height: '100%', background: '#4caf50', transition: 'width 0.2s'}"></div>
      </div>
    </div>
    <div v-if="uploadMessage" :style="{color: uploadMessage.includes('成功') ? 'green' : 'red', marginBottom: '8px'}">{{ uploadMessage }}</div>
    
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
import { listVideos, downloadVideo, previewVideo, deleteVideo, type VideoInfo } from '../api/video'

const videos = ref<VideoInfo[]>([])
const fileObj = ref<File | null>(null)
const videoInput = ref<HTMLInputElement>()
const previewUrl = ref('')
const uploading = ref(false)
const uploadProgress = ref(0)
const uploadMessage = ref('')
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
  if (!fileObj.value) {
    alert('请先选择要上传的视频文件！')
    return
  }
  uploading.value = true
  uploadProgress.value = 0
  uploadMessage.value = ''
  try {
    await new Promise<void>((resolve, reject) => {
      const formData = new FormData()
      formData.append('file', fileObj.value as File)
      const xhr = new XMLHttpRequest()
      xhr.open('POST', '/api/video/upload', true)
      xhr.upload.onprogress = function (event) {
        if (event.lengthComputable) {
          uploadProgress.value = Math.round((event.loaded / event.total) * 100)
        }
      }
      xhr.onload = function () {
        if (xhr.status === 200) {
          uploadMessage.value = '上传成功'
          resolve()
        } else {
          uploadMessage.value = '上传失败: ' + (xhr.responseText || xhr.status)
          reject(new Error(uploadMessage.value))
        }
      }
      xhr.onerror = function () {
        uploadMessage.value = '上传失败'
        reject(new Error('上传失败'))
      }
      xhr.send(formData)
    })
    await load()
    clearFile()
  } catch (error: any) {
    alert('上传失败: ' + (error.message || error))
  } finally {
    uploading.value = false
    setTimeout(() => { uploadProgress.value = 0; uploadMessage.value = '' }, 1500)
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