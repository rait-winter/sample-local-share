import os
import json
import socket
from pathlib import Path

class Config:
    def __init__(self):
        self.config_file = Path(__file__).parent / "config.json"
        self.load_config()
    
    def load_config(self):
        """加载配置文件，如果不存在则创建默认配置"""
        default_config = {
            "app_name": "内网文件共享工具",
            "company_name": "内部共享系统",
            "version": "1.0.0",
            "description": "便捷的内网文件、视频和消息共享工具",
            "icon_path": "",
            "auto_start": True,
            "show_startup_info": True,
            "backend_port": 5000,
            "frontend_port": 5173,
            "max_file_size": 100 * 1024 * 1024,  # 100MB
            "allowed_extensions": [".txt", ".pdf", ".doc", ".docx", ".xls", ".xlsx", 
                                 ".jpg", ".jpeg", ".png", ".gif", ".mp4", ".avi", ".mov"],
            "upload_folder": "uploads",
            "video_folder": "videos"
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # 合并默认配置和用户配置
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
            except Exception as e:
                print(f"配置文件读取错误，使用默认配置: {e}")
                config = default_config
        else:
            config = default_config
            self.save_config(config)
        
        self.config = config
    
    def save_config(self, config=None):
        """保存配置文件"""
        if config is None:
            config = self.config
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"配置文件保存错误: {e}")
    
    def get(self, key, default=None):
        """获取配置值"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """设置配置值"""
        self.config[key] = value
        self.save_config()
    
    def get_local_ip(self):
        """获取本机IP地址"""
        try:
            # 获取本机IP地址
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"
    
    def get_share_url(self):
        """获取共享URL"""
        ip = self.get_local_ip()
        port = self.get("backend_port", 5000)
        return f"http://{ip}:{port}"
    
    def get_frontend_url(self):
        """获取前端URL，优先读取frontend_port.txt"""
        ip = self.get_local_ip()
        port = None
        port_file = Path(__file__).parent.parent / 'frontend' / 'frontend_port.txt'
        if port_file.exists():
            try:
                with open(port_file, 'r', encoding='utf-8') as f:
                    port_str = f.read().strip()
                    if port_str.isdigit():
                        port = int(port_str)
            except Exception:
                pass
        if not port:
            port = self.get("frontend_port", 5173)
        return f"http://{ip}:{port}"

# 全局配置实例
config = Config() 