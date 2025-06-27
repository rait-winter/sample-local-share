<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { ChatLineSquare, Document, VideoCamera } from '@element-plus/icons-vue'
import { sendMessage, getMessage } from './api/message'
import { uploadFile, listFiles, downloadFile as dlFile } from './api/file'
import { uploadVideo, listVideos, downloadVideo as dlVideo } from './api/video'

// 消息
const message = ref('')
const lastMessage = ref('')
const loadingMsg = ref(false)
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
    message.value = ''
  } catch {
    ElMessage.error('消息发送失败')
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

// 文件
const file = ref<File | null>(null)
const loadingFile = ref(false)
const fileList = ref<{ name: string; size: number }[]>([])
const beforeFileUpload = (rawFile: File) => {
  file.value = rawFile
  return false // 阻止自动上传
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
  } catch {
    ElMessage.error('文件上传失败')
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
const downloadFile = (name: string) => {
  window.open(dlFile(name), '_blank')
}

// 视频
const video = ref<File | null>(null)
const loadingVideo = ref(false)
const videoList = ref<{ name: string; size: number }[]>([])
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
  } catch {
    ElMessage.error('视频上传失败')
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
const downloadVideo = (name: string) => {
  window.open(dlVideo(name), '_blank')
}

// 工具
const formatSize = (_: any, __: any, row: any) => {
  const size = row.size
  if (size < 1024) return size + 'B'
  if (size < 1024 * 1024) return (size / 1024).toFixed(1) + 'KB'
  if (size < 1024 * 1024 * 1024) return (size / 1024 / 1024).toFixed(1) + 'MB'
  return (size / 1024 / 1024 / 1024).toFixed(1) + 'GB'
}

// 拖拽事件（防止报错）
const onDropFile = (e: DragEvent) => {};
const onDropVideo = (e: DragEvent) => {};

onMounted(() => {
  fetchMessage()
  fetchFiles()
  fetchVideos()
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
        <div class="module-title"><el-icon><ChatLineSquare /></el-icon> 消息</div>
        <div class="module-body">
          <div class="module-left">
            <el-input
              v-model="message"
              type="textarea"
              :rows="4"
              placeholder="请输入要发送的消息"
              class="input"
            />
            <el-button type="primary" class="btn" @click="handleSendMessage" :loading="loadingMsg">
              发送
            </el-button>
          </div>
          <div class="module-right">
            <div class="msg-title">可粘贴的消息内容：</div>
            <div class="msg-content">{{ lastMessage }}</div>
          </div>
        </div>
      </div>
      <!-- 文件模块 -->
      <div class="module-card">
        <div class="module-title"><el-icon><Document /></el-icon> 文件</div>
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
              上传
            </el-button>
          </div>
          <div class="module-right">
            <div class="list-title">可下载文件列表</div>
            <el-table :data="fileList" border style="width: 100%;margin-top:8px;" size="small">
              <el-table-column prop="name" label="文件名" />
              <el-table-column prop="size" label="大小" :formatter="formatSize" width="100"/>
              <el-table-column label="操作" width="100">
                <template #default="scope">
                  <el-button type="primary" link @click="downloadFile(scope.row.name)">下载</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </div>
      </div>
      <!-- 视频模块 -->
      <div class="module-card">
        <div class="module-title"><el-icon><VideoCamera /></el-icon> 视频</div>
        <div class="module-body">
          <div class="module-left">
            <el-upload
              class="upload-demo"
              drag
              :show-file-list="false"
              :before-upload="beforeVideoUpload"
              :on-change="onVideoChange"
              accept="video/*"
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
              上传
            </el-button>
          </div>
          <div class="module-right">
            <div class="list-title">可下载视频列表</div>
            <el-table :data="videoList" border style="width: 100%;margin-top:8px;" size="small">
              <el-table-column prop="name" label="文件名" />
              <el-table-column prop="size" label="大小" :formatter="formatSize" width="100"/>
              <el-table-column label="操作" width="100">
                <template #default="scope">
                  <el-button type="primary" link @click="downloadVideo(scope.row.name)">下载</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.main-bg {
  min-height: 100vh;
  background: #f6f8fb;
}
.topbar {
  width: 100%;
  background: #fff;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.04);
  padding: 0;
}
.topbar-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  height: 110px;
  padding: 0 32px;
  justify-content: center;
  flex-direction: column;
}
.logo-img {
  width: 48px;
  height: 48px;
  margin-bottom: 8px;
}
.title {
  font-size: 2.2rem;
  font-weight: 700;
  color: #2357d5;
  margin-bottom: 4px;
}
.subtitle {
  color: #7a8599;
  font-size: 1.1rem;
  font-weight: 400;
  letter-spacing: 1px;
}
.main-content {
  max-width: 1600px;
  margin: 0 auto;
  padding: 40px 12px 40px 12px;
  display: flex;
  flex-direction: column;
  gap: 36px;
}
.module-card {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 4px 24px 0 rgba(0,0,0,0.08);
  padding: 40px 48px 36px 48px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
}
.module-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2357d5;
  margin-bottom: 22px;
  display: flex;
  align-items: center;
  gap: 10px;
}
.module-body {
  display: flex;
  gap: 48px;
}
.module-left {
  flex: 0 0 400px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.module-right {
  flex: 1 1 0;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.input {
  margin-bottom: 12px;
}
.btn {
  margin: 10px 0 8px 0;
}
.upload-btn {
  margin-left: 10px;
}
.list-title, .msg-title {
  margin: 0 0 6px 0;
  font-weight: 600;
  color: #2357d5;
  font-size: 1.08rem;
}
.msg-content {
  background: #f6f8fb;
  border-radius: 6px;
  padding: 8px 12px;
  color: #333;
  min-height: 32px;
  margin-top: 4px;
  font-size: 1.05rem;
  word-break: break-all;
}
@media (max-width: 1200px) {
  .main-content {
    max-width: 98vw;
    padding: 16px 2vw;
    gap: 18px;
  }
  .module-card {
    padding: 16px 6px 12px 6px;
  }
  .module-body {
    flex-direction: column;
    gap: 16px;
  }
  .module-left, .module-right {
    flex: unset;
    width: 100%;
  }
}
</style>
