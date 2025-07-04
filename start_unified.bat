@echo off
chcp 65001
echo ========================================
echo 内网共享工具 - 一体化启动
echo ========================================
echo.

echo [1/3] 检查环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

node --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Node.js，请先安装Node.js 16.9.0+
    pause
    exit /b 1
)

echo [2/3] 构建前端...
cd /d %~dp0frontend
if not exist "node_modules" (
    echo 安装前端依赖...
    npm install > ..\frontend_install.log 2>&1
    if errorlevel 1 (
        echo 前端依赖安装失败，请查看frontend_install.log
        start notepad ..\frontend_install.log
        pause
        exit /b 1
    )
)
echo 构建前端项目...
npm run build > ..\frontend_build.log 2>&1
if errorlevel 1 (
    echo 错误: 前端构建失败，请查看frontend_build.log
    start notepad ..\frontend_build.log
    pause
    exit /b 1
)

echo [3/3] 启动后端服务...
cd /d %~dp0backend
python app.py > ..\backend.log 2>&1
if errorlevel 1 (
    echo 后端启动失败，请查看backend.log
    start notepad ..\backend.log
    pause
    exit /b 1
)

pause 