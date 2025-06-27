from flask import Blueprint, request, jsonify, send_from_directory, send_file
import os
from werkzeug.utils import secure_filename

video_bp = Blueprint('video', __name__)
VIDEO_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'videos')
ALLOWED_VIDEO_EXTENSIONS = set(['mp4', 'avi', 'mov', 'wmv', 'mkv'])

if not os.path.exists(VIDEO_FOLDER):
    os.makedirs(VIDEO_FOLDER)

@video_bp.route('/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    ext = file.filename.rsplit('.', 1)[-1].lower()
    if ext not in ALLOWED_VIDEO_EXTENSIONS:
        return jsonify({'error': 'Video type not allowed'}), 400
    filename = secure_filename(file.filename)
    file.save(os.path.join(VIDEO_FOLDER, filename))
    return jsonify({'message': 'Video uploaded'})

@video_bp.route('/list', methods=['GET'])
def list_videos():
    files = [f for f in os.listdir(VIDEO_FOLDER) if os.path.isfile(os.path.join(VIDEO_FOLDER, f))]
    return jsonify({'videos': files})

@video_bp.route('/download/<filename>', methods=['GET'])
def download_video(filename):
    return send_from_directory(VIDEO_FOLDER, filename, as_attachment=True)

@video_bp.route('/preview/<filename>', methods=['GET'])
def preview_video(filename):
    return send_file(os.path.join(VIDEO_FOLDER, filename)) 