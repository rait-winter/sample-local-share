# 内网共享工具

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](../../pulls)
[![Issues](https://img.shields.io/github/issues/rait-winter/sample-local-share.svg)](../../issues)
[![Stars](https://img.shields.io/github/stars/rait-winter/sample-local-share.svg)](../../stargazers)

一个基于Python Flask后端和Vue3前端的局域网文件、消息、视频共享工具，支持多终端实时同步。

## ✨ 核心特性
- 一体化启动，前后端同端口，自动分配随机五位数端口
- 局域网自动获取本机IP，便于多端访问
- 消息、文件、视频上传/下载/预览/删除，实时同步
- 日志自动写入项目根目录 backend.log，便于排查
- 代码结构清晰，文档完善，易于维护

## 🚀 快速开始

### 环境要求
- Python 3.7+
- Node.js 16.9.0+
- 现代浏览器

### 一体化启动（推荐/唯一方式）
```bash
# 双击运行
start_unified.bat
# 启动后自动弹出浏览器，访问 http://[本机IP]:[随机端口]
```

### 日志文件
- 所有后端日志自动写入项目根目录 backend.log
- 包含访问日志、异常、警告等

### 目录结构
```
project/
├── backend/                 # Flask后端
│   ├── api/                # API模块
│   ├── app.py              # 主应用
│   └── ...
├── frontend/               # Vue3前端
│   ├── src/                # 源码目录
│   └── ...
├── docs/                   # 项目文档
├── start_unified.bat       # 一体化启动脚本
├── backend.log             # 后端日志
└── README.md               # 项目说明
```

## 📖 详细文档
- [一体化启动说明](docs/一体化启动说明.md)
- [API文档](docs/API文档.md)
- [部署与运维](docs/部署与运维.md)
- [安全与合规](docs/安全与合规.md)
- [FAQ](docs/FAQ.md)
- [项目总结](docs/项目总结.md)

## 📝 常见问题
- 启动后未弹出页面？请检查Python/Node环境，或手动访问控制台提示的局域网地址
- 日志文件未生成？请确认有写入权限，或检查backend.log是否在根目录
- 其他问题请查阅FAQ或日志文件

## 🤝 贡献指南
欢迎任何形式的贡献！Fork项目、创建分支、提交PR。

---
如有建议或问题，请通过Issue联系维护者。

## 🎯 使用场景

- **团队协作**：快速分享文件和消息
- **演示展示**：实时共享演示材料
- **文件传输**：局域网内大文件传输
- **临时存储**：临时文件存储和分享

## 🔒 安全特性

- **文件类型限制**：只允许安全文件类型
- **文件大小限制**：防止超大文件上传
- **文件名安全**：自动处理特殊字符
- **删除确认**：防止误删重要文件

## 🚀 性能优化

- **实时轮询**：智能轮询间隔（消息5秒，文件/视频10秒）
- **文件去重**：自动处理重名文件
- **响应式设计**：支持移动端访问
- **错误处理**：完善的错误提示和处理

## 🗂️ 目录结构说明
- `backend/uploads/`、`backend/videos/` 目录为上传/视频存储目录，已添加 `.gitkeep` 文件保证空目录在GitHub可见。
- 仅保留核心源码、配置、文档，所有临时、历史、产物、依赖等文件已清理。

## 📄 开源协议
本项目采用 MIT License，详见 LICENSE 文件。

## 🤝 贡献指南
欢迎任何形式的贡献！请先 Fork 项目，创建分支后提交 Pull Request。

## 📝 其他说明
如有建议或问题，请通过 Issue 联系维护者。

## 📖 API 文档（简要示例）

### 消息相关
- `GET /api/message/history`  获取消息历史
  **返回：**
  ```json
  [
    {"content": "hello", "timestamp": "2024-06-01 12:00:00"}
  ]
  ```
- `POST /api/message/`  发送消息
  **参数：**
  ```json
  { "content": "hello" }
  ```
  **返回：**
  ```json
  { "success": true }
  ```

### 文件相关
- `GET /api/file/list`  获取文件列表
- `POST /api/file/upload`  上传文件（form-data）
- `GET /api/file/download/<filename>`  下载文件

### 视频相关
- `GET /api/video/list`  获取视频列表
- `POST /api/video/upload`  上传视频（form-data）
- `GET /api/video/download/<filename>`  下载视频

> 更多详细参数和返回格式请见 [docs/API文档.md](docs/API文档.md)

--- 