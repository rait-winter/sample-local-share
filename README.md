# 内网共享工具

一个基于Python Flask后端和Vue3前端的局域网文件、消息、视频共享工具，支持多终端实时同步。

## ✨ 功能特性

### 📝 消息管理
- **实时消息发送**：支持多行文本消息发送
- **消息历史记录**：查看最近50条消息历史
- **快捷键支持**：Ctrl+Enter快速发送
- **实时同步**：多终端5秒自动同步

### 📁 文件管理
- **文件上传**：支持拖拽上传，最大100MB
- **文件预览**：支持图片和文本文件预览
- **文件下载**：一键下载文件
- **文件删除**：安全删除确认
- **文件列表**：显示文件名、大小、修改时间
- **实时同步**：多终端10秒自动同步

### 🎥 视频管理
- **视频上传**：支持多种视频格式，最大500MB
- **视频预览**：在线视频播放
- **视频下载**：一键下载视频
- **视频删除**：安全删除确认
- **视频列表**：显示视频名、大小、修改时间
- **实时同步**：多终端10秒自动同步

## 🚀 快速开始

### 环境要求
- Python 3.7+
- Node.js 16.9.0+
- 现代浏览器

### 一键启动

#### Windows用户
```bash
# 启动后端服务
start_backend.bat

# 启动前端服务（新终端）
start_frontend.bat
```

#### 手动启动
```bash
# 1. 启动后端
cd backend
pip install -r requirements.txt
python app.py

# 2. 启动前端（新终端）
cd frontend
npm install
npm run dev
```

### 访问地址
- 前端界面：http://localhost:5173
- 后端API：http://localhost:8000
- 内网访问：http://[你的IP]:5173

## 📁 项目结构

```
project/
├── backend/                 # Flask后端
│   ├── api/                # API模块
│   │   ├── message.py      # 消息API
│   │   ├── file.py         # 文件API
│   │   └── video.py        # 视频API
│   ├── uploads/            # 文件存储目录
│   ├── videos/             # 视频存储目录
│   ├── app.py              # 主应用
│   └── requirements.txt    # Python依赖
├── frontend/               # Vue3前端
│   ├── src/
│   │   ├── api/           # API封装
│   │   │   ├── message.ts # 消息API
│   │   │   ├── file.ts    # 文件API
│   │   │   └── video.ts   # 视频API
│   │   └── App.vue        # 主组件
│   ├── package.json       # Node.js依赖
│   └── vite.config.ts     # Vite配置
├── docs/                  # 项目文档
├── start_backend.bat      # 后端启动脚本
├── start_frontend.bat     # 前端启动脚本
└── README.md             # 项目说明
```

## 🔧 技术栈

### 后端
- **Flask**：轻量级Web框架
- **Flask-CORS**：跨域支持
- **Werkzeug**：文件处理

### 前端
- **Vue 3**：渐进式JavaScript框架
- **TypeScript**：类型安全
- **Element Plus**：UI组件库
- **Vite**：构建工具
- **Axios**：HTTP客户端

## 📖 详细文档

- [API文档](docs/API文档.md) - 完整的API接口说明
- [启动指南](docs/启动指南.md) - 详细的安装和启动步骤
- [项目总结](docs/项目总结.md) - 项目开发总结和优化建议

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

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 📄 许可证

MIT License

## 📞 联系方式

如有问题或建议，请提交Issue或联系开发者。

---

**享受安全、极速的内网共享体验！** 🎉 

## 前端启动与端口说明
- 启动命令：
  ```sh
  cd frontend
  npm install
  npm run dev
  ```
- 启动时端口为**随机五位数**（10000~65535），每次自动分配。
- 启动后自动尝试开放防火墙端口（仅限 Windows 原生 PowerShell/CMD，需 netsh）。
- 关闭 Vite 时自动关闭防火墙端口。
- 若无 netsh，会有警告但不影响开发，需手动确保内网可访问该端口。

## 防火墙与内网访问
- 若未自动开放端口，需手动在 Windows 防火墙中添加入站规则，允许对应端口被内网访问。
- 推荐用管理员权限运行 PowerShell/CMD。

## 依赖安装建议
- 推荐开发前执行：
  ```sh
  npm install --save-dev @types/node
  ```
- 解决 Vite 配置等 Node 环境下的类型报错。

## 常见问题与解决方案
- **自动防火墙仅支持 Windows 原生 PowerShell/CMD**，WSL/Git Bash 不支持自动开放端口。
- 若遇 `netsh` 不可用，脚本会警告但不退出，需手动配置防火墙。
- Vite 配置如报 `process` 未定义，建议安装 @types/node 或在 vite.config.ts 顶部加 `/// <reference types="node" />`。

## 主要特性与变更日志
- 统一设置弹窗，集中管理消息/文件/视频保留数量。
- 消息区支持一键复制当前消息和历史消息。
- 前端端口随机分配，自动开放/关闭防火墙端口，提升安全性。
- 代码结构优化，易于维护和扩展。
- 支持大屏自适应、现代美观UI。

---

如有更多问题请查阅源码注释或联系维护者。 