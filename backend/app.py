from flask import Flask
from flask_cors import CORS
from api.message import message_bp
from api.file import file_bp
from api.video import video_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(message_bp, url_prefix='/api/message')
    app.register_blueprint(file_bp, url_prefix='/api/file')
    app.register_blueprint(video_bp, url_prefix='/api/video')
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000, debug=True) 