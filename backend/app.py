# 主应用入口，负责创建Flask实例、注册蓝图、配置CORS等
from flask import Flask
from flask_cors import CORS
from api.message import message_bp
from api.file import file_bp
from api.video import video_bp

# 工厂函数，创建并配置Flask应用
# 返回: 配置好的Flask app实例
# 用于WSGI服务器或直接运行

def create_app():
    app = Flask(__name__)
    # 启用跨域支持，允许前端跨域访问API
    CORS(app)
    # 注册消息、文件、视频API蓝图
    app.register_blueprint(message_bp, url_prefix='/api/message')
    app.register_blueprint(file_bp, url_prefix='/api/file')
    app.register_blueprint(video_bp, url_prefix='/api/video')
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000, debug=True) 