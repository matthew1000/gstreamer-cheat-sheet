#!/usr/bin/env python
'''
This is an example of how to use Playbin, and send its output somewhere other
than local video/audio playback.

Using the 'video-sink' and 'audio-sink' properties, different ends of the Playbin
pipeline can be set.

Try experimenting with the 'DISABLE_VIDEO' and 'DISABLE_AUDIO' constants below.
When set to true, they allow the Playbin sink to be set to 'fakesink', which
stops them from playing locally.
'''

DISABLE_VIDEO=False
DISABLE_AUDIO=True

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
import os

Gst.init(None)
mainloop = GObject.MainLoop()

pipe1 = Gst.parse_launch("playbin uri=\"file://" + os.environ['SRC'] + "\"")
playsink = pipe1.get_by_name('playsink')

if DISABLE_VIDEO:
    fakesink1 = Gst.ElementFactory.make("fakesink", "fakesink1")
    playsink.set_property('video-sink', fakesink1)

if DISABLE_AUDIO:
    fakesink2 = Gst.ElementFactory.make("fakesink", "fakesink2")
    playsink.set_property('audio-sink', fakesink2)

pipe1.set_state(Gst.State.PLAYING)

def on_error(bus, message):
    print(message.parse_error())

bus1 = pipe1.get_bus()
bus1.add_signal_watch()
bus1.connect('message::error', on_error)

mainloop.run()
