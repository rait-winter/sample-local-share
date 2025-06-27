from flask import Blueprint, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename

file_bp = Blueprint('file', __name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
ALLOWED_FILE_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'md', 'zip', 'rar', '7z', 'csv', 'xlsx', 'docx', 'pptx'])
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_FILE_EXTENSIONS

@file_bp.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': '没有选择文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': '不支持的文件类型'}), 400
        
        # 检查文件大小
        file.seek(0, 2)  # 移动到文件末尾
        file_size = file.tell()
        file.seek(0)  # 重置到文件开头
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({'error': f'文件大小超过限制（最大{MAX_FILE_SIZE//1024//1024}MB）'}), 400
        
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        # 如果文件已存在，添加数字后缀
        counter = 1
        original_filename = filename
        while os.path.exists(file_path):
            name, ext = os.path.splitext(original_filename)
            filename = f"{name}_{counter}{ext}"
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            counter += 1
        
        file.save(file_path)
        
        return jsonify({
            'message': '文件上传成功',
            'filename': filename,
            'size': file_size
        })
    
    except Exception as e:
        return jsonify({'error': f'上传失败: {str(e)}'}), 500

@file_bp.route('/list', methods=['GET'])
def list_files():
    try:
        files = []
        for filename in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(file_path):
                file_stat = os.stat(file_path)
                files.append({
                    'name': filename,
                    'size': file_stat.st_size,
                    'modified': file_stat.st_mtime
                })
        
        # 按修改时间排序，最新的在前
        files.sort(key=lambda x: x['modified'], reverse=True)
        
        return jsonify({'files': files})
    
    except Exception as e:
        return jsonify({'error': f'获取文件列表失败: {str(e)}'}), 500

@file_bp.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.exists(file_path):
            return jsonify({'error': '文件不存在'}), 404
        
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    
    except Exception as e:
        return jsonify({'error': f'下载失败: {str(e)}'}), 500

@file_bp.route('/preview/<filename>', methods=['GET'])
def preview_file(filename):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.exists(file_path):
            return jsonify({'error': '文件不存在'}), 404
        
        ext = filename.rsplit('.', 1)[-1].lower()
        
        if ext in ['png', 'jpg', 'jpeg', 'gif', 'bmp']:
            return send_from_directory(UPLOAD_FOLDER, filename)
        elif ext in ['txt', 'md', 'csv']:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                return f'<pre style="white-space:pre-wrap;word-break:break-all;">{content}</pre>'
            except UnicodeDecodeError:
                return '文件编码不支持预览', 400
        else:
            return '不支持预览此类型文件', 400
    
    except Exception as e:
        return jsonify({'error': f'预览失败: {str(e)}'}), 500

@file_bp.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.exists(file_path):
            return jsonify({'error': '文件不存在'}), 404
        
        os.remove(file_path)
        return jsonify({'message': '文件删除成功'})
    
    except Exception as e:
        return jsonify({'error': f'删除失败: {str(e)}'}), 500 