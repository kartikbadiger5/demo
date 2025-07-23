# No relative imports to change
import platform
import subprocess
import ctypes
import pyautogui

class MediaController:
    def volume_up(self):
        if self.os_type == "Windows":
            self._send_windows_key(self.VK_VOLUME_UP)
        elif self.os_type == "Darwin":
            subprocess.run([
                "osascript", "-e",
                'set volume output volume ((output volume of (get volume settings)) + 10)'
            ])
        elif self.os_type == "Linux":
            subprocess.run(["xdotool", "key", "XF86AudioRaiseVolume"])
        return "Increased volume."

    def volume_down(self):
        if self.os_type == "Windows":
            self._send_windows_key(self.VK_VOLUME_DOWN)
        elif self.os_type == "Darwin":
            subprocess.run([
                "osascript", "-e",
                'set volume output volume ((output volume of (get volume settings)) - 10)'
            ])
        elif self.os_type == "Linux":
            subprocess.run(["xdotool", "key", "XF86AudioLowerVolume"])
        return "Decreased volume."

    def mute(self):
        if self.os_type == "Windows":
            self._send_windows_key(self.VK_VOLUME_MUTE)
        elif self.os_type == "Darwin":
            subprocess.run([
                "osascript", "-e",
                'set volume with output muted'
            ])
        elif self.os_type == "Linux":
            subprocess.run(["xdotool", "key", "XF86AudioMute"])
        return "Muted."

    def set_volume(self, level: int):
        level = max(0, min(100, level))
        if self.os_type == "Windows":
            try:
                from comtypes import CLSCTX_ALL
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                from ctypes import cast, POINTER
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(
                    IAudioEndpointVolume._iid_, CLSCTX_ALL, None
                )
                volume_interface = cast(interface, POINTER(IAudioEndpointVolume))
                scalar = level / 100.0
                volume_interface.SetMasterVolumeLevelScalar(scalar, None)
            except Exception:
                return "Volume control not available."
        elif self.os_type == "Darwin":
            subprocess.run([
                "osascript", "-e",
                f"set volume output volume {level}"
            ])
        else:  # Linux
            subprocess.run([
                "pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{level}%"
            ])
        return f"Volume set to {level}%."
    def __init__(self):
        self.os_type = platform.system()
        # Virtual-Key codes for Windows media keys
        self.VK_MEDIA_NEXT_TRACK   = 0xB0
        self.VK_MEDIA_PREV_TRACK   = 0xB1
        self.VK_MEDIA_PLAY_PAUSE   = 0xB3
        self.VK_VOLUME_MUTE        = 0xAD
        self.VK_VOLUME_DOWN        = 0xAE
        self.VK_VOLUME_UP          = 0xAF
        self.KEYEVENTF_EXTENDEDKEY = 0x0001
        self.KEYEVENTF_KEYUP       = 0x0002

    def _send_windows_key(self, vk_code: int):
        ctypes.windll.user32.keybd_event(vk_code, 0, self.KEYEVENTF_EXTENDEDKEY, 0)
        ctypes.windll.user32.keybd_event(vk_code, 0, self.KEYEVENTF_EXTENDEDKEY | self.KEYEVENTF_KEYUP, 0)

    def toggle_playback(self):
        if self.os_type == "Windows":
            self._send_windows_key(self.VK_MEDIA_PLAY_PAUSE)
            pyautogui.hotkey('k')
        elif self.os_type == "Darwin":
            subprocess.run(["osascript", "-e", 'tell application "System Events" to key code 16'])
        elif self.os_type == "Linux":
            subprocess.run(["xdotool", "key", "XF86AudioPlay"])
        return "Done"

    def next_track(self):
        if self.os_type == "Windows":
            self._send_windows_key(self.VK_MEDIA_NEXT_TRACK)
            pyautogui.hotkey('shift', 'n')
        elif self.os_type == "Darwin":
            subprocess.run(["osascript", "-e", 'tell application "System Events" to key code 17'])
        elif self.os_type == "Linux":
            subprocess.run(["xdotool", "key", "XF86AudioNext"])
        return "played next song."

    def previous_track(self):
        if self.os_type == "Windows":
            self._send_windows_key(self.VK_MEDIA_PREV_TRACK)
            pyautogui.hotkey('shift', 'p')
        elif self.os_type == "Darwin":
            subprocess.run(["osascript", "-e", 'tell application "System Events" to key code 18'])
        elif self.os_type == "Linux":
            subprocess.run(["xdotool", "key", "XF86AudioPrev"])
        return "played previous song."
