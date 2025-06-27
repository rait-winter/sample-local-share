from flask import Blueprint, request, jsonify, send_from_directory, send_file
import os
from werkzeug.utils import secure_filename

video_bp = Blueprint('video', __name__)
VIDEO_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'videos')
ALLOWED_VIDEO_EXTENSIONS = set(['mp4', 'avi', 'mov', 'wmv', 'mkv', 'flv', 'webm'])
MAX_VIDEO_SIZE = 500 * 1024 * 1024  # 500MB

if not os.path.exists(VIDEO_FOLDER):
    os.makedirs(VIDEO_FOLDER)

def allowed_video(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS

@video_bp.route('/upload', methods=['POST'])
def upload_video():
    try:
        if 'file' not in request.files:
            return jsonify({'error': '没有选择文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400
        
        if not allowed_video(file.filename):
            return jsonify({'error': '不支持的视频格式'}), 400
        
        # 检查文件大小
        file.seek(0, 2)  # 移动到文件末尾
        file_size = file.tell()
        file.seek(0)  # 重置到文件开头
        
        if file_size > MAX_VIDEO_SIZE:
            return jsonify({'error': f'视频文件大小超过限制（最大{MAX_VIDEO_SIZE//1024//1024}MB）'}), 400
        
        filename = secure_filename(file.filename)
        file_path = os.path.join(VIDEO_FOLDER, filename)
        
        # 如果文件已存在，添加数字后缀
        counter = 1
        original_filename = filename
        while os.path.exists(file_path):
            name, ext = os.path.splitext(original_filename)
            filename = f"{name}_{counter}{ext}"
            file_path = os.path.join(VIDEO_FOLDER, filename)
            counter += 1
        
        file.save(file_path)
        
        return jsonify({
            'message': '视频上传成功',
            'filename': filename,
            'size': file_size
        })
    
    except Exception as e:
        return jsonify({'error': f'上传失败: {str(e)}'}), 500

@video_bp.route('/list', methods=['GET'])
def list_videos():
    try:
        videos = []
        for filename in os.listdir(VIDEO_FOLDER):
            file_path = os.path.join(VIDEO_FOLDER, filename)
            if os.path.isfile(file_path):
                file_stat = os.stat(file_path)
                videos.append({
                    'name': filename,
                    'size': file_stat.st_size,
                    'modified': file_stat.st_mtime
                })
        
        # 按修改时间排序，最新的在前
        videos.sort(key=lambda x: x['modified'], reverse=True)
        
        return jsonify({'videos': videos})
    
    except Exception as e:
        return jsonify({'error': f'获取视频列表失败: {str(e)}'}), 500

@video_bp.route('/download/<filename>', methods=['GET'])
def download_video(filename):
    try:
        file_path = os.path.join(VIDEO_FOLDER, filename)
        if not os.path.exists(file_path):
            return jsonify({'error': '视频文件不存在'}), 404
        
        return send_from_directory(VIDEO_FOLDER, filename, as_attachment=True)
    
    except Exception as e:
        return jsonify({'error': f'下载失败: {str(e)}'}), 500

@video_bp.route('/preview/<filename>', methods=['GET'])
def preview_video(filename):
    try:
        file_path = os.path.join(VIDEO_FOLDER, filename)
        if not os.path.exists(file_path):
            return jsonify({'error': '视频文件不存在'}), 404
        
        return send_file(file_path)
    
    except Exception as e:
        return jsonify({'error': f'预览失败: {str(e)}'}), 500

@video_bp.route('/delete/<filename>', methods=['DELETE'])
def delete_video(filename):
    try:
        file_path = os.path.join(VIDEO_FOLDER, filename)
        if not os.path.exists(file_path):
            return jsonify({'error': '视频文件不存在'}), 404
        
        os.remove(file_path)
        return jsonify({'message': '视频删除成功'})
    
    except Exception as e:
        return jsonify({'error': f'删除失败: {str(e)}'}), 500 