from flask import Blueprint, request, jsonify
import os
import json
from datetime import datetime
import threading

# 消息相关API蓝图
message_bp = Blueprint('message', __name__)
MESSAGE_FILE = os.path.join(os.path.dirname(__file__), '..', 'message.txt')
HISTORY_FILE = os.path.join(os.path.dirname(__file__), '..', 'message_history.json')

MAX_MESSAGES = 20
MAX_MESSAGES_LOCK = threading.Lock()

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_history(message):
    history = load_history()
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    history.append({
        'text': message,
        'timestamp': datetime.now().isoformat(),
        'ip': ip
    })
    # 只保留最近MAX_MESSAGES条消息
    if len(history) > get_max_messages():
        history = history[-get_max_messages():]
    
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存历史记录失败: {e}")

@message_bp.route('/', methods=['POST'])
def post_message():
    """
    发送新消息接口。
    参数: text - 消息内容
    返回: 保存结果、消息内容、时间戳
    """
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': '缺少消息内容'}), 400
        
        msg = data.get('text', '').strip()
        if not msg:
            return jsonify({'error': '消息内容不能为空'}), 400
        
        # 保存当前消息
        with open(MESSAGE_FILE, 'w', encoding='utf-8') as f:
            f.write(msg)
        
        # 保存到历史记录
        save_history(msg)
        
        return jsonify({
            'message': '消息保存成功',
            'text': msg,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': f'保存消息失败: {str(e)}'}), 500

@message_bp.route('/', methods=['GET'])
def get_message():
    """
    获取当前最新消息。
    返回: 消息内容
    """
    try:
        if os.path.exists(MESSAGE_FILE):
            with open(MESSAGE_FILE, 'r', encoding='utf-8') as f:
                msg = f.read()
        else:
            msg = ''
        
        return jsonify({'text': msg})
    
    except Exception as e:
        return jsonify({'error': f'获取消息失败: {str(e)}'}), 500

@message_bp.route('/history', methods=['GET'])
def get_history():
    """
    获取历史消息记录。
    返回: 消息内容、时间戳、IP等
    """
    try:
        history = load_history()
        return jsonify({'history': history})
    
    except Exception as e:
        return jsonify({'error': f'获取历史记录失败: {str(e)}'}), 500

def get_max_messages():
    global MAX_MESSAGES
    return MAX_MESSAGES

def set_max_messages(val):
    global MAX_MESSAGES
    with MAX_MESSAGES_LOCK:
        MAX_MESSAGES = val

@message_bp.route('/max_count', methods=['GET', 'POST'])
def message_max_count():
    """
    获取/设置消息最大保留条数。
    GET返回当前数量，POST设置新数量。
    """
    if request.method == 'GET':
        return jsonify({'max_count': get_max_messages()})
    data = request.get_json()
    if not data or 'max_count' not in data:
        return jsonify({'error': '缺少max_count参数'}), 400
    try:
        val = int(data['max_count'])
        if val < 1 or val > 100:
            return jsonify({'error': 'max_count应在1-100之间'}), 400
        set_max_messages(val)
        return jsonify({'max_count': get_max_messages()})
    except Exception as e:
        return jsonify({'error': str(e)}), 400 