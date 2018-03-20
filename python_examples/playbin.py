#!/usr/bin/env python
#
# Make sure the environment variable SRC is set to a playable file
# e.g.
#   export SRC='/tmp/me.mp4'
#

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
import os

Gst.init()
mainloop = GObject.MainLoop()

pl = Gst.ElementFactory.make("playbin", "player")
pl.set_property('uri','file://'+os.environ['SRC'])

#running the playbin
pl.set_state(Gst.State.PLAYING)
mainloop.run()
