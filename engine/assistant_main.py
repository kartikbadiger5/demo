
import sys
import eel
from engine.voice_engine import VoiceEngine
from engine.command_handler import CommandHandler

@eel.expose
def background_listen():
    voice = VoiceEngine()
    # Listen briefly for the wake word only
    cmd = voice.listen()
    if 'lumina' in cmd:
        return 'lumina'
    return ''

@eel.expose
def takecommand():
    voice = VoiceEngine()
    handler = CommandHandler()
    WAKE_WORD = "lumina"
    SLEEP_WORD = "sleep"
    SHUTDOWN_WORD = "bye"
    import time
    # Always immediately enter command mode (no wake word prompt)
    eel.DisplayMessage("I'm awake. How can I help?")
    voice.speak("I'm awake. How can I help?")
    last_command_time = time.time()
    while True:
        try:
            eel.DisplayMessage("Listening for command...")
            user_cmd = ""
            # Show recognizing status
            eel.DisplayMessage("Listening...")
            user_cmd = voice.listen()
            eel.DisplayMessage("Recognizing...")
        except Exception:
            continue
        # Timeout: 2 minutes (120 seconds) of inactivity
        if not user_cmd:
            if time.time() - last_command_time > 120:
                msg = "No command detected for 2 minutes. Going back to sleep. Tap the mic or say 'lumina' to wake me."
                eel.DisplayMessage(msg)
                voice.speak(msg)
                eel.ShowHood()
                break
            continue
        last_command_time = time.time()
        if SLEEP_WORD in user_cmd:
            msg = "Going back to sleep. Tap the mic or say 'lumina' to wake me."
            eel.DisplayMessage(msg)
            voice.speak(msg)
            eel.ShowHood()
            break
        if SHUTDOWN_WORD in user_cmd:
            msg = "Have a Great Day. Goodbye!"
            eel.DisplayMessage(msg)
            voice.speak(msg)
            eel.ShowHood()
            sys.exit(0)
        response = handler.process(user_cmd)
        if response:
            eel.DisplayMessage(response)
            voice.speak(response)
