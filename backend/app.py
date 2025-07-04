# 主应用入口，负责创建Flask实例、注册蓝图、配置CORS等
from flask import Flask, send_from_directory
from flask_cors import CORS
import os
import random
import webbrowser
import logging
from logging.handlers import RotatingFileHandler
import socket
from api.message import message_bp
from api.file import file_bp
from api.video import video_bp

# 日志配置
def setup_logging(log_path):
    abs_log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', log_path))
    handler = RotatingFileHandler(abs_log_path, maxBytes=5*1024*1024, backupCount=2, encoding='utf-8')
    logging.basicConfig(level=logging.INFO, handlers=[handler])
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.INFO)
    log.addHandler(handler)

# 获取局域网IP
def get_lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

# 工厂函数，创建并配置Flask应用
# 返回: 配置好的Flask app实例
# 用于WSGI服务器或直接运行

def create_app():
    app = Flask(__name__, static_folder='../frontend/dist', static_url_path='')
    # 启用跨域支持，允许前端跨域访问API
    CORS(app)
    # 注册消息、文件、视频API蓝图
    app.register_blueprint(message_bp, url_prefix='/api/message')
    app.register_blueprint(file_bp, url_prefix='/api/file')
    app.register_blueprint(video_bp, url_prefix='/api/video')
    
    # 添加前端路由，支持SPA
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path != "" and os.path.exists(app.static_folder + '/' + path):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')
    
    return app

if __name__ == '__main__':
    setup_logging('backend.log')
    app = create_app()
    port = random.randint(10000, 65535)
    # 写入端口号到前端dist目录
    dist_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend/dist'))
    try:
        os.makedirs(dist_dir, exist_ok=True)
        with open(os.path.join(dist_dir, 'port.txt'), 'w', encoding='utf-8') as f:
            f.write(str(port))
    except Exception as e:
        logging.warning(f"[警告] 端口写入port.txt失败: {e}")
    lan_ip = get_lan_ip()
    url = f"http://{lan_ip}:{port}"
    print(f"服务已启动，局域网访问：{url}")
    # 只在主进程弹窗
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        try:
            webbrowser.open(url)
        except Exception as e:
                logging.warning(f"[警告] 自动打开浏览器失败: {e}")
    app.run(host='0.0.0.0', port=port, debug=True) 