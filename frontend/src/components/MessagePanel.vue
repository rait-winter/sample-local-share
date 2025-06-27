<template>
  <div>
    <h2>消息</h2>
    <textarea v-model="msg" placeholder="输入消息..." style="width:100%;height:60px;"></textarea>
    <button @click="send" class="btn">发送</button>
    <div style="margin-top:10px;background:#f4f6fa;padding:8px;border-radius:4px;">
      <strong>可粘贴的消息内容：</strong>
      <div>{{ currentMsg }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { sendMessage, getMessage } from '../api/message'

const msg = ref('')
const currentMsg = ref('')

function send() {
  if (!msg.value.trim()) return
  sendMessage(msg.value).then(() => {
    msg.value = ''
    load()
  })
}
function load() {
  getMessage().then(res => {
    currentMsg.value = res.data.text
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
  margin-top: 8px;
  cursor: pointer;
}
.btn:hover {
  background: #1746a2;
}
</style> 