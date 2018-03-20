#!/usr/bin/env python
#
# Plays a file to screen.
#
# Make sure the environment variable SRC is set to a playable file
# e.g.
#   export SRC='/tmp/me.mp4'
#

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
import os

Gst.init(None)
mainloop = GObject.MainLoop()

pipeline = Gst.ElementFactory.make("playbin", "player")
pipeline.set_property('uri','file://'+os.environ['SRC'])

pipeline.set_state(Gst.State.PLAYING)
mainloop.run()
