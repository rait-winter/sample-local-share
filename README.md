# 内网共享工具

基于 Flask（后端）+ Vue3 + Element Plus（前端）的局域网文件/消息/视频共享工具，支持多端访问，界面美观，适合公司、实验室、家庭等内网环境下的临时文件、消息、视频互传。

---

## 功能特性

- **消息区**：文本消息的发送与展示
- **文件区**：文件上传、下载、列表展示，支持拖拽上传
- **视频区**：视频上传、下载、列表展示，支持拖拽上传
- **响应式布局**：大屏横向分栏，移动端自动竖排
- **现代化 UI**：Element Plus 组件，美观易用
- **前后端分离**：API 规范，易于扩展

---

## 目录结构

```
project-root/
├── backend/           # Flask 后端
│   ├── app.py
│   └── api/           # 各功能蓝图
├── frontend/          # Vue3 + Element Plus 前端
│   ├── src/
│   │   ├── api/       # 前端 API 封装
│   │   ├── App.vue
│   │   └── ...
│   ├── public/
│   ├── package.json
│   └── ...
├── README.md
└── ...
```

---

## 快速启动

### 1. 后端（Flask）

```bash
cd backend
pip install -r requirements.txt
python app.py
```
默认监听 5000 端口，可在 `app.py` 中修改。

### 2. 前端（Vue3）

```bash
cd frontend
npm install
npm run dev
```
默认监听 5173 端口，支持内网访问。

---

## 常见问题

- **端口冲突**：可在 `backend/app.py` 和 `frontend/vite.config.ts` 中修改端口。
- **API 跨域**：前端已配置代理，开发环境无需担心跨域。
- **静态资源问题**：logo 等图片建议放在 `public` 或用网络图片。

---

## 贡献指南

1. Fork 本仓库并 clone 到本地
2. 新建分支进行开发
3. 提交 PR 并描述你的修改内容

---

## License

MIT 