<template>
  <div class="global-search-bar">
    <div class="search-box">
      <input
        v-model="keyword"
        @keydown.enter="onSearch"
        placeholder="全局搜索：文件、视频、消息..."
        class="search-input"
        :disabled="loading"
        ref="searchInputRef"
      />
      <button @click="onSearch" :disabled="loading || !keyword.trim()" class="search-btn">搜索</button>
    </div>
    <transition name="fade">
      <div v-if="showResult" class="search-result-card">
        <div class="tabs">
          <span v-for="tab in tabs" :key="tab.key" :class="['tab', {active: tab.key === activeTab}]" @click="activeTab = tab.key">
            {{ tab.label }} <span v-if="result[tab.key]">({{ result[tab.key].length }})</span>
          </span>
        </div>
        <div class="tab-content">
          <!-- 文件tab -->
          <div v-if="activeTab === 'file'">
            <div v-if="result.file.length === 0" class="empty">无相关文件</div>
            <div v-for="item in (showAll.file ? result.file : result.file.slice(0,5))" :key="item.name" class="item clickable" @click="downloadFileHandler(item.name)">
              <span class="item-title" v-html="renderHighlight((item as FileResult).name, (item as FileResult).highlight)"></span>
              <span class="item-meta">{{ formatFileSize((item as FileResult).size) }} | {{ formatDate((item as FileResult).modified) }}</span>
              <button class="item-action" @click.stop="downloadFileHandler(item.name)">下载</button>
            </div>
            <button v-if="result.file.length > 5" class="show-more-btn" @click="toggleShowAll('file')">
              {{ showAll.file ? '收起' : '查看更多' }}
            </button>
          </div>
          <!-- 视频tab -->
          <div v-if="activeTab === 'video'">
            <div v-if="result.video.length === 0" class="empty">无相关视频</div>
            <div v-for="item in (showAll.video ? result.video : result.video.slice(0,5))" :key="item.name" class="item clickable" @click="previewVideoHandler(item.name)">
              <span class="item-title" v-html="renderHighlight((item as VideoResult).name, (item as VideoResult).highlight)"></span>
              <span class="item-meta">{{ formatFileSize((item as VideoResult).size) }} | {{ formatDate((item as VideoResult).modified) }}</span>
              <button class="item-action" @click.stop="downloadVideoHandler(item.name)">下载</button>
              <button class="item-action" @click.stop="previewVideoHandler(item.name)">预览</button>
            </div>
            <button v-if="result.video.length > 5" class="show-more-btn" @click="toggleShowAll('video')">
              {{ showAll.video ? '收起' : '查看更多' }}
            </button>
          </div>
          <!-- 消息tab -->
          <div v-if="activeTab === 'message'">
            <div v-if="result.message.length === 0" class="empty">无相关消息</div>
            <div v-for="item in (showAll.message ? result.message : result.message.slice(0,5))" :key="item.id || item.timestamp" class="item clickable" @click="copyMsg(item.text)">
              <span class="item-title" v-html="renderHighlight((item as MessageResult).text, (item as MessageResult).highlight)"></span>
              <span class="item-meta">{{ formatDate((item as MessageResult).timestamp) }}</span>
              <button class="item-action" @click.stop="copyMsg(item.text)">复制</button>
            </div>
            <button v-if="result.message.length > 5" class="show-more-btn" @click="toggleShowAll('message')">
              {{ showAll.message ? '收起' : '查看更多' }}
            </button>
          </div>
          <!-- 图片tab -->
          <div v-if="activeTab === 'image'">
            <div v-if="result.image.length === 0" class="empty">无相关图片</div>
            <div v-for="item in (showAll.image ? result.image : result.image.slice(0,5))" :key="item.name" class="item clickable" @click="previewImage(item.name)">
              <img :src="`/api/file/preview/${encodeURIComponent(item.name)}`" alt="Image" class="image-thumb">
            </div>
            <button v-if="result.image.length > 5" class="show-more-btn" @click="toggleShowAll('image')">
              {{ showAll.image ? '收起' : '查看更多' }}
            </button>
          </div>
        </div>
        <div v-if="!loading && searched && !hasResult" class="search-empty">未找到相关内容</div>
      </div>
    </transition>
    <div v-if="loading" class="search-loading">搜索中...</div>
    <div v-if="showImagePreview" class="image-preview-modal" @click="showImagePreview = false">
      <img :src="previewImageUrl" alt="Image Preview" @click.stop="showImagePreview = false">
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { globalSearch, type GlobalSearchResult } from '../api/globalSearch'

interface FileResult { name: string; size: number; modified: number; highlight?: any; }
interface VideoResult { name: string; size: number; modified: number; highlight?: any; }
interface MessageResult { text: string; timestamp: string; id?: string|number; highlight?: any; }

const keyword = ref('')
const loading = ref(false)
const searched = ref(false)
const result = ref<GlobalSearchResult>({ file: [], image: [], video: [], message: [] })
const activeTab = ref<keyof GlobalSearchResult>('file')
const tabs: { key: keyof GlobalSearchResult; label: string }[] = [
  { key: 'file', label: '文件' },
  { key: 'image', label: '图片' },
  { key: 'video', label: '视频' },
  { key: 'message', label: '消息' }
]
const previewImageUrl = ref('')
const showImagePreview = ref(false)
function previewImage(name: string) {
  console.log('预览图片', name);
  if (!name || typeof name !== 'string') {
    alert('图片名无效，无法预览');
    return;
  }
  previewImageUrl.value = `/api/file/preview/${encodeURIComponent(name)}`
  showImagePreview.value = true
}
const showAll = ref<{ [key: string]: boolean }>({ file: false, image: false, video: false, message: false })
const hasResult = computed(() => {
  return result.value.file.length > 0 || result.value.image.length > 0 || result.value.video.length > 0 || result.value.message.length > 0
})
const showResult = computed(() => searched.value && (keyword.value.trim() || loading.value))

const searchInputRef = ref<HTMLInputElement | null>(null)

function focusSearch() {
  searchInputRef.value?.focus()
}

function handleGlobalKeydown(e: KeyboardEvent) {
  if ((e.ctrlKey && e.key.toLowerCase() === 'k') || e.key === '/') {
    e.preventDefault()
    focusSearch()
  }
  if (e.key === 'Escape') {
    closeResult()
  }
}

function closeResult() {
  searched.value = false
}

function handleClickOutside(e: MouseEvent) {
  const searchBar = document.querySelector('.global-search-bar')
  if (searchBar && !searchBar.contains(e.target as Node)) {
    closeResult()
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleGlobalKeydown)
  window.addEventListener('mousedown', handleClickOutside)
})
onUnmounted(() => {
  window.removeEventListener('keydown', handleGlobalKeydown)
  window.removeEventListener('mousedown', handleClickOutside)
})

async function onSearch() {
  if (!keyword.value.trim()) return
  loading.value = true
  searched.value = false
  result.value = { file: [], image: [], video: [], message: [] }
  try {
    const res = await globalSearch(keyword.value)
    result.value = res.data
    searched.value = true
  } catch (e) {
    alert('搜索失败')
  } finally {
    loading.value = false
  }
}

function formatFileSize(bytes: number): string {
  if (!bytes) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}
function formatDate(ts: number | string): string {
  if (!ts) return ''
  const d = typeof ts === 'number' ? new Date(ts * 1000) : new Date(ts)
  return d.toLocaleString('zh-CN')
}
function renderHighlight(text: string, highlight: any): string {
  if (!highlight || !text) return text
  if (highlight.type === 'direct' && highlight.range) {
    const [start, end] = highlight.range
    return (
      text.slice(0, start) +
      `<mark class='hl-direct'>${text.slice(start, end)}</mark>` +
      text.slice(end)
    )
  }
  if (highlight.type === 'pinyin' && highlight.keyword) {
    // 只高亮首个出现的拼音命中
    const idx = text.toLowerCase().indexOf(highlight.keyword)
    if (idx >= 0) {
      return (
        text.slice(0, idx) +
        `<mark class='hl-pinyin'>${text.slice(idx, idx + highlight.keyword.length)}</mark>` +
        text.slice(idx + highlight.keyword.length)
      )
    }
    return `<mark class='hl-pinyin'>${text}</mark>`
  }
  if (highlight.type === 'segment' && highlight.keyword) {
    const reg = new RegExp(highlight.keyword, 'gi')
    return text.replace(reg, m => `<mark class='hl-segment'>${m}</mark>`)
  }
  return text
}
// 复制功能优化
function copyMsg(text: string) {
  if (!text || typeof text !== 'string') {
    alert('内容无效，无法复制');
    return;
  }
  try {
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text)
        .then(() => alert('消息已复制'))
        .catch(() => fallbackCopy(text));
    } else {
      fallbackCopy(text);
    }
  } catch {
    fallbackCopy(text);
  }
}
function fallbackCopy(text: string) {
  try {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    document.body.appendChild(textarea);
    textarea.focus();
    textarea.select();
    const success = document.execCommand('copy');
    document.body.removeChild(textarea);
    if (success) {
      alert('消息已复制');
    } else {
      alert('复制失败，请手动选中内容复制');
    }
  } catch {
    alert('复制失败，请手动选中内容复制');
  }
}
function downloadFileHandler(name: string) {
  console.log('下载文件', name);
  if (!name || typeof name !== 'string') {
    alert('文件名无效，无法下载');
    return;
  }
  const url = `/api/file/download/${encodeURIComponent(name)}`;
  const a = document.createElement('a');
  a.href = url;
  a.download = name;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}
function downloadVideoHandler(name: string) {
  console.log('下载视频', name);
  if (!name || typeof name !== 'string') {
    alert('视频名无效，无法下载');
    return;
  }
  const url = `/api/video/download/${encodeURIComponent(name)}`;
  const a = document.createElement('a');
  a.href = url;
  a.download = name;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}
function previewVideoHandler(name: string) {
  console.log('预览视频', name);
  if (!name || typeof name !== 'string') {
    alert('视频名无效，无法预览');
    return;
  }
  const url = `/api/video/preview/${encodeURIComponent(name)}`;
  window.open(url, '_blank');
}

function toggleShowAll(tab: string) {
  showAll.value[tab] = !showAll.value[tab]
}
</script>

<style scoped>
.global-search-bar {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 32px 0 24px 0;
  position: relative;
  z-index: 20;
}
.search-box {
  display: flex;
  align-items: center;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
  padding: 16px 24px;
  width: 420px;
  max-width: 90vw;
  margin-bottom: 0;
}
.search-input {
  flex: 1;
  padding: 10px 16px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 16px;
  margin-right: 8px;
}
.search-btn {
  padding: 10px 24px;
  background: #2563eb;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.2s;
}
.search-btn:disabled {
  background: #bcd0f7;
  cursor: not-allowed;
}
.search-result-card {
  position: absolute;
  top: 60px;
  left: 50%;
  transform: translateX(-50%);
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.12);
  padding: 24px 32px 16px 32px;
  min-width: 380px;
  max-width: 90vw;
  min-height: 120px;
  z-index: 100;
  margin-top: 8px;
}
.tabs {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
  border-bottom: 1px solid #f3f4f6;
}
.tab {
  cursor: pointer;
  padding: 4px 16px 8px 16px;
  border-radius: 8px 8px 0 0;
  font-weight: 500;
  color: #2563eb;
  background: #f3f6fd;
  transition: background 0.2s;
  font-size: 16px;
}
.tab.active {
  background: #2563eb;
  color: #fff;
}
.tab-content {
  min-height: 80px;
}
.item {
  padding: 8px 0;
  border-bottom: 1px solid #f3f4f6;
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: background 0.15s;
}
.item:last-child {
  border-bottom: none;
}
.item:hover {
  background: #f3f6fd;
}
.item-title {
  font-size: 16px;
  font-weight: 500;
  flex: 1;
}
.item-meta {
  font-size: 12px;
  color: #888;
  margin-right: 8px;
}
.item-action {
  background: #f3f6fd;
  border: none;
  border-radius: 6px;
  padding: 4px 10px;
  margin-left: 4px;
  color: #2563eb;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.2s;
}
.item-action:hover {
  background: #2563eb;
  color: #fff;
}
.empty {
  color: #aaa;
  padding: 16px 0;
  text-align: center;
}
.search-empty {
  color: #888;
  text-align: center;
  margin-top: 32px;
  font-size: 16px;
}
.search-loading {
  color: #2563eb;
  margin-top: 12px;
  font-size: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.search-loading::before {
  content: '';
  display: inline-block;
  width: 18px;
  height: 18px;
  border: 3px solid #bcd0f7;
  border-top: 3px solid #2563eb;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
mark {
  background: #ffe066;
  color: #222;
  border-radius: 2px;
  padding: 0 2px;
}
mark.hl-direct {
  background: #ffe066;
  color: #222;
}
mark.hl-pinyin {
  background: #b2f2ff;
  color: #222;
}
mark.hl-segment {
  background: #ffd6e0;
  color: #222;
}
.show-more-btn {
  display: block;
  margin: 12px auto 0 auto;
  background: #f3f6fd;
  border: none;
  border-radius: 8px;
  color: #2563eb;
  font-size: 15px;
  padding: 6px 24px;
  cursor: pointer;
  transition: background 0.2s;
}
.show-more-btn:hover {
  background: #2563eb;
  color: #fff;
}
.image-thumb {
  width: 64px;
  height: 64px;
  object-fit: cover;
  border-radius: 8px;
  border: 1px solid #eee;
  margin-right: 12px;
  cursor: pointer;
  transition: box-shadow 0.2s;
}
.image-thumb:hover {
  box-shadow: 0 2px 8px rgba(37,99,235,0.15);
}
.image-preview-modal {
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0,0,0,0.7);
  position: fixed;
  left: 0; top: 0; right: 0; bottom: 0;
  z-index: 9999;
}
.image-preview-modal img {
  max-width: 90vw;
  max-height: 90vh;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.25);
}
@media (max-width: 600px) {
  .search-box, .search-result-card {
    width: 98vw;
    min-width: unset;
    padding: 12px 6px;
  }
  .search-result-card {
    left: 0;
    transform: none;
    right: 0;
    margin: 0 auto;
  }
}
</style> 