# FAQ 常见问题

## 启动与运行

**Q1：为什么启动后没有自动弹出页面？**
A：请检查Python/Node.js环境，或手动访问控制台输出的局域网地址。

**Q2：如何确定访问端口？**
A：端口为后端启动时自动分配的随机五位数，控制台和页面均有提示。

**Q3：如何在局域网其他设备访问？**
A：请用本机IP+端口访问（如 http://192.168.x.x:54321），并确保防火墙已放行对应端口。

**Q4：日志文件在哪里？**
A：所有后端日志自动写入项目根目录 backend.log，可用记事本等工具查看。

## 打包与安装

**Q5：依赖安装失败怎么办？**
A：可手动进入 backend/frontend 目录分别执行 `pip install -r requirements.txt` 和 `npm install`。

**Q6：NSIS/PyInstaller 报错如何排查？**
A：详见《Windows一键打包与安装指南.md》常见问题部分。

## 文件与消息

**Q7：如何限制上传文件类型和大小？**
A：后端已做限制，普通文件100MB，视频500MB，类型详见安全与合规文档。

**Q8：上传失败/进度条不显示？**
A：请检查网络、文件大小、浏览器兼容性，或重试。

## 权限与安全

**Q9：如何保障数据安全？**
A：所有数据仅在本地和内网传输，不上传云端。建议仅在可信内网环境下使用。

**Q10：如何实现服务自启动？**
A：可用 Supervisor、systemd 等工具实现后台自启动，详见运维文档。

## 升级与维护

**Q11：如何升级项目？**
A：拉取最新代码后，重新运行 `start_unified.bat` 即可。

---
如有更多问题请查阅文档或联系维护者。 