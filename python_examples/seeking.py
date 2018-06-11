#!/usr/bin/env python
# Shows seeking in action.

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
import os
from time import sleep
from threading import Thread

Gst.init(None)
mainloop = GObject.MainLoop()
pipe = Gst.parse_launch("playbin uri=\"file://" + os.environ['SRC'] + "\"")
pipe.set_state(Gst.State.PLAYING)

def separate_thread():
    while True:
        seconds = input("Enter the number of seconds to jump to (0=start): ")
        seek_success = pipe.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH, Gst.SECOND * int(seconds))
        print ('seek_success=' + str(seek_success))

myThread = Thread(target=separate_thread, args=())
myThread.start()

mainloop.run()
