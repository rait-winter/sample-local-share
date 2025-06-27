<template>
  <div>
    <h2>消息管理</h2>
    <div class="message-input">
      <textarea 
        v-model="msg" 
        placeholder="输入消息内容..." 
        class="message-textarea"
        @keydown.ctrl.enter="send"
      ></textarea>
      <div class="input-actions">
        <button @click="send" class="btn" :disabled="!msg.trim()">发送</button>
        <button @click="clearInput" class="btn btn-secondary" :disabled="!msg.trim()">清空</button>
        <span class="hint">Ctrl+Enter 快速发送</span>
      </div>
    </div>
    
    <div class="current-message">
      <h3>当前消息</h3>
      <div v-if="currentMsg" class="message-content">
        {{ currentMsg }}
      </div>
      <div v-else class="empty-message">
        暂无消息
      </div>
    </div>
    
    <div class="message-history">
      <h3>消息历史</h3>
      <button @click="loadHistory" class="btn btn-small">刷新历史</button>
      <div v-if="history.length === 0" class="empty-history">
        暂无历史记录
      </div>
      <div v-else class="history-list">
        <div v-for="(item, index) in history" :key="index" class="history-item">
          <div class="history-content">{{ item.text }}</div>
          <div class="history-time">{{ formatDate(item.timestamp) }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { sendMessage, getMessage, getMessageHistory, type MessageHistory } from '../api/message'

const msg = ref('')
const currentMsg = ref('')
const history = ref<MessageHistory[]>([])
let pollInterval: number | null = null

async function send() {
  if (!msg.value.trim()) return
  
  try {
    await sendMessage(msg.value.trim())
    msg.value = ''
    await load()
    await loadHistory()
  } catch (error: any) {
    alert('发送失败: ' + (error.response?.data?.error || error.message))
  }
}

function clearInput() {
  msg.value = ''
}

async function load() {
  try {
    const res = await getMessage()
    currentMsg.value = res.data.text
  } catch (error: any) {
    console.error('加载消息失败:', error)
  }
}

async function loadHistory() {
  try {
    const res = await getMessageHistory()
    history.value = res.data.history
  } catch (error: any) {
    console.error('加载历史记录失败:', error)
  }
}

function formatDate(timestamp: string): string {
  return new Date(timestamp).toLocaleString('zh-CN')
}

// 开始自动轮询
function startPolling() {
  pollInterval = window.setInterval(() => {
    load()
    loadHistory()
  }, 5000) // 每5秒刷新一次
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
  loadHistory()
  startPolling()
})

onUnmounted(() => {
  stopPolling()
})
</script>

<style scoped>
.message-input {
  margin-bottom: 20px;
}

.message-textarea {
  width: 100%;
  height: 80px;
  padding: 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  resize: vertical;
  font-family: inherit;
  font-size: 14px;
}

.message-textarea:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.input-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
}

.hint {
  font-size: 12px;
  color: #666;
  margin-left: auto;
}

.current-message {
  margin-bottom: 20px;
}

.message-content {
  background: #f0f9ff;
  border: 1px solid #bae6fd;
  border-radius: 8px;
  padding: 12px;
  margin-top: 8px;
  white-space: pre-wrap;
  word-break: break-word;
}

.empty-message {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 12px;
  margin-top: 8px;
  text-align: center;
  color: #666;
}

.message-history {
  margin-top: 20px;
}

.history-list {
  margin-top: 12px;
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
}

.history-item {
  padding: 12px;
  border-bottom: 1px solid #f3f4f6;
}

.history-item:last-child {
  border-bottom: none;
}

.history-content {
  margin-bottom: 4px;
  white-space: pre-wrap;
  word-break: break-word;
}

.history-time {
  font-size: 12px;
  color: #666;
}

.empty-history {
  text-align: center;
  color: #666;
  padding: 32px;
  background: #f9fafb;
  border-radius: 8px;
  margin-top: 12px;
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
</style> 