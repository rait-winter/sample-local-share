# API 文档

本文档详细说明了内网共享工具的所有API接口。

## 基础信息

- **基础URL**: `http://localhost:8000`
- **内容类型**: `application/json`
- **字符编码**: `UTF-8`
- **实时同步**: 前端采用轮询机制实现多终端同步

## 消息API

### 发送消息

**POST** `/api/message/`

发送新消息，同时保存到历史记录。

**请求体:**
```json
{
  "text": "要发送的消息内容"
}
```

**响应:**
```json
{
  "message": "消息保存成功",
  "text": "要发送的消息内容",
  "timestamp": "2024-01-01T12:00:00"
}
```

**错误响应:**
```json
{
  "error": "错误信息"
}
```

### 获取当前消息

**GET** `/api/message/`

获取最新的一条消息。

**响应:**
```json
{
  "text": "当前消息内容"
}
```

### 获取消息历史

**GET** `/api/message/history`

获取最近50条消息历史记录。

**响应:**
```json
{
  "history": [
    {
      "text": "消息内容",
      "timestamp": "2024-01-01T12:00:00"
    }
  ]
}
```

## 文件API

### 上传文件

**POST** `/api/file/upload`

上传文件到服务器。

**请求体:** `multipart/form-data`
- `file`: 要上传的文件

**支持的文件类型:**
- 文档: `txt`, `pdf`, `md`, `csv`, `xlsx`, `docx`, `pptx`
- 图片: `png`, `jpg`, `jpeg`, `gif`, `bmp`
- 压缩: `zip`, `rar`, `7z`

**文件大小限制:** 100MB

**响应:**
```json
{
  "message": "文件上传成功",
  "filename": "文件名.ext",
  "size": 1024
}
```

**错误响应:**
```json
{
  "error": "错误信息"
}
```

### 获取文件列表

**GET** `/api/file/list`

获取所有已上传文件的列表。

**响应:**
```json
{
  "files": [
    {
      "name": "文件名.ext",
      "size": 1024,
      "modified": 1704067200
    }
  ]
}
```

### 下载文件

**GET** `/api/file/download/<filename>`

下载指定文件。

**参数:**
- `filename`: 文件名（URL编码）

**响应:** 文件二进制流

**错误响应:**
```json
{
  "error": "文件不存在"
}
```

### 预览文件

**GET** `/api/file/preview/<filename>`

预览文件内容。

**参数:**
- `filename`: 文件名（URL编码）

**支持预览的文件类型:**
- 图片: `png`, `jpg`, `jpeg`, `gif`, `bmp` - 直接返回图片
- 文本: `txt`, `md`, `csv` - 返回HTML格式的文本内容

**响应:**
- 图片文件: 图片二进制流
- 文本文件: HTML格式的文本内容

**错误响应:**
```json
{
  "error": "错误信息"
}
```

### 删除文件

**DELETE** `/api/file/delete/<filename>`

删除指定文件。

**参数:**
- `filename`: 文件名（URL编码）

**响应:**
```json
{
  "message": "文件删除成功"
}
```

**错误响应:**
```json
{
  "error": "错误信息"
}
```

## 视频API

### 上传视频

**POST** `/api/video/upload`

上传视频文件到服务器。

**请求体:** `multipart/form-data`
- `file`: 要上传的视频文件

**支持的视频格式:**
- `mp4`, `avi`, `mov`, `wmv`, `mkv`, `flv`, `webm`

**文件大小限制:** 500MB

**响应:**
```json
{
  "message": "视频上传成功",
  "filename": "视频名.mp4",
  "size": 1024000
}
```

**错误响应:**
```json
{
  "error": "错误信息"
}
```

### 获取视频列表

**GET** `/api/video/list`

获取所有已上传视频的列表。

**响应:**
```json
{
  "videos": [
    {
      "name": "视频名.mp4",
      "size": 1024000,
      "modified": 1704067200
    }
  ]
}
```

### 下载视频

**GET** `/api/video/download/<filename>`

下载指定视频文件。

**参数:**
- `filename`: 视频文件名（URL编码）

**响应:** 视频文件二进制流

**错误响应:**
```json
{
  "error": "视频文件不存在"
}
```

### 预览视频

**GET** `/api/video/preview/<filename>`

在线预览视频。

**参数:**
- `filename`: 视频文件名（URL编码）

**响应:** 视频文件二进制流（支持HTML5 video标签播放）

**错误响应:**
```json
{
  "error": "错误信息"
}
```

### 删除视频

**DELETE** `/api/video/delete/<filename>`

删除指定视频文件。

**参数:**
- `filename`: 视频文件名（URL编码）

**响应:**
```json
{
  "message": "视频删除成功"
}
```

**错误响应:**
```json
{
  "error": "错误信息"
}
```

## 实时同步机制

前端采用轮询机制实现多终端实时同步：

- **消息同步**: 每5秒自动调用 `/api/message/` 和 `/api/message/history`
- **文件同步**: 每10秒自动调用 `/api/file/list`
- **视频同步**: 每10秒自动调用 `/api/video/list`

所有操作（发送消息、上传文件、删除文件等）都会立即触发刷新，确保数据实时性。

## 错误响应

所有API在发生错误时都会返回以下格式的响应：

```json
{
  "error": "错误描述信息"
}
```

**常见HTTP状态码:**
- `200`: 成功
- `400`: 请求参数错误
- `404`: 资源不存在
- `500`: 服务器内部错误

## 使用示例

### JavaScript/TypeScript

```javascript
// 发送消息
const response = await fetch('/api/message/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ text: 'Hello World' })
});

// 上传文件
const formData = new FormData();
formData.append('file', fileInput.files[0]);
const response = await fetch('/api/file/upload', {
  method: 'POST',
  body: formData
});

// 获取文件列表
const response = await fetch('/api/file/list');
const data = await response.json();
```

### Python

```python
import requests

# 发送消息
response = requests.post('http://localhost:8000/api/message/', 
                        json={'text': 'Hello World'})

# 上传文件
with open('file.txt', 'rb') as f:
    response = requests.post('http://localhost:8000/api/file/upload',
                           files={'file': f})

# 获取文件列表
response = requests.get('http://localhost:8000/api/file/list')
files = response.json()['files']
```

### cURL

```bash
# 发送消息
curl -X POST http://localhost:8000/api/message/ \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello World"}'

# 上传文件
curl -X POST http://localhost:8000/api/file/upload \
  -F "file=@/path/to/file.txt"

# 获取文件列表
curl http://localhost:8000/api/file/list
```

## 注意事项

1. **文件大小限制**: 单个文件最大100MB，视频最大500MB
2. **文件名安全**: 上传的文件名会被自动清理，移除特殊字符
3. **重复文件**: 如果上传同名文件，会自动添加数字后缀
4. **编码问题**: 所有文本内容使用UTF-8编码
5. **跨域支持**: API已配置CORS，支持跨域请求
6. **实时同步**: 前端轮询机制确保多终端数据同步

## 版本历史

### v1.1.0 (最新)
- ✅ 新增文件预览功能
- ✅ 新增文件删除功能
- ✅ 新增视频预览功能
- ✅ 新增视频删除功能
- ✅ 新增消息历史功能
- ✅ 优化错误处理和响应

### v1.0.0
- ✅ 基础消息、文件、视频管理功能
- ✅ 实时同步机制
- ✅ 基础API接口 