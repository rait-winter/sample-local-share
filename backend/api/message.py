from flask import Blueprint, request, jsonify
import os

message_bp = Blueprint('message', __name__)
MESSAGE_FILE = os.path.join(os.path.dirname(__file__), '..', 'message.txt')

@message_bp.route('/', methods=['POST'])
def post_message():
    data = request.get_json()
    msg = data.get('text', '').strip()
    with open(MESSAGE_FILE, 'w', encoding='utf-8') as f:
        f.write(msg)
    return jsonify({'message': 'ok'})

@message_bp.route('/', methods=['GET'])
def get_message():
    if os.path.exists(MESSAGE_FILE):
        with open(MESSAGE_FILE, 'r', encoding='utf-8') as f:
            msg = f.read()
    else:
        msg = ''
    return jsonify({'text': msg}) 