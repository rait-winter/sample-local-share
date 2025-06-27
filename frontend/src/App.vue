<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ChatLineSquare, Document, VideoCamera, Delete, View, Download } from '@element-plus/icons-vue'
import { sendMessage, getMessage, getMessageHistory } from './api/message'
import { uploadFile, listFiles, downloadFile as dlFile, previewFile, deleteFile } from './api/file'
import { uploadVideo, listVideos, downloadVideo as dlVideo, previewVideo, deleteVideo } from './api/video'

// 消息
const message = ref('')
const lastMessage = ref('')
const messageHistory = ref<Array<{text: string, timestamp: string}>>([])
const loadingMsg = ref(false)
const showHistory = ref(false)

const handleSendMessage = async () => {
  if (!message.value.trim()) {
    ElMessage.warning('请输入消息内容')
    return
  }
  loadingMsg.value = true
  try {
    await sendMessage(message.value)
    ElMessage.success('消息发送成功')
    fetchMessage()
    fetchMessageHistory()
    message.value = ''
  } catch (error: any) {
    ElMessage.error('消息发送失败: ' + (error.response?.data?.error || error.message))
  }
  loadingMsg.value = false
}

const fetchMessage = async () => {
  try {
    const res = await getMessage()
    lastMessage.value = res.data.text || ''
  } catch {
    lastMessage.value = ''
  }
}

const fetchMessageHistory = async () => {
  try {
    const res = await getMessageHistory()
    messageHistory.value = res.data.history || []
  } catch {
    messageHistory.value = []
  }
}

// 文件
const file = ref<File | null>(null)
const loadingFile = ref(false)
const fileList = ref<Array<{name: string, size: number, modified: number}>>([])
const filePreviewVisible = ref(false)
const filePreviewUrl = ref('')
const filePreviewContent = ref('')

const beforeFileUpload = (rawFile: File) => {
  file.value = rawFile
  return false
}

const onFileChange = (fileObj: any) => {
  file.value = fileObj.raw
}

const handleUploadFile = async () => {
  if (!file.value) return
  loadingFile.value = true
  try {
    await uploadFile(file.value)
    ElMessage.success('文件上传成功')
    file.value = null
    fetchFiles()
  } catch (error: any) {
    ElMessage.error('文件上传失败: ' + (error.response?.data?.error || error.message))
  }
  loadingFile.value = false
}

const fetchFiles = async () => {
  try {
    const res = await listFiles()
    fileList.value = res.data.files || []
  } catch {
    fileList.value = []
  }
}

const downloadFileHandler = (name: string) => {
  window.open(dlFile(name), '_blank')
}

const previewFileHandler = async (name: string) => {
  try {
    if (name.match(/\.(png|jpg|jpeg|gif|bmp)$/i)) {
      filePreviewUrl.value = previewFile(name)
      filePreviewContent.value = ''
    } else if (name.match(/\.(txt|md|csv)$/i)) {
      const response = await fetch(previewFile(name))
      filePreviewContent.value = await response.text()
      filePreviewUrl.value = ''
    } else {
      ElMessage.warning('不支持预览此类型文件')
      return
    }
    filePreviewVisible.value = true
  } catch (error: any) {
    ElMessage.error('预览失败: ' + (error.response?.data?.error || error.message))
  }
}

const deleteFileHandler = async (name: string) => {
  try {
    await ElMessageBox.confirm(`确定要删除文件 "${name}" 吗？`, '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await deleteFile(name)
    ElMessage.success('文件删除成功')
    fetchFiles()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败: ' + (error.response?.data?.error || error.message))
    }
  }
}

// 视频
const video = ref<File | null>(null)
const loadingVideo = ref(false)
const videoList = ref<Array<{name: string, size: number, modified: number}>>([])
const videoPreviewVisible = ref(false)
const videoPreviewUrl = ref('')

const beforeVideoUpload = (rawFile: File) => {
  video.value = rawFile
  return false
}

const onVideoChange = (fileObj: any) => {
  video.value = fileObj.raw
}

const handleUploadVideo = async () => {
  if (!video.value) return
  loadingVideo.value = true
  try {
    await uploadVideo(video.value)
    ElMessage.success('视频上传成功')
    video.value = null
    fetchVideos()
  } catch (error: any) {
    ElMessage.error('视频上传失败: ' + (error.response?.data?.error || error.message))
  }
  loadingVideo.value = false
}

const fetchVideos = async () => {
  try {
    const res = await listVideos()
    videoList.value = res.data.videos || []
  } catch {
    videoList.value = []
  }
}

const downloadVideoHandler = (name: string) => {
  window.open(dlVideo(name), '_blank')
}

const previewVideoHandler = (name: string) => {
  videoPreviewUrl.value = previewVideo(name)
  videoPreviewVisible.value = true
}

const deleteVideoHandler = async (name: string) => {
  try {
    await ElMessageBox.confirm(`确定要删除视频 "${name}" 吗？`, '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await deleteVideo(name)
    ElMessage.success('视频删除成功')
    fetchVideos()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败: ' + (error.response?.data?.error || error.message))
    }
  }
}

// 工具函数
const formatSize = (size: number) => {
  if (size < 1024) return size + ' B'
  if (size < 1024 * 1024) return (size / 1024).toFixed(1) + ' KB'
  if (size < 1024 * 1024 * 1024) return (size / 1024 / 1024).toFixed(1) + ' MB'
  return (size / 1024 / 1024 / 1024).toFixed(1) + ' GB'
}

const formatDate = (timestamp: number) => {
  return new Date(timestamp * 1000).toLocaleString('zh-CN')
}

// 实时同步
let messagePollInterval: number | null = null
let filePollInterval: number | null = null
let videoPollInterval: number | null = null

const startPolling = () => {
  messagePollInterval = window.setInterval(() => {
    fetchMessage()
    fetchMessageHistory()
  }, 5000)
  
  filePollInterval = window.setInterval(() => {
    fetchFiles()
  }, 10000)
  
  videoPollInterval = window.setInterval(() => {
    fetchVideos()
  }, 10000)
}

const stopPolling = () => {
  if (messagePollInterval) clearInterval(messagePollInterval)
  if (filePollInterval) clearInterval(filePollInterval)
  if (videoPollInterval) clearInterval(videoPollInterval)
}

onMounted(() => {
  fetchMessage()
  fetchMessageHistory()
  fetchFiles()
  fetchVideos()
  startPolling()
})

onUnmounted(() => {
  stopPolling()
})
</script>

<template>
  <div class="main-bg">
    <header class="topbar">
      <div class="topbar-inner">
        <img class="logo-img" src="https://avatars.githubusercontent.com/u/9919?s=200&v=4" alt="logo" />
        <span class="title">内网共享工具</span>
        <span class="subtitle">安全 · 极速 · 局域网文件/消息/视频互传</span>
      </div>
    </header>
    
    <main class="main-content">
      <!-- 消息模块 -->
      <div class="module-card">
        <div class="module-title">
          <el-icon><ChatLineSquare /></el-icon> 消息管理
          <el-button type="text" @click="showHistory = !showHistory" class="history-btn">
            {{ showHistory ? '隐藏历史' : '查看历史' }}
          </el-button>
        </div>
        <div class="module-body">
          <div class="module-left">
            <el-input
              v-model="message"
              type="textarea"
              :rows="4"
              placeholder="请输入要发送的消息内容..."
              class="input"
              @keydown.ctrl.enter="handleSendMessage"
            />
            <div class="input-hint">Ctrl+Enter 快速发送</div>
            <el-button type="primary" class="btn" @click="handleSendMessage" :loading="loadingMsg">
              发送消息
            </el-button>
          </div>
          <div class="module-right">
            <div class="msg-title">当前消息：</div>
            <div class="msg-content" v-if="lastMessage">{{ lastMessage }}</div>
            <div class="msg-empty" v-else>暂无消息</div>
            
            <!-- 消息历史 -->
            <div v-if="showHistory" class="history-section">
              <div class="history-title">消息历史：</div>
              <div class="history-list">
                <div v-for="(item, index) in messageHistory" :key="index" class="history-item">
                  <div class="history-text">{{ item.text }}</div>
                  <div class="history-time">{{ new Date(item.timestamp).toLocaleString('zh-CN') }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 文件模块 -->
      <div class="module-card">
        <div class="module-title"><el-icon><Document /></el-icon> 文件管理</div>
        <div class="module-body">
          <div class="module-left">
            <el-upload
              class="upload-demo"
              drag
              :show-file-list="false"
              :before-upload="beforeFileUpload"
              :on-change="onFileChange"
            >
              <el-button type="primary">选择文件</el-button>
              <div class="el-upload__text">拖拽文件到此处上传</div>
            </el-upload>
            <el-button
              type="success"
              class="btn upload-btn"
              @click="handleUploadFile"
              :disabled="!file"
              :loading="loadingFile"
            >
              上传文件
            </el-button>
          </div>
          <div class="module-right">
            <div class="list-title">文件列表</div>
            <el-table :data="fileList" border style="width: 100%;margin-top:8px;" size="small">
              <el-table-column prop="name" label="文件名" min-width="200" />
              <el-table-column prop="size" label="大小" width="100">
                <template #default="scope">
                  {{ formatSize(scope.row.size) }}
                </template>
              </el-table-column>
              <el-table-column prop="modified" label="修改时间" width="150">
                <template #default="scope">
                  {{ formatDate(scope.row.modified) }}
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="scope">
                  <el-button type="primary" link size="small" @click="previewFileHandler(scope.row.name)">
                    <el-icon><View /></el-icon> 预览
                  </el-button>
                  <el-button type="success" link size="small" @click="downloadFileHandler(scope.row.name)">
                    <el-icon><Download /></el-icon> 下载
                  </el-button>
                  <el-button type="danger" link size="small" @click="deleteFileHandler(scope.row.name)">
                    <el-icon><Delete /></el-icon> 删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </div>
      </div>

      <!-- 视频模块 -->
      <div class="module-card">
        <div class="module-title"><el-icon><VideoCamera /></el-icon> 视频管理</div>
        <div class="module-body">
          <div class="module-left">
            <el-upload
              class="upload-demo"
              drag
              accept="video/*"
              :show-file-list="false"
              :before-upload="beforeVideoUpload"
              :on-change="onVideoChange"
            >
              <el-button type="primary">选择视频</el-button>
              <div class="el-upload__text">拖拽视频到此处上传</div>
            </el-upload>
            <el-button
              type="success"
              class="btn upload-btn"
              @click="handleUploadVideo"
              :disabled="!video"
              :loading="loadingVideo"
            >
              上传视频
            </el-button>
          </div>
          <div class="module-right">
            <div class="list-title">视频列表</div>
            <el-table :data="videoList" border style="width: 100%;margin-top:8px;" size="small">
              <el-table-column prop="name" label="视频名" min-width="200" />
              <el-table-column prop="size" label="大小" width="100">
                <template #default="scope">
                  {{ formatSize(scope.row.size) }}
                </template>
              </el-table-column>
              <el-table-column prop="modified" label="修改时间" width="150">
                <template #default="scope">
                  {{ formatDate(scope.row.modified) }}
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="scope">
                  <el-button type="primary" link size="small" @click="previewVideoHandler(scope.row.name)">
                    <el-icon><View /></el-icon> 预览
                  </el-button>
                  <el-button type="success" link size="small" @click="downloadVideoHandler(scope.row.name)">
                    <el-icon><Download /></el-icon> 下载
                  </el-button>
                  <el-button type="danger" link size="small" @click="deleteVideoHandler(scope.row.name)">
                    <el-icon><Delete /></el-icon> 删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </div>
      </div>
    </main>

    <!-- 文件预览对话框 -->
    <el-dialog v-model="filePreviewVisible" title="文件预览" width="80%" :before-close="() => filePreviewVisible = false">
      <div v-if="filePreviewUrl" class="preview-image">
        <img :src="filePreviewUrl" style="max-width: 100%; height: auto;" />
      </div>
      <div v-else-if="filePreviewContent" class="preview-text">
        <pre style="white-space: pre-wrap; word-break: break-all; max-height: 400px; overflow-y: auto;">{{ filePreviewContent }}</pre>
      </div>
    </el-dialog>

    <!-- 视频预览对话框 -->
    <el-dialog v-model="videoPreviewVisible" title="视频预览" width="80%" :before-close="() => videoPreviewVisible = false">
      <video v-if="videoPreviewUrl" :src="videoPreviewUrl" controls style="width: 100%; max-height: 500px;"></video>
    </el-dialog>
  </div>
</template>

<style scoped>
.main-bg {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.topbar {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.topbar-inner {
  display: flex;
  align-items: center;
  gap: 16px;
}

.logo-img {
  width: 48px;
  height: 48px;
  border-radius: 8px;
}

.title {
  font-size: 24px;
  font-weight: bold;
  color: #2c3e50;
}

.subtitle {
  color: #7f8c8d;
  font-size: 14px;
}

.main-content {
  display: grid;
  gap: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.module-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.module-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 2px solid #ecf0f1;
}

.history-btn {
  margin-left: auto;
  font-size: 12px;
}

.module-body {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 24px;
}

.module-left {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.input {
  font-family: inherit;
}

.input-hint {
  font-size: 12px;
  color: #7f8c8d;
  text-align: center;
}

.btn {
  height: 40px;
  font-weight: 500;
}

.upload-btn {
  margin-top: 8px;
}

.module-right {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.list-title, .msg-title, .history-title {
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 8px;
}

.msg-content {
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 12px;
  min-height: 60px;
  white-space: pre-wrap;
  word-break: break-word;
}

.msg-empty {
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 12px;
  min-height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6c757d;
  font-style: italic;
}

.history-section {
  margin-top: 16px;
  border-top: 1px solid #e9ecef;
  padding-top: 16px;
}

.history-list {
  max-height: 200px;
  overflow-y: auto;
  border: 1px solid #e9ecef;
  border-radius: 8px;
}

.history-item {
  padding: 8px 12px;
  border-bottom: 1px solid #f1f3f4;
}

.history-item:last-child {
  border-bottom: none;
}

.history-text {
  margin-bottom: 4px;
  white-space: pre-wrap;
  word-break: break-word;
}

.history-time {
  font-size: 12px;
  color: #6c757d;
}

.preview-image, .preview-text {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

.preview-text pre {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #e9ecef;
  width: 100%;
}

@media (max-width: 768px) {
  .module-body {
    grid-template-columns: 1fr;
  }
  
  .main-content {
    padding: 0 10px;
  }
  
  .topbar-inner {
    flex-direction: column;
    text-align: center;
  }
}
</style>
