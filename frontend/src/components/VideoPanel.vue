<template>
  <div>
    <h2>视频</h2>
    <input type="file" @change="onFileChange" accept="video/*" />
    <button @click="upload" class="btn">上传</button>
    <h3 style="margin-top:16px;">可下载视频列表</h3>
    <ul>
      <li v-for="video in videos" :key="video">
        {{ video }}
        <button @click="preview(video)" class="btn">预览</button>
        <a :href="downloadUrl(video)" download class="btn">下载</a>
      </li>
    </ul>
    <video v-if="previewUrl" :src="previewUrl" controls style="width:320px;margin-top:10px;border-radius:8px;"></video>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { uploadVideo, listVideos, downloadVideo, previewVideo } from '../api/video'

const videos = ref<string[]>([])
const fileObj = ref<File | null>(null)
const previewUrl = ref('')

function onFileChange(e: Event) {
  const target = e.target as HTMLInputElement
  fileObj.value = target.files ? target.files[0] : null
}
function upload() {
  if (!fileObj.value) return
  uploadVideo(fileObj.value).then(() => {
    fileObj.value = null
    load()
  })
}
function load() {
  listVideos().then(res => {
    videos.value = res.data.videos
  })
}
function downloadUrl(name: string) {
  return downloadVideo(name)
}
function preview(name: string) {
  previewUrl.value = previewVideo(name)
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