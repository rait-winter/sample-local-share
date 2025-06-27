<!--
FilePanel.vue
文件管理区组件，负责文件上传、列表、预览、下载、删除、详情等功能。
props: 支持传入文件列表、分页等参数
emit: 支持操作反馈、刷新等事件
主要逻辑：文件上传、分页、操作按钮、详情弹窗
-->
<template>
  <div>
    <h2>文件管理</h2>
    <div class="upload-section">
      <input type="file" @change="onFileChange" ref="fileInput" />
      <button @click="upload" class="btn" :disabled="!fileObj">上传</button>
      <button @click="clearFile" class="btn btn-secondary" :disabled="!fileObj">清除</button>
    </div>
    
    <div v-if="uploading" class="upload-status">
      正在上传...
    </div>
    
    <h3 style="margin-top:16px;">文件列表</h3>
    <div v-if="files.length === 0" class="empty-state">
      暂无文件
    </div>
    <div v-else class="file-list">
      <div v-for="file in files" :key="file.name" class="file-item">
        <div class="file-info">
          <div class="file-name">{{ file.name }}</div>
          <div class="file-meta">
            {{ formatFileSize(file.size) }} | {{ formatDate(file.modified) }}
          </div>
        </div>
        <div class="file-actions">
          <button @click="preview(file.name)" class="btn btn-small">预览</button>
          <a :href="downloadUrl(file.name)" download class="btn btn-small">下载</a>
          <button @click="deleteFileHandler(file.name)" class="btn btn-small btn-danger">删除</button>
        </div>
      </div>
    </div>
    
    <div v-if="previewContent" class="preview-section">
      <h4>预览</h4>
      <button @click="closePreview" class="btn btn-small">关闭预览</button>
      <div v-html="previewContent" class="preview-content"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { uploadFile, listFiles, downloadFile, previewFile, deleteFile, type FileInfo } from '../api/file'

const files = ref<FileInfo[]>([])
const fileObj = ref<File | null>(null)
const fileInput = ref<HTMLInputElement>()
const previewContent = ref('')
const uploading = ref(false)
let pollInterval: number | null = null

function onFileChange(e: Event) {
  const target = e.target as HTMLInputElement
  fileObj.value = target.files ? target.files[0] : null
}

function clearFile() {
  fileObj.value = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

async function upload() {
  if (!fileObj.value) return
  
  uploading.value = true
  try {
    await uploadFile(fileObj.value)
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
    const res = await listFiles()
    files.value = res.data.files
  } catch (error: any) {
    console.error('加载文件列表失败:', error)
  }
}

function downloadUrl(name: string) {
  return downloadFile(name)
}

async function preview(name: string) {
  try {
    if (name.match(/\.(png|jpg|jpeg|gif|bmp)$/i)) {
      previewContent.value = `<img src='${previewFile(name)}' style='max-width:100%;' />`
    } else {
      const res = await fetch(previewFile(name))
      const html = await res.text()
      previewContent.value = html
    }
  } catch (error: any) {
    alert('预览失败: ' + (error.response?.data?.error || error.message))
  }
}

function closePreview() {
  previewContent.value = ''
}

async function deleteFileHandler(filename: string) {
  if (!confirm(`确定要删除文件 "${filename}" 吗？`)) {
    return
  }
  
  try {
    await deleteFile(filename)
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

.file-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.file-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: #f9fafb;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.file-info {
  flex: 1;
}

.file-name {
  font-weight: 500;
  margin-bottom: 4px;
}

.file-meta {
  font-size: 12px;
  color: #666;
}

.file-actions {
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

.preview-content {
  margin-top: 12px;
  max-height: 400px;
  overflow-y: auto;
  background: white;
  padding: 12px;
  border-radius: 4px;
  border: 1px solid #d1d5db;
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