import os
import subprocess
import platform

class SystemUtils:
    @staticmethod
    def open_app(app_name):
        app_map = {
            "notepad": "notepad.exe" if platform.system() == "Windows" else "gedit",
            "calculator": "calc.exe" if platform.system() == "Windows" else "gnome-calculator",
            "task manager": "taskmgr.exe" if platform.system() == "Windows" else "gnome-system-monitor",
            "control panel": "control.exe" if platform.system() == "Windows" else None,
            "command prompt": "cmd.exe" if platform.system() == "Windows" else "gnome-terminal",
            "powershell": "powershell.exe" if platform.system() == "Windows" else None,
            "browser": "start msedge" if platform.system() == "Windows" else "xdg-open https://www.google.com"
        }
        if app_name in app_map and app_map[app_name]:
            subprocess.Popen(app_map[app_name], shell=True)
            return f"Opening {app_name}"
        return "Application not found"
