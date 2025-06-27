@echo off
echo 启动后端服务...
cd backend
python -m pip install -r requirements.txt
python app.py
pause 