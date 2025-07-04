// main.ts
// 前端应用入口文件，负责创建Vue应用实例、挂载根组件、引入全局样式等

import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App)
app.use(ElementPlus)
app.mount('#app')
