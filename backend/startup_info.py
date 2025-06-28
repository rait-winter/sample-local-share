import platform
import webbrowser
import subprocess
import sys
from pathlib import Path

class StartupInfo:
    def __init__(self, config):
        self.config = config
        self.system = platform.system().lower()
    
    def show_startup_info(self):
        """显示启动信息"""
        if not self.config.get("show_startup_info", True):
            return
        
        share_url = self.config.get_share_url()
        frontend_url = self.config.get_frontend_url()
        
        message = f"""
{self.config.get('app_name')} v{self.config.get('version')}
{self.config.get('company_name')}

✅ 服务已启动成功！

📡 共享地址：
后端API: {share_url}
前端界面: {frontend_url}

💡 使用说明：
1. 在同一局域网内的其他设备上打开浏览器
2. 访问上述地址即可使用文件共享功能
3. 支持文件上传、视频播放、消息发送等功能

🔧 配置说明：
- 配置文件: backend/config.json
- 上传目录: backend/{self.config.get('upload_folder')}
- 视频目录: backend/{self.config.get('video_folder')}

按任意键继续...
        """
        
        if self.system == "windows":
            self._show_windows_info(message, share_url, frontend_url)
        elif self.system == "darwin":  # macOS
            self._show_macos_info(message, share_url, frontend_url)
        else:  # Linux
            self._show_linux_info(message, share_url, frontend_url)
    
    def _show_windows_info(self, message, share_url, frontend_url):
        """Windows系统显示启动信息"""
        try:
            import tkinter as tk
            from tkinter import messagebox
            
            # 创建隐藏的根窗口
            root = tk.Tk()
            root.withdraw()
            
            # 显示消息框
            result = messagebox.askyesno(
                f"{self.config.get('app_name')} - 启动成功",
                message,
                icon='info'
            )
            
            # 如果用户点击"是"，则打开浏览器
            if result:
                webbrowser.open(frontend_url)
            
            root.destroy()
            
        except ImportError:
            # 如果没有tkinter，使用命令行显示
            print(message)
            input("按回车键继续...")
    
    def _show_macos_info(self, message, share_url, frontend_url):
        """macOS系统显示启动信息"""
        try:
            # 使用osascript显示对话框
            escaped_message = message.replace('"', '\\"')
            script = f'''
            display dialog "{escaped_message}" with title "{self.config.get('app_name')} - 启动成功" buttons {{"打开浏览器", "确定"}} default button "打开浏览器"
            '''
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True)
            
            if "打开浏览器" in result.stdout:
                webbrowser.open(frontend_url)
                
        except Exception:
            # 如果osascript失败，使用命令行显示
            print(message)
            input("按回车键继续...")
    
    def _show_linux_info(self, message, share_url, frontend_url):
        """Linux系统显示启动信息"""
        try:
            # 尝试使用zenity显示对话框
            script = f'''
            zenity --info --title="{self.config.get('app_name')} - 启动成功" --text="{message}" --ok-label="打开浏览器" --cancel-label="确定"
            '''
            result = subprocess.run(['bash', '-c', script], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:  # 用户点击了"打开浏览器"
                webbrowser.open(frontend_url)
                
        except Exception:
            # 如果zenity不可用，使用命令行显示
            print(message)
            input("按回车键继续...")
    
    def show_error_info(self, error_message):
        """显示错误信息"""
        message = f"""
❌ 启动失败！

错误信息: {error_message}

请检查：
1. 端口是否被占用
2. 防火墙设置
3. 网络连接状态

按任意键退出...
        """
        
        if self.system == "windows":
            try:
                import tkinter as tk
                from tkinter import messagebox
                root = tk.Tk()
                root.withdraw()
                messagebox.showerror(f"{self.config.get('app_name')} - 启动失败", message)
                root.destroy()
            except ImportError:
                print(message)
                input("按回车键退出...")
        else:
            print(message)
            input("按回车键退出...") 