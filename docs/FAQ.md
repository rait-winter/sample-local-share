# FAQ 常见问题

**Q1：为什么启动后没有自动弹出页面？**
A：请检查Python/Node.js环境，或手动访问控制台输出的局域网地址。

**Q2：如何确定访问端口？**
A：端口为后端启动时自动分配的随机五位数，控制台和页面均有提示。

**Q3：如何在局域网其他设备访问？**
A：请用本机IP+端口访问（如 http://192.168.x.x:54321），并确保防火墙已放行对应端口。

**Q4：日志文件在哪里？**
A：所有后端日志自动写入项目根目录 backend.log，可用记事本等工具查看。

**Q5：依赖安装失败怎么办？**
A：可手动进入 backend/frontend 目录分别执行 `pip install -r requirements.txt` 和 `npm install`。

**Q6：如何限制上传文件类型和大小？**
A：后端已做限制，普通文件100MB，视频500MB，类型详见安全与合规文档。

**Q7：如何实现服务自启动？**
A：可用 Supervisor、systemd 等工具实现后台自启动，详见运维文档。

**Q8：如何升级项目？**
A：拉取最新代码后，重新运行 `start_unified.bat` 即可。

---
如有更多问题请查阅文档或联系维护者。 