import os
import sys
import platform
import subprocess
from pathlib import Path

class AutoStartManager:
    def __init__(self, config):
        self.config = config
        self.system = platform.system().lower()
        self.app_name = config.get("app_name", "内网文件共享工具")
        
        # 获取当前脚本路径
        if getattr(sys, 'frozen', False):
            # 如果是打包后的可执行文件
            self.app_path = sys.executable
        else:
            # 如果是Python脚本
            self.app_path = sys.argv[0]
        
        # 获取项目根目录
        self.project_root = Path(self.app_path).parent.parent if self.app_path.endswith('.py') else Path(self.app_path).parent
    
    def setup_auto_start(self):
        """设置开机自启动"""
        if not self.config.get("auto_start", True):
            return False
        
        try:
            if self.system == "windows":
                return self._setup_windows_auto_start()
            elif self.system == "darwin":  # macOS
                return self._setup_macos_auto_start()
            else:  # Linux
                return self._setup_linux_auto_start()
        except Exception as e:
            print(f"设置开机自启动失败: {e}")
            return False
    
    def remove_auto_start(self):
        """移除开机自启动"""
        try:
            if self.system == "windows":
                return self._remove_windows_auto_start()
            elif self.system == "darwin":  # macOS
                return self._remove_macos_auto_start()
            else:  # Linux
                return self._remove_linux_auto_start()
        except Exception as e:
            print(f"移除开机自启动失败: {e}")
            return False
    
    def _setup_windows_auto_start(self):
        """Windows系统设置开机自启动"""
        try:
            import winreg
            
            # 创建启动命令
            if self.app_path.endswith('.py'):
                # Python脚本
                python_exe = sys.executable
                startup_cmd = f'"{python_exe}" "{self.app_path}"'
            else:
                # 可执行文件
                startup_cmd = f'"{self.app_path}"'
            
            # 注册表路径
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            
            # 打开注册表
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, self.app_name, 0, winreg.REG_SZ, startup_cmd)
            winreg.CloseKey(key)
            
            print(f"✅ Windows开机自启动设置成功")
            return True
            
        except ImportError:
            print("❌ 无法导入winreg模块，Windows开机自启动设置失败")
            return False
        except Exception as e:
            print(f"❌ Windows开机自启动设置失败: {e}")
            return False
    
    def _remove_windows_auto_start(self):
        """Windows系统移除开机自启动"""
        try:
            import winreg
            
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)
            winreg.DeleteValue(key, self.app_name)
            winreg.CloseKey(key)
            
            print(f"✅ Windows开机自启动已移除")
            return True
            
        except ImportError:
            print("❌ 无法导入winreg模块，Windows开机自启动移除失败")
            return False
        except Exception as e:
            print(f"❌ Windows开机自启动移除失败: {e}")
            return False
    
    def _setup_macos_auto_start(self):
        """macOS系统设置开机自启动"""
        try:
            # 创建启动项plist文件
            plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.{self.app_name.replace(' ', '').lower()}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{sys.executable}</string>
        <string>{self.app_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>WorkingDirectory</key>
    <string>{self.project_root}</string>
</dict>
</plist>"""
            
            # 写入plist文件
            plist_path = Path.home() / "Library/LaunchAgents" / f"com.{self.app_name.replace(' ', '').lower()}.plist"
            plist_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(plist_path, 'w', encoding='utf-8') as f:
                f.write(plist_content)
            
            # 加载启动项
            subprocess.run(['launchctl', 'load', str(plist_path)], check=True)
            
            print(f"✅ macOS开机自启动设置成功")
            return True
            
        except Exception as e:
            print(f"❌ macOS开机自启动设置失败: {e}")
            return False
    
    def _remove_macos_auto_start(self):
        """macOS系统移除开机自启动"""
        try:
            plist_path = Path.home() / "Library/LaunchAgents" / f"com.{self.app_name.replace(' ', '').lower()}.plist"
            
            if plist_path.exists():
                # 卸载启动项
                subprocess.run(['launchctl', 'unload', str(plist_path)], check=True)
                # 删除plist文件
                plist_path.unlink()
            
            print(f"✅ macOS开机自启动已移除")
            return True
            
        except Exception as e:
            print(f"❌ macOS开机自启动移除失败: {e}")
            return False
    
    def _setup_linux_auto_start(self):
        """Linux系统设置开机自启动"""
        try:
            # 创建桌面文件
            desktop_content = f"""[Desktop Entry]
Type=Application
Name={self.app_name}
Exec={sys.executable} {self.app_path}
Terminal=false
Hidden=false
X-GNOME-Autostart-enabled=true
"""
            
            # 写入桌面文件
            autostart_dir = Path.home() / ".config/autostart"
            autostart_dir.mkdir(parents=True, exist_ok=True)
            
            desktop_file = autostart_dir / f"{self.app_name.replace(' ', '').lower()}.desktop"
            with open(desktop_file, 'w', encoding='utf-8') as f:
                f.write(desktop_content)
            
            # 设置执行权限
            desktop_file.chmod(0o755)
            
            print(f"✅ Linux开机自启动设置成功")
            return True
            
        except Exception as e:
            print(f"❌ Linux开机自启动设置失败: {e}")
            return False
    
    def _remove_linux_auto_start(self):
        """Linux系统移除开机自启动"""
        try:
            autostart_dir = Path.home() / ".config/autostart"
            desktop_file = autostart_dir / f"{self.app_name.replace(' ', '').lower()}.desktop"
            
            if desktop_file.exists():
                desktop_file.unlink()
            
            print(f"✅ Linux开机自启动已移除")
            return True
            
        except Exception as e:
            print(f"❌ Linux开机自启动移除失败: {e}")
            return False
    
    def is_auto_start_enabled(self):
        """检查是否已设置开机自启动"""
        try:
            if self.system == "windows":
                return self._check_windows_auto_start()
            elif self.system == "darwin":  # macOS
                return self._check_macos_auto_start()
            else:  # Linux
                return self._check_linux_auto_start()
        except Exception:
            return False
    
    def _check_windows_auto_start(self):
        """检查Windows开机自启动状态"""
        try:
            import winreg
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
            winreg.QueryValueEx(key, self.app_name)
            winreg.CloseKey(key)
            return True
        except:
            return False
    
    def _check_macos_auto_start(self):
        """检查macOS开机自启动状态"""
        plist_path = Path.home() / "Library/LaunchAgents" / f"com.{self.app_name.replace(' ', '').lower()}.plist"
        return plist_path.exists()
    
    def _check_linux_auto_start(self):
        """检查Linux开机自启动状态"""
        autostart_dir = Path.home() / ".config/autostart"
        desktop_file = autostart_dir / f"{self.app_name.replace(' ', '').lower()}.desktop"
        return desktop_file.exists() 