import os 
import eel 

from engine.command import *

eel.init("www")

def on_close_callback(route, websockets):
    import sys
    sys.exit(0)

# Start the application with specific size and position
eel.start('index.html', 
          size=(400, 700),
          position=(1500, 370),  # Left side positioning
          mode='edge',
          host='localhost',
          block=True,
          close_callback=on_close_callback)







