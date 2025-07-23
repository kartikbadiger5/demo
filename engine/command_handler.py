import os
import subprocess
import platform
from engine.media_controller import MediaController
from engine.system_utils import SystemUtils

class CommandHandler:
    def __init__(self):
        self.media_controller = MediaController()
        self.system_utils = SystemUtils()
        self.exe_map = {
            'calculator': 'calc' if platform.system() == 'Windows' else 'gnome-calculator',
            'notepad': 'notepad' if platform.system() == 'Windows' else 'gedit',
            'vs code': 'code',
            'visual studio code': 'code',
            'edge': 'msedge',
            'chrome': 'chrome',
            'firefox': 'firefox',
            'explorer': 'explorer' if platform.system() == 'Windows' else 'nautilus'
        }

    def process(self, text):
        import re, webbrowser, requests, time
        from datetime import datetime
        t = text.lower().strip()

        # Set volume to specific level
        m = re.search(r"set (?:volume(?: to)?)(?: up)? (\d{1,3})", t)
        if m:
            level = int(m.group(1))
            return self.media_controller.set_volume(level)

        # Media commands
        media_commands = {
            'pause':             self.media_controller.toggle_playback,
            'pause song':        self.media_controller.toggle_playback,
            'stop this song':    self.media_controller.toggle_playback,
            'resume':            self.media_controller.toggle_playback,
            'play again':        self.media_controller.toggle_playback,
            'next song':         self.media_controller.next_track,
            'next track':        self.media_controller.next_track,
            'previous song':     self.media_controller.previous_track,
            'previous track':    self.media_controller.previous_track,
            'volume up':         self.media_controller.volume_up,
            'increase volume':   self.media_controller.volume_up,
            'volume down':       self.media_controller.volume_down,
            'decrease volume':   self.media_controller.volume_down,
            'mute':              self.media_controller.mute,
            'unmute':            self.media_controller.mute
        }
        for cmd, action in media_commands.items():
            if cmd in t:
                return action()

        # Open YouTube
        if 'open youtube' in t:
            webbrowser.open("https://www.youtube.com")
            return "Opening YouTube in your browser."

        # Play song on YouTube
        if t.startswith('play ') and ' on youtube' in t:
            song = t.replace('play ', '').replace(' on youtube', '').strip()
            query = song.replace(' ', '+')
            search_url = f"https://www.youtube.com/results?search_query={query}"
            try:
                resp = requests.get(search_url)
                match = re.search(r'"videoId":"([^"]+)"', resp.text)
                if match:
                    video_id = match.group(1)
                    url = f"https://www.youtube.com/watch?v={video_id}"
                    webbrowser.open(url)
                    time.sleep(3)
                    return f"Playing {song} on YouTube."
            except Exception:
                pass
            webbrowser.open(search_url)
            return f"Opened YouTube search for {song}."

        # Google search
        if t.startswith('search '):
            query = t.replace('search ', '').strip()
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(url)
            return f"Searching Google for {query}."

        # Open installed app or link
        if t.startswith('open '):
            app_name = t.replace('open ', '').strip().lower()

            if app_name.startswith('http') or '.' in app_name:
                webbrowser.open(app_name)
                return f"Opening {app_name}."

            if hasattr(self, 'app_map') and app_name in self.app_map:
                try:
                    os.startfile(self.app_map[app_name])
                    return f"Launching {app_name}."
                except Exception:
                    pass

            exe = self.exe_map.get(app_name)
            if exe:
                try:
                    subprocess.Popen(exe)
                    return f"Launching {app_name}."
                except Exception:
                    pass

            try:
                subprocess.Popen(app_name)
                return f"Launching {app_name}."
            except Exception:
                return f"Sorry, I couldn't find or open {app_name}."

        # Time
        if 'time' in t:
            return datetime.now().strftime("The current time is %H:%M.")

        return "Sorry, I didn't understand that command."
