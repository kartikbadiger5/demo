import os 
import eel 

from engine.command import *

eel.init("www")

os.system('start msedge.exe --app="http://localhost:8000/index.html"')


def on_close_callback(route, websockets):
    
    import sys
    sys.exit(0)

eel.start("index.html", mode=None, host='localhost', block=True, close_callback=on_close_callback)







