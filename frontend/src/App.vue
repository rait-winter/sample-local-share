<!--
App.vue
主页面组件，负责整体布局、消息/文件/视频管理、统一设置弹窗、全局样式等。
包含：
- 消息管理区（发送、历史、复制）
- 文件管理区（上传、列表、预览、下载、删除、详情）
- 视频管理区（上传、列表、预览、下载、删除、详情）
- 统一设置弹窗
- 本机访问地址栏、右上角设置按钮
-->
<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ChatLineSquare, Document, VideoCamera, Delete, View, Download, InfoFilled } from '@element-plus/icons-vue'
import { sendMessage, getMessage, getMessageHistory } from './api/message'
import { uploadFile, listFiles, downloadFile as dlFile, previewFile, deleteFile } from './api/file'
import { uploadVideo, listVideos, downloadVideo as dlVideo, previewVideo, deleteVideo } from './api/video'
import SettingsDialog from './components/SettingsDialog.vue'

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
const filePreviewType = ref('')

// 文件分页
const filePage = ref(1)
const filePageSize = ref(10)
const fileTotal = computed(() => fileList.value.length)
const filePageData = computed(() => fileList.value.slice((filePage.value-1)*filePageSize.value, filePage.value*filePageSize.value))

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
    if (name.match(/\.(png|jpg|jpeg|gif|bmp|webp|svg)$/i)) {
      filePreviewUrl.value = previewFile(name)
      filePreviewContent.value = ''
      filePreviewType.value = 'image'
    } else if (name.match(/\.(txt|md|csv|json|xml|yaml|yml|ini|log|conf|config)$/i)) {
      const response = await fetch(previewFile(name))
      filePreviewContent.value = await response.text()
      filePreviewUrl.value = ''
      filePreviewType.value = 'text'
    } else if (name.match(/\.(js|ts|jsx|tsx|css|scss|less|html|htm|vue|py|java|c|cpp|h|hpp|php|rb|go|rs|swift|kt|scala|sql|sh|bat|ps1|dockerfile|yaml|yml|toml|ini|conf|config|log)$/i)) {
      const response = await fetch(previewFile(name))
      filePreviewContent.value = await response.text()
      filePreviewUrl.value = ''
      filePreviewType.value = 'code'
    } else if (name.match(/\.(pdf)$/i)) {
      filePreviewUrl.value = previewFile(name)
      filePreviewContent.value = ''
      filePreviewType.value = 'pdf'
    } else if (name.match(/\.(docx|xlsx|pptx|doc|xls|ppt)$/i)) {
      // 使用微软Office在线预览
      const url = window.location.origin + previewFile(name)
      filePreviewUrl.value = `https://view.officeapps.live.com/op/view.aspx?src=${encodeURIComponent(url)}`
      filePreviewContent.value = ''
      filePreviewType.value = 'office'
    } else if (name.match(/\.(zip|rar|7z)$/i)) {
      // 压缩包预览（显示文件列表）
      filePreviewContent.value = '压缩包文件，请下载后解压查看内容。\n\n支持格式：ZIP、RAR、7Z'
      filePreviewUrl.value = ''
      filePreviewType.value = 'archive'
    } else if (name.match(/\.(mp3|wav|flac|aac|ogg|wma)$/i)) {
      // 音频文件预览
      filePreviewUrl.value = previewFile(name)
      filePreviewContent.value = ''
      filePreviewType.value = 'audio'
    } else {
      ElMessage.warning('不支持预览此类型文件，请下载后查看')
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

// 视频分页
const videoPage = ref(1)
const videoPageSize = ref(10)
const videoTotal = computed(() => videoList.value.length)
const videoPageData = computed(() => videoList.value.slice((videoPage.value-1)*videoPageSize.value, videoPage.value*videoPageSize.value))

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

// 新增：本机访问地址
const localUrl = ref(window.location.origin)
const copyLocalUrl = async () => {
  try {
    await navigator.clipboard.writeText(localUrl.value)
    ElMessage.success('地址已复制到剪贴板')
  } catch {
    // 降级方案：使用input+execCommand
    try {
      const input = document.createElement('input')
      input.value = localUrl.value
      document.body.appendChild(input)
      input.select()
      document.execCommand('copy')
      document.body.removeChild(input)
      ElMessage.success('地址已复制到剪贴板')
    } catch {
      ElMessage.error('复制失败，请手动复制')
    }
  }
}

// 文件详情弹窗
const fileDetailVisible = ref(false)
const fileDetail = ref<any>({})
const showFileDetail = (row: any) => {
  fileDetail.value = { ...row }
  fileDetailVisible.value = true
}

// 视频详情弹窗
const videoDetailVisible = ref(false)
const videoDetail = ref<any>({})
const showVideoDetail = (row: any) => {
  videoDetail.value = { ...row }
  videoDetailVisible.value = true
}

// 消息详情弹窗
const msgDetailVisible = ref(false)
const msgDetail = ref<any>({})
const showMsgDetail = (row: any) => {
  msgDetail.value = { ...row }
  msgDetailVisible.value = true
}

// 复制IP方法
const copyIp = async (ip: string) => {
  try {
    await navigator.clipboard.writeText(ip)
    ElMessage.success('IP已复制到剪贴板')
  } catch {
    try {
      const input = document.createElement('input')
      input.value = ip
      document.body.appendChild(input)
      input.select()
      document.execCommand('copy')
      document.body.removeChild(input)
      ElMessage.success('IP已复制到剪贴板')
    } catch {
      ElMessage.error('复制失败，请手动复制')
    }
  }
}

// 复制消息内容方法
const copyMsgContent = async (text: string) => {
  try {
    await navigator.clipboard.writeText(text)
    ElMessage.success('消息已复制到剪贴板')
  } catch {
    try {
      const input = document.createElement('input')
      input.value = text
      document.body.appendChild(input)
      input.select()
      document.execCommand('copy')
      document.body.removeChild(input)
      ElMessage.success('消息已复制到剪贴板')
    } catch {
      ElMessage.error('复制失败，请手动复制')
    }
  }
}

const handleFilePageChange = (val: number) => { filePage.value = val }
const handleVideoPageChange = (val: number) => { videoPage.value = val }

const showSettings = ref(false)

function handleSettingsSaved() {
  fetchMessageHistory()
  fetchFiles()
  fetchVideos()
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
    <!-- 地址栏靠左，设置按钮右上角浮动 -->
    <div class="top-row-bar">
      <div class="local-url-bar-flex">
        <span>本机访问地址：</span>
        <span class="local-url">{{ localUrl }}</span>
        <el-button type="primary" size="small" class="url-btn" @click="copyLocalUrl">复制</el-button>
      </div>
      <el-button type="primary" size="small" class="setting-btn" @click="showSettings = true">设置</el-button>
    </div>
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
            <div class="msg-title">当前消息：
              <el-button v-if="lastMessage" type="primary" link size="small" style="margin-left:8px;" @click="copyMsgContent(lastMessage)">复制</el-button>
            </div>
            <div class="msg-content" v-if="lastMessage">{{ lastMessage }}</div>
            <div class="msg-empty" v-else>暂无消息</div>
            
            <!-- 消息历史 -->
            <div v-if="showHistory" class="history-section">
              <div class="history-title">消息历史：</div>
              <div class="history-list">
                <div v-for="(item, index) in messageHistory" :key="index" class="history-item">
                  <div class="history-text">{{ item.text }}
                    <el-button type="primary" link size="small" style="margin-left:8px;" @click="copyMsgContent(item.text)">复制</el-button>
                  </div>
                  <div class="history-time">{{ new Date(item.timestamp).toLocaleString('zh-CN') }}
                    <el-button type="info" link size="small" @click="showMsgDetail(item)">
                      <el-icon><InfoFilled /></el-icon>
                    </el-button>
                  </div>
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
            <div class="selected-file-name" v-if="file">
              已选文件：{{ file.name }}
            </div>
            <div class="selected-file-name empty" v-else>
              暂未选择文件
            </div>
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
            <div class="table-scroll">
              <el-table :data="filePageData" border style="width: 100%;margin-top:8px;" size="small" :empty-text="'暂无文件'" highlight-current-row>
                <el-table-column prop="name" label="文件名" min-width="180">
                  <template #default="scope">
                    <span class="ellipsis" :title="scope.row.name">{{ scope.row.name }}</span>
                  </template>
                </el-table-column>
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
                <el-table-column label="操作" width="240" fixed="right">
                  <template #default="scope">
                    <el-tooltip content="预览" placement="top">
                      <el-button type="primary" link size="small" @click="previewFileHandler(scope.row.name)">
                        <el-icon><View /></el-icon>
                      </el-button>
                    </el-tooltip>
                    <el-tooltip content="下载" placement="top">
                      <el-button type="success" link size="small" @click="downloadFileHandler(scope.row.name)">
                        <el-icon><Download /></el-icon>
                      </el-button>
                    </el-tooltip>
                    <el-tooltip content="删除" placement="top">
                      <el-button type="danger" link size="small" @click="deleteFileHandler(scope.row.name)">
                        <el-icon><Delete /></el-icon>
                      </el-button>
                    </el-tooltip>
                    <el-tooltip content="详情" placement="top">
                      <el-button type="info" link size="small" @click="showFileDetail(scope.row)">
                        <el-icon><InfoFilled /></el-icon>
                      </el-button>
                    </el-tooltip>
                  </template>
                </el-table-column>
              </el-table>
            </div>
            <el-pagination
              v-if="fileTotal > filePageSize"
              style="margin: 8px 0 0 0; text-align: right;"
              background
              layout="prev, pager, next, jumper"
              :total="fileTotal"
              :page-size="filePageSize"
              :current-page.sync="filePage"
              @current-change="handleFilePageChange"
              :hide-on-single-page="true"
            />
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
            <div class="selected-file-name" v-if="video">
              已选视频：{{ video.name }}
            </div>
            <div class="selected-file-name empty" v-else>
              暂未选择视频
            </div>
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
            <div class="table-scroll">
              <el-table :data="videoPageData" border style="width: 100%;margin-top:8px;" size="small" :empty-text="'暂无视频'" highlight-current-row>
                <el-table-column prop="name" label="视频名" min-width="180">
                  <template #default="scope">
                    <span class="ellipsis" :title="scope.row.name">{{ scope.row.name }}</span>
                  </template>
                </el-table-column>
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
                <el-table-column label="操作" width="240" fixed="right">
                  <template #default="scope">
                    <el-tooltip content="预览" placement="top">
                      <el-button type="primary" link size="small" @click="previewVideoHandler(scope.row.name)">
                        <el-icon><View /></el-icon>
                      </el-button>
                    </el-tooltip>
                    <el-tooltip content="下载" placement="top">
                      <el-button type="success" link size="small" @click="downloadVideoHandler(scope.row.name)">
                        <el-icon><Download /></el-icon>
                      </el-button>
                    </el-tooltip>
                    <el-tooltip content="删除" placement="top">
                      <el-button type="danger" link size="small" @click="deleteVideoHandler(scope.row.name)">
                        <el-icon><Delete /></el-icon>
                      </el-button>
                    </el-tooltip>
                    <el-tooltip content="详情" placement="top">
                      <el-button type="info" link size="small" @click="showVideoDetail(scope.row)">
                        <el-icon><InfoFilled /></el-icon>
                      </el-button>
                    </el-tooltip>
                  </template>
                </el-table-column>
              </el-table>
            </div>
            <el-pagination
              v-if="videoTotal > videoPageSize"
              style="margin: 8px 0 0 0; text-align: right;"
              background
              layout="prev, pager, next, jumper"
              :total="videoTotal"
              :page-size="videoPageSize"
              :current-page.sync="videoPage"
              @current-change="handleVideoPageChange"
              :hide-on-single-page="true"
            />
          </div>
        </div>
      </div>
    </main>

    <!-- 文件预览对话框 -->
    <el-dialog v-model="filePreviewVisible" title="文件预览" width="80%" :before-close="() => filePreviewVisible = false">
      <div v-if="filePreviewType === 'image' && filePreviewUrl" class="preview-image">
        <img :src="filePreviewUrl" style="max-width: 100%; height: auto;" />
      </div>
      <div v-else-if="filePreviewType === 'text' && filePreviewContent" class="preview-text">
        <pre style="white-space: pre-wrap; word-break: break-all; max-height: 400px; overflow-y: auto;">{{ filePreviewContent }}</pre>
      </div>
      <div v-else-if="filePreviewType === 'code' && filePreviewContent" class="preview-code">
        <pre style="white-space: pre-wrap; word-break: break-all; max-height: 500px; overflow-y: auto; background: #f8f9fa; padding: 16px; border-radius: 8px; border: 1px solid #e9ecef; font-family: 'Courier New', monospace; font-size: 14px;">{{ filePreviewContent }}</pre>
      </div>
      <div v-else-if="filePreviewType === 'pdf' && filePreviewUrl" class="preview-pdf">
        <iframe :src="filePreviewUrl" style="width:100%;height:600px;border:none;"></iframe>
      </div>
      <div v-else-if="filePreviewType === 'office' && filePreviewUrl" class="preview-office">
        <iframe :src="filePreviewUrl" style="width:100%;height:600px;border:none;"></iframe>
      </div>
      <div v-else-if="filePreviewType === 'archive' && filePreviewContent" class="preview-archive">
        <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; border: 1px solid #e9ecef; text-align: center;">
          <pre style="white-space: pre-wrap; word-break: break-all; margin: 0; font-size: 16px;">{{ filePreviewContent }}</pre>
        </div>
      </div>
      <div v-else-if="filePreviewType === 'audio' && filePreviewUrl" class="preview-audio">
        <audio :src="filePreviewUrl" controls style="width: 100%; max-width: 500px; margin: 0 auto; display: block;"></audio>
      </div>
      <div v-else class="preview-unsupported">
        <span>无法预览该文件类型，请下载后查看。</span>
      </div>
    </el-dialog>

    <!-- 视频预览对话框 -->
    <el-dialog v-model="videoPreviewVisible" title="视频预览" width="80%" :before-close="() => videoPreviewVisible = false">
      <video v-if="videoPreviewUrl" :src="videoPreviewUrl" controls style="width: 100%; max-height: 500px;"></video>
    </el-dialog>

    <!-- 文件详情弹窗 -->
    <el-dialog v-model="fileDetailVisible" title="文件详情" width="400px">
      <div class="detail-item">
        <span class="detail-label">文件名：</span>
        <span class="detail-value">{{ fileDetail.name }}</span>
      </div>
      <div class="detail-item">
        <span class="detail-label">大小：</span>
        <span class="detail-value">{{ formatSize(fileDetail.size) }}</span>
      </div>
      <div class="detail-item">
        <span class="detail-label">修改时间：</span>
        <span class="detail-value">{{ formatDate(fileDetail.modified) }}</span>
      </div>
      <div class="detail-item">
        <span class="detail-label">上传IP：</span>
        <div class="ip-section">
          <span class="ip-address">{{ fileDetail.ip || '未知' }}</span>
          <el-button type="primary" size="small" @click="copyIp(fileDetail.ip)" :disabled="!fileDetail.ip">
            <el-icon><Download /></el-icon>复制IP
          </el-button>
        </div>
      </div>
    </el-dialog>

    <!-- 视频详情弹窗 -->
    <el-dialog v-model="videoDetailVisible" title="视频详情" width="400px">
      <div class="detail-item">
        <span class="detail-label">视频名：</span>
        <span class="detail-value">{{ videoDetail.name }}</span>
      </div>
      <div class="detail-item">
        <span class="detail-label">大小：</span>
        <span class="detail-value">{{ formatSize(videoDetail.size) }}</span>
      </div>
      <div class="detail-item">
        <span class="detail-label">修改时间：</span>
        <span class="detail-value">{{ formatDate(videoDetail.modified) }}</span>
      </div>
      <div class="detail-item">
        <span class="detail-label">上传IP：</span>
        <div class="ip-section">
          <span class="ip-address">{{ videoDetail.ip || '未知' }}</span>
          <el-button type="primary" size="small" @click="copyIp(videoDetail.ip)" :disabled="!videoDetail.ip">
            <el-icon><Download /></el-icon>复制IP
          </el-button>
        </div>
      </div>
    </el-dialog>

    <!-- 消息详情弹窗 -->
    <el-dialog v-model="msgDetailVisible" title="消息详情" width="400px">
      <div class="detail-item">
        <span class="detail-label">内容：</span>
        <div class="detail-value message-content">{{ msgDetail.text }}</div>
      </div>
      <div class="detail-item">
        <span class="detail-label">时间：</span>
        <span class="detail-value">{{ new Date(msgDetail.timestamp).toLocaleString('zh-CN') }}</span>
      </div>
      <div class="detail-item">
        <span class="detail-label">发送IP：</span>
        <div class="ip-section">
          <span class="ip-address">{{ msgDetail.ip || '未知' }}</span>
          <el-button type="primary" size="small" @click="copyIp(msgDetail.ip)" :disabled="!msgDetail.ip">
            <el-icon><Download /></el-icon>复制IP
          </el-button>
        </div>
      </div>
    </el-dialog>

    <SettingsDialog v-model="showSettings" @saved="handleSettingsSaved" />
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
  padding: 24px 8px;
  max-width: 1920px;
  margin-left: auto;
  margin-right: auto;
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
  font-size: 36px;
  font-weight: bold;
  color: #2c3e50;
}

.subtitle {
  font-size: 22px;
  color: #7f8c8d;
}

.main-content {
  display: grid;
  gap: 24px;
  max-width: 1920px;
  margin: 0 auto;
  padding: 0 8px;
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
  font-size: 26px;
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

.btn, .upload-btn {
  font-size: 22px !important;
  height: 54px;
  font-weight: 500;
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

.top-row-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 12px 0 16px 0;
  max-width: 1920px;
  margin-left: auto;
  margin-right: auto;
}
.local-url-bar-flex {
  background: #f8f9fa;
  border-radius: 10px;
  padding: 10px 18px;
  font-size: 15px;
  color: #2c3e50;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  gap: 8px;
}
.url-btn {
  height: 32px !important;
  border-radius: 8px !important;
  font-size: 18px !important;
  padding: 0 18px !important;
  font-weight: 500;
}
.setting-btn {
  height: 32px !important;
  border-radius: 8px !important;
  font-size: 18px !important;
  padding: 0 18px !important;
  font-weight: 500;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.local-url {
  font-weight: bold;
  color: #3b82f6;
  margin-left: 4px;
  margin-right: 8px;
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
  .top-row-bar {
    flex-direction: column;
    gap: 8px;
    align-items: stretch;
  }
  .local-url-bar-flex {
    flex-wrap: wrap;
    gap: 6px;
    justify-content: flex-start;
  }
  .setting-btn {
    align-self: flex-end;
    margin-top: 4px;
  }
}

.table-scroll {
  max-height: 300px;
  overflow-y: auto;
  background: #fff;
  border-radius: 8px;
}

.ellipsis {
  display: inline-block;
  max-width: 140px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  vertical-align: middle;
}
.el-table .el-button + .el-button {
  margin-left: 4px;
}
.el-table .el-button[link][type="danger"] {
  color: #e74c3c;
}
.el-table .el-button[link][type="success"] {
  color: #27ae60;
}
.el-table .el-button[link][type="primary"] {
  color: #2563eb;
}

.selected-file-name {
  margin: 6px 0 0 0;
  font-size: 14px;
  color: #2563eb;
  word-break: break-all;
}
.selected-file-name.empty {
  color: #aaa;
}

.el-dialog__body {
  padding: 32px 32px 24px 32px !important;
}

.detail-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 20px;
  font-size: 22px;
}
.detail-label {
  font-weight: bold;
  color: #2c3e50;
  min-width: 100px;
  text-align: right;
  margin-right: 12px;
  flex-shrink: 0;
}
.detail-value, .ip-address {
  color: #2563eb;
  font-size: 22px;
  word-break: break-all;
}
.ip-section {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 2px;
}
.el-dialog__title {
  font-size: 26px !important;
  font-weight: bold;
  letter-spacing: 1px;
}
.el-dialog {
  border-radius: 16px !important;
}

body, .main-bg {
  font-size: 22px;
}

.el-input__inner, .el-textarea__inner {
  font-size: 22px !important;
}
</style>
