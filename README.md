# 内网文件共享工具

一个基于Flask后端和Vue3前端的完整内网文件共享解决方案，支持消息分享、文件上传下载和视频管理，具备实时同步功能。

## ✨ 功能特性

### 📝 消息功能
- 实时消息发布和显示
- 消息历史记录（最近50条）
- 支持中文内容
- **实时同步**：多终端消息自动同步（5秒轮询）

### 📁 文件管理
- 支持多种文件格式上传（txt, pdf, png, jpg, jpeg, gif, bmp, md, zip, rar, 7z, csv, xlsx, docx, pptx）
- 文件大小限制：100MB
- 文件预览（图片、文本文件）
- 文件下载
- 文件删除
- 文件列表按时间排序
- **实时同步**：文件列表自动更新（10秒轮询）

### 🎥 视频管理
- 支持多种视频格式（mp4, avi, mov, wmv, mkv, flv, webm）
- 视频大小限制：500MB
- 视频在线预览
- 视频下载
- 视频删除
- 视频列表按时间排序
- **实时同步**：视频列表自动更新（10秒轮询）

## 🛠️ 技术栈

### 后端
- **Flask** - Python Web框架
- **Flask-CORS** - 跨域支持
- **Werkzeug** - 文件处理

### 前端
- **Vue 3** - 渐进式JavaScript框架
- **TypeScript** - 类型安全的JavaScript
- **Vite** - 快速构建工具
- **Element Plus** - Vue 3 UI组件库
- **Axios** - HTTP客户端

## 📁 项目结构

```
project/
├── backend/                 # 后端Flask应用
│   ├── app.py              # 主应用文件
│   ├── requirements.txt    # Python依赖
│   ├── api/                # API模块
│   │   ├── message.py      # 消息API
│   │   ├── file.py         # 文件API
│   │   └── video.py        # 视频API
│   ├── uploads/            # 文件存储目录
│   ├── videos/             # 视频存储目录
│   └── message.txt         # 当前消息文件
├── frontend/               # 前端Vue3应用
│   ├── src/
│   │   ├── components/     # Vue组件
│   │   │   ├── MessagePanel.vue
│   │   │   ├── FilePanel.vue
│   │   │   └── VideoPanel.vue
│   │   ├── api/           # API封装
│   │   │   ├── message.ts
│   │   │   ├── file.ts
│   │   │   └── video.ts
│   │   └── App.vue        # 主应用组件
│   ├── package.json       # Node.js依赖
│   └── vite.config.ts     # Vite配置
├── docs/                  # 项目文档
├── start_backend.bat      # 后端启动脚本
├── start_frontend.bat     # 前端启动脚本
└── README.md             # 项目说明
```

## 🚀 快速开始

### 环境要求
- Python 3.7+
- Node.js 16.9.0+ (推荐18+)
- npm 或 yarn

### 1. 启动后端服务

**方法一：使用批处理脚本（推荐）**
```bash
# Windows
start_backend.bat
```

**方法二：手动启动**
```bash
cd backend
pip install -r requirements.txt
python app.py
```

后端服务将在 `http://localhost:8000` 启动

### 2. 启动前端服务

**方法一：使用批处理脚本（推荐）**
```bash
# Windows
start_frontend.bat
```

**方法二：手动启动**
```bash
cd frontend
npm install
npm run dev
```

前端服务将在 `http://localhost:3000` 启动

### 3. 访问应用

- 本地访问：`http://localhost:3000`
- 内网访问：`http://[你的IP地址]:3000`

## 🔌 API接口

### 消息API
- `POST /api/message/` - 发送消息
- `GET /api/message/` - 获取当前消息
- `GET /api/message/history` - 获取消息历史

### 文件API
- `POST /api/file/upload` - 上传文件
- `GET /api/file/list` - 获取文件列表
- `GET /api/file/download/<filename>` - 下载文件
- `GET /api/file/preview/<filename>` - 预览文件
- `DELETE /api/file/delete/<filename>` - 删除文件

### 视频API
- `POST /api/video/upload` - 上传视频
- `GET /api/video/list` - 获取视频列表
- `GET /api/video/download/<filename>` - 下载视频
- `GET /api/video/preview/<filename>` - 预览视频
- `DELETE /api/video/delete/<filename>` - 删除视频

## ⚙️ 配置说明

### 后端配置
- 端口：8000
- 主机：0.0.0.0（允许外部访问）
- 文件大小限制：文件100MB，视频500MB

### 前端配置
- 端口：3000
- 主机：0.0.0.0（允许外部访问）
- API代理：自动代理到后端8000端口
- 实时同步：消息5秒轮询，文件/视频10秒轮询

## 📖 使用说明

### 消息功能
1. 在消息面板输入要分享的内容
2. 点击"发送"按钮或使用Ctrl+Enter快速发送
3. 消息将显示在消息显示区域
4. 可以查看历史消息记录
5. **多终端实时同步**：其他设备会自动看到新消息

### 文件管理
1. 点击"选择文件"按钮选择要上传的文件
2. 点击"上传"按钮上传文件
3. 文件列表会显示所有已上传的文件
4. 点击文件名可以预览（支持的文件类型）
5. 点击下载按钮下载文件
6. 点击删除按钮删除文件
7. **多终端实时同步**：其他设备会自动看到新上传的文件

### 视频管理
1. 点击"选择视频"按钮选择要上传的视频文件
2. 点击"上传"按钮上传视频
3. 视频列表会显示所有已上传的视频
4. 点击视频名可以在线预览
5. 点击下载按钮下载视频
6. 点击删除按钮删除视频
7. **多终端实时同步**：其他设备会自动看到新上传的视频

## 🔄 实时同步机制

项目采用轮询机制实现多终端实时同步：

- **消息同步**：每5秒自动刷新当前消息和历史记录
- **文件同步**：每10秒自动刷新文件列表
- **视频同步**：每10秒自动刷新视频列表

所有操作（发送消息、上传文件、删除文件等）都会立即触发刷新，确保数据实时性。

## ⚠️ 注意事项

1. **文件大小限制**：单个文件最大100MB，视频最大500MB
2. **支持格式**：请查看API文档了解支持的文件和视频格式
3. **内网访问**：确保防火墙允许3000和8000端口访问
4. **存储空间**：注意监控uploads和videos目录的磁盘使用情况
5. **安全性**：当前版本为内网使用，如需外网访问请添加适当的安全措施
6. **实时同步**：轮询间隔可根据需要在组件中调整

## 🔧 故障排除

### 常见问题

**Q: 前端无法连接后端API**
A: 检查后端是否正常启动在8000端口，检查防火墙设置

**Q: 文件上传失败**
A: 检查文件大小是否超过限制，检查文件格式是否支持

**Q: 内网其他设备无法访问**
A: 检查防火墙设置，确保3000和8000端口开放

**Q: 消息/文件不同步**
A: 检查网络连接，轮询机制会自动重试

**Q: Node.js版本兼容性问题**
A: 建议升级到Node.js 18+版本以获得最佳兼容性

## 🛠️ 开发说明

### 添加新功能
1. 在后端`api/`目录添加新的API模块
2. 在`app.py`中注册新的蓝图
3. 在前端`src/api/`目录添加对应的API封装
4. 在前端`src/components/`目录添加对应的Vue组件

### 自定义配置
- 修改文件大小限制：编辑`backend/api/file.py`和`backend/api/video.py`中的`MAX_FILE_SIZE`和`MAX_VIDEO_SIZE`
- 修改支持的文件格式：编辑`ALLOWED_FILE_EXTENSIONS`和`ALLOWED_VIDEO_EXTENSIONS`
- 修改端口：编辑`backend/app.py`和`frontend/vite.config.ts`
- 修改轮询间隔：编辑各组件中的`setInterval`时间参数

## 📄 许可证

本项目仅供内网使用，请遵守相关法律法规。

## 🆕 更新日志

### v1.0.0 (2024-01-01)
- ✅ 完成基础功能开发
- ✅ 实现消息、文件、视频管理
- ✅ 添加实时同步功能
- ✅ 完善错误处理和用户体验
- ✅ 提供完整的文档和启动脚本 