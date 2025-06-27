<template>
  <div>
    <h2>文件</h2>
    <input type="file" @change="onFileChange" />
    <button @click="upload" class="btn">上传</button>
    <h3 style="margin-top:16px;">可下载文件列表</h3>
    <ul>
      <li v-for="file in files" :key="file">
        {{ file }}
        <button @click="preview(file)" class="btn">预览</button>
        <a :href="downloadUrl(file)" download class="btn">下载</a>
      </li>
    </ul>
    <div v-if="previewContent" style="margin-top:10px;">
      <div v-html="previewContent"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { uploadFile, listFiles, downloadFile, previewFile } from '../api/file'

const files = ref<string[]>([])
const fileObj = ref<File | null>(null)
const previewContent = ref('')

function onFileChange(e: Event) {
  const target = e.target as HTMLInputElement
  fileObj.value = target.files ? target.files[0] : null
}
function upload() {
  if (!fileObj.value) return
  uploadFile(fileObj.value).then(() => {
    fileObj.value = null
    load()
  })
}
function load() {
  listFiles().then(res => {
    files.value = res.data.files
  })
}
function downloadUrl(name: string) {
  return downloadFile(name)
}
function preview(name: string) {
  fetch(previewFile(name)).then(res => {
    if (name.match(/\.(png|jpg|jpeg|gif|bmp)$/i)) {
      previewContent.value = `<img src='${previewFile(name)}' style='max-width:100%;' />`
    } else {
      res.text().then(html => {
        previewContent.value = html
      })
    }
  })
}
onMounted(load)
</script>

<style scoped>
.btn {
  background: #2563eb;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 6px 16px;
  margin-right: 6px;
  cursor: pointer;
}
.btn:hover {
  background: #1746a2;
}
</style> 