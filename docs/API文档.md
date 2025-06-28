# API 文档

本项目后端API基于RESTful风格，所有接口均以 `/api/` 开头，返回JSON格式数据。

---

## 消息相关

### 1. 获取消息历史
- **接口**：`GET /api/message/history`
- **描述**：获取最近50条消息
- **请求参数**：无
- **返回示例**：
  ```json
  [
    {
      "content": "hello",
      "timestamp": "2024-06-01 12:00:00"
    }
  ]
  ```

---

### 2. 发送消息
- **接口**：`POST /api/message/`
- **描述**：发送一条新消息
- **请求参数**（JSON）：
  ```json
  {
    "content": "消息内容"
  }
  ```
- **返回示例**：
  ```json
  {
    "success": true
  }
  ```

---

## 文件相关

### 1. 获取文件列表
- **接口**：`GET /api/file/list`
- **描述**：获取所有已上传文件信息
- **请求参数**：无
- **返回示例**：
  ```json
  [
    {
      "name": "example.pdf",
      "size": 123456,
      "mtime": "2024-06-01 12:00:00"
    }
  ]
  ```

---

### 2. 上传文件
- **接口**：`POST /api/file/upload`
- **描述**：上传新文件（支持多种类型）
- **请求参数**：`multipart/form-data`，字段名为 `file`
- **返回示例**：
  ```json
  {
    "success": true,
    "filename": "example.pdf"
  }
  ```

---

### 3. 下载文件
- **接口**：`GET /api/file/download/<filename>`
- **描述**：下载指定文件
- **请求参数**：URL路径参数
- **返回**：文件流

---

### 4. 删除文件
- **接口**：`POST /api/file/delete`
- **描述**：删除指定文件
- **请求参数**（JSON）：
  ```json
  {
    "name": "example.pdf"
  }
  ```
- **返回示例**：
  ```json
  {
    "success": true
  }
  ```

---

## 视频相关

### 1. 获取视频列表
- **接口**：`GET /api/video/list`
- **描述**：获取所有已上传视频信息
- **请求参数**：无
- **返回示例**：
  ```json
  [
    {
      "name": "demo.mp4",
      "size": 12345678,
      "mtime": "2024-06-01 12:00:00"
    }
  ]
  ```

---

### 2. 上传视频
- **接口**：`POST /api/video/upload`
- **描述**：上传新视频
- **请求参数**：`multipart/form-data`，字段名为 `file`
- **返回示例**：
  ```json
  {
    "success": true,
    "filename": "demo.mp4"
  }
  ```

---

### 3. 下载视频
- **接口**：`GET /api/video/download/<filename>`
- **描述**：下载指定视频
- **请求参数**：URL路径参数
- **返回**：文件流

---

### 4. 删除视频
- **接口**：`POST /api/video/delete`
- **描述**：删除指定视频
- **请求参数**（JSON）：
  ```json
  {
    "name": "demo.mp4"
  }
  ```
- **返回示例**：
  ```json
  {
    "success": true
  }
  ```

---

## 配置相关

### 获取配置信息
- **接口**：`GET /api/config`
- **描述**：获取应用配置信息
- **请求参数**：无
- **返回示例**：
  ```json
  {
    "app_name": "内网文件共享工具",
    "company_name": "内部共享系统",
    "version": "1.0.0",
    "description": "便捷的内网文件、视频和消息共享工具",
    "share_url": "http://192.168.1.100:5000",
    "frontend_url": "http://192.168.1.100:实际端口"
  }
  ```

---

## 通用返回格式

- 成功：
  ```json
  { "success": true, ... }
  ```
- 失败：
  ```json
  { "success": false, "error": "错误信息" }
  ```

---

## 说明

- 所有接口均支持跨域（CORS）。
- 上传/下载接口需配合前端表单或工具（如curl、Postman）使用。
- 文件/视频大小、类型等限制详见后端配置。

---

## 示例代码

### JavaScript/TypeScript (fetch)
```js
// 发送消息
await fetch('/api/message/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ content: 'Hello World' })
});

// 上传文件
const formData = new FormData();
formData.append('file', fileInput.files[0]);
await fetch('/api/file/upload', { method: 'POST', body: formData });

// 获取文件列表
const res = await fetch('/api/file/list');
const files = await res.json();
```

### Python (requests)
```python
import requests

# 发送消息
requests.post('http://localhost:5000/api/message/', json={'content': 'Hello World'})

# 上传文件
with open('file.txt', 'rb') as f:
    requests.post('http://localhost:5000/api/file/upload', files={'file': f})

# 获取文件列表
files = requests.get('http://localhost:5000/api/file/list').json()
```

### cURL
```bash
# 发送消息
curl -X POST http://localhost:5000/api/message/ -H "Content-Type: application/json" -d '{"content": "Hello World"}'

# 上传文件
curl -X POST http://localhost:5000/api/file/upload -F "file=@/path/to/file.txt"

# 获取文件列表
curl http://localhost:5000/api/file/list
```

---

## 常见问题（FAQ）

**Q1：为什么上传大文件失败？**  
A：请检查后端 `config.json` 的 `max_file_size` 配置，默认100MB。前端和后端都有限制，超出会被拒绝。

**Q2：前端页面无法访问/端口不一致？**  
A：请确保前端启动后端口已同步到后端（如有端口写入机制），并检查防火墙设置。

**Q3：API跨域报错？**  
A：后端已启用CORS，若仍有问题请检查浏览器缓存或代理配置。

**Q4：如何自定义上传/视频/消息的保留数量？**  
A：可在 `backend/config.json` 中调整相关配置项。

**Q5：如何在局域网其他设备访问？**  
A：请用后端启动台输出的"前端界面地址"，并确保防火墙已放行对应端口。

---

## 接口变更历史

### v1.1.0
- 新增：文件/视频删除接口
- 新增：文件/视频预览接口
- 优化：API返回格式统一，错误处理更友好

### v1.0.0
- 初始版本，支持消息、文件、视频的上传、下载、历史、同步等基础功能

---

如需更详细的开发示例或遇到特殊问题，欢迎提交 Issue 或查阅源码！ 