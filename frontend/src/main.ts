import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App)
app.use(ElementPlus)
app.mount('#app')

const onDropFile = (e: DragEvent) => {
  // 可选：实现拖拽上传逻辑
};
const onDropVideo = (e: DragEvent) => {
  // 可选：实现拖拽上传逻辑
};
