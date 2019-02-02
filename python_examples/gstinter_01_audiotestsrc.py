#!/usr/bin/env python
# Shows how two pipelines can be connected, using interaudiosink/interaudiosrc.
# (Search and replace 'audio' with 'video' to get a video example.)
# It will output a test audio sound.
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
import os

Gst.init(None)
mainloop = GObject.MainLoop()

pipe1 = Gst.parse_launch("audiotestsrc is-live=1 ! interaudiosink name=psink")
pipe2 = Gst.parse_launch("interaudiosrc name=psrc ! autoaudiosink")

pipe1.set_state(Gst.State.PLAYING)
pipe2.set_state(Gst.State.PLAYING)

mainloop.run()
