# Windows一键打包与安装指南

本指南适用于本项目在 Windows 平台下的前后端一体化打包、生成可安装 exe 文件，并实现一键启动。

---

## 1. 前端打包

1. 进入前端目录：
   ```bash
   cd frontend
   npm install
   npm run build
   # 确保 vite.config.ts 配置 outDir: '../backend/dist'
   ```

---

## 2. 后端打包为 exe

1. 进入后端目录：
   ```bash
   cd backend
   pip install -r requirements.txt
   pip install pyinstaller
   pyinstaller --onefile --add-data "dist;dist" app.py
   # 生成 dist/app.exe
   ```
2. 确认 backend/dist 目录下有 app.exe、assets/、index.html、icon.svg、vite.svg、uploads/、videos/（含 .gitkeep 文件）

---

## 3. 生成安装包（NSIS）

1. 安装 [NSIS](https://nsis.sourceforge.io/Download)
2. 用 Notepad++ 打开 installer.nsi，**保存为 ANSI/GBK 编码**。
3. 编译 installer.nsi，生成 `内网文件消息共享安装包.exe`。

---

## 4. 安装与运行

- 双击安装包，按提示安装。
- 桌面和开始菜单会生成快捷方式，双击即可启动。
- 启动后自动弹出浏览器，显示局域网访问地址。

---

## 5. 常见问题

- **NSIS 编码报错**：用 Notepad++ 另存为 ANSI/GBK。
- **PyInstaller 静态资源丢失**：确保 --add-data 参数正确，dist 目录结构完整。
- **端口冲突**：修改 config.json 或重启服务。
- **防火墙拦截**：允许程序通过防火墙。
- **文件夹为空报错**：确保 uploads/、videos/ 目录存在且含 .gitkeep 文件。

---

如需更高级的桌面App封装（如 Electron 一键启动），请参考项目文档或联系开发者。 