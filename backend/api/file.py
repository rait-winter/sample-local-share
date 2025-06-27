from flask import Blueprint, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename

file_bp = Blueprint('file', __name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
ALLOWED_FILE_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'md', 'zip', 'rar', '7z', 'csv', 'xlsx', 'docx', 'pptx'])

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@file_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    ext = file.filename.rsplit('.', 1)[-1].lower()
    if ext not in ALLOWED_FILE_EXTENSIONS:
        return jsonify({'error': 'File type not allowed'}), 400
    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return jsonify({'message': 'File uploaded'})

@file_bp.route('/list', methods=['GET'])
def list_files():
    files = [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]
    return jsonify({'files': files})

@file_bp.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@file_bp.route('/preview/<filename>', methods=['GET'])
def preview_file(filename):
    ext = filename.rsplit('.', 1)[-1].lower()
    if ext in ['png', 'jpg', 'jpeg', 'gif', 'bmp']:
        return send_from_directory(UPLOAD_FOLDER, filename)
    elif ext in ['txt', 'md', 'csv']:
        with open(os.path.join(UPLOAD_FOLDER, filename), 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        return f'<pre style="white-space:pre-wrap;word-break:break-all;">{content}</pre>'
    else:
        return '不支持预览', 400 